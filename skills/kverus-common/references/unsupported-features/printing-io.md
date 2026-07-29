# Printing / I/O

**Status:** Not supported
**Category:** Types / Standard Library
**Guide ref:** [features.md — Types and standard library functionality](source/docs/guide/src/features.md)

## What's unsupported

Verus does not model I/O operations. This includes all printing macros, file I/O, network I/O, and standard streams.

```rust
// REJECTED by Verus
fn log_value(x: u64) {
    println!("value = {}", x);      // unsupported
    eprintln!("error!");             // unsupported
    std::fs::write("out.txt", "x"); // unsupported
}
```

Unsupported items include:
- `println!`, `print!`, `eprintln!`, `eprint!`, `format!`
- `dbg!`
- `std::io::*` (`Read`, `Write`, `BufReader`, `stdin`, `stdout`, etc.)
- `std::fs::*`
- `std::net::*`

## Workarounds

### 1. Remove I/O from verified code

The cleanest approach: verified functions compute results, unverified code handles I/O.

```rust
// Verified: pure computation
fn compute_result(input: &[u64]) -> (result: u64)
    ensures result == spec_compute(input@),
{
    // ...
}

// Unverified: I/O
fn main() {
    let input = read_input();       // unverified
    let result = compute_result(&input);  // verified
    println!("{}", result);         // unverified
}
```

### 2. `external_body` for logging

If you need logging calls in otherwise-verified code:

```rust
#[verifier::external_body]
fn debug_log(msg: &str)
{
    eprintln!("[DEBUG] {}", msg);
}
```

This is safe because `debug_log` has no postconditions — Verus trusts nothing about its behavior.

### 3. `external_fn_specification` for format-free wrappers

If you have a simple I/O function that doesn't use format strings:

```rust
#[verifier::external_body]
fn write_bytes(path: &str, data: &[u8]) -> (result: Result<(), IoError>)
{
    unimplemented!()
}
```

## Edge cases

- `format!` is unsupported because it relies on `Debug`/`Display` traits (see [debug-serde-traits.md](debug-serde-traits.md)).
- `write!` / `writeln!` to a `Vec<u8>` or `String` buffer is also unsupported.
- `panic!` with format args is unsupported; `panic!("literal")` may work in some contexts.
- `#[test]` functions that use `println!` are fine — Verus doesn't verify test functions.

## Related

- [debug-serde-traits.md](debug-serde-traits.md)
