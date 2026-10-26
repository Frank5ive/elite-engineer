# AI Output Audit Scorecard

Use whenever you accept AI-generated code, design, explanation or analysis into your work (Mode C), and during Lesson 7.1. The goal is not to avoid AI; it is to remain the owner of correctness. Fill one scorecard per significant output (more than about 20 lines of code, any design recommendation, any statistical or numerical claim).

**Date:** __  **Project/lesson:** __  **Tool and model:** __  **Mode:** C
**What I asked (paste the prompt or summarize):** __
**What I received (link or commit):** __

## Part 1: Independent verification (do before accepting)

| # | Check | Result (pass/fail/NA) | Evidence |
|---|---|---|---|
| 1 | I can explain every line without the AI. | | |
| 2 | Every API, flag, function and import exists in the documented version I use (checked in official docs, not asked back to the AI). | | |
| 3 | It runs; I ran it, and the output matches what I predicted before running. | | |
| 4 | Tests exist, and I verified they fail when I deliberately break the code. | | |
| 5 | Edge cases (empty, maximum, malformed, concurrent, repeated, error paths) were exercised. | | |
| 6 | Security review: input validation, authorization, injection, secrets, unsafe deserialization, error leakage. | | |
| 7 | Resource and lifetime review: unclosed resources, unbounded growth, ownership, thread/async safety, transaction boundaries. | | |
| 8 | Fits the codebase and team standards: naming, layering, dependencies (no new dependency without a reason I can defend). | | |
| 9 | No hallucinated citations, numbers, benchmark results or statistics; every numeric claim traced to a source or a measurement I made. | | |
| 10 | The simplest design that meets the requirement; no speculative abstraction. | | |

## Part 2: Defects found

| Defect | Category (wrong API / logic / security / lifetime / concurrency / statistical / style / spec misread) | How found | Severity | Would I have caught it without checks above? |
|---|---|---|---|---|
| | | | | |

## Part 3: Scoring

| Dimension | Points | Score |
|---|---|---|
| Verification rigor (Part 1 items passed with evidence, 2 points each) | 20 | |
| Defect discovery (found defects that truly existed, or documented why none exist after adversarial review) | 20 | |
| Understanding (explained the code to an imagined reviewer, or live: modify without AI) | 25 | |
| Ownership of decisions (alternatives considered; reasons for accept/reject recorded) | 15 | |
| Test integrity (tests verified able to fail) | 10 | |
| Honest disclosure (recorded in ai-use.md, including rejected output) | 10 | |
| **Total** | 100 | |

Interpretation: 85 or more, the output may be merged. 70-84, merge only after fixing the unverified items. Below 70, discard or rewrite it yourself; treat as a Mode A/B exercise.

## Part 4: Dependency check (monthly, across scorecards)

- How many outputs did I accept this month? __ How many had at least one real defect? __
- In which categories do AI outputs fail most for me? __
- For which tasks did I reach for AI before trying myself? __ Re-do one of them from a blank file in Mode A this week: __
- Which skill in the ledger is slipping because of AI use? __

## Part 5: Better prompting (record what worked)

- Did I give versions, constraints and the failing test? __
- Did I ask for alternatives and trade-offs rather than a single answer? __
- Did I ask the model to attack its own answer (list the ways it could be wrong)? __ (This does not replace Part 1.)
