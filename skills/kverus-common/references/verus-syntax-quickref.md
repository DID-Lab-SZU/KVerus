# Verus Syntax Quick Reference

Sources:
- `source/docs/guide/src/modes.md`
- `source/docs/guide/src/spec_vs_proof.md`
- `source/docs/guide/src/requires_ensures.md`
- `source/docs/guide/src/reference-at-sign.md`
- `source/docs/guide/src/reference-attributes.md`
- `source/docs/guide/src/calling-unverified-from-verified.md`
- `source/docs/guide/src/exec_attr.md`
- `examples/guide/exec_attr.rs`

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

For spec and proof declarations, use `verus!` syntax:

```rust
verus! {

spec fn model(x: int) -> bool { x >= 0 }

proof fn lemma(x: int)
    requires
        x >= 0,
    ensures
        model(x),
{
}

}
```

## Attribute-First Executable Specifications

For newly added specifications on executable Rust, prefer `#[verus_spec(...)]`
when the active Verus version supports the required position. This preserves the
native Rust signature and keeps verification annotations outside the executable
body:

```rust
#[verus_spec(r =>
    requires
        x < 10,
    ensures
        r == x + 1,
)]
fn checked(x: u64) -> u64 {
    x + 1
}
```

Attach `#[verus_spec(...)]` to loops for invariants and other supported loop
clauses. Function-item attributes do not normally require an extra crate
feature, but attributes on loops, expressions, or call sites require
`#![feature(proc_macro_hygiene)]` on the current Verus toolchain. Add that
feature only when such non-item attributes are used; an E0658 diagnostic saying
that custom attributes cannot be applied to expressions indicates it is
missing.

When moving an executable function out of `verus!`, convert `proof { ... }` to
`proof! { ... }`. Use `proof_decl!` for ghost or tracked variables that must
remain in scope across executable statements or later proof blocks; values
declared inside `proof!` remain local to that block. For hidden ghost/tracked
parameters and returns, use the attribute's `with` clause and the active
checkout's supported call-site `#[verus_spec(with ...)]` or `proof_with!` form.

Prefer `#[verus_spec]` for every executable function in a ghost/tracked call
chain. The guide documents compatibility problems when `proof_with!` targets an
executable function defined inside `verus!`. Keep `verus!` for `spec fn`,
`proof fn`, `assume_specification`, and constructs not supported by attributes.
Do not rewrite an already working contract solely for style unless the task asks
for syntax modernization. Confirm exact syntax against
`examples/guide/exec_attr.rs` in the active Verus checkout and verify it with the
resolved command. After an attribute-based migration, also run the project's
normal Rust build or Verus `--compile` path when available to check the erased
executable code.

## Preconditions and Postconditions

Use `requires` for caller obligations and `ensures` for callee guarantees. In
`#[verus_spec(r => ...)]`, the binder before `=>` names the executable return
value for postconditions; in `verus!`, use a named return such as
`-> (r: u64)`.

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

For `Tracked<T>` or `Ghost<T>`, the guide shows pattern matching to unwrap values at function boundaries; see `ghost-tracked.md`.

## Minimal Migration Reminders

`#[verifier::external_body]` marks a verified/unverified boundary: Verus checks the signature contract but not the body. This introduces trusted assumptions, so use it only when the active task explicitly allows externalizing an implementation.
