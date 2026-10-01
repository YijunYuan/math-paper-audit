# Targeted stress-test families

Choose families from the actual mathematical content. For each attempted refutation, retain the complete assumptions and show exactly which conclusion fails.

## Logical targets

- Universal conclusion: seek one admissible violating instance.
- Existence: show an admissible instance for which every candidate fails, not just failure of one attempted construction.
- Uniqueness: exhibit two distinct admissible solutions under the stated equivalence relation.
- Uniform estimate: construct a family with the claimed constant-independent quantity unbounded; track which parameters the constant may depend on.
- Convergence: use a nonconvergent admissible sequence, a wrong limit, or a subsequence with incompatible behavior in the stated topology.
- Equivalence: test both directions separately. A necessary condition need not be sufficient.
- Almost sure or generic assertion: a special exceptional point may not refute it; the violating set must have the relevant positive probability, measure, category, or other size.
- Optimality: an example outside the theorem's hypotheses may show why an assumption is needed, but cannot refute the theorem as written.

## First checks for most claims

- Zero, identity, constant, empty, singleton, rank-zero, or smallest allowed dimension; use only admissible cases.
- Endpoint and equality cases in exponents, inequalities, dimensions, and parameter constraints.
- Sign reversal, rescaling, translation, symmetry transformations, and dimension or unit consistency.
- Disconnected or noncompact instances when connectedness or compactness is absent.
- Repeated eigenvalues, noninvertible maps, nonunique minimizers, and objects with symmetries when a proof assumes generic behavior.
- Limits of otherwise admissible instances; verify whether the limiting object remains in the hypothesis class.
- A claim that is vacuous because its hypotheses are inconsistent is not false. Explain the mathematical or expositional consequence separately.

## Analysis and PDE

- Concentrating bumps or spikes: test uniform integrability, compactness, pointwise bounds, and mass loss.
- Translated fixed profiles: test compactness on noncompact domains and escape to infinity.
- Rapid oscillations: test weak versus strong convergence and nonlinear passage to the limit.
- Slowly decaying tails or borderline singularities: calculate membership in every required function space and the endpoint integral explicitly.
- Boundary layers and nonsmooth domains: verify the stipulated boundary regularity and trace assumptions before using them as tests.
- Explicit equilibria, traveling waves, finite-dimensional reductions, or separable solutions: check the full equation and initial/boundary conditions.
- Scale-invariant or high-frequency families: track constants and normalization, including any smallness restriction that rules a candidate out.

## Probability

- Atomic or two-point distributions: test inequalities, conditional statements, and distinctions between moments.
- Heavy tails: calculate required moments rather than assuming they exist; test expectation-limit exchanges.
- Dependent variables with zero covariance: test any step replacing uncorrelatedness by independence.
- Rare events with increasing magnitudes: test convergence in probability against expectation or `L^p` conclusions.
- Parameter-dependent null sets: test whether the claim requires one simultaneous event of probability one.
- Stopping times or filtrations: an inadmissible stopping rule does not refute a theorem restricted to stopping times with additional bounds.

## Geometry, topology, algebra, and discrete mathematics

- Simple circles, tori, spheres, disconnected spaces, and nontrivial coverings: test local-to-global, orientability, and topology-sensitive claims within the allowed category.
- Quotients with stabilizers or poor separation: test claims whose hypotheses do not already rule out those pathologies.
- Small matrices: use singular, defective, noncommuting, and repeated-eigenvalue examples when admissible.
- Rings with zero divisors, positive characteristic fields, torsion modules, or nonreduced objects: check the declared algebraic setting first.
- Small graphs, finite groups, short recurrences, low-degree polynomials, or smallest prime cases: use exact enumeration only over a fully specified finite set.
- Counting examples: distinguish multiplicity, labels, symmetries, and boundary indices to isolate off-by-one or overcounting mechanisms.

## Record evidence without overstating it

- State the construction, all parameters and ranges, verification of each hypothesis, and the explicit contradiction.
- For a computed candidate, preserve exact values or a justified error enclosure. Rounding error or nonconvergence of a solver alone is not mathematical failure.
- For no-refutation results, name the tested family and bounds. Do not describe a finite search as exhaustive over an infinite class.
- If a proposed correction survives these tests, call it a candidate correction until a proof and all affected uses are checked.
