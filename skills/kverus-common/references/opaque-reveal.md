# Opaque and Reveal

Sources:
- `source/docs/guide/src/opaque.md`

If unfolding a spec function causes timeouts or bad automation, use `opaque` on the function and reveal it only inside focused proof blocks:

```rust
reveal(f);
assert(f(x) == expected);
```

Use `closed spec` for module abstraction; use `opaque`/`reveal` for controlling automation and performance.
