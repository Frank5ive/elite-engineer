# Generic 100-Point Rubric (adapt per project)

Pass for any lesson mastery gate: **80/100 with no critical failure.** Capstones use their own tuned rubric (in each capstone file) with the same pass rule. Score from evidence in the repository, not from intent. Score yourself first, then have the rubric applied by a second reader (a mentor, a peer, or a fresh Claude session shown only the artifacts) and record both scores and the gap.

## Weighted categories

| Category | Weight | What earns full marks | Common deductions |
|---|---|---|---|
| Correctness | 25 | Meets every acceptance criterion; edge cases handled; behavior verified by running it | Untested paths; edge cases only reasoned about; works on happy path only |
| Testing | 20 | Tests that fail when the code is wrong (verified by deliberately breaking it); right level; isolated; deterministic; regression tests for bugs found | Tests that assert nothing meaningful; shared state; coverage as the goal; flaky tests tolerated |
| Design and readability | 15 | Simplest design meeting the requirements; clear boundaries and names; no unneeded abstraction or dependency | Over-engineering; god functions; leaky layers; unexplained cleverness |
| Security and robustness | 10 | Inputs validated at boundaries; least privilege; secrets handled; failure paths defined; timeouts and limits | Trusting input; swallowed exceptions; unbounded resources; secrets in code |
| Performance and resource reasoning | 5 | Claims backed by a stated method; no premature optimization; complexity understood | Numbers without method; optimizing without measuring |
| Documentation and communication | 10 | README or design note a stranger can follow; decisions recorded with reasons; honest limitations | Documentation restating code; missing "why"; overclaiming |
| Process evidence | 5 | Meaningful commits, failure log entries, ledger updated, time estimates compared with actuals | Single giant commit; no log; no reflection |
| Explanation and defense | 10 | Can explain and modify own code live without the lesson or AI; admits uncertainty accurately | Cannot explain own code; confident wrong answers |
| **Total** | **100** | | |

## Critical failures (any one means not passed, whatever the total)

1. A defect that violates the lesson's central correctness property (for example data loss, authorization bypass, undefined behavior, look-ahead bias, a fabricated result).
2. Security issue of the injection, authorization bypass, or secret exposure class in submitted code.
3. Tests that cannot fail (no assertions, mocks of the code under test) presented as evidence.
4. Fabricated or unmeasured performance numbers, or any claim of trading profitability (quant work).
5. Submitted code the author cannot explain, in a Mode A or B exercise that was done with AI assistance not disclosed.
6. Using or consulting reference solutions before a serious attempt, and not disclosing it.
7. Lesson-specific critical failures named in the lesson's mastery gate.

## Scoring bands (informational)

| Score | Interpretation |
|---|---|
| 90-100 | Strong; move on, schedule the 14-day retest |
| 80-89 | Pass; list the two weakest rubric lines and fix them in the next related lesson |
| 65-79 | Not yet; do the lesson's focused remedial exercise, then re-submit only the weak parts |
| below 65 | Return to the prerequisite lesson's retrieval practice, then redo the project from a blank file |

## Scoring sheet

| Category | Max | Self | Reviewer | Evidence/notes |
|---|---|---|---|---|
| Correctness | 25 | | | |
| Testing | 20 | | | |
| Design and readability | 15 | | | |
| Security and robustness | 10 | | | |
| Performance and resource reasoning | 5 | | | |
| Documentation and communication | 10 | | | |
| Process evidence | 5 | | | |
| Explanation and defense | 10 | | | |
| **Total** | 100 | | | |
| Critical failures found | | | | |
| Pass? (yes/no) | | | | |
