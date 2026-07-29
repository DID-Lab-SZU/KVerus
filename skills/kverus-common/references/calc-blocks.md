# Structured Calculation

Sources:
- `source/docs/guide/src/calc.md`

Use `calc!` when proving a transitive chain:

```rust
calc! {
    (==)
    a; {
        lemma_step_1();
    }
    b; {
        lemma_step_2();
    }
    c;
}
```

Use this for algebraic equality, ordering chains, and readability around intermediate expressions.
