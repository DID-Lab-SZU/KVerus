---
name: kverus-common
description: Shared Verus guide-derived syntax and proof-pattern reference material for other KVerus skills. Use when Codex is repairing Verus verification failures, adding Verus specs, migrating Rust to Verus-compatible code, or is uncertain about Verus modes, ghost/tracked variables, loop invariants, quantifiers, specialized solvers, state-machine/concurrency guidance, or common verification-error repair patterns.
---

# KVerus Common

Use this skill as a shared reference layer for KVerus tasks. It does not define a standalone repair workflow; pair it with task skills such as `kverus-fix`, `kverus-spec`, or `kverus-migrate`.

## Loading Rule

Before editing Verus code, load only the relevant reference:

- Syntax or mode confusion: read `references/verus-syntax-quickref.md`.
- Verification repair strategy or error triage: read `references/common-errors.md`.
- Proof construction, quantifiers, arithmetic, bit-vector, or SMT context issues: read the relevant file under `references/` — `proof-localization.md`, `quantifiers.md`, `solvers.md`, `arithmetic-lemmas.md`, `calc-blocks.md`, `opaque-reveal.md`, `lemma-shape.md`, or `set-reasoning.md`.
- Loop or recursive proof failures: read `references/invariants.md`.
- `ghost`, `tracked`, `Tracked<T>`, `Ghost<T>`, `@`, or erasure issues: read `references/ghost-tracked.md`.
- concurrency, invariants, permissions, or state-machine navigation: read `references/tokenized-state-machine.md`.
- Verus-unsupported features, forced rewrites, or trait associated constant limitations: read `references/unsupported-features/index.md`, then load the relevant topic file from that directory.

If more detail is needed, follow the source links at the top of each reference into:

- `database/verified/code/tools/verus/source/docs/guide/src`

## Global Verus Guide Rules

Carry these rules into all KVerus skills unless the user explicitly requests a different policy:

1. Follow the active task skill's hard constraints for whether contracts, executable code, assumptions, or external bodies may be changed.
2. Use `requires`, `ensures`, `assert`, loop invariants, and helper lemmas as the modular verification tools described by the guide.
3. Use `expr@` as the guide's shorthand for `expr.view()` when working with abstract views.
4. For loops, add invariants strong enough for entry, preservation, and exit reasoning; include surrounding facts explicitly when loop isolation requires them.
5. Use `assert(...) by (bit_vector)` for bitwise facts, `assert(...) by (compute_only)` for fully computable spec facts, and `assert(...) by (nonlinear_arith)` for nonlinear arithmetic facts.
6. Treat `#[verifier::external_body]` as a trusted verified/unverified boundary, not as an ordinary proof hint.

## Source Basis

This skill summarizes the local Verus guide under `database/verified/code/tools/verus/source/docs/guide/src`.
