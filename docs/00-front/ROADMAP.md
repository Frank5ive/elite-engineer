# Roadmap

This roadmap sequences the 38 lessons and five capstones across three horizons. Every duration is an **estimate** from the lesson time budgets and the pacing assumptions in `README.md` (about 21 hours per week: five work days at 2-3 hours, two free days at 4-5 hours, at least 7 hours of sleep protected). Your diagnostic routing changes it. When a week slips, shift the plan; do not compress sleep. No outcome (job, role, income) is guaranteed by following it.

## 1. Horizon 1: before you start (days before Monday)

Goal: arrive with a working environment, a baseline, and no new commitments you cannot keep.

| Item | Time | Output |
|---|---|---|
| Take `DIAGNOSTIC.md` in two sittings (Mode A) | 4 hours total | answers in `progress/diagnostic/` |
| Grade it (key or continuation session) and write the routing summary | 1 hour | `progress/diagnostic/summary.md` |
| Create `progress/`: copy LEDGER, FAILURE-LOG, WEEKLY-REVIEW templates | 30 min | ledger initialized |
| Read Lesson 0.1 sections 1-5 and prepare the day-one checklist | 1-2 hours | checklist for your first day |
| Set up a personal scratch environment: Python 3.12 venv, PostgreSQL, PHP 8.2, a C++20 compiler, git | 2-3 hours | each runs a hello-world and a test |
| Fix your sleep schedule and study slot | 0 | a written latest-end time for work-day study |

Do not start Vol 1 or any large project before day one at the job. Rest is part of the plan.

## 2. Horizon 2: first 30 to 90 days

Goal: become reliably productive in the job's codebase, and establish habits: tests, Git hygiene, debugging method, written communication.

**Days 1-30 (Weeks 1-4):** Vol 0 in week 1 (apply to the real repository; produce a repo dossier), Vol 1 (Python internals, testing) in weeks 2-3, start Vol 2 (HTTP contracts and FastAPI). Measure: ledger rows for 0.1-0.4 Demonstrated; first PR reviewed by a colleague; failure log with at least 10 entries.

**Days 30-90 (Weeks 5-12):** finish Vol 2 (SQL, transactions, auth, async, observability), complete Capstone A, and begin Vol 3 (PHP/Moodle). Measure: Capstone A defended; first retention retests (14-day) passed for Vol 0 and Vol 1; one example of study material applied at work with evidence.

**Job-driven reordering rule:** the job outranks the book. If your first assignments are in Moodle, start Vol 3 in week 5 and move Vol 2 lessons 2.3, 2.4 and 2.5 into the gaps; Capstone B then precedes Capstone A. If your assignments are database heavy, pull 2.3 and 2.4 forward. Record the change in the ledger notes.

## 3. Horizon 3: 6 to 24 months

| Period (approx.) | Focus | Completion evidence |
|---|---|---|
| Months 3-5 | Finish Vol 3 and Capstone B; Vol 4 (architecture, testing strategy, security, performance method) interleaved with real work | Capstone B defended; at least one real design doc and one real post-mortem written |
| Months 5-9 | Vol 5 C++ (5.1-5.6), Capstone C | Order-book component with sanitizer-clean tests and a measured benchmark report |
| Months 9-13 | Vol 6 quant (6.1-6.5) and Capstone D | A research report with a limitations section; no profitability claims; null calibration |
| Months 12-16 | Vol 7 (AI independence audits, design docs, defenses) and Capstone E | Defended boundary justification; 7.1 audit passed |
| Months 16-24 | Retests, a second pass over weak ledger rows, real-world applications, open-source or work contributions, public portfolio write-ups | Ledger rows moved to Applied/Production-ready only on evidence |

The 6-24 month horizon is flexible: P2 and P3 material (Vol 5, 6, Capstones C-E) should be compressed or extended based on your job, and depth in C++ or quant is limited by the time you can protect. Interleave Vol 7 (7.1 especially) earlier if you find yourself using AI as a crutch.

## 4. Project roadmap: lessons to deliverables

Keep one portfolio repository per track under a `portfolio/` directory (outside the book folders). Each lesson project in section 9 of the lesson names its own deliverable; this table says what you retain and extend so projects accumulate rather than being thrown away.

| Lessons | Deliverable you keep | Cumulative project it feeds |
|---|---|---|
| 0.1-0.4 | Repo dossier of your job's codebase; Git workflow notes; failure log; communication templates | Used all the time; evidence for Applied status |
| 1.1-1.4 | Small library with typed, tested modules; pytest suite with fixtures; logging/config module | Seeds the shared `core/` package used by the backend project |
| 2.1-2.2 | API contract (OpenAPI) and a first service | Capstone A skeleton (Course Enrollment service) |
| 2.3-2.4 | Schema, migrations, query/EXPLAIN notes, keyset pagination | Capstone A data layer |
| 2.5-2.6 | Auth module, idempotent ingest, background jobs | Capstone A security and reliability |
| 2.7 | Health checks, metrics, deploy artifacts, runbook | Capstone A operations; finish and defend Capstone A |
| 3.1-3.2 | PHP library and a minimal Moodle plugin skeleton | Capstone B skeleton |
| 3.3-3.4 | Capability-gated pages, Forms API, DB API | Capstone B access control and CRUD |
| 3.5-3.6 | Events, tasks, web service, privacy provider, PHPUnit/Behat, upgrade test | Capstone B; defend |
| 4.1-4.4 | ADRs, test strategy, review of a legacy code sample, threat model, performance investigation | Retroactively strengthens A and B; reused in C, D, E |
| 5.1-5.4 | C++ build setup, RAII wrappers, container/algorithm implementations with invariants | Capstone C reference order book |
| 5.5-5.6 | Sanitizer/profile reports, allocator and layout experiments | Capstone C optimized implementation |
| 6.1-6.3 | Probability, numerical and statistical notebooks as tested library code | Capstone D estimators and null calibration |
| 6.4-6.5 | Pricing and risk functions; backtest engine with cost model | Capstone D engine |
| 7.1-7.2 | AI audit scorecards, a design doc, an ADR set, a post-mortem, a recorded defense | Used to defend every capstone |
| Capstones A-E | Five defended systems | Portfolio evidence |

**Capstone order (default):** A, then B, then C, then D, then E. E depends on C and one of A or D. Capstones may be reordered by the job rule above.

## 5. The first 12 weeks

Assumptions: Week 1 starts the Monday you begin the job. Monday to Friday are work days (study blocks of 2-3 hours); Saturday and Sunday are free days (4-5 hours). Each cell is a block; "W" means a work-day block, "F" means a free-day block. Block contents: retrieval (10-15 min cold) always opens a block, and the end of the block is the failure-log/ledger tidy (10 min). Total weekly target about 21 hours.

**Daily block templates**

- Work-day block (2-3 h): 10 min cold retrieval; 60-90 min learn/break or build (one at a time); 30-45 min exercise (Mode A/B); 10 min log.
- Free-day block (4-5 h): 15 min retrieval; 90-120 min build; 20-30 min break (away from screen); 90 min second build or debug; 30 min review (Saturday: tidy; Sunday: weekly review).

**Cut-first list when a week slips:** (1) extension challenges, (2) optional "Further depth", (3) second variants of exercises, (4) the second free-day block. Never cut: retrieval, failure log, the mastery-gate project, sleep.

| Week | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| 1 | W: 0.1 sections 1-5 applied to the real repo (clone, run, test) | W: 0.1 repo dossier and request trace | W: 0.2 Git workflow sections 1-5 | W: 0.2 exercises (rebase, bisect, reflog) | W: 0.2 gate project; ask for PR feedback at work | F: 0.3 debugging method and failure log; first failure log entries | F: 0.4 communication templates; weekly review; ledger |
| 2 | W: 1.1 object model sections 1-5 | W: 1.1 failure lab, retrieval | W: 1.1 project; gate | W: 1.2 iterators and generators | W: 1.2 context managers, exceptions | F: 1.2 project and gate | F: retest 0.x cold; weekly review |
| 3 | W: 1.3 types and packaging | W: 1.3 config, logging | W: 1.3 project; gate | W: 1.4 pytest, fixtures | W: 1.4 mocking and isolation | F: 1.4 project and gate | F: retest 1.1-1.2 cold; weekly review |
| 4 | W: 2.1 HTTP semantics, status codes | W: 2.1 contracts and OpenAPI | W: 2.1 project; gate | W: 2.2 FastAPI lifecycle, routing | W: 2.2 Pydantic v2, DI | F: 2.2 project and gate; start Capstone A M0 | F: Capstone A M0 completed; weekly review |
| 5 | W: 2.3 SQL and joins | W: 2.3 schema design and indexes | W: 2.3 EXPLAIN; project start | W: catch-up slot if needed; else 2.3 gate | W: 2.4 transactions and isolation | F: 2.4 migrations and pagination | F: 2.4 project and gate; weekly review |
| 6 | W: 2.5 passwords, authn | W: 2.5 authz, JWT/OAuth basics | W: 2.5 secrets; project | W: 2.6 async vs blocking | W: 2.6 jobs, retries | F: 2.6 idempotency project; gate | F: retest 1.3-1.4, 2.1-2.2; weekly review |
| 7 | W: 2.7 observability | W: 2.7 health checks and timeouts | W: 2.7 deploy; project | W: Capstone A M1 (schema, migrations) | W: Capstone A M2 (state machine) | F: Capstone A M3 (authn/z matrix) | F: Capstone A M4 start; weekly review |
| 8 | W: A M4 (idempotent ingest) | W: A M4 concurrency tests | W: A M5 (jobs) | W: A M5 failure injection | W: A M6 (observability) | F: A M6 shutdown and timeouts; M7 threat model | F: A M7; weekly review |
| 9 | W: A M8 docs and runbook | W: A defense prep (questions 1-7, Mode A) | W: A defense prep (questions 8-14) | W: Capstone A defense (or record it) | W: fix defense findings; ledger | F: R1/R2/R3 no-AI challenge | F: retest 2.3-2.5; weekly review |
| 10 | W: 3.1 modern PHP | W: 3.1 Composer and project | W: 3.1 gate | W: 3.2 Moodle architecture | W: 3.2 plugin types and layout | F: 3.2 project and gate | F: Moodle instance health check; weekly review |
| 11 | W: 3.3 capabilities and contexts | W: 3.3 access control | W: 3.3 project; gate | W: 3.4 Forms API and params | W: 3.4 output API and strings | F: 3.4 DB API; project and gate | F: retest 2.6-2.7; weekly review |
| 12 | W: 3.5 events and tasks | W: 3.5 web services, caching | W: 3.5 File API and privacy API | W: 3.5 project | W: 3.6 PHPUnit | F: 3.6 Behat, upgrades, gate; Capstone B M0 | F: review the quarter; update roadmap; weekly review |

Notes on the table:

- Week 5 Thursday is a catch-up slot by design; use it for the lesson you are behind on, otherwise finish the gate.
- The table assumes a diagnostic at Standard routing. For Accelerated or Test-out routes, replace the learn blocks with a cold attempt at the gate project; spend recovered time on Capstone A earlier or on retests.
- Weeks 10-12 deliver Vol 3 only if Vol 2 is done. If your job is Moodle-heavy, swap weeks 4-9 and 10-12 blocks as in section 2.
- Capstone B (35-60 hours) and Vol 4 begin after week 12; they are not scheduled here.

### What to review each Sunday (20-30 minutes, see WEEKLY-REVIEW.md)

Hours versus sleep; delivered versus planned; ledger changes; five cold retrieval items older than 14 days; failures and their category; one job-relevant application; AI use; cuts for next week.

### Milestone checklist for the first 12 weeks

- [ ] Diagnostic graded; routing written
- [ ] Vol 0 gates passed; repo dossier delivered at work
- [ ] Vol 1 gates passed; 14-day retests done for 1.1-1.2
- [ ] Vol 2 gates passed
- [ ] Capstone A defended (score recorded)
- [ ] First Vol 3 gates passed (3.1-3.3 at least)
- [ ] Failure log with 30 or more entries, categorized; the top three root-cause categories identified
- [ ] At least five ledger rows at Retained or Applied with evidence
- [ ] Average sleep at or above 7 hours per night (honest count)

If you are well behind at week 12 (for example fewer than half of the milestones met), that is normal information about your real capacity, not a failure; re-estimate velocity from the weekly reviews and rebuild the plan from week 13.
