# Loop and Recursive Proof Invariants

Sources:
- `source/docs/guide/src/while.md`
- `source/docs/guide/src/invariants.md`
- `source/docs/guide/src/recursion.md`
- `source/docs/guide/src/recursion_loops.md`

## Core Rule

Verus verifies loops modularly. A loop does not automatically inherit all facts from the surrounding function. If the loop body or exit proof needs a function precondition, copy that fact into the loop invariant.

Pattern:

```rust
while i < n
    invariant
        0 <= i <= n,
        precondition_needed_inside_loop,
        accumulator == model(i),
{
    ...
}
```

## Build an Invariant Set

For most loops, add invariants in this order:

1. Index bounds, with the post-iteration endpoint included: `0 <= i <= n`.
2. Function preconditions needed inside the loop.
3. Relation between executable state and spec model.
4. Bounds needed to rule out overflow/underflow.
5. Frame facts for values not modified by the loop.
6. Quantified facts summarizing processed elements.

## Entry vs Preservation

If an invariant fails on entry, it is too strong for the initial state or needs initialization proof.

If it fails at the end of the body, preserve it by adding a local assertion after the update:

```rust
let old_model = model(i);
...
assert(model(i + 1) == update(old_model, x));
```

## Exit Reasoning

Make invariants strong enough that the negated loop condition gives the desired final index relation.

Example:

```rust
while i < n
    invariant
        i <= n,
{
    i = i + 1;
}
// Here Verus can combine i <= n with !(i < n) to prove i == n.
```

Do not write `i < n` as an invariant when the loop is supposed to finish with `i == n`.

## Accumulator Model

Tie each mutable accumulator to a spec expression over the processed prefix:

```rust
invariant
    sum == spec_sum(seq@.take(i as int)),
```

When preservation fails, expose sequence equalities:

```rust
let next = seq@.take((i + 1) as int);
assert(seq@.take(i as int) == next.drop_last());
assert(seq[i as int] == next.last());
```

## Overflow Bounds

Executable arithmetic needs bounds. Add loop invariants that bound each arithmetic operand, not only the final result.

Example shapes:

```rust
invariant
    fib(i as nat) <= u64::MAX,
    cur == fib(i as nat),
    prev == fib((i - 1) as nat),
```

If the bound relies on monotonicity, introduce a lemma and call it in a `proof { ... }` block before the arithmetic operation.

## Quantified Progress

For loops over arrays, slices, sequences, maps, or sets, summarize processed elements:

```rust
invariant
    forall|j: int| 0 <= j < i ==> P(#[trigger] seq@[j]),
```

Choose triggers that appear in later goals. If Verus does not instantiate the invariant, assert a trigger-shaped expression near the goal.

## Recursion and Decreases

Recursive proof/spec functions usually require `decreases` when the structural decrease is not obvious:

```rust
proof fn lemma(i: nat, j: nat)
    requires
        i <= j,
    decreases j - i
{
    if i < j {
        lemma(i, (j - 1) as nat);
    }
}
```

For induction, split base cases explicitly, then make recursive lemma calls that match the decreases measure.
