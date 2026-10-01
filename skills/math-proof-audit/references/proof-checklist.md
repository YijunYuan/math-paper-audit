# Focused proof checklist

Read only the sections relevant to the proof. Record the actual reasoning, not a checklist of unsupported “pass” labels.

## Logic, objects, and estimates

- Quantifiers: distinguish `for every x there exists y` from a single `y` valid for every `x`; verify dependence of choices on parameters and independence of constants claimed uniform.
- Domains: track real/complex values, integer ranges, dimensions, regularity classes, and whether maps are defined at all points used. Check zero denominators, empty sets, and endpoint values.
- Existence: establish nonempty admissible sets, attainment versus infimum, solvability, and whether a selected object has all properties used later.
- Cases: test base cases and degenerate cases, exhaustiveness, overlap, induction step range, and whether recursive quantities decrease in a well-founded order.
- Implications: distinguish necessity from sufficiency, converse from contrapositive, pointwise from uniform, and existence from uniqueness or a canonical choice.
- Inequalities: track strictness, sign before division, monotonicity of applied functions, absolute values, constants, dimensions, and whether a bound closes under the stated smallness condition.
- Dependencies: identify the earliest unsupported assertion and all affected claims. A later lemma cannot justify an earlier one if its proof uses the earlier result.
- Constructions: verify independence of representatives, coordinates, approximations, or arbitrary choices; show consistency on overlaps before gluing.

## Analysis and functional analysis

- Limits: identify the exact topology and convergence mode; justify each exchange of limits, sums, derivatives, and integrals with usable domination, uniformity, or another applicable theorem.
- Compactness: distinguish boundedness, precompactness, compactness, sequential compactness, and weak compactness in the relevant space. A convergent subsequence need not prove convergence of the full sequence.
- Subsequences: verify diagonal constructions cover the asserted set of parameters; countable extraction alone does not establish an uncountable simultaneous conclusion.
- Function spaces: check norms versus seminorms, equivalence classes, completeness, dual spaces, embeddings and their exponent/dimension/end-point restrictions.
- Weak convergence: ensure tests lie in the correct dual space; products and nonlinear terms require additional justification. Identify lower semicontinuity and coercivity assumptions actually available.
- Density and extension: ensure approximants preserve required constraints; extension by continuity requires the relevant norm bound and target completeness.
- Operators: specify domain, range, closure, boundedness, adjoints, and invertibility; a formal inverse or formal adjoint need not define the claimed operator.
- Almost-everywhere statements: distinguish common exceptional sets from sets depending on a parameter; check representative choices and whether boundary or point evaluations are defined.

## Probability and stochastic analysis

- Measurability: check sigma-algebras, random elements, versions, conditional expectations, and measurable or predictable selections where needed.
- Independence: verify the exact independent objects; uncorrelatedness is insufficient in general. Conditioning can alter independence.
- Convergence: separate almost sure, in probability, in distribution, and `L^p`; verify uniform integrability or moment hypotheses when passing expectations through a limit.
- Stochastic processes: track filtration, adaptedness/predictability, integrability and localization, stopping-time conditions, and any optional-stopping hypotheses.
- Uniform events: for statements holding for all times or parameters on one event of probability one, justify the passage from countably many values using the available regularity.
- Distributional identities: distinguish equality in law from coupling/pathwise equality; verify any common probability-space construction.

## PDE, variational methods, and dynamics

- Formulation: specify classical, weak, mild, distributional, or viscosity solutions and verify transitions between formulations.
- Boundaries: check domain regularity, traces, compatibility conditions, initial data, integration by parts, and omitted boundary terms.
- Estimates: inspect coercivity/ellipticity, commutators, exponent ranges, Sobolev embeddings, and constants uniform in approximation or regularization parameters.
- Limits: justify nonlinear passage to the limit, identify possible loss of mass or concentration, and show the limit preserves constraints and boundary conditions.
- Existence and uniqueness: separate a priori estimates from actual construction; distinguish local from global time and uniqueness in the exact asserted class.
- Bootstrap: each improved regularity step must have applicable input hypotheses; check that the bootstrap terminates at the claimed level without assuming its conclusion.

## Geometry and topology

- Local-to-global: verify overlap compatibility, orientability, connectedness, completeness, and compactness where the proof uses them.
- Coordinates: check chart domains, differentiability and inverse hypotheses, tensor transformation rules, and coordinate independence of constructed quantities.
- Quotients: establish a well-defined quotient object and the claimed Hausdorff, smooth, or separation properties; stabilizers and freeness may matter.
- Homotopy and invariants: check base points, naturality, exactness hypotheses, degree/orientation conventions, and whether maps preserve the stated structures.
- Genericity: specify topology or measure and prove dense/open/residual/full-measure claims in that meaning; one notion does not imply the others.

## Algebra, combinatorics, and number theory

- Algebraic setting: record characteristic, commutativity, identity elements, finiteness, and assumptions such as algebraically closed or integral domain.
- Algebraic operations: cancellation, division, diagonalization, splitting, and tensor exactness each require hypotheses; check zero divisors and torsion cases.
- Quotients and maps: verify ideals/subobjects, well-definedness on representatives, kernel/image claims, and injectivity/surjectivity separately.
- Counting: check multiplicities, symmetry factors, disjointness, exhaustiveness, and whether the argument counts labeled or unlabeled objects.
- Induction/recurrences: verify starting indices, all boundary conditions, and that summation ranges match the claimed closed form.
- Arithmetic: verify congruence moduli, units/inverses, divisibility, exceptional primes, and whether an argument silently moves between integer, rational, and field settings.
