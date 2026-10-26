# The Elite Engineer: How to Use This Book

This is a training program in book form. It is built to produce **demonstrable capability**, meaning things you can build, explain, debug and defend without the book in front of you. It is not built to produce the feeling of having learned. Reading a lesson earns the status "Introduced" and nothing more.

No outcome is guaranteed: not a job, a promotion, a salary, or a role in quantitative finance. The book gives you structured practice, honest assessment and evidence of your own ability. What you do with the evidence is up to you and the market.

## 1. Who this is for

An existing developer (Python, FastAPI, PHP, Moodle, databases, testing) starting a new job and also aiming to master modern C++ and move toward quantitative development. The tone is demanding about quality and never insulting. If something here is unclear, that is a defect in the book; write it in your failure log and ask in a continuation session (see `CONTINUE-HERE.md`).

## 2. First steps (do these in order)

1. Read `STYLE-GUIDE.md` only if you plan to extend the book. Readers can skip it.
2. Take `DIAGNOSTIC.md` in two sittings, closed-book, no AI. Do not read `DIAGNOSTIC-ANSWER-KEY.md` until you have finished and written your self-score estimate.
3. Grade it (self-grade with the key, or ask a Claude session as described in `CONTINUE-HERE.md`). Use the routing table in the diagnostic to decide which lessons you can test out of and which need the full treatment.
4. Create a `progress/` folder outside the lesson folders and copy into it from `00-front/templates/`: `LEDGER.md`, a `failure-log.md` (from `FAILURE-LOG.md`), and a `reviews/` folder for weekly reviews. These are yours; do not commit them into the shared book folders.
5. Follow `ROADMAP.md`. Week 1 begins with Lesson 0.1, which is designed to be applied to your real job's repository on day one.

## 3. The learning cycle

Every lesson follows the same 12-section structure. The cycle you run on every lesson:

1. **Predict.** Before reading a worked example or running code, write down what you expect. Wrong predictions are the most valuable data you produce.
2. **Learn.** Sections 1-5 (problem, objectives, first principles, worked example, production perspective). Take notes in your own words; close the book to write them.
3. **Break.** Section 6 (failure laboratory). Predict first; then read the Reveal; then diagnose a fresh variant yourself.
4. **Retrieve.** Section 7. Answer cold, on paper or in a text file, before opening the solutions. Spacing is the point: repeat items from earlier lessons at roughly 1, 3, 7, 14 and 30 days. (Spaced retrieval is well supported in learning research; the exact intervals are a convention, not a law.)
5. **Build.** Sections 8 and 9. Independent implementation, then the project, from a blank file wherever the lesson says so.
6. **Review.** Section 10. Review your own work as if it were a stranger's pull request, then use the rubric.
7. **Gate.** Section 11. Pass is 80 of 100 with no critical failure. If you fail, do the named remedial exercise, not a reread.
8. **Account.** Section 12. Update the ledger, the failure log, and the weekly review. Retest at 14 days; status "Retained" requires it.

**Solutions policy.** Reference solutions live in `../solutions/` and are never inside lesson files. Consult them only after a serious attempt, defined as: you produced working code or a complete written answer, you ran it, and you can state what remains wrong or unsure. Looking early does not break anything, but it converts the exercise to "Introduced" in the ledger. Record it honestly.

## 4. Modes A, B and C

| Mode | Rules | Use |
|---|---|---|
| A: closed-book | No AI, no internet, no notes except your own previously written notes | Retrieval practice, reconstruction challenges, defenses, the diagnostic |
| B: docs-only | No AI for design or code. Official documentation, language references and man pages allowed. No searching for solutions to the exercise itself | Independent implementations and most projects |
| C: AI-assisted | AI allowed. You own correctness: you must verify APIs in official docs, run and break the code, and be able to explain every line. Fill in the AI audit scorecard for significant outputs | Boilerplate, exploration, reviewing your own work, comparison of alternatives, later stages of capstones |

Defaults: practice is A or B. Never require AI, never hide AI use. Mastery gates are always explainable without AI; Lesson 7.1 formalizes this and teaches better AI use as a skill rather than a crutch. A mode violation is recorded in the weekly review and the exercise is repeated in the correct mode.

## 5. Priority labels

| Label | Meaning | How to treat |
|---|---|---|
| P0 | Immediate, essential foundation | Do first; do not skip even if the diagnostic is strong, only compress through the gate |
| P1 | Core for independent professional competence | Do fully in order |
| P2 | Advanced specialization | Do after P0/P1 foundations are Demonstrated |
| P3 | Optional specialization | Do when relevant to your work or interest |

Each lesson states its priority with a one-line reason.

## 6. Folder map

All paths are relative to `/home/frank/Documents/engineering-book/`. Lesson filenames follow `<N.M>-<slug>.md`; the slug is chosen by the lesson author, so locate lessons with the glob shown. Solutions mirror lesson numbers: `solutions/<N.M>-<slug>-solutions.md`.

```
00-front/
  README.md  DIAGNOSTIC.md  DIAGNOSTIC-ANSWER-KEY.md  ROADMAP.md  CONTINUE-HERE.md  STYLE-GUIDE.md
  templates/  LEDGER.md  WEEKLY-REVIEW.md  FAILURE-LOG.md  PROJECT-SPEC-TEMPLATE.md  RUBRIC.md  AI-AUDIT-SCORECARD.md
01-vol0-job-readiness/
  0.1-day-one-protocol.md   Day-one protocol (setup, run, test, trace a request, repo dossier)             [P0]
  0.2-git-workflow.md   Git workflow (branches, diffs, rebase, PRs, bisect, reflog)                   [P0]
  0.3-debugging-and-failure-log.md   Debugging method and failure log                                              [P0]
  0.4-communication.md   Communication (standups, blockers, questions, PR descriptions)                [P0]
02-vol1-python/
  1.1-object-model.md   Object model, mutability, scope, closures
  1.2-iterators-generators-context-managers-exceptions.md   Iterators, generators, context managers, exceptions
  1.3-types-packaging-config-logging.md   Types, packaging, venv, pyproject, config, logging
  1.4-pytest-fixtures-mocking.md   pytest, fixtures, mocking, isolation
03-vol2-fastapi-backend/
  2.1-http-rest-contracts.md   HTTP, REST, JSON, status codes, contracts, OpenAPI
  2.2-fastapi-lifecycle-pydantic-di.md   FastAPI lifecycle, routing, Pydantic, dependency injection
  2.3-sql-schema-indexes-explain.md   SQL, schema design, joins, indexes, EXPLAIN
  2.4-transactions-migrations-pagination.md   Transactions, isolation, migrations, pagination
  2.5-authn-authz-passwords-secrets.md   AuthN/Z, passwords, JWT/OAuth basics, secrets
  2.6-async-background-jobs-idempotency.md   Async vs blocking, background jobs, retries, idempotency
  2.7-observability-deploy-reliability.md   Observability, deploy, health checks, timeouts (Capstone A prep)
04-vol3-php-moodle/
  3.1-modern-php.md   Modern PHP semantics, types, OOP, namespaces, Composer
  3.2-moodle-architecture-and-plugins.md   Moodle architecture, plugin types, directory layout
  3.3-capabilities-contexts-roles.md   Capabilities, contexts, roles, access control
  3.4-forms-output-database-api.md   Forms API, params, output API, strings, DB API
  3.5-events-tasks-webservices-files-privacy.md   Events, tasks, web services, caching, File API, privacy API
  3.6-testing-style-upgrades.md   PHPUnit, Behat, coding style, upgrades (Capstone B prep)
05-vol4-engineering/
  4.1-architecture-and-boundaries.md   Architecture: cohesion, boundaries, ports/adapters, ADRs
  4.2-testing-strategy-review-refactoring.md   Testing strategy, code review, refactoring legacy code
  4.3-security-and-reliability.md   Security and reliability
  4.4-performance-engineering-method.md   Performance engineering method
06-vol5-cpp/
  5.1-build-types-lifetime-const.md   Build, types, lifetime, references, const
  5.2-raii-copy-move-smart-pointers.md   RAII, copy/move, smart pointers, ownership
  5.3-stl-lambdas-templates-concepts.md   STL, iterators, lambdas, templates, concepts
  5.4-data-structures-and-algorithms.md   Data structures and algorithms with invariants
  5.5-sanitizers-ub-debugging-profiling.md   Sanitizers, UB, debugging, profiling
  5.6-cache-allocators-concurrency-memory-model.md   Cache locality, allocators, concurrency, memory model
07-vol6-quant/
  6.1-probability-and-distributions.md   Probability, distributions, expectation, Bayes
  6.2-linear-algebra-calculus-numerics.md   Linear algebra, calculus, numerical methods, floating point
  6.3-statistics-timeseries-montecarlo.md   Statistics, regression, time series, Monte Carlo
  6.4-markets-returns-options-risk.md   Markets, returns, options, Black-Scholes, risk
  6.5-backtesting-orderbook-marketdata.md   Backtesting, bias, costs, order book, market data
08-vol7-independence/
  7.1-ai-independence-and-audits.md   AI-independence program and audits (and better AI usage)
  7.2-design-docs-adrs-postmortems.md   Design docs, ADRs, post-mortems, technical defense
capstones/
  capstone-A-production-backend.md   capstone-B-moodle-plugin.md   capstone-C-cpp-component.md
  capstone-D-quant-research.md       capstone-E-cross-language.md
solutions/
  <N.M>-<slug>-solutions.md   one per lesson, consult only after a serious attempt
progress/   (yours; create it) LEDGER.md, failure-log.md, reviews/
```

Total: 38 lessons and 5 capstones.

## 7. Pacing

Assumptions, adjust to reality and record the adjustment in your weekly review: five work days (Monday to Friday) at 2-3 hours of study each, two free days (Saturday and Sunday) at 4-5 hours each. That is roughly 18-25 hours per week, about 21 on average. A lesson with its project is typically 8-14 hours including debugging; this is an estimate, not a promise. Your speed will differ and the diagnostic will change it.

**Work-day block (2-3 hours)**
- 10 minutes: cold retrieval of yesterday's items.
- 60-90 minutes: the day's lesson segment (learn, break, or build; one of those, not all three).
- 30-45 minutes: implementation or exercise in Mode A/B.
- 10 minutes: log the day (failure log, ledger).

**Free-day block (4-5 hours, with a real break in the middle)**
- 15 minutes: cold retrieval of the week's items.
- 90-120 minutes: the larger build (project or capstone milestone).
- 20-30 minute break away from the screen.
- 90 minutes: second build block, debugging or review.
- 30 minutes: weekly review (Sunday) or ledger/failure log tidy (Saturday).

**Protect sleep.** Aim for at least 7 hours of sleep every night. Set a fixed latest study end time on work days and honor it. If the weekly review shows more than two nights under 7 hours, cut the next week's plan; do not cut sleep. Sleep is part of how consolidation of what you study works, and depriving yourself degrades the debugging you will do tomorrow. The plan is designed to be shortened: when a week slips, the stated "cut first" items in `ROADMAP.md` go before anything else, and a slipped week is shifted, not crammed.

**Work comes first.** In your first weeks the job will teach you more than any lesson. If a work task and a lesson collide, do the work task, then log what it taught you and attach it to the ledger as evidence for the relevant lesson (status "Applied" is earned this way).

## 8. Honesty notes

- Versions: every lesson states minimum versions. Framework facts (Moodle, FastAPI, Pydantic, C++23) change; where a lesson says VERIFY, you check the official documentation yourself and write down what you found.
- Numbers: the book does not contain benchmark results as facts. It gives measurement methods and tells you to measure on your machine.
- Quant: nothing in this book implies any strategy is profitable. Capstone D forbids profitability claims.
- AI: lessons never require AI. If you use it, you own the result.
