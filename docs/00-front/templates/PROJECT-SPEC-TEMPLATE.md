# Project Specification Template (14 fields)

Use this for every lesson project and capstone, and for any personal project you want assessed. Write the spec **before** you write code. A spec you cannot fill in is a signal that you do not yet understand the problem; treat that as the first finding. Specs may be revised, but record each revision and why (changes after the work starts are themselves a skill, 7.2).

**Project title:** __   **Lesson/capstone:** __   **Mode (A/B/C per part):** __   **Date:** __

| # | Field | Content guidance | Your entry |
|---|---|---|---|
| 1 | Problem statement | One paragraph: who has what problem, and what changes if it is solved. No solution language. | |
| 2 | Context | Where this runs, existing systems, users, team standards, versions (language, framework, OS, database). What you may and may not change. | |
| 3 | Requirements | Numbered, testable statements ("The endpoint returns 409 when..."). Separate must, should, may. | |
| 4 | Constraints | Time, dependencies allowed, no-AI or docs-only rules, performance or memory limits (as assumptions, with source), compatibility, security. | |
| 5 | Acceptance criteria | Observable pass/fail checks, each mapped to a requirement number and to a test or command. | |
| 6 | Edge cases | Explicit list: empty, maximum, malformed, concurrent, repeated, partial failure, time and timezone, encoding, permission boundaries. | |
| 7 | Quality requirements | Maintainability, test expectations, observability, security, accessibility, documentation level. State measurable thresholds where possible. | |
| 8 | Deliverables | Exact artifacts and their locations (repository, design doc, test report, benchmark report, runbook, postmortem). | |
| 9 | Difficulty | Foundation / Intermediate / Advanced / Expert, with one line on why. | |
| 10 | Estimated effort | A range including debugging (for example 6-10 hours). After finishing record actual hours and the reason for any gap above 30%. | |
| 11 | Progressive hints | At least three levels, least revealing first: (1) a question to think about, (2) the concept or tool to apply, (3) the shape of the approach without code. Record which hint level you used and when. | |
| 12 | Evaluation rubric | 100 points with weights and critical failures; copy and adapt `RUBRIC.md`. | |
| 13 | Extension challenge | One harder variant (scale, a changed requirement, a second language, a stricter constraint) to attempt after passing. | |
| 14 | Reflection questions | At least three, specific to this project (what surprised you; which decision would you reverse; what did the tests miss). | |

## Spec quality checklist (answer before starting)

- Could another engineer build a correct solution from this spec without asking me anything? If not, which question would they ask? Add it.
- Is every requirement testable? Rewrite the ones that are not.
- Are performance statements marked as assumptions with a stated measurement method?
- Is anything in "Constraints" actually a design decision in disguise? Move it to the design doc.
- Does the spec say what is out of scope?

## Change log

| Date | Change | Reason | Impact on rubric/schedule |
|---|---|---|---|
| | | | |
