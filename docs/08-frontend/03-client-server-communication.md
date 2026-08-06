# Client-Server Communication

## HTTP

| Method | Idempotent | Safe | Description |
| --- | --- | --- | --- |
| GET | Yes | Yes | Retrieve resource |
| POST | No | No | Create resource |
| PUT | Yes | No | Replace resource |
| PATCH | No | No | Partial update |
| DELETE | Yes | No | Delete resource |

| Code Range | Category | Examples |
| --- | --- | --- |
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx | Server Error | 500 Internal Error, 502 Bad Gateway |

## REST

Uses HTTP semantics for API design. Resources identified by URI, stateless requests.

```text
GET    /api/users           # List
GET    /api/users/123       # Get one
POST   /api/users           # Create
PUT    /api/users/123       # Replace
DELETE /api/users/123       # Delete

GET /api/users?role=admin&active=true    # Filter
GET /api/users/123/posts                 # Relationship
```

## GraphQL

Clients request exactly the data they need — no over- or under-fetching.

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
| Endpoints | Multiple | Single |
| Over-fetching | Common | None |
| Type safety | Optional | Built-in |
| Caching | Native HTTP | Requires setup |

## WebSockets

Bidirectional real-time communication over a persistent TCP connection.

```javascript
const socket = new WebSocket('wss://api.example.com/ws');

socket.onopen = () => socket.send(JSON.stringify({ type: 'SUBSCRIBE', channel: 'updates' }));
socket.onmessage = (event) => console.log('Received:', JSON.parse(event.data));
socket.onclose = (event) => console.log('Disconnected:', event.code);
socket.onerror = (error) => console.error('Error:', error);

socket.close(1000, 'Done');
```

## Server-Sent Events

One-way streaming from server to client over a single HTTP connection. The browser
reconnects automatically and resumes from the last received event id.

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
| `data` | Payload; repeat the field for multi-line values |
| `event` | Named event type; defaults to `message` |
| `id` | Sent back as `Last-Event-ID` on reconnect |
| `retry` | Reconnect delay in milliseconds |

Notes:

- Text only — binary payloads must be encoded (e.g. base64).
- Over HTTP/1.1 the 6-connections-per-origin limit applies; HTTP/2 removes it.
- Proxies may buffer the stream; disable buffering and send periodic comments (`: ping`) as keep-alive.

| Technology | Use Case | Browser Support |
| --- | --- | --- |
| WebSockets | Bidirectional real-time | Excellent |
| Server-Sent Events | Server-to-client streaming | Good |
| Long Polling | Fallback | Universal |
