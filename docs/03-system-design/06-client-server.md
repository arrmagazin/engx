---
type: Guide
title: Client-Server Communication and Networking
description: Network and load-balancing terms, HTTP semantics, REST and GraphQL API design, and the streaming transports a browser can use.
tags: [frontend, http, rest, graphql, api-design]
---

How a client and a server exchange data: the network underneath, HTTP semantics, the two dominant API styles, and the transports that keep a connection open.

## Network Terms

Cloud network terms, in AWS names; the cross-cloud mapping is in [Networking — Inside the Network](../08-clouds/01-concept-map.md#networking--inside-the-network).

- **Egress vs. ingress** — traffic leaving vs. entering. Clouds charge for egress, not ingress, and data theft is an egress problem, yet egress is filtered far less carefully.
- **Private vs. public subnet** — only a public subnet routes to an internet gateway; a private one can still reach out through a NAT gateway.
- **Security group vs. NACL** — a security group is *stateful* (a request's response is allowed) and can name another group as its source; a NACL is *stateless*, so a missing outbound rule silently breaks connections.
- **VPC endpoint** — a private path to a cloud service. A *gateway* endpoint is free but serves only S3 and DynamoDB; an *interface* endpoint serves almost everything and bills per hour and per GB — which decides whether a design can drop its NAT gateway.

## Load Balancing

Load Balancing
: Spreading incoming requests across a pool of interchangeable servers, so capacity grows by adding machines rather than by enlarging one

Layer 4 Balancing
: Forwarding on address and port without reading the request; cheap and protocol-agnostic, but blind to paths, headers, and cookies

Layer 7 Balancing
: Routing on path, header, or cookie, at the cost of terminating and parsing every request

Balancing Algorithm
: The rule picking the next server — round robin where requests cost the same, least connections where they do not, a consistent hash of a key where one caller must keep landing on one node

Health Check
: A periodic probe deciding whether a server stays in the pool, so a failing instance is taken out before users meet its errors

Sticky Session
: Pinning a client to the server holding its state, which unbalances the pool and loses the state when that server dies

Connection Draining
: Letting in-flight requests finish on a server already removed from rotation, so a deploy or scale-in does not cut live work short

DNS Round Robin
: Handing out different addresses in turn at name resolution; free, but blind to server health, and client caches outlive a failure

## HTTP

| Method | Safe · Idempotent | Does |
| --- | --- | --- |
| **GET** | Yes · Yes | Read the resource |
| **POST** | No · No | Submit data; the resource decides the effect |
| **PUT** | No · Yes | Replace the resource |
| **PATCH** | No · No | Change part of the resource |
| **DELETE** | No · Yes | Remove the resource |

A *safe* method is read-only; an *idempotent* one has the same effect sent twice as once (RFC 9110). PATCH is neither, because a patch may describe a relative change.

### Versions and Connection Model

| Version | Connection Model | Consequence |
| --- | --- | --- |
| **HTTP/1.1** | One exchange at a time per TCP connection | Browsers open about six connections per origin — a convention, not an RFC rule |
| **HTTP/2** | Many streams over one TCP connection | Bounded by the peer's `SETTINGS_MAX_CONCURRENT_STREAMS` (at least 100 recommended) — a higher ceiling, not none |
| **HTTP/3** | Streams over QUIC, on UDP | A lost packet stalls only its own stream |

The version is a deployment choice: method and status semantics are the same in all three. Cache headers are in [HTTP Caching](../06-frontend/04-rendering-network-performance.md#http-caching); the same-origin policy and CORS in [Web Security](../06-frontend/07-security-web.md#same-origin-policy-and-cors).

### Request Waterfalls

A **waterfall** is a chain of requests run in sequence, each waiting for the previous one, when they could run in parallel — the usual cause of a slow page with no slow request in it: six 100 ms calls in a chain make a 600 ms page. Parallelize, or move the composition next to the data, as a backend-for-frontend does.

## REST

An architectural style (Fielding, 2000) that reuses HTTP's semantics instead of tunneling a custom protocol through it: a URI names a resource, the method says what to do to it, the status code says what happened. Requests are **stateless**, responses state whether they are **cacheable**, the **interface is uniform**, and the system is **layered**, so a client cannot tell the origin from a proxy or cache.

### Resource Naming

```text
GET    /api/users?role=admin&page=2   # List, filter, and paginate the collection
POST   /api/users                     # Create a member
PATCH  /api/users/123                 # Change some fields of one member
GET    /api/users/123/posts           # Sub-collection of one member
```

The path names a thing and the method the action — `POST /api/getUser` puts the verb in the wrong place. Use plural nouns, and nest at most one level.

### Choosing a Status Code

| Outcome | Response |
| --- | --- |
| **Resource created** | 201 with a `Location` header |
| **Accepted for later processing** | 202 with a URI to poll |
| **Malformed / semantically invalid** | 400 / 422, naming the failing fields |
| **Not authenticated / not allowed** | 401 / 403 |
| **Conflicts with current state** | 409 |
| **Client is sending too fast** | 429 with a `Retry-After` header |

Reserve 5xx for faults the client cannot fix. Return one error shape for every endpoint; RFC 9457 `application/problem+json` is the standard one, and its `type` URI is the field clients branch on.

### Versioning

Most changes need no version: adding a field is compatible; renaming or removing one, or tightening validation, is not. A path version (`/api/v2/users`) is the easiest to route and cache; a media-type version keeps one URI per entity but is harder to call by hand.

### Retries

Clients and proxies retry a request that got no response. POST is not idempotent, so a create endpoint should accept a client-generated `Idempotency-Key` header, store the first response against it, and replay it when the key repeats — see [Idempotency](01-common-concepts.md#idempotency).

## GraphQL

One endpoint and a typed schema; the client states the fields it wants, so the response shape is decided per request.

```graphql
query GetUsers {
    users(first: 10) { id name posts { title } }
}
```

| Aspect | REST | GraphQL |
| --- | --- | --- |
| **Response shape** | Fixed by the server | Selected by the query |
| **Caching** | HTTP caching applies directly | Needs a client cache or persisted queries — requests are POSTs to one URI |
| **Errors** | The HTTP status code | Usually 200 with an `errors` array |

The cost moves rather than disappearing: one query can fan out into many resolver calls.

- **Resolver** — the function producing one field's value, called once per field per object, so its cost is multiplied by the shape of the query. Written independently, resolvers cause [N+1 queries](02-databases.md#schema-design) that no single piece of code shows — the first thing to check when an endpoint is slow.
- **DataLoader** — a layer that collects the loads made in one tick and issues them as one batch. It must be created *per request*, or one user's cache leaks into another's.
- **Persisted query** — a query registered in advance and sent by identifier. An endpoint accepting only known queries cannot be asked an arbitrarily expensive one.

## WebSockets

Bidirectional messaging over a persistent connection, opened by an HTTP GET with `Upgrade: websocket` that the server answers with `101 Switching Protocols`.

- Nothing reconnects for you: handle the close event and retry with a growing delay.
- Intermediaries drop idle connections, so send a periodic ping and treat a missed pong as a dead socket.
- Use `wss://`; plain `ws://` is blocked from pages served over HTTPS.

## Server-Sent Events

One-way streaming from server to client over a single `text/event-stream` HTTP response of `id:`, `event:`, and `data:` lines. The browser's `EventSource` reconnects on its own and resumes by sending the last `id` as `Last-Event-ID`.

- Text only, and `EventSource` cannot set custom headers, so authentication travels in a cookie or a query parameter.
- Over HTTP/1.1 each stream holds one of the browser's few per-origin connections.
- Proxies may buffer the response: disable buffering and send periodic comment lines (`: ping`).

## Choosing a Transport

| Transport | Direction (Runs Over) | Reconnect |
| --- | --- | --- |
| **Request/response** | Client asks, server answers (HTTP) | Not applicable |
| **Long polling** | Server to client (HTTP) | Implicit — the client asks again after each response |
| **Server-Sent Events** | Server to client (HTTP) | Built in, resuming from `Last-Event-ID` |
| **WebSockets** | Both directions (TCP, after an HTTP upgrade) | Your code owns it |

Take the simplest option that carries the traffic: plain [Fetch](../06-frontend/02-browser-technologies.md) requests for most screens, Server-Sent Events for a server-driven stream, and WebSockets only when the client must push as freely as the server.

## References

1. [HTTP Methods Cheat Sheet](https://devsheets.io/sheets/http-methods) — DevSheets
2. [HTTP Status Codes Cheat Sheet](https://devsheets.io/sheets/http-status-codes) — DevSheets
3. [GraphQL Cheat Sheet](https://devsheets.io/sheets/graphql) — DevSheets
4. [Nginx Load Balancing](https://devsheets.io/sheets/nginx/load-balancing) — DevSheets
