# `Pin`

**Status:** Not supported
**Category:** Types / Standard Library
**Guide ref:** [features.md — Types and standard library functionality](source/docs/guide/src/features.md)

## What's unsupported

Verus has no model for `std::pin::Pin<P>`. The type cannot be used in verified code — not as a parameter, return type, struct field, or local variable.

```rust
use std::pin::Pin;

// REJECTED by Verus
fn process(pinned: Pin<&mut MyStruct>) {
    // ...
}
```

## Workarounds

### 1. Use regular references

If pinning is only needed for async (e.g., `Future::poll`), and you've moved async out of the verified boundary, replace `Pin<&mut T>` with `&mut T` in the verified interface.

```rust
fn process(data: &mut MyStruct) -> (result: u64)
    requires old(data).is_valid(),
    ensures data.is_valid(),
{
    // verified logic
}
```

### 2. `external_body` wrapper

If you need `Pin` at runtime (e.g., interfacing with an async runtime or self-referential struct), wrap the pinned operation:

```rust
#[verifier::external_body]
fn poll_future(cx: &mut Context) -> (result: Poll<Output>)
{
    unimplemented!()
}
```

### 3. Avoid self-referential types

The main Rust use case for `Pin` is self-referential types. In verified code, redesign data structures to avoid self-references — use indices or handles instead of internal pointers.

## Edge cases

- `Pin<Box<T>>` is also unsupported, even though `Box<T>` is supported.
- `Unpin` trait bounds are ignored by Verus but the `Pin` wrapper itself is still rejected.
- If a dependency's API requires `Pin`, you must wrap that dependency call in `external_body`.

## Related

- [async-functions.md](async-functions.md)
- [await.md](await.md)
