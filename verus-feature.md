This file contains a bunch of Verus features discussed in the Github repo but not covered in official tutorial. 

- [Mutable reference](https://github.com/verus-lang/verus/blob/main/source/docs/new-mut-ref.md)
- [Proof closures](https://github.com/verus-lang/verus/pull/1524)
- [Different styles of specifying std traits like Clone, Hash, and PartialEq ](https://github.com/verus-lang/verus/discussions/1527)
- [Default_ensures](https://github.com/verus-lang/verus/pull/1548) and [its syntax](https://github.com/verus-lang/verus/blob/cc0012df1ba31add6deac633b52841959fbf1b10/examplesyntax.rs#L553-L603)
- [Attribute-based syntax for exec function specifications](https://verus-lang.github.io/verus/guide/exec_attr.html)
- [Attribute-based syntax for struct constructors](https://github.com/verus-lang/verus/pull/2298/files#diff-b06cc41b4d6eb0c3a2398c1671dd66267680e0c6e5f908ff77a03252db5e913d)
- [External_trait_extension](https://verus-lang.github.io/verus/guide/external_trait_specifications.html)
- [constrain_type](https://github.com/verus-lang/verus/pull/1799)
- Dual mode function is a feature for simple functions that one can get both the specification and executable code by writing the function only once, a high level discussion can be found [here](https://github.com/verus-lang/verus/discussions/1429).
  - Direction exec to spec: [`dual_spec`](https://verus-lang.github.io/verus/guide/exec_to_spec.html)
  - Direction exec to spec: [`auto_spec`](https://github.com/verus-lang/verus/pull/1813) and [examples](https://github.com/verus-lang/verus/pull/1813/files#diff-22a06477ea027bbffe784a0d3532ece777fd8c0cc2fe1197c0f1ad6d3a498c6a)
  - Direction spec to exec: [`exec_spec_verified!/exec_spec_unverified!`](https://verus-lang.github.io/verus/guide/exec_spec.html), [examples for verified](https://github.com/verus-lang/verus/blob/main/source/rust_verify_test/tests/exec_spec_verified.rs) and [examples for unverified](https://github.com/verus-lang/verus/blob/main/source/rust_verify_test/tests/exec_spec_unverified.rs).