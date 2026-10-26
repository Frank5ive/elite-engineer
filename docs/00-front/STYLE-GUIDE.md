# Style Guide and Contract for Every Lesson (read fully before writing)

Book: **The Elite Engineer**. Reader: Frank, an existing developer starting a job next Monday
(Python, FastAPI, PHP, Moodle, databases, testing) who also wants to master modern C++ and become a
quantitative developer. Reader's goal: demonstrable capability, not consumption. Be demanding about the
quality of his work, never insulting. No filler, no motivational speeches, no repeated summaries.

## File rules
- One lesson = one Markdown file: `<folder>/<NN.M>-<slug>.md` (e.g. `02-vol1-python/1.1-object-model.md`).
- Reference solutions go in `/home/frank/Documents/engineering-book/solutions/<NN.M>-<slug>-solutions.md`,
  NEVER inside the lesson file. The lesson file must say "Attempt first. Solutions: ../solutions/...".

- Start each lesson with YAML-ish header lines:
  `# Lesson X.Y: Title`, then a metadata table: Priority (P0-P3 + one-line reason), Mode (A/B/C per exercise),
  Time budget, Prerequisites, Minimum versions (e.g. Python 3.12, PHP 8.2, C++20), Deliverable.

- Code must be correct and runnable as written. Mark the minimum language/framework version. Do not invent APIs,
  flags, compiler behavior, benchmark numbers or documentation references. If unsure, write
  `VERIFY: <how to check>` instead of asserting. Never fabricate benchmark results: give the method and say
  to measure.

- Version-sensitive facts (Moodle APIs, FastAPI/Pydantic v2 behavior, C++23 features) must be labelled with the version
  and, when tools allow, checked against official docs (docs.python.org, fastapi.tiangolo.com, php.net, moodledev.io,
  en.cppreference.com). Distinguish language guarantees / framework behavior / implementation detail / convention / opinion.

- Python examples use Python 3.12+, type hints, Pydantic v2, SQLAlchemy 2.x style, pytest. PHP 8.2+. C++20 (flag C++23 explicitly).
- Math: use plain text / simple LaTeX-free notation (e.g. `E[X] = sum x_i p_i`) so it renders anywhere.
- Diagrams: ASCII or Mermaid code blocks (```mermaid```). Use them when they materially help (request flows, memory layouts,
  ownership, state machines, DB schemas).

- Length: 3,000-5,000 words per lesson including code. Dense, specific, no padding.
- Assume reader knows basic programming. Do not explain what a variable is. Do explain internals of the specific language.

## Required lesson structure (all 12 sections, in this order, these exact headings)
1. `## 1. Engineering problem` - a realistic scenario, why it matters, what goes wrong when handled poorly.
2. `## 2. Learning objectives` - 4-7 MEASURABLE objectives ("Implement X that handles Y and write tests for Z"), never "understand X".
3. `## 3. First-principles explanation` - what / why / problem solved / how it works internally / when to use / when to avoid /
   alternatives / trade-offs / how it fails. Diagrams, traces, memory layouts where useful.

4. `## 4. Worked example` - built step by step with reasoning for each design choice. Include a naive version vs improved
   version where useful and say exactly what changed and why.

5. `## 5. Production perspective` - only the relevant dimensions: maintainability, correctness, performance, security, failure
   handling, testing, observability, operations. Include "what a senior engineer does differently" and common beginner mistakes
   with how to recognize and diagnose them.

6. `## 6. Failure laboratory` - a deliberately flawed implementation/test/assumption. Ask the reader to PREDICT the failure
   first. Put the explanation under a clearly marked `### Reveal (read after predicting)` heading, with a systematic diagnosis procedure.

7. `## 7. Retrieval practice` - 8-12 questions: explain, code-reading, output prediction, short reasoning. Answers NOT here
   (they go in the solutions file).

8. `## 8. Independent implementation challenge` - specify behavior and constraints, do NOT give the implementation. Tag Mode A/B.
9. `## 9. Project` - a meaningful deliverable. Must include ALL 14 fields as a table or labelled list:
   Problem statement; Context; Requirements; Constraints; Acceptance criteria; Edge cases; Quality requirements;
   Deliverables; Difficulty (Foundation/Intermediate/Advanced/Expert); Estimated effort (range incl. debugging);
   Progressive hints (3+ levels, least revealing first); Evaluation rubric (100 points); Extension challenge; Reflection questions.
   Deliverable types vary by lesson: program, library, DB design, endpoint, plugin, test suite, debugging report, code review,
   performance investigation, threat model, design doc, benchmark report, derivation, simulation, postmortem. At least some
   lessons start from a blank repository. Sometimes add a constraint: no external libs, no AI, time budget, failing test suite,
   perf target, incomplete spec, mid-way requirement change.

10. `## 10. Engineering review` - self-review checklist (correctness, readability, tests, edge cases, security, etc.) and
    "explain your design decisions" prompts.
11. `## 11. Mastery gate` - explicit pass criteria. Pass = 80/100 with no critical failure (name the critical failures for this lesson).
    State the required evidence. If failed: describe the focused remedial exercise (never "reread the chapter").
12. `## 12. Reflection and accountability` - short template: what I learned; what I initially misunderstood; what took the most
    effort; bugs and how I diagnosed them; what I'd change; what remains unclear. Plus "Ledger update: status -> ..." and
    a "Failure log entry" prompt.
After section 12 add `## References` (3-6 high-quality official/primary links, each with one line saying what to read it for) and
`## Further depth (optional)` for P2/P3 deep dives.

## Pedagogy rules
- Every important concept answers: what, why, problem solved, internals, when to use, when to avoid, alternatives, trade-offs, failure,
  how to test understanding, how it appears in production, beginner mistakes + diagnosis, senior approach.

- Teach the simplest design that meets requirements. Call out unnecessary complexity as well as insufficient engineering.
- Never encourage redesigning an existing codebase or adding dependencies/patterns without understanding team standards.
- Mark exercises Mode A (closed-book, no AI), Mode B (docs-only, no AI design/code) or Mode C (AI-assisted, learner owns correctness).
  Default to A/B for practice. Do not require AI.

- Defensive security only; no offensive exercises against real systems.
- Mastery is shown by reproducing, adapting, explaining and defending without the lesson. Reading = "Introduced" at most.
- Maintain continuity: refer back to earlier lessons by number instead of re-explaining. Forward-refer sparingly.
- Moodle/PHP, FastAPI/Python, C++ and quant tracks are distinct; do not blur them.
- Quant: never imply a toy strategy is profitable. Separate mathematical correctness from implementation correctness.
- Solutions file: for each exercise give the reference approach, trade-offs, and at least one plausible alternative; answers to every
  retrieval question; reveal rubric scoring notes.

- Honest uncertainty beats confident error.

## Priority labels
P0 immediate / essential foundation; P1 core for independent professional competence; P2 advanced specialization;
P3 optional specialization. Explain each assigned priority in one line.

## Curriculum map (lesson numbers and folders are fixed)
Vol 0 `01-vol0-job-readiness`: 0.1 day-one protocol (setup, run, test, trace a request, repo dossier); 0.2 Git workflow (branches,
 diffs, rebase, PRs, bisect, reflog); 0.3 debugging method + failure log; 0.4 communication (standups, blocker messages, questions, PR descriptions).
Vol 1 `02-vol1-python`: 1.1 object model/mutability/scope/closures; 1.2 iterators, generators, context managers, exceptions;
 1.3 types, packaging, venv, pyproject, config, logging; 1.4 pytest, fixtures, mocking, isolation.
Vol 2 `03-vol2-fastapi-backend`: 2.1 HTTP/REST/JSON/status codes/contracts/OpenAPI; 2.2 FastAPI lifecycle, routing, Pydantic, DI;
 2.3 SQL, schema design, joins, indexes, EXPLAIN; 2.4 transactions, isolation, migrations, pagination; 2.5 AuthN/Z, passwords,
 JWT/OAuth basics, secrets; 2.6 async vs blocking, background jobs, retries, idempotency; 2.7 observability, deploy, health checks, timeouts (Capstone A prep).
Vol 3 `04-vol3-php-moodle`: 3.1 modern PHP semantics/types/OOP/namespaces/Composer; 3.2 Moodle architecture, plugin types, directory layout;
 3.3 capabilities, contexts, roles, access control; 3.4 Forms API, params, output API, strings, DB API; 3.5 events, tasks, web services,
 caching, File API, privacy API; 3.6 PHPUnit, Behat, coding style, upgrades (Capstone B prep).
Vol 4 `05-vol4-engineering`: 4.1 architecture (cohesion, boundaries, ports/adapters, ADRs); 4.2 testing strategy, code review, refactoring legacy;
 4.3 security and reliability; 4.4 performance engineering method.
Vol 5 `06-vol5-cpp`: 5.1 build, types, lifetime, references, const; 5.2 RAII, copy/move, smart pointers, ownership; 5.3 STL, iterators,
 lambdas, templates, concepts; 5.4 data structures and algorithms with invariants; 5.5 sanitizers, UB, debugging, profiling;
 5.6 cache locality, allocators, concurrency, memory model.
Vol 6 `07-vol6-quant`: 6.1 probability, distributions, expectation, Bayes; 6.2 linear algebra, calculus, numerical methods, floating point;
 6.3 statistics, regression, time series, Monte Carlo; 6.4 markets, returns, options, Black-Scholes, risk; 6.5 backtesting, bias, costs, order book, market data.
Vol 7 `08-vol7-independence`: 7.1 AI-independence program and audits (+ better AI usage); 7.2 design docs, ADRs, post-mortems, technical defense.
Capstones `capstones/`: A production backend service; B Moodle plugin; C high-performance C++ component; D quantitative research system;
 E cross-language integration. Each: realistic specification, architecture/interface requirements, milestones, acceptance criteria, testing,
 security/reliability expectations, performance criteria, documentation requirements, final technical defense, no-AI reconstruction challenge.
