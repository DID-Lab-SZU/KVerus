# Async Functions

**Status:** Not supported
**Category:** Items
**Guide ref:** [features.md — Items](source/docs/guide/src/features.md)

## What's unsupported

Verus cannot verify `async fn` declarations. The verifier rejects any function declared with the `async` keyword.

```rust
// REJECTED by Verus
async fn fetch_data(url: &str) -> Result<Vec<u8>, Error> {
    // ...
}
```

## Workarounds

### 1. Synchronous wrapper with `external_body`

Write the async logic in an unverified module and expose a synchronous interface to verified code.

```rust
// In unverified code:
pub async fn fetch_data_async(url: &str) -> Result<Vec<u8>, Error> { /* ... */ }

// In verified code: call via external_body synchronous wrapper
#[verifier::external_body]
fn fetch_data(url: &str) -> (result: Result<Vec<u8>, Error>)
{
    // Call the async version using a runtime block_on or similar
    unimplemented!()
}
```

### 2. Factor async out of verified boundary

Keep all async code outside the verified crate entirely. Verified code handles pure computation; the unverified async layer orchestrates I/O.

## Edge cases

- `async fn` in trait definitions is also unsupported.
- `async` closures are unsupported (see also [async-blocks.md](async-blocks.md)).
- Even if the function body contains no `.await`, the `async` keyword alone causes rejection.

## Related

- [async-blocks.md](async-blocks.md)
- [await.md](await.md)
