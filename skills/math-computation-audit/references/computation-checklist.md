# Focused computation checklist

Use only relevant sections. The objective is to justify what each result establishes, including accepted calculations, rather than to maximize the number of tool runs.

## Algebra, symbolic identities, and exact arithmetic

- Write domain assumptions explicitly before simplification: nonzero denominators, signs, reality/complexity, invertibility, characteristic, and integer constraints.
- Check square roots, logarithms, inverse trigonometric functions, powers, and branch cuts. Squaring, taking roots, or clearing denominators can introduce or remove solutions.
- Verify signs, transposes versus conjugate transposes, matrix order, summation indices, multiplicities, and normalization conventions.
- Compare expanded and factored forms when useful; a simplifier returning zero is conditional on its assumptions and the semantics of the represented expression.
- Handle exceptional parameter values separately. A generic symbolic formula may miss repeated roots, singular matrices, vanishing coefficients, or endpoint cases.
- Exact integer or rational arithmetic certifies the executed arithmetic only. Check that the encoded expression and input values are the intended mathematics.

## Calculus, estimates, and asymptotics

- Independently differentiate or integrate nontrivial displayed formulas, retaining boundary terms, integration constants, and domain restrictions.
- Check changes of variables, Jacobians, orientation, integration domains, and whether the substitution is valid across singularities or branches.
- Confirm series coefficients, initial terms, recurrence indices, and the radius or domain of convergence when used.
- For inequalities, inspect sign changes, monotonicity, endpoint extrema, equality cases, and dependencies of all constants.
- For big-O, little-o, and asymptotic equivalence, state the limiting variable, direction of approach, parameter dependence, and uniformity actually justified.
- Bound remainders in the regime where they are used; an expansion valid for fixed parameters may fail in a joint limit.
- For truncations, verify tail bounds and how truncation error propagates to the final claim.

## Numerical and certified calculations

- Identify discretization, truncation, rounding, conditioning, iteration, and data errors separately; increasing floating-point precision addresses only some of them.
- Test sensitivity to precision, mesh/time step, tolerances, initialization, and evaluation order when instability could affect the conclusion.
- Residual smallness is not automatically solution accuracy; justify conditioning or an a posteriori bound. Solver termination is not an existence or uniqueness theorem.
- An interval enclosure must use validated outward rounding or another justified enclosure method. Printing rounded endpoints does not make an interval rigorous.
- For a certificate, check the reduction, admissible domain coverage, boundary treatment, and the checker or mathematical argument validating it.
- Treat cancellation, overflow, underflow, NaNs, infinities, and failed iterations explicitly. Do not silently drop failed points from the reported sample.
- A plot's resolution and scale can conceal exceptions; use underlying values and error bounds to assess a claimed inequality or zero.

## Enumeration, algorithms, and combinatorics

- Specify the finite search space, why it covers the claim, parameter bounds, equivalence reductions, and admissibility tests.
- Show that symmetry reductions preserve at least one representative of every relevant case and apply correct multiplicities when counting.
- Check base cases, boundary indices, inclusive/exclusive endpoints, and duplicates or missing cases in generation.
- Justify pruning rules mathematically. A heuristic search without a coverage argument is not exhaustive.
- Record termination and actual coverage; a timed-out search proves nothing about unchecked cases.
- Distinguish a verified finite instance, a verified algorithm on those inputs, and a general correctness or complexity theorem.

## Simulation, tables, and empirical claims

- Identify data provenance, transformations, exclusions, missing values, units, and the exact population or sampling model.
- Record seeds and randomization method, sample size, dependence between samples, uncertainty estimates, and relevant stopping rules.
- Check whether repeated searching, parameter selection, or multiple comparisons affect an asserted empirical confidence level.
- Reproduce table entries and plotted quantities from stated definitions when the data are available. Missing data or inaccessible code stays visible as incomplete evidence.
- Distinguish empirical tendencies from deterministic or almost-sure conclusions. A simulation cannot certify that an event has probability zero.

## Minimal reproducibility record

For an executed check, retain the source claim, assumptions, exact input or input hash, calculation/script, tools and relevant versions, execution settings, observed output, and its interpretation. Preserve enough detail to rerun the meaningful check without preserving unrelated environment data or secrets.
