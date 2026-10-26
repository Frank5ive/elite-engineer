# Failure Log

A failure log turns mistakes into reusable knowledge. Record every defect that cost you more than 15 minutes, every wrong prediction in a failure laboratory, and every review comment that identified a real bug in your work. Blame no one, including yourself; record mechanisms.

Keep one entry per failure in `failure-log.md` in your working repository, newest first. Review the whole log weekly and look for repeated root causes: repetition is the signal that deserves a lesson-sized remedial exercise.

## Entry template (9 fields)

```
### FL-NNN: <short title>
1. Date and context: <date, lesson/project, language/framework and versions>
2. Symptom: <what was observed, exact error text or wrong output>
3. Expected behavior and my prediction/assumption: <what I believed would happen and why>
4. Root cause: <the actual mechanism, stated at the lowest level you could verify>
5. How it was diagnosed: <steps, tools, hypotheses tried including wrong ones, time spent>
6. Fix: <what changed, link to commit or diff>
7. Regression guard: <test, assertion, lint rule, or checklist item that now prevents recurrence; link>
8. Category and prevention: <knowledge gap | method gap | carelessness | tooling | spec ambiguity>; <what I do differently>
9. Retest: <date to re-attempt a similar problem cold, and result when done>
```

## Worked example 1

### FL-001: Mutable default argument shared across calls
1. Date and context: 2026-11-03, Lesson 1.1 exercise, Python 3.12.
2. Symptom: `add_tag("a")` followed by `add_tag("b")` returned `["a", "b"]` for the second call, although each call used no explicit list. A test passed alone and failed when run after another test.
3. Expected behavior and my prediction/assumption: each call without `tags` gets a fresh empty list. I assumed default values are evaluated on each call, as in a few other languages I use.
4. Root cause: default values in a Python function signature are evaluated once, when the `def` statement executes, and stored on the function object (`add_tag.__defaults__`). The same list object is mutated on every call that uses the default.
5. How it was diagnosed: printed `id(tags)` on each call and saw the same value; inspected `add_tag.__defaults__` and saw the accumulated list. First wrong hypothesis (30 minutes): test-order dependence caused by a fixture; ruled out by running the single test twice in one process. Total time: 50 minutes.
6. Fix: signature `tags: list[str] | None = None`, then `if tags is None: tags = []`. Commit abc1234 (placeholder for your commit).
7. Regression guard: unit test calling the function twice and asserting independent results; enabled the linter rule for mutable defaults (VERIFY rule name in your linter, for example flake8-bugbear B006 or the Ruff equivalent).
8. Category and prevention: knowledge gap (evaluation time of defaults). Prevention: treat any mutable literal in a signature as a review blocker; check `__defaults__` when state leaks between calls.
9. Retest: 2026-11-17, rewrite a similar function cold. Result: (fill in).

## Worked example 2

### FL-002: Authorization check missing on one export endpoint
1. Date and context: 2026-12-02, Capstone A milestone M3, FastAPI, SQLAlchemy 2.x, PostgreSQL.
2. Symptom: the authorization matrix test passed for every route in the table except `GET /v1/courses/{id}/export`, which returned 200 for an instructor who does not own the course. The route had not been added to the matrix table, so the test never exercised it.
3. Expected behavior and my prediction/assumption: every course-scoped route denies non-owners. I assumed the shared dependency on the router applied the ownership check to every route under it.
4. Root cause: the ownership check was implemented in the individual route handlers, not in the dependency. The new export handler copied the listing handler's query but not its check. The matrix test was hand-maintained, so incompleteness was invisible.
5. How it was diagnosed: during a manual review pass I listed all routes from the OpenAPI document and compared against the matrix table: one missing. Reproduced with two users. Time: 40 minutes, discovered by review rather than by a failing test.
6. Fix: moved the ownership check into the service-layer use case (used by every course-scoped operation) and made the export handler call it. Commit def5678 (placeholder).
7. Regression guard: the authorization matrix test now iterates over all routes discovered from the application's route table and fails if any route is absent from the matrix or lacks an explicit expectation for each role.
8. Category and prevention: method gap (test completeness relied on human maintenance) and design gap (check at the wrong layer). Prevention: enforce at the lowest shared layer and make the test enumerate routes automatically.
9. Retest: 2026-12-16, add a new nested resource to a toy API and show the matrix test catches a missing check without being edited.
