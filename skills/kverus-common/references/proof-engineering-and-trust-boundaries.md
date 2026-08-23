# Proof Engineering and Trust Boundaries

Source scope: guide

Sources:
- `source/docs/guide/src/proof_functions.md`
- `source/docs/guide/src/broadcast_proof.md`
- `source/docs/guide/src/reference-proof-signature.md`
- `source/docs/guide/src/reference-assume-specification.md`
- `source/docs/guide/src/ghost_vs_exec.md`
- `source/docs/guide/src/reference-var-modes.md`
- `source/docs/guide/src/reference-attributes.md`
- `source/docs/guide/src/reference-unwind-sig.md`
- `source/docs/guide/src/exec_attr.md`

Use this reference for axiom-like declarations, external API specifications,
trusted-boundary decisions, and final proof cleanup.

## Contents

- [Axiom Outcomes](#axiom-outcomes)
- [Classification](#classification)
- [Ghost and Tracked Construction](#ghost-and-tracked-construction)
- [External API Specifications](#external-api-specifications)
- [Proof Hygiene](#proof-hygiene)

## Axiom Outcomes

A bodyless `axiom fn`, `broadcast axiom fn`, bodyless proof declaration, or
trait method that supplies an unproved contract is a trusted assumption. Do not
report it as proved merely because Verus accepts its postcondition.

Use one of these resolved outcomes:

- `proved`: replace the assumption with a checked proof body or lemma.
- `moved-to-invariant`: make constructors, callers, or implementors establish it.
- `deleted`: remove an unused, false, or unnecessary assumption.
- `narrowed`: retain only the contract required at its call sites.
- `trusted-boundary`: retain a minimal assumption for a concrete unmodeled source.

Use `blocked` or `deferred` when a plausible local proof is unfinished. Proof
difficulty, a missing helper lemma, or an initial mode error is not evidence of
a trusted boundary. Never replace an axiom with `assume`, `admit`, or
`#[verifier::external_body]`.

## Classification

Classify the fact before editing:

| Class | Typical facts | Preferred treatment |
| --- | --- | --- |
| A: mathematical | Collections, arithmetic, alignment, shifts, bounds | Prove a narrow lemma with quantifiers, extensional reasoning, arithmetic lemmas, or a specialized solver. |
| B: construction | Tracked constructors, token repackaging, direct view equalities | Construct or update the tracked value in proof mode and repair ghost/tracked ownership. |
| C: derived contract | State invariants, constructor guarantees, trait requirements | Move the primitive fact into an invariant, precondition, or implementor obligation and derive consequences with lemmas. |
| D: unmodeled boundary | FFI, MMIO, hardware, raw pointers, allocator behavior, opaque runtime/library state | Audit A/B/C routes, narrow the assumption, and document the exact external source. |

An `uninterp spec fn` is not automatically Class D. First decide whether it is
an intentional model of external behavior or an unfinished project-local model
that should be defined, constrained by an invariant, or proved by construction.

For A, B, and C, attempt the smallest checked proof route before choosing an
outcome. If it fails, record the attempted route and the fresh verifier blocker.
For D, inspect every call site and keep only the guarantee that callers need.

## Ghost and Tracked Construction

- Return tracked resources with `tracked` parameters or return binders.
- Construct tracked structs and enums directly when their fields permit it.
- Use proof-mode collection operations such as `tracked_insert`, `tracked_push`,
  split/join methods, or checked constructors rather than spec-mode updates.
- Mark proof-only fields `ghost` or `tracked` according to their ownership role.
  Review a tracked type whose entire state is ghost as a possible ghost/spec model.
- Return all-tracked tuple components directly. Use `Tracked<T>` wrappers when a
  tracked value crosses an exec boundary or participates in a mixed-mode value.

A `spec`-versus-`proof` error in a constructor is a proof-shape problem. It is a
trusted boundary only when the constructed resource necessarily contains an
opaque external fact.

## External API Specifications

`assume_specification` supplies a contract for calls to an external function; it
does not verify that function's implementation. Likewise, replacing an
`external_body` with a checked body does not verify an opaque, unsafe, atomic,
raw-pointer, or hardware operation called by that body.

Audit proof state transitions and executable side effects separately. Trace each
opaque call to its active external contract, including panic behavior, atomic
memory ordering, and caller safety obligations. Do not move local ownership or
invariant facts into an external specification merely to make a call verify.

When an external operation is used in spec position, connect the operation to
its model with `#[verifier::when_used_as_spec(model)]`. Keep the model at the
external contract and use the original qualified API at call sites. Do not claim
`no_unwind` for an operation that can panic; express the condition under which
unwinding is excluded or use a conditional `may_panic()` allowance so callers
must prove the non-panic path or carry that allowance.

At expression-level `#[verus_spec(...)]` overrides, call the target through a
module-qualified path so the override resolves to the intended function.

## Proof Hygiene

- Name proved facts and tracked-state constructors by distinct roles when the
  project has such a convention.
- Use `old(...)` directly for entry-state expressions instead of introducing a
  ghost alias only to recover the pre-state.
- Reuse an existing spec result and its projections instead of duplicating its
  filters, sets, maps, or ranges in proof code.
- Combine adjacent lower and upper bounds with a chained comparison when they
  constrain the same value.
- After removing an assertion, remove locals, comments, empty branches, and
  witness scaffolding that served only that assertion.
- Test repeated quantified bridges, unchanged-field equalities, and empty
  `assert(...) by {}` blocks as removal candidates; retain the smallest facts
  required for SMT instantiation.
- Remove single-caller bridge lemmas left behind after proving an axiom unless
  the lemma has a stable API role or concrete reuse.
- Preserve executable expressions, side effects, ownership behavior, and data
  flow. Do not add runtime clones or equivalent rewrites only to simplify proof.

Verification success is necessary but does not prove external runtime behavior
and does not justify a broader trusted boundary.
