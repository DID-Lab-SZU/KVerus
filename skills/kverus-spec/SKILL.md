---
name: kverus-spec
description: Add Verus specification scaffolding to an entry target file while preserving executable behavior. Use when you want stronger proof-ready specs (requires, ensures, invariants, decreases, recommends, spec helpers) without fully finishing proofs.
argument-hint: target=path/to/entry.rs verify="<verification command>" [knowledge="<related knowledge>"]
license: MIT
compatibility: Requires Codex CLI and a working Verus verification command.
user-invocable: true
metadata:
  author: kverus
  version: "1.0"
---

Add Verus specification scaffolding to a target file and iterate with verification until the file becomes a stronger proof-ready baseline.

Preferred invocation:

```text
$kverus-spec target=path/to/entry.rs verify="<verification command>" knowledge="<related knowledge>"
```

If either `target` or `verify` is missing, ask for the missing value and stop.

If `knowledge` is missing, continue without it.

## Shared Verus References

If adding specs requires Verus syntax, modes, loop invariants, `decreases`, `recommends`, ghost/tracked values, or spec/proof helper patterns, read the relevant reference under `../kverus-common/references/` before editing.

## Objective

Add only the specification structure needed to improve proof readiness of the target file.

Focus on:

1. `requires`
2. `ensures`
3. loop invariants
4. `decreases`
5. `recommends`
6. `spec fn`
7. ghost/spec helper declarations

Do not focus on finishing proofs.

## Important Clarification

The goal is NOT to fully prove the code.

The goal is to improve the specification layer while preserving executable behavior and preparing the file for a later proof-generation stage.

## Hard Constraints

1. In-place edits only: edit the target file in place.
2. Preserve behavior: do not rewrite executable logic unless a tiny local change is required to express a valid specification.
3. Spec-only bias: prefer adding or refining specifications over adding proof steps.
4. Avoid introducing `assert(... ) by (...)`, `calc!`, new proof lemmas, or proof bodies unless the file would otherwise become syntactically invalid.
5. No unsound shortcuts: do not add `assume`, `admit`, or `#[verifier::external_body]`.
6. Preserve source structure as much as possible: item order, function order, impl/block structure, comments, and source locality.

## Working Style

1. Inspect the target file.
2. Use `knowledge` when relevant.
3. Make minimal edits.
4. Run the verification command after meaningful changes.
5. Use verification results to guide small follow-up edits.

## Output Expectations

Apply edits directly to the target file.

Do not return explanations unless requested.
