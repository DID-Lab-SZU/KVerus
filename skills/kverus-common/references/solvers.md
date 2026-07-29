# Specialized Solvers

Sources:
- `source/docs/guide/src/assert_by_compute.md`
- `source/docs/guide/src/bitvec.md`
- `source/docs/guide/src/nonlinear.md`

Use the narrowest solver that matches the fact.

Bitwise facts:

```rust
assert((x & y) == (y & x)) by (bit_vector);
```

Fully computable spec facts:

```rust
assert(pow(2, 8) == 256) by (compute_only);
```

Nonlinear integer arithmetic:

```rust
assert(x * y <= 100) by (nonlinear_arith)
    requires
        x <= 10,
        y <= 10,
        0 <= x,
        0 <= y;
```

Important: `bit_vector`, `compute_only`, and `nonlinear_arith` assertions are context-sensitive in different ways. When a specialized assertion does not inherit the needed fact, supply it explicitly through the assertion's `requires` or move the concrete expression inside the assertion.
