# Quantifiers

Sources:
- `source/docs/guide/src/forall.md`
- `source/docs/guide/src/quantproofs.md`

Using a `forall` depends on triggers. If a quantified fact does not instantiate, mention a trigger-shaped expression explicitly:

```rust
assert(s[i] == expected);
assert(P(s[i]));
```

Proving a `forall` that needs a lemma:

```rust
assert forall|i: int| 0 <= i < n implies P(i) by {
    lemma_p(i);
};
```

Using an `exists` with a hidden witness:

```rust
let j = choose|j: int| G(i, j);
lemma_g_proves_f(i, j);
```

Trigger rules:

- A trigger must mention all bound variables, possibly across a multi-trigger.
- A trigger should be a function call, field access, indexing expression, or bitwise expression.
- Avoid triggers based only on arithmetic or boolean comparisons.
- Prefer a trigger that appears naturally near the desired goal.
