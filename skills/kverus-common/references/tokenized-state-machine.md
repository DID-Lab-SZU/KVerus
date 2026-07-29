# Concurrency and State-Machine Navigation

Sources:
- `source/docs/guide/src/concurrency.md`
- `source/docs/guide/src/invariants.md`
- `source/docs/guide/src/interior_mutability.md`
- `source/docs/guide/src/reference-var-modes.md`
- `source/docs/guide/src/reference-opens-invariants.md`

## Guide Scope

The local Verus guide does not document the `tokenized_state_machine!` macro or token sharding API in detail. Its concurrency chapter points readers to the separate VerusSync/state-machine material for nontrivial ownership disciplines, including concurrent code and unsafe features such as pointers or unsafe cells.

Do not rely on undocumented token API details from this skill. For concrete tokenized state-machine syntax, inspect the local verified source or the Verus state-machine documentation available in the workspace.

Search hints:

```text
rg -n "tokenized_state_machine|sharding|InstanceId|opens_invariants" source/vstd source/docs
```

## What the Guide Does Cover

Use the guide-derived references for adjacent proof issues:

- `references/ghost-tracked.md`: `ghost`, `tracked`, `Tracked<T>`, and `Ghost<T>` variable modes.
- `references/ghost-tracked.md`: tracked ghost state for interior mutability patterns.
- `references/tokenized-state-machine.md`: guide-backed navigation for invariant-opening and state-machine-adjacent topics.
- `references/invariants.md`: loop invariants that relate executable state to ghost/spec state.

## Practical Rule

When a proof involves tokens, permissions, invariants, or state-machine resources:

1. First determine whether the issue is a general Verus mode/invariant issue covered by the guide.
2. If it is tokenized-state-machine-specific, read the local source definitions and examples before editing.
3. Avoid inventing token methods or sharding behavior from memory; use the concrete API present in the codebase.
