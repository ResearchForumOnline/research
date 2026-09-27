# Reset Compatibility in Zero Boundary Algebra
## Six-Element Transformation Monoids and Conservative Validator Synthesis

**Shafaet Brady Hussain — Independent researcher**  
**27 September 2026 · Working paper 0.1 · Not externally peer reviewed**

[Full manuscript with proofs (LaTeX)](zba-reset-compatibility-0.1.tex) · [Reproducibility package](../artifacts/zba-reset-compatibility-0.1/README.md)

## Abstract

A reset whose destination depends on validation need not commute with a symmetry, even when both destinations are fixed by that symmetry. We study this issue in the reset–mirror fragment of Zero Boundary Algebra (ZBA) 1.1. For a nonidentity involution on a finite set with two fixed anchors and an arbitrary Boolean validator, the generated transformation monoid has at most six elements. Its size is exactly 3, 4, 5, or 6. We classify each case, count the validators in each class, and derive the greatest conservative anchored invariant repair when one exists. The repair applies classical Pawlak lower approximation; an exact deletion formula quantifies its cost. Algorithmically independent checks cover 496 small validator cases and 248 feasible repair inputs. Complete proofs appear in the linked manuscript.

## Contract and compatibility theorem

Let X be a finite labelled set of N ≥ 4 states. Let M be a nonidentity involution fixing two distinct anchors a₀ and a₁ individually. For a Boolean validator v, define R(x) = aᵥ₍ₓ₎ and g(i) = v(aᵢ). Composition is right to left.

- MR = R always.
- RM = MR exactly when v(Mx) = v(x) for every state.
- R² = R exactly when g(v(x)) = v(x) for every state; equivalently, g is the identity or v is constant.
- Every generated transformation belongs to {identity, M, R, RM, R², R²M}.

The ZBA application fixes all retained coordinates and studies a structural fibre, not the full state with appended audit history.

## Complete classification

| Anchor map g | Validator condition | Monoid size |
| --- | --- | ---: |
| Identity | Mirror invariant | 3 |
| Identity | Not mirror invariant | 4 |
| Bit swap | Mirror invariant | 4 |
| Bit swap | Not mirror invariant | 6 |
| Constant b | v is constant b | 3 |
| Constant b | Nonconstant and mirror invariant | 4 |
| Constant b | Not mirror invariant | 5 |

If M has K orbits, put H = 2^(N−2) and J = 2^(K−2). The counts across all validators are C₃ = J+2, C₄ = H+2J−2, C₅ = 2(H−J), and C₆ = H−J. These count validators on a fixed labelled structure, not monoid isomorphism classes.

## Refinement to ZBA 1.1

The general commutation argument in [ZBA 1.1](zero-boundary-algebra-formal-specification-1.1.md) needs validator invariance as an explicit hypothesis. Its concrete evidence-only reference implementation already satisfies it.

For a counterexample, consider four states a₀, a₁, u, t with mirror swapping u and t. Accept a₁ and u only. Reset is idempotent, but RM(u) = a₀ whereas MR(u) = a₁. Idempotence does not imply commutation.

## Greatest conservative repair

Seek w ≤ v with w(Mx) = w(x), w(a₀) = 0, and w(a₁) = 1. A solution exists exactly when v(a₁) = 1. Its unique greatest member sets w(a₀) = 0 and, elsewhere, w(x) = v(x) AND v(Mx).

The exact number of removed acceptances is:

**v(a₀) + half the number of states where v(x) differs from v(Mx).**

This construction applies [Pawlak's lower approximation](https://doi.org/10.1007/BF01001956), with anchor constraints. It is not claimed as a newly invented approximation operator. Do not apply it to policies that intentionally distinguish mirror-related states.

## Reproducible evidence

| Check | Result |
| --- | ---: |
| All validators for five specified involutions on 4–8 states | 496 passed |
| Feasible repair inputs checked against enumerated alternatives | 248 passed |
| Explicit 36-state examples of all four monoid sizes | Passed |

For the 36-state ZBA fibre, K = 24. The theorem gives 4,194,306 size-three validators; 17,188,257,790 size-four; 34,351,349,760 size-five; and 17,175,674,880 size-six. These sum to 2³⁶. This distribution is **formula-derived**, not an exhaustive execution of 68 billion cases.

The pinned GitHub and Hugging Face specification and reference-code snapshots match byte for byte. Their URLs and hashes are preserved in the artifact manifest.

## Status and attribution

This is a specification refinement and executable algebraic audit. Global priority, new physical laws, and cryptographic security are not established. AI assistance was used for drafting, derivation, source comparison, critique, and verification-code preparation; the manuscript retains this disclosure and author-review status.

The complete manuscript is supplied as editable LaTeX. PDF compilation was unavailable in the authoring environment, so this release includes no compiled PDF and makes no visual-layout verification claim.

## References

1. S. B. Hussain. *Zero Boundary Algebra: Formal Specification 1.1* (2026). [GitHub](zero-boundary-algebra-formal-specification-1.1.md); [Hugging Face](https://huggingface.co/datasets/researchforumonline/zero-boundary-algebra).
2. Z. Pawlak. Rough sets. *International Journal of Computer & Information Sciences* 11, 341–356 (1982). https://doi.org/10.1007/BF01001956
3. Y. Y. Yao. Constructive and algebraic methods of the theory of rough sets. *Information Sciences* 109, 21–47 (1998). [Author manuscript](https://www2.cs.uregina.ca/~yyao/PAPERS/is_constructive.pdf).
4. M. V. Volkov. Synchronization of finite automata. *Russian Mathematical Surveys* 77, 819–891 (2022). https://doi.org/10.4213/rm10005e
