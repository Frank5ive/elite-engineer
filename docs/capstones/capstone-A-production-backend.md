# Capstone A: Production Backend Service

| Field | Value |
|---|---|
| Priority | P0/P1: the core professional artifact for a FastAPI/Python developer. |
| Mode | Build: A/B for core logic, C permitted for boilerplate (declare it). Defense and reconstruction: A. |
| Time budget | 40-70 hours over 3-5 weeks, including debugging and documentation. |
| Prerequisites (lessons) | 0.1, 0.2, 0.3, 0.4, 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 4.1, 4.2, 4.3. Helpful: 4.4, 7.2. |
| Minimum versions | Python 3.12, FastAPI (current stable; VERIFY: `pip index versions fastapi`), Pydantic v2, SQLAlchemy 2.x, Alembic, PostgreSQL 15+ (VERIFY the version you deploy), pytest. |
| Deliverable | A repository, a running containerized service, a design doc with ADRs, a runbook, and a recorded or live technical defense. |

Attempt first. Reference notes for this capstone live in `../solutions/` only after you have submitted your own work and defended it. There is no full reference implementation by design; there is a reference decomposition and a list of common defects.

## 1. The specification: a Course Enrollment and Grading Events Service

You are building the backend for a small training organization. It tracks **learners**, **courses**, **enrollments**, and **assessment results**, and it receives results from external systems (for example, a Moodle site, which Capstone B or your day job may produce) via an authenticated API and a webhook-style ingest endpoint. The domain is deliberately close to the work you will do, but you may substitute another domain of equal complexity if you write the substitute specification first and it is approved by you against this document's criteria (a self-review is acceptable if no reviewer exists; record that fact).

### 1.1 Functional requirements

1. CRUD for learners and courses with validation, soft-delete for learners, and uniqueness constraints expressed in the database, not only in code.
2. Enrollment lifecycle: `pending -> active -> completed | withdrawn`. Illegal transitions return a defined error. The state machine must be a single, tested piece of code.
3. Assessment result ingest: `POST /v1/results` accepts a batch (up to a documented maximum) of results. It must be **idempotent**: a retried request with the same `Idempotency-Key` and identical payload returns the original outcome; the same key with a different payload returns a conflict (see 2.6).
4. Read endpoints with **keyset (cursor) pagination** for listings that can exceed a few thousand rows, plus filtering by course, status, and date range.
5. A reporting endpoint returning per-course completion counts and mean score, computed in SQL, with a documented consistency guarantee (what a reader may see while ingest is running).
6. Asynchronous work: when a learner completes a course, a background job produces a completion record and calls an outbound HTTP notifier. The notifier is unreliable by assumption.
7. Authentication and authorization: users with roles `admin`, `instructor`, `service`. Instructors may only read/write data for their own courses. A `service` credential may only call the ingest endpoint.

### 1.2 Non-functional requirements

- Every endpoint documented via OpenAPI with accurate response models, error models, and examples. The OpenAPI document is generated, committed, and diff-checked in CI (2.1).
- Errors use one consistent envelope with a stable machine-readable code, a human message, and a correlation id.
- Configuration through environment variables validated at startup; the service refuses to start with missing secrets (1.3).
- The service runs under a process manager or container with health (liveness) and readiness endpoints that mean different things (2.7).

### 1.3 Explicit scope exclusions

No frontend. No multi-region. No message broker required; if you introduce one you must justify it in an ADR against the simpler option of a database-backed job table. Do not add a dependency you cannot defend.

## 2. Architecture and interface requirements

- **Layering (4.1):** HTTP layer (routers, schemas) -> application/service layer (use cases, state machine, transaction boundaries) -> persistence (repositories or query modules). Domain rules must not import FastAPI. External systems (notifier, clock, ID generation) sit behind small interfaces you can fake in tests.
- **Database (2.3, 2.4):** Normalized schema with foreign keys, check constraints for enum-like columns, and indexes justified by named queries. Include at least one `EXPLAIN (ANALYZE)` investigation in the design doc: a query you expected to use an index, the plan you observed, and what you changed. Migrations are Alembic, forward-only in production, and each migration must be safe to run against a populated table (describe the lock behavior of any `ALTER TABLE` you write; VERIFY against PostgreSQL documentation for your version).
- **Transactions (2.4):** One use case, one transaction, unless you document otherwise. State the isolation level you rely on and the anomaly you are protecting against for each of: enrollment transitions, idempotency-key insertion, and the report query.
- **Idempotency (2.6):** Database-backed key store with a unique constraint on (principal, key), a stored request fingerprint, a stored response (or reference), and a defined behavior for a concurrent duplicate that arrives while the first is in flight.
- **Async and blocking (2.6):** Never block the event loop. If you use `async def` endpoints with an async driver, say so and test it. If you use sync endpoints and a sync driver, say so; this is a legitimate choice if justified. Mixing them accidentally is a defect.
- **Background jobs (2.6):** Jobs persist in the database, survive process restart, are claimed with a concurrency-safe pattern (VERIFY `SELECT ... FOR UPDATE SKIP LOCKED` semantics in PostgreSQL docs), retry with capped exponential backoff and jitter, and move to a dead-letter state after a bounded number of attempts. The notifier call carries its own idempotency key.
- **Auth (2.5):** Passwords hashed with a memory-hard or otherwise currently recommended algorithm via a maintained library (VERIFY current OWASP guidance; do not hand-roll). Tokens: short-lived access tokens; define your refresh or re-authentication strategy and its revocation limits honestly. Secrets never logged, never in the repository, never in the image.
- **Observability (2.7):** Structured JSON logs with correlation id propagated to the job and outbound call; metrics for request rate, error rate, latency by route template (not raw path), job queue depth and age, and notifier failures. If you do not run a metrics backend, expose the metrics endpoint and describe the queries you would alert on.

## 3. Milestones with checkpoints

Each checkpoint is a hard gate: do not start the next milestone until the checkpoint evidence exists in the repository. Record time spent per milestone; the discrepancy against your estimate goes in the retrospective.

| # | Milestone | Checkpoint evidence |
|---|---|---|
| M0 | Skeleton and repo dossier (0.1): package layout, `pyproject.toml`, pinned lock, pre-commit/lint/type-check, CI running tests, Dockerfile, `make`-style entry points | CI green on an empty-but-real test; a README another engineer can follow in 15 minutes |
| M1 | Schema and migrations; repositories; seed script | Migration up/down/up test on a clean database; documented constraint list; first `EXPLAIN` note |
| M2 | Learners, courses, enrollments, state machine | Table-driven transition tests covering every (state, event) pair, legal and illegal |
| M3 | AuthN/Z and role enforcement | Authorization matrix test: every role x every endpoint, asserting the allowed and denied outcome, generated from one table |
| M4 | Idempotent batch ingest and pagination | Concurrency test with at least 20 simultaneous identical requests yielding exactly one set of rows; cursor pagination test under concurrent inserts |
| M5 | Reporting, background jobs, notifier, retry/dead-letter | Failure-injection tests: notifier times out, returns 500, returns 200 after a retry; process killed mid-job and job recovered |
| M6 | Observability, health/readiness, graceful shutdown, timeouts | Demonstrated shutdown with in-flight requests; documented timeout budget from client to database |
| M7 | Hardening and security review | Threat model (STRIDE-style or equivalent) with each threat mapped to a control or an accepted risk |
| M8 | Documentation, runbook, defense preparation | Design doc, ADRs, runbook, completed rubric self-score |

## 4. Acceptance criteria

The submission is accepted for defense only if all of the following are demonstrably true (each with a test or a reproducible command):

1. A clean checkout builds, migrates, seeds, and passes the full test suite using documented commands, on a machine that is not yours if at all possible (a fresh container counts).
2. Every endpoint in the OpenAPI document has at least one success test and one failure test; request and response bodies in tests are validated against the schema.
3. No endpoint returns a stack trace, SQL text, or internal identifier in an error response.
4. Duplicate and concurrent ingest produces no duplicate rows and no lost results (proved by a test, not an argument).
5. Killing the process during job execution loses no completion notification and sends no unbounded duplicates; at-least-once delivery with an idempotent receiver is the stated guarantee, and you state it as such.
6. Role escalation is impossible via any endpoint you wrote (horizontal: another instructor's course; vertical: instructor performing admin actions).
7. Startup fails fast and clearly on invalid configuration.

## 5. Testing requirements (1.4, 4.2)

- A test pyramid with stated proportions and a stated reason: unit tests for the state machine and pure logic; integration tests against a real PostgreSQL instance (not SQLite standing in for it, unless you document which behaviors you are not testing); a small number of end-to-end tests through HTTP.
- Test isolation: each test starts from a known database state; tests pass in random order and in parallel if you claim parallelism.
- Time and randomness injected, never patched ad hoc across the codebase.
- Mutation-style spot check: choose five lines of critical logic, deliberately break each, and record whether the suite fails. Report the ones that did not and fix the gaps.
- Coverage numbers may be reported but never used as the quality argument; explain which untested lines are untested on purpose.
- A regression test for each bug you hit during the build; list them in the failure log (0.3).

## 6. Security and reliability expectations (4.3)

Security: input validation at the boundary with explicit size limits; parameterized queries only; no secret in logs; dependency audit command documented and run (VERIFY the tool you use, for example `pip-audit`); rate limiting or a documented decision not to implement it with the compensating control; CORS configured deliberately; password reset or token flows, if present, resistant to enumeration; authorization checks at the use-case layer so a new route cannot forget them.

Reliability: every outbound call has a timeout, a retry policy, and a bounded concurrency; every retry has a corresponding idempotency story; the readiness endpoint reflects the database dependency; a degraded-mode statement says what the service does when the notifier is down for an hour (the answer should be: ingest continues, jobs accumulate, queue-age alert fires, nothing is lost).

## 7. Performance criteria (methodology only)

You are not given target numbers; you must derive them. Do the following, in the design doc:

1. State an expected workload (requests per second, batch sizes, data volume) as an explicit **assumption** with its source or rationale. Mark it as an assumption.
2. Choose the metrics that matter (latency percentiles by route, throughput, database time per request, queue age) and say why mean latency is insufficient (4.4).
3. Build a load test you can rerun; record hardware, versions, dataset size, warm-up, and run duration. Run it at least three times and report the spread, not one number.
4. Find the actual bottleneck with a profiler or database statistics, not by guessing. Report one change, the measurement before and after, and whether the improvement exceeds run-to-run noise.
5. State what you did not measure.

Do not copy numbers from blog posts. Do not claim a requests-per-second figure without the method that produced it.

## 8. Documentation requirements

- `README.md`: purpose, quick start, configuration reference, how to run tests, how to run the service.
- `docs/design.md`: context, requirements, architecture diagram (Mermaid or ASCII), data model, key flows (ingest, completion job), failure modes table, security model, and the performance investigation.
- `docs/adr/`: at least five ADRs, each with context, options considered, decision, consequences. Required topics: sync vs async stack; job mechanism; idempotency storage; pagination strategy; auth token design.
- `docs/runbook.md`: how to tell the service is unhealthy, the three most likely failures with diagnosis steps and commands, how to roll back a migration, how to drain the dead-letter queue.
- `docs/failure-log.md`: entries in the 9-field format from `00-front/templates/FAILURE-LOG.md`.
- `docs/ai-use.md`: if any AI was used, which parts, which outputs you rejected and why, and one defect that AI-generated code introduced and you caught (use the AI audit scorecard). If none was used, say so.

## 9. Final technical defense

**Format.** 60 minutes, live, with no AI and no notes beyond the repository itself. Evaluator can be a peer, a mentor, or yourself recorded on video and reviewed against the rubric a day later (state which). Structure: 10 minutes uninterrupted walkthrough of the architecture; 35 minutes of questions; 15 minutes of live modification (section 10).

**Question bank (expect any of these, with follow-ups that probe your actual code):**

1. Walk through exactly what happens, in order, from the socket accepting a request to the response for `POST /v1/results`. Where are transactions opened and closed?
2. Two identical ingest requests arrive in the same millisecond. Show me the exact mechanism that prevents duplicate rows. What happens if the first crashes after inserting the key but before storing the response?
3. Which isolation level does the report query run under, and what can a reader see that surprises them? Would you change it?
4. Why keyset pagination here? Show a case where offset pagination would return wrong results.
5. Your notifier receives the same completion twice. Is that a bug in your system? Defend your answer.
6. Explain how you know the event loop is not blocked. How would you detect it if it were?
7. Demonstrate that an instructor cannot read another instructor's enrollments. Where is the check, and why is it there and not in the router?
8. Show the query plan for your slowest endpoint. Why that plan? What would change it?
9. A migration adds a NOT NULL column with a default to a 50-million-row table. What do you need to know before running it?
10. What does your readiness probe check, and what is the failure mode of checking too much?
11. Which of your tests would still pass if you introduced a subtle authorization bug? Show me.
12. What is the first thing you do if the dead-letter queue starts growing at 03:00?
13. Which decision in the ADRs would you now reverse, and what evidence changed your mind?
14. Where did AI-generated code (if any) introduce a defect, and how did you detect it?

Answers must cite your code, tests, or measurements. "It should" is not an answer; "line N does X, test T proves it" is.

## 10. No-AI reconstruction or extension challenge

Choose one, drawn by a random method (die roll or a peer) so you cannot pre-rehearse:

- **R1 reconstruction (4 hours, Mode A):** From a blank directory, with only the OpenAPI document and the schema DDL from your submission, rebuild the idempotent ingest endpoint with its concurrency-safe key handling, plus tests that prove the concurrency property. No AI, docs allowed (Mode B variant permitted only for syntax lookups; declare which).
- **R2 extension (3 hours, Mode A/B):** The requirements change mid-way: add a `cohort` entity, make enrollments belong to a cohort, migrate existing data without downtime semantics, update the authorization rules so instructors see cohorts they co-teach, and keep the OpenAPI diff backward compatible for existing clients.
- **R3 incident (2 hours):** You are given your own service with a planted defect (supplied by a peer or by you in a branch you did not read for a week): a missing transaction boundary, a swallowed exception, or an N+1 query. Find, fix, and write the regression test and a short postmortem (7.2).

Pass requires the working change, the passing tests, and a spoken explanation of every line you wrote.

## 11. The 100-point rubric

| Area | Points | Notes |
|---|---|---|
| Correctness and acceptance criteria | 20 | Every criterion in section 4 demonstrated |
| Architecture and design clarity | 10 | Boundaries, interfaces, simplest design that meets the requirements; penalize both over- and under-engineering |
| Data modeling and SQL | 10 | Constraints, indexes justified, plans examined, migrations safe |
| Testing | 15 | Pyramid, isolation, concurrency and failure tests, regression tests |
| Security | 10 | Authz matrix, secret handling, validation, threat model |
| Reliability and operations | 10 | Timeouts, retries, idempotency, shutdown, health, runbook |
| Performance method | 5 | Honest methodology, spread reported, bottleneck found by measurement |
| Documentation | 5 | Design doc, ADRs, runbook usable by a stranger |
| Technical defense | 10 | Specific, code-grounded answers; honest about gaps |
| No-AI reconstruction/extension | 5 | Completed within limits and explained |
| **Total** | **100** | Pass: 80 or more and no critical failure |

**Critical failures (any one blocks a pass regardless of total):** a concurrency or idempotency test that is absent or does not actually run concurrently; any authorization bypass found in review; secrets committed to the repository; an endpoint building SQL by string concatenation with user input; inability to explain code you submitted as your own; claims of performance without a method.

**If failed:** a focused remedial task is assigned by the weakest rubric area (for example, a standalone idempotency exercise from 2.6 repeated from a blank file, or the authorization matrix rebuilt for a new resource), followed by a re-defense of only the failed topics. Reread-the-chapter is not remediation.

Ledger update: set Capstone A to `Demonstrated` after pass; `Production-ready` only after the service has been deployed somewhere real, operated for at least two weeks, and one real defect was found and fixed through your observability.
