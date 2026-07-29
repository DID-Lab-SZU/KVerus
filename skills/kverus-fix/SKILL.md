---
name: kverus-fix
description: Fix Verus verification errors starting from an entry target file by iterating edits with an explicit verify command until verification succeeds. Use when verification fails and you want minimal proof-preserving repairs across the smallest necessary dependency closure.
argument-hint: target=path/to/entry.rs verify="<verification command>" [error_message="<initial error message>"] [out_path=path/to/summary-dir]
license: MIT
compatibility: Requires Codex CLI and a working Verus verification command.
user-invocable: true
metadata:
  author: kverus
  version: "1.0"
---

Fix Verus verification failures starting from one explicit entry target file by iterating edits and verification until the verify command succeeds.

Preferred invocation:

```text
$kverus-fix target=path/to/entry.rs verify="<verification command>" error_message="<initial error message>" out_path=path/to/output
```

If either `target` or `verify` is missing, ask for the missing value and stop.

Treat `target` as an entry file for diagnosis, not as the only file that may be edited.

If `error_message` is provided, use it as a first-pass hint, then always trust fresh output from the verification command.

If `out_path` is missing, use a reasonable workspace-local default path and report it.

## Shared Verus References

If a failure appears caused by Verus syntax, modes, ghost/tracked values, loop invariants, quantifiers, specialized solvers, or tokenized state-machine rules, read the relevant reference under `../kverus-common/references/` before editing.

## Objective

Given Verus code and its verification failure, produce a corrected version that passes verification while preserving proof intent.

Start from `target`, then modify only the smallest necessary dependency closure required to clear the verification failure.

## Hard Constraints

1. Do not modify existing `requires`.
2. Do not modify existing `ensures`.
3. Do not add new `assume`.
4. Do not add new `admit`.
5. Do not add `#[verifier::external_body]` to skip proof obligations.
6. Keep edits minimal and localized to the smallest necessary dependency closure.
7. Do not edit unrelated files.
8. Do not modify the exec code.

## Required Workflow

1. Inspect the entry target file and immediate dependencies.
2. If `error_message` is provided, use it to prioritize the first repair attempt.
3. Run the provided verification command to collect current errors.
4. Apply the smallest fix addressing the highest-signal error.
5. Re-run verification.
6. Repeat until verification succeeds or a real blocker remains.

Avoid broad refactors up front.

## Validation Loop

Use this exact loop:

1. inspect
2. verify
3. minimally edit
4. verify again
5. repeat

## Failure Policy

If you cannot make verification succeed without violating constraints:

1. Stop at the smallest blocking point.
2. Do not fabricate behavior.
3. Do not bypass proof obligations with banned constructs.
4. Generate a concise summary file under `out_path` describing:
   - blocking location(s)
   - why constraints prevent a compliant fix
   - what additional assumptions or spec changes would be required

## Output Expectations

Perform edits in-place in the workspace when allowed.

Keep explanation short unless asked for details.
