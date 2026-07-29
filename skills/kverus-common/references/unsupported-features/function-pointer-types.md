# Function Pointer Types

**Status:** Not supported
**Category:** Types
**Guide ref:** [features.md — Types and standard library functionality](source/docs/guide/src/features.md)

## What's unsupported

Verus does not support function pointer types (`fn(T) -> U`). You cannot store, pass, or invoke bare function pointers in verified code.

```rust
// REJECTED by Verus
fn apply(f: fn(u64) -> u64, x: u64) -> u64 {
    f(x)
}

// REJECTED by Verus
let fp: fn(u64) -> u64 = my_function;
```

## Workarounds

### 1. Use generic type parameters with `Fn` trait bounds

Verus supports closures and `Fn`/`FnOnce` trait bounds. Replace function pointer parameters with generics:

```rust
fn apply<F: Fn(u64) -> u64>(f: F, x: u64) -> (result: u64)
{
    f(x)
}
```

### 2. Use `FSpec` for spec-mode function values

In specifications, use `spec_fn` (spec closures) or `FnSpec`:

```rust
proof fn example(f: spec_fn(u64) -> u64)
    requires f(0) == 1,
{
    // ...
}
```

### 3. Use `external_body` dispatch

If you need runtime function pointer dispatch (e.g., vtable-like patterns), wrap it:

```rust
#[verifier::external_body]
fn dispatch(table: &FnTable, op: Op, arg: u64) -> (result: u64)
{
    unimplemented!()
}
```

### 4. Use an enum-based dispatch

Replace function pointer tables with an enum and a match:

```rust
enum Operation {
    Add,
    Multiply,
}

fn dispatch(op: Operation, a: u64, b: u64) -> (result: u64)
{
    match op {
        Operation::Add => a + b,
        Operation::Multiply => a * b,
    }
}
```

## Edge cases

- `fn()` types in struct fields are rejected.
- Casting a function item to `fn(...)` pointer type is rejected.
- Closures that don't capture anything still cannot be coerced to `fn(...)` in Verus.
- `extern "C" fn(...)` pointer types are also unsupported.
