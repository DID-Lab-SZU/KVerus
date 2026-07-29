# Verus Syntax Quick Reference

Sources:
- `source/docs/guide/src/modes.md`
- `source/docs/guide/src/spec_vs_proof.md`
- `source/docs/guide/src/requires_ensures.md`
- `source/docs/guide/src/reference-at-sign.md`
- `source/docs/guide/src/reference-attributes.md`
- `source/docs/guide/src/calling-unverified-from-verified.md`

## Modes

Verus has three function modes:

- `spec`: ghost, mathematical, deterministic, not compiled.
- `proof`: ghost, proves facts, not compiled.
- `exec`: compiled Rust code; `exec` is the default.

Call permissions:

| Context | Can use spec | Can use proof             | Can use exec |
| ------- | ------------ | ------------------------- | ------------ |
| `spec`  | yes          | no                        | no           |
| `proof` | yes          | yes                       | no           |
| `exec`  | yes          | yes, inside proof context | yes          |

Typical syntax:

```rust
spec fn model(x: int) -> bool { x >= 0 }

proof fn lemma(x: int)
    requires
        x >= 0,
    ensures
        model(x),
{
}

fn checked(x: u64) -> (r: u64)
    ensures
        r == x,
{
    x
}
```

## Preconditions and Postconditions

Use `requires` for caller obligations and `ensures` for callee guarantees. Name return values when postconditions refer to them:

```rust
fn f(x: u64) -> (r: u64)
    requires
        x < 10,
    ensures
        r == x + 1,
{
    x + 1
}
```

If an existing contract is too weak for modular verification, strengthen it only when the active task permits specification changes. For proof-repair tasks, follow the active task skill's constraints.

## Spec Preconditions

`spec fn` uses `recommends`, not `requires`:

```rust
spec fn index_ok(i: int, len: int) -> bool
    recommends
        0 <= i < len,
{
    i < len
}
```

## Assertions

Use `assert` to expose a local fact to the SMT solver. `assume` is useful while developing a proof, but complete proofs should replace assumptions with checked facts.

Use specialized assertion forms when the obligation matches the solver:

```rust
assert((x & mask) <= x) by (bit_vector);
assert(pow(2, 8) == 256) by (compute_only);
assert(x * y == y * x) by (nonlinear_arith);
```

## Verus View

`expr@` is shorthand for `expr.view()` and is commonly used for the abstract view of exec-mode values:

```rust
assert(seq@.len() == n);
assert(tracked_value@ == expected);
```

For `Tracked<T>` or `Ghost<T>`, the guide shows pattern matching to unwrap values at function boundaries; see `references/ghost-tracked.md`.

## Minimal Migration Reminders

`#[verifier::external_body]` marks a verified/unverified boundary: Verus checks the signature contract but not the body. This introduces trusted assumptions, so use it only when the active task explicitly allows externalizing an implementation.
