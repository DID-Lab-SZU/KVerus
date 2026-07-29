# `Mutex` / `RwLock` (Standard Library)

**Status:** Not supported
**Category:** Multi-threading
**Guide ref:** [features.md — Multi-threading](source/docs/guide/src/features.md)

## What's unsupported

Verus does not support `std::sync::Mutex` or `std::sync::RwLock`. These types cannot be used in verified code because Verus cannot reason about their locking semantics and interior mutability.

```rust
use std::sync::Mutex;

// REJECTED by Verus
fn increment(counter: &Mutex<u64>) {
    let mut guard = counter.lock().unwrap();
    *guard += 1;
}
```

## Workarounds

### 1. Use vstd verified lock implementations

Verus provides its own verified lock types with proof obligations:

```rust
use vstd::prelude::*;
use vstd::lock::*;

fn increment(lock: &Lock<u64>)
    // Lock carries an invariant that Verus can reason about
{
    let (val, guard) = lock.acquire();
    // use val, then release guard
}
```

See: [vstd lock documentation](https://verus-lang.github.io/verus/verusdoc/vstd/lock/index.html)

### 2. `external_body` wrapper

If you need `std::sync::Mutex` at runtime for compatibility:

```rust
#[verifier::external_body]
struct VerifiedMutex<T> {
    inner: std::sync::Mutex<T>,
}

#[verifier::external_body]
fn lock_and_read<T: Copy>(m: &VerifiedMutex<T>) -> (val: T)
{
    *m.inner.lock().unwrap()
}
```

### 3. Use vstd atomics for simple counters

For atomic integer operations, vstd provides verified atomic types:

```rust
use vstd::atomic_ghost::*;

// AtomicU64 with ghost state for verification
```

See: [vstd atomic_ghost documentation](https://verus-lang.github.io/verus/verusdoc/vstd/atomic_ghost/index.html)

## Edge cases

- `MutexGuard` and `RwLockReadGuard` / `RwLockWriteGuard` are also unsupported (they come from std).
- `parking_lot::Mutex` and similar third-party locks are equally unsupported.
- `Condvar` is unsupported.
- vstd's `Lock` and atomics have different APIs — not a drop-in replacement.
- `Mutex::new()` in a `static` (via `OnceLock` or `lazy_static!`) is unsupported on multiple levels.

## Related

- [drop.md](drop.md) — `MutexGuard` relies on `Drop` for unlock
- Verus guide: [concurrency](source/docs/guide/src/concurrency.md)
- Verus guide: [interior mutability](source/docs/guide/src/interior_mutability.md)
