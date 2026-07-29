# `await` Expressions

**Status:** Not supported
**Category:** Expressions
**Guide ref:** [features.md — Expressions and Statements](source/docs/guide/src/features.md)

## What's unsupported

Verus rejects `.await` expressions. Since async functions and async blocks are unsupported, there is no context in which `.await` could appear in verified code.

```rust
// REJECTED by Verus
async fn example() {
    let data = fetch().await; // `.await` is unsupported
}
```

## Workarounds

### 1. Synchronous call via `external_body`

Replace the awaited call with a synchronous `external_body` wrapper.

```rust
#[verifier::external_body]
fn fetch_sync() -> (data: Vec<u8>)
{
    unimplemented!()
}

fn example() -> (data: Vec<u8>)
{
    fetch_sync()
}
```

### 2. Boundary pattern

Structure the crate so all `.await` calls live in unverified async glue code, while verified functions receive and return plain values.

## Edge cases

- `.await` on a pinned future is doubly unsupported (`Pin` is also unsupported).
- `futures::block_on` or `tokio::Runtime::block_on` inside `external_body` is valid at runtime since Verus ignores those bodies.

## Related

- [async-functions.md](async-functions.md)
- [async-blocks.md](async-blocks.md)
- [pin.md](pin.md)
