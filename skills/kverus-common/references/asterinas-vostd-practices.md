# Asterinas and VOSTD Practices

Source scope: project

Sources:
- Asterinas/VOSTD repository layout and verification workflow.
- [PR #630 review](https://github.com/asterinas/vostd/pull/630#discussion_r3576915131)
- [PR #656 review](https://github.com/asterinas/vostd/pull/656#issuecomment-5019089808)
- [PR #657 review](https://github.com/asterinas/vostd/pull/657#discussion_r3612471054)
- [PR #673 review](https://github.com/asterinas/vostd/pull/673#discussion_r3662532282)
- [PR #674 review](https://github.com/asterinas/vostd/pull/674#discussion_r3672552179)
- [PR #677 review](https://github.com/asterinas/vostd/pull/677#discussion_r3682395055)
- [PR #692 review](https://github.com/asterinas/vostd/pull/692)

Use this reference only for targets in the Asterinas/VOSTD repository. Apply the
general proof and trust-boundary rules before these project-specific conventions.

## Contents

- [Verification Gates](#verification-gates)
- [Repository Context](#repository-context)
- [External API Boundaries](#external-api-boundaries)
- [Project Proof Conventions](#project-proof-conventions)
- [Historical Classification Examples](#historical-classification-examples)

## Verification Gates

Use `make` as the full repository verification gate. For fast iteration on a
known OSTD module, use:

```bash
cargo dv verify --targets ostd -- -Awarnings --verify-only-module <module_path>
```

Treat targeted verification as partial feedback. Report full success only after
`make`, unless the task explicitly requested targeted-only verification or the
full gate is blocked. Preserve the exit status of `make`; do not infer success
from a shell pipeline whose last process succeeded.

For a focused target such as `path/to/file.rs::item_name`, verify the enclosing
module rather than passing the item locator to Verus. Keep edits centered on the
item and its smallest verifier-demonstrated dependency closure.

## Repository Context

- Read the target file and relevant `.rs` siblings in the same module.
- For targets under `ostd/src/`, inspect the corresponding `ostd/specs/**`
  subsystem model when it defines the same concepts.
- Inspect `crate::specs::arch::*`, `crate::specs::task::*`,
  `verified_libs/vstd_extra`, `verified_libs/verified_bitflags`,
  `verified_libs/ostd-pod`, and `ostd/libs/align_ext` only when imported or
  implicated by a verification failure.
- Use `tools/verus/source/vstd` as the standard-library proof fallback when local
  helpers are insufficient.

## External API Boundaries

Place reusable external API specifications in
`verified_libs/vstd_extra/src/external/<topic>.rs` and re-export them through the
`external` module. Do not place an ad hoc assumption beside an OSTD caller.

For each retained external helper, check that `requires` states the caller's
safety obligations and `ensures` exposes the semantic facts callers use. Moving
an unconstrained contract under `external/` centralizes it but does not justify it.

When removing `external_body`, trace standard-library atomics, unsafe calls, raw
pointers, and other opaque side effects to their active `assume_specification` or
external contract. A checked tracked permission update does not verify the
runtime operation. Record the residual boundary in evaluation and semantic-audit
results even when `make` passes.

## Project Proof Conventions

- Use `lemma_*` for proved facts and invariant preservation, and `tracked_*` for
  helpers that create or update tracked state.
- Declare proof-only model types and fields explicitly as `ghost` or `tracked`.
  Review all-ghost tracked structs as possible ghost/spec-state designs.
- Return all-tracked proof tuple components directly rather than wrapping every
  component in `Tracked<_>`; retain wrappers at exec or mixed-mode boundaries.
- Preserve the documented direction and upstream API shape of roundtrip
  definitions and verified-library mirrors such as `bitflags`.
- Avoid `Set::new_assuming_finite` and warning-suppression attributes as proof
  workarounds. Prefer reviewed spec-library construction patterns.
- Put newly added `vstd`/Verus imports before imports inherited from the original
  Rust source and keep the groups visually separate.
- Keep adjacent verified items in one `verus!` block when no non-Verus item
  separates them.
- Preserve the original executable API and data flow. For example, retain
  `range.len()` and repair proof ownership instead of reconstructing the value or
  adding an executable `clone()` solely for proof convenience.
- Run redundant-assert cleanup, `make`, `make fmt`, and the postprocess checks
  before finalizing proof-sensitive changes or a proof PR.

## Historical Classification Examples

Use history as evidence for a proof shape or boundary classification, never as
permission to copy `assume`, `admit`, or `external_body`.

- Page-table arithmetic and finite-set freshness facts are Class A and should be
  checked lemmas when their statements are mathematical.
- Entry-owner tracked constructors are Class B and should normally become direct
  proof constructors after ghost/tracked mode repair.
- Ghost-tree positivity and page-table configuration facts are Class C when they
  follow from validity predicates, constructors, or trait obligations.
- `kvirt_alloc_range_bounds` is a Class D example because it connects an
  uninterpreted allocator model to an external runtime allocator.
- `axiom_kernel_range_valid` is a Class D example when it bridges architecture
  constants and page-table bounds that the current model does not establish.
- `perm_u64_with_value` is a Class D example when its permission depends on
  opaque `vstd::atomic` view state.

Recheck every historical classification against current source and call sites.
A prior trusted boundary may become provable after the model or library changes.
