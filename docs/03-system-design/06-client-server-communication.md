---
type: Guide
title: Client-Server Communication and Networking
description: HTTP semantics, REST and GraphQL API design, and the streaming transports a browser can use to reach a server.
tags: [frontend, http, rest, graphql, api-design]
---

How a client and a server exchange data: the HTTP semantics every request depends on, the two dominant API styles, and the transports that keep a connection open. Written for engineers on either side of the contract who are deciding how a browser and a service should talk.

**Egress vs ingress** — Traffic leaving versus entering. The distinction matters
mostly because of cost and control: AWS charges for egress to the internet and
generally not for ingress, and most security postures restrict egress far less
carefully than ingress despite exfiltration being an egress problem. 

**Gateway endpoint vs interface endpoint** — Two ways to reach an AWS service
privately, priced completely differently: a *gateway* endpoint is a route table
entry and is free but exists only for S3 and DynamoDB, while an *interface*
endpoint is an ENI in your subnet, works for almost everything, and bills hourly
per AZ plus data. Which of the two a service supports is what decides whether a
design can afford to have no NAT Gateway at all.

**Private vs public subnet** — A public subnet has a route to an internet
gateway; a private one does not. The distinction is the route table, not a
setting called "private" — which is why a subnet can be private and still have
outbound access, via a NAT, and why a genuinely isolated subnet needs VPC
endpoints for anything it must reach. An instance in a public subnet is not
reachable from the internet unless it also has a public IP and a permissive
security group.

**Security group vs NACL** — A security group is **stateful**, so allowing
inbound on 443 permits the response automatically; a NACL is **stateless** and
evaluates each direction independently, which is why an inbound allow without a
matching ephemeral-port outbound rule silently breaks the connection. The detail
that matters here is that a security group rule can reference *another security
group* rather than a CIDR block — that is how "only the load balancer may reach
the task" is expressed without hardcoding addresses.

**Target group** — The set of destinations a load balancer routes to, plus the
health check that decides which of them are eligible right now. It is the seam
where deployment and traffic meet: registering and deregistering targets is how
a rolling deploy shifts traffic, and the deregistration delay is how long the
load balancer waits for in-flight requests before cutting a target off.

**VPC endpoint** — A private entrance to an AWS service from inside a VPC, so
traffic never touches the public internet. Beyond the security argument it is
usually a cost argument, because a gateway endpoint avoids NAT Gateway data
processing charges entirely — 

**Waterfall** — Requests that run in sequence because each needs the previous
one's result, when they could have run in parallel. It is the most common cause
of a slow page that has no slow request in it — six 100 ms calls in a chain are
a 600 ms page. The fix is either to parallelise or to move the composition to
where the data lives, which is one of the arguments for a BFF.

## Load Balancing

Load Balancing
: Spreading incoming requests across a pool of interchangeable servers, so capacity grows by adding machines rather than by enlarging one

Layer 4 Balancing
: Forwarding at the transport level on address and port without reading the request; cheap and protocol-agnostic, but blind to paths, headers, and cookies

Layer 7 Balancing
: Routing on application data such as path, header, or cookie, which buys per-route pools and content-aware policy at the cost of terminating and parsing every request

Balancing Algorithm
: The rule picking the next server — round robin where requests cost the same, least connections where they do not, and a hash of a chosen key where a caller must keep landing on one node

Backend Pool
: The set of interchangeable servers a balancer distributes across, whose membership changes as instances are added, drained, or removed

Health Check
: A periodic probe deciding whether a server stays in the pool, so a failing instance is taken out before users meet its errors

Sticky Session
: Pinning a client to the server holding its state, which keeps that state reachable but unbalances the pool and loses the state outright when that server dies

Cache Affinity
: Routing every request for one key to the same backend so its local copy stays warm, using consistent hashing so that adding a node moves few keys

Connection Draining
: Letting in-flight requests finish on a server already removed from rotation, so a deploy or scale-in does not cut live work short

Single Point of Failure
: A component whose loss takes down everything behind it — the balancer's own exposure, answered by a redundant pair sharing a failover address

DNS Round Robin
: Distributing at name resolution by handing out different addresses in turn; free, but with no view of server health and with client caches that outlive a failure

---

## HTTP

A request names a method and a target; a response returns a status code and, usually, a body. Every API style below is a set of conventions layered on that exchange.

| Method | Safe | Idempotent | Description |
| --- | --- | --- | --- |
| **GET** | Yes | Yes | Retrieve a representation of the target resource |
| **HEAD** | Yes | Yes | Identical to GET, but the response carries no body |
| **OPTIONS** | Yes | Yes | Report the communication options available for the target |
| **POST** | No | No | Submit data; the target resource decides what the effect is |
| **PUT** | No | Yes | Replace the target resource with the request body |
| **PATCH** | No | No | Apply a partial modification to the target resource |
| **DELETE** | No | Yes | Remove the target resource |

RFC 9110 defines a *safe* method as one whose semantics are read-only, and an *idempotent* method as one where sending the request twice has the same effect on the server as sending it once. Every safe method is therefore idempotent. PATCH (RFC 5789) is neither, because a patch document may describe a relative change.

| Code Range | Category | Examples |
| --- | --- | --- |
| **1xx** | Informational | 100 Continue, 101 Switching Protocols |
| **2xx** | Success | 200 OK, 201 Created, 204 No Content |
| **3xx** | Redirection | 301 Moved Permanently, 304 Not Modified, 307 Temporary Redirect |
| **4xx** | Client Error | 400 Bad Request, 401 Unauthorized, 404 Not Found, 409 Conflict, 429 Too Many Requests |
| **5xx** | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### Versions and Connection Model

| Version | Connection Model | Consequence |
| --- | --- | --- |
| **HTTP/1.1** | One exchange at a time per TCP connection, which is kept alive for reuse | Browsers open several connections per origin to get parallelism — commonly six. That number is a browser convention; no RFC specifies it |
| **HTTP/2** | Many concurrent streams multiplexed over a single TCP connection | Concurrency is bounded by the peer's `SETTINGS_MAX_CONCURRENT_STREAMS` setting (RFC 9113), which the RFC recommends be no smaller than 100 — it is a higher ceiling, not the absence of one |
| **HTTP/3** | Streams carried over QUIC, which runs on UDP | A lost packet stalls only its own stream instead of every stream on the connection |

Which version you are on is a deployment choice, not an API design choice: the method and status semantics above are identical across all three.

Two adjacent mechanisms have their own homes. Cache headers such as `Cache-Control` and `ETag` are covered in [Performance Optimization](../06-frontend/03-performance-optimization.md); the same-origin policy and CORS preflight are covered in [Web Security](../06-frontend/05-security-web.md).

## REST

An architectural style, described in Roy Fielding's 2000 dissertation, that reuses HTTP's existing semantics rather than tunnelling a custom protocol through it. A URI names a resource, the method says what to do to it, and the status code says what happened.

### Constraints

| Constraint | What It Requires |
| --- | --- |
| **Client-server** | The interface separates user-facing concerns from data storage, so each side can change independently |
| **Stateless** | Each request carries everything needed to serve it; the server holds no client session between requests |
| **Cacheable** | Every response states whether it may be stored, and for how long |
| **Uniform interface** | Resources are identified by URI and manipulated through the same small set of methods and media types |
| **Layered system** | A client cannot tell whether it is talking to the origin server or to a proxy, gateway, or cache |
| **Code on demand** | Optional. The server may extend the client by sending executable code |

### Resource Naming

```text
GET    /api/users              # List the collection
POST   /api/users              # Create a member
GET    /api/users/123          # Read one member
PUT    /api/users/123          # Replace it in full
PATCH  /api/users/123          # Change some of its fields
DELETE /api/users/123          # Remove it

GET /api/users?role=admin&active=true    # Filter with query parameters
GET /api/users?page=2&per_page=50        # Paginate
GET /api/users/123/posts                 # Sub-collection of one member
```

- The path names a thing, the method names the action. `POST /api/getUser` puts the verb in the wrong place.
- Plural nouns for collections, so a member is always the collection path plus an identifier.
- Nest at most one level. Past `/users/123/posts`, return links to the deeper resources instead of extending the path.
- Use kebab-case for multi-word path segments, and keep query parameter names identical across endpoints.

### Choosing a Status Code

| Outcome | Response |
| --- | --- |
| **Resource created** | 201 with a `Location` header pointing at the new resource |
| **Accepted for later processing** | 202 with a URI the client can poll for progress |
| **Nothing to return** | 204 with an empty body |
| **Malformed request** | 400 |
| **Well-formed but semantically invalid** | 422, with the failing fields named in the body |
| **Credentials missing or invalid** | 401, with a `WWW-Authenticate` header |
| **Credentials valid but insufficient** | 403 |
| **Conflicts with current state** | 409 |
| **Client is sending too fast** | 429 with a `Retry-After` header |

Reserve 5xx for faults the client cannot fix. A rejected payload is a 4xx even when a server-side validator raised the error.

### Error Bodies

Return one machine-readable shape for every error, not a different one per endpoint. RFC 9457 defines such a shape, `application/problem+json`, which most clients and gateways already understand:

```json
{
    "type": "https://example.com/probs/insufficient-credit",
    "title": "Insufficient credit",
    "status": 403,
    "detail": "Balance is 30 but the operation costs 50",
    "instance": "/accounts/12345/transactions/abc"
}
```

The `type` URI is the stable field — clients branch on it. `title` and `detail` are for humans. See [Data Formats](07-data-formats.md) for JSON itself.

### Versioning

| Strategy | Example | Trade-off |
| --- | --- | --- |
| **URI path** | `/api/v2/users` | Visible and easy to route or cache; the same entity now has two URIs, which weakens the uniform interface |
| **Media type** | `Accept: application/vnd.example.v2+json` | One URI per resource; harder to call by hand and easy for intermediaries to ignore |
| **Query parameter** | `/api/users?version=2` | Trivial to add; easy to omit by accident, and it enlarges the cache key |

Most changes need no version at all. Adding a field or an optional parameter is compatible with existing clients; renaming a field, removing one, or tightening validation is not.

### Idempotency and Retries

A client, a proxy, or a browser may retry a request that failed with no response, so safe and idempotent methods must tolerate duplicates. POST does not, which is why a create endpoint should accept a client-generated `Idempotency-Key` header, store the first response against that key, and replay it if the key arrives again. [System Design Glossary](01-common-concepts.md) covers idempotency as a general design concept, and [Caching](03-caching.md) covers the caching patterns.

## GraphQL

One endpoint, and a typed schema the client queries against. The client states the fields it wants, so the response shape is decided per request rather than per endpoint.

```graphql
query GetUsers {
    users(first: 10) {
        id
        name
        posts { title }
    }
}

mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
        id
        name
        errors { field message }
    }
}
```

| Aspect | REST | GraphQL |
| --- | --- | --- |
| **Endpoints** | One per resource | One, conventionally `/graphql` |
| **Response shape** | Fixed by the server | Selected by the query |
| **Over-fetching** | Common — an endpoint returns its whole representation | Avoidable, though a careless query can still request more than it uses |
| **Schema** | Optional, through OpenAPI or similar | Mandatory and part of the protocol |
| **Caching** | HTTP caching applies directly | Needs a client-side cache or persisted queries, because requests are usually POSTs to one URI |
| **Error reporting** | The HTTP status code | Typically 200 with an `errors` array in the body |

The cost moves rather than disappearing: one query can fan out into many resolver calls, so servers guard with query depth limits, cost analysis, and batched data loaders.

### GraphQL concepts

**N+1 problem** — One query for a list, then one more query per item in it. It
arises naturally in GraphQL because each resolver is written independently and
knows nothing about being called fifty times, so the inefficiency is invisible
in any single piece of code. It is the first thing to look for when a GraphQL
endpoint is slow.

**DataLoader** — A per-request batching and caching layer that collects the
individual loads made during one tick and issues them as a single batch. It is
the standard answer to N+1, and the two constraints matter: it must be created
*per request*, or one user's cache leaks into another's, and the backing store
must actually support a batch fetch.

**Persisted query** — Registering a query in advance and having the client send
an identifier instead of the query text. It shrinks the request, but the real
value is control: an endpoint that only accepts known queries cannot be asked an
arbitrarily expensive one, which removes a whole class of denial-of-service
without a depth or complexity limiter.

**Resolver** — The function that produces the value for one field. The mental
model that avoids most GraphQL mistakes is that resolvers are called
independently, potentially concurrently, once per field per object — so anything
expensive in one is multiplied by the shape of the query, not by the number of
requests.

**Schema stitching vs federation** — Two ways to present several GraphQL services
as one endpoint. Stitching merges schemas at a gateway that knows how to
delegate, keeping the subgraphs unaware; federation has each service declare
which types it owns and extends, so the composition is described by the services
themselves. Federation scales better organisationally because ownership is
explicit; stitching is simpler when one team owns everything.

**Union result type** — Modelling the possible outcomes of a field as a union of
object types, so the client discriminates on `__typename`. It moves expected
failures out of the `errors` array and into the schema, where they are typed and
exhaustively handled.

## WebSockets

Bidirectional messaging over a persistent connection. The client opens it with an ordinary HTTP GET carrying `Upgrade: websocket`; the server answers `101 Switching Protocols`, and from then on both sides send frames whenever they like.

```javascript
const socket = new WebSocket('wss://api.example.com/ws');

socket.onopen = () => socket.send(JSON.stringify({ type: 'SUBSCRIBE', channel: 'updates' }));
socket.onmessage = (event) => console.log('Received:', JSON.parse(event.data));
socket.onclose = (event) => console.log('Disconnected:', event.code);
socket.onerror = (error) => console.error('Error:', error);

socket.close(1000, 'Done');
```

- Nothing reconnects for you. Handle `onclose` and retry with a growing delay.
- Intermediaries drop idle connections, so send a periodic ping and treat a missed pong as a dead socket.
- Use the `wss://` scheme. Plain `ws://` is blocked from pages served over HTTPS.
- Both text and binary frames are allowed, so no encoding step is needed for binary payloads.

## Server-Sent Events

One-way streaming from server to client over a single HTTP response. The browser reconnects on its own and resumes from the last received event id.

```javascript
const source = new EventSource('/api/events', { withCredentials: true });

source.onmessage = (event) => console.log('Message:', JSON.parse(event.data));
source.addEventListener('progress', (event) => console.log('Progress:', event.data));
source.onerror = () => console.log('Reconnecting...', source.readyState);

source.close();
```

Wire format — `text/event-stream`, messages separated by a blank line:

```text
id: 42
event: progress
data: {"percent": 60}

data: plain message
```

| Field | Purpose |
| --- | --- |
| **`event`** | Named event type; defaults to `message` |
| **`data`** | Payload; repeat the field for multi-line values |
| **`id`** | Sent back as `Last-Event-ID` on reconnect |
| **`retry`** | Reconnect delay in milliseconds |

A line beginning with a colon is a comment and is ignored. Any other field name is discarded.

- Text only — binary payloads must be encoded, for example as base64.
- `EventSource` issues a GET and cannot set custom headers, so authentication has to travel in a cookie or a query parameter.
- Each open stream occupies one connection. Over HTTP/1.1 that competes with the browser's per-origin connection limit — six by convention. HTTP/2 multiplexes streams onto one connection, which raises the ceiling to the negotiated `SETTINGS_MAX_CONCURRENT_STREAMS` rather than removing it.
- Proxies may buffer the response. Disable buffering on the path and send periodic comment lines (`: ping`) as keep-alive.

## Choosing a Transport

| Transport | Direction | Runs Over | Reconnect |
| --- | --- | --- | --- |
| **Request/response** | Client asks, server answers | HTTP | Not applicable; each request stands alone |
| **Long polling** | Server to client | HTTP | Implicit — the client reissues the request after each response |
| **Server-Sent Events** | Server to client | HTTP, `text/event-stream` | Built in, with `Last-Event-ID` for resumption |
| **WebSockets** | Both directions | TCP, after an HTTP upgrade | Your code owns it |

Take the simplest option that carries the traffic. Plain requests through the [Fetch API](../06-frontend/02-browser-technologies.md) cover most screens; Server-Sent Events add a server-driven stream without a second protocol; WebSockets are worth their operational cost only when the client must push as freely as the server does.
