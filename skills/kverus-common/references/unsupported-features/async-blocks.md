# Async Blocks

**Status:** Not supported
**Category:** Expressions
**Guide ref:** [features.md — Expressions and Statements](source/docs/guide/src/features.md)

## What's unsupported

Verus rejects `async { ... }` block expressions. These create anonymous `Future` values, which Verus has no model for.

```rust
// REJECTED by Verus
let fut = async {
    let x = some_async_op().await;
    x + 1
};
```

## Workarounds

### 1. Replace with synchronous block

If the async block is used purely for composition (no actual I/O), replace with a regular block or closure.

```rust
// Instead of async block, use a regular closure or block
let result = {
    let x = some_sync_op();
    x + 1
};
```

### 2. Move async blocks to unverified code

Wrap the async block in an `external_body` function that returns the computed result synchronously.

```rust
#[verifier::external_body]
fn compute_result() -> (r: u64)
{
    unimplemented!() // actual async logic lives here at runtime
}
```

## Edge cases

- `async move { ... }` is equally unsupported.
- Async blocks inside `external_body` functions are fine since Verus does not inspect those bodies.

## Related

- [async-functions.md](async-functions.md)
- [await.md](await.md)
