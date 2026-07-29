# Localize Proof Context

Sources:
- `source/docs/guide/src/assert_by.md`

Use `assert(F) by { ... }` when the proof needs temporary facts that should not pollute the rest of the function:

```rust
assert(goal) by {
    lemma_a(x);
    lemma_b(x);
};
```

This is usually better than exposing many quantified facts globally.
