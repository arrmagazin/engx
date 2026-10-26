---
type: Guide
title: Node.js
description: Node.js 26 distilled — the event loop, modules, core APIs, HTTP, configuration, testing, security, and the release schedule.
tags: [backend, nodejs, javascript, typescript, runtime]
---

Node.js runs JavaScript on the server: one thread executes your code, an event loop dispatches I/O completions to it, and a small pool of native threads does the blocking work underneath. This guide distills the official documentation as of **Node.js 26** (Active LTS from 2026-10-28) and uses ES modules, promises, and `node:`-prefixed imports throughout.

| Fact | Value |
| --- | --- |
| **Release lines** | 26: Active LTS from 2026-10-28, end of life 2029-04-30. 24: Maintenance LTS until 2028-04-30. 22: end of life 2027-04-30 |
| **Production rule** | Run only Active or Maintenance LTS lines |
| **Schedule** | Up to 26, even majors became LTS. From 27, one major a year, each Alpha → Current → LTS |
| **TypeScript** | Runs `.ts` files directly by stripping types (stable) |
| **Built in** | `fetch`, `WebSocket`, Web Streams, `AbortController`, test runner, watch mode, `.env` loading |

```mermaid
flowchart LR
    T[timers] --> P[pending callbacks] --> PO[poll: I/O] --> C["check: setImmediate"] --> CL[close callbacks] --> T
```

After every callback, Node drains the `process.nextTick` queue and then the promise microtask queue, before the loop moves on. A callback that runs long — a big `JSON.parse`, a sync crypto call, a tight loop — stalls every other request on the process.

## Setup

```bash
npm init -y && npm pkg set type=module   # .js files are ES modules
node --watch app.ts                     # TypeScript runs directly; restarts on change
node --env-file=.env app.ts             # loads .env without a dependency
node --run test                         # runs a package.json script, skipping pre/post hooks
node --test                             # runs *.test.* files with the built-in runner
```

TypeScript support strips types and runs what is left, so it accepts only syntax that erases cleanly. No enums, no namespaces with runtime code, no parameter properties, no decorators, and no `.tsx`. `tsconfig.json` is ignored, including `paths`. Imports need the `.ts` extension, and type-only imports need `import type`. Type-check separately with `tsc --noEmit`.

## Modules

| File | Module system |
| --- | --- |
| `.mjs` | Always ESM |
| `.cjs` | Always CommonJS |
| `.js` | The nearest `package.json` `"type"`; with none, Node detects ESM syntax |

- `"exports"` in `package.json` is the public surface of a package: subpaths it does not list cannot be imported.
- `require()` can load an ES module, unless its graph uses top-level `await` (`ERR_REQUIRE_ASYNC_MODULE`).
- Always import built-ins with the `node:` prefix: `node:fs/promises`, `node:path`, `node:http`.

## Concurrency

The libuv thread pool — 4 threads by default, set with `UV_THREADPOOL_SIZE` before start-up — runs file system calls, `dns.lookup`, `zlib`, and asynchronous crypto. Network sockets do not use it.

| Tool | Runs | For |
| --- | --- | --- |
| `async`/`await` | On the main thread, between I/O waits | All I/O-bound code |
| `worker_threads` | JavaScript on another thread, sharing memory through `SharedArrayBuffer` | CPU-heavy work: hashing, parsing, image processing |
| `child_process` | Another OS process | Running other programs |
| `cluster` | Several processes sharing one port | Using every core without an external balancer |

```js
import { Worker } from 'node:worker_threads';

const worker = new Worker(new URL('./resize.js', import.meta.url), { workerData: { file } });
worker.on('message', (result) => console.log(result));
```

`AsyncLocalStorage` from `node:async_hooks` carries per-request context, such as a request id for logs, across every `await` without passing it by hand.

## Core APIs

| Module | Essentials |
| --- | --- |
| `node:fs/promises` | `readFile`, `writeFile`, `mkdir(p, { recursive: true })`, `readdir(p, { withFileTypes: true })`, `rm` |
| `node:path` | `join`, `resolve`, `extname`; `import.meta.dirname` replaces `__dirname` in ESM |
| `node:events` | `EventEmitter` with `on`, `once`, `emit`; `events.once(emitter, 'ready')` returns a promise |
| `node:stream` | Readable, Writable, Duplex, Transform; `pipeline` from `node:stream/promises` |
| `node:crypto` | `randomUUID`, `randomBytes`, `createHash`, `scrypt` for passwords, `timingSafeEqual` for secrets |
| Globals | `fetch`, `AbortSignal.timeout(ms)`, `URL`, `URLPattern`, `structuredClone`, `Temporal` (on by default in 26) |

Streams move data in chunks with back-pressure: when `write()` returns `false`, the writer waits for `'drain'`. Use `pipeline`, not `pipe`: it forwards errors, destroys every stream on failure, and accepts an `AbortSignal`.

```js
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

await pipeline(createReadStream('app.log'), createGzip(), createWriteStream('app.log.gz'));
```

```js
const res = await fetch('https://api.example.com/rates', { signal: AbortSignal.timeout(5_000) });
if (!res.ok) throw new Error(`rates: ${res.status}`);
const rates = await res.json();
```

## HTTP

```js
import { createServer } from 'node:http';

const server = createServer((req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ ok: true }));
});
server.listen(3000);
```

The Node.js project endorses no framework. Versions below are the current releases on npm:

| Framework | Character |
| --- | --- |
| **Express 5** | The default minimal router; v5 forwards rejected promises from async handlers to error middleware. Express 4 is in maintenance |
| **Fastify 5** | Faster, with JSON-schema validation and serialization built in, and a plugin system |
| **Hono 4** | Built on Web-standard `Request`/`Response`; the same code runs on Node, Bun, Deno, and edge runtimes |
| **NestJS** | An opinionated, Angular-style structure with dependency injection and decorators, compiled by `tsc` |

```js
import express from 'express';

const app = express();
app.use(express.json());
app.get('/users/:id', async (req, res) => {
  const user = await users.find(req.params.id);   // a rejection reaches the error handler
  user ? res.json(user) : res.sendStatus(404);
});
app.use((err, req, res, next) => res.status(500).json({ error: 'internal' }));
app.listen(3000);
```

## Errors and Shutdown

- An unhandled promise rejection crashes the process: since v15 the default `--unhandled-rejections` mode is `throw`. Await every promise, or attach a `catch`.
- Do not keep running after `uncaughtException`: the process state is unknown. Log, exit, and let the supervisor restart it.
- On `SIGTERM`, stop accepting connections and let the open requests finish:

```js
process.on('SIGTERM', () => server.close(() => process.exit(0)));
```

## Configuration

`--env-file=.env` and `process.loadEnvFile()` replace the `dotenv` package; `--env-file-if-exists` tolerates a missing file. Read `process.env` once at start-up into a validated config object, and fail fast when a value is missing. Since 26.12, `--config-file` reads Node's own flags from a JSON file.

## Testing

```js
// price.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { price } from './price.js';

test('applies the discount', () => {
  assert.equal(price(100, { discount: 0.1 }), 90);
});
```

`node --test` finds and runs test files. The runner has `describe`/`it`, hooks, mocks (`t.mock.fn`, mock timers), and snapshots, all stable. Coverage (`--experimental-test-coverage`) and module mocking are still experimental.

## Security

| Threat | Defence from the official guide |
| --- | --- |
| **Denial of service** | A reverse proxy in front; set `headersTimeout`, `requestTimeout`, `keepAliveTimeout`; handle socket errors |
| **Supply chain** | Lockfile and `npm ci`; pin versions; `npm audit`; `--ignore-scripts` where install scripts are not needed |
| **Prototype pollution** | Validate JSON against a schema; `Object.create(null)` for maps; `Object.hasOwn`; no recursive merges of user input |
| **Timing attacks** | `crypto.timingSafeEqual` to compare secrets |
| **Request smuggling** | Never enable `insecureHTTPParser` |
| **Debugger exposure** | No `--inspect` in production |

The permission model (`--permission`, stable) denies file system, network, child process, and worker access unless granted with `--allow-fs-read`, `--allow-net` and the like. The docs call it a seat belt for trusted code, not a sandbox for hostile code. The attack classes themselves are in [Web Application Security](../06-frontend/07-security-web.md).

---

## References

- [Node.js API Documentation](https://nodejs.org/api/) and [Learn Node.js](https://nodejs.org/en/learn)
- [Previous Releases and Schedule](https://nodejs.org/en/about/previous-releases)
- [TypeScript in Node.js](https://nodejs.org/api/typescript.html) and [Permissions](https://nodejs.org/api/permissions.html)
- [Event Loop, Timers, and nextTick](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- [Security Best Practices](https://nodejs.org/en/learn/getting-started/security-best-practices)
- [Node.js Core Modules](https://devsheets.io/sheets/nodejs-core-modules) and [Express](https://devsheets.io/sheets/express) cheat sheets (devsheets.io)

## Related Guides

- [Reactive Programming and FRP](../05-coding/02-reactive-programming.md) — event streams and back-pressure beyond Node's own streams
- [Messaging](../03-system-design/04-messaging.md) — queues and events between Node services
- [Java and Spring Boot](01-java-spring.md) and [.NET and ASP.NET Core](03-dot-net.md) — the same concerns on thread-per-request stacks
