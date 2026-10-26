# Continue Here: Handoff for a New Claude Session

Use this document to resume the program in a different Claude session (or after a long break) without losing state. Claude sessions do not remember each other. Everything a new session needs is on disk or in the prompt you paste. Keep this file accurate: update the "State snapshot" section after every weekly review.

## 1. What this book is

**The Elite Engineer** is a training program for one reader (Frank), an existing developer (Python, FastAPI, PHP, Moodle, databases, testing) starting a new job and aiming to master modern C++ and move toward quantitative development. It has 38 lessons across Vols 0-7, five capstones, a diagnostic, templates, and a solutions folder. Its goal is demonstrable capability: building, explaining, debugging and defending without the book or AI. Mastery gate: 80/100 with no critical failure. No career outcome is guaranteed. Quant material never implies profitability.

## 2. Location and structure

Root: `/home/frank/Documents/engineering-book/`

```
00-front/        README.md, DIAGNOSTIC.md, DIAGNOSTIC-ANSWER-KEY.md, ROADMAP.md, CONTINUE-HERE.md, STYLE-GUIDE.md, templates/
01-vol0-job-readiness/      lessons 0.1-0.4
02-vol1-python/             1.1-1.4
03-vol2-fastapi-backend/    2.1-2.7
04-vol3-php-moodle/         3.1-3.6
05-vol4-engineering/        4.1-4.4
06-vol5-cpp/                5.1-5.6
07-vol6-quant/              6.1-6.5
08-vol7-independence/       7.1-7.2
capstones/       capstone-A..E
solutions/       reference solutions (one file per lesson)
progress/        the reader's own state (create if missing): LEDGER.md, failure-log.md, reviews/, diagnostic/, portfolio notes
```

Lesson file format: 12 sections (engineering problem; objectives; first principles; worked example; production perspective; failure laboratory; retrieval practice; independent implementation; project with 14 fields; engineering review; mastery gate; reflection) plus References. Read `00-front/STYLE-GUIDE.md` before editing or extending lessons.

**Solutions policy for any session:** reference solutions are in `solutions/` and should only be consulted after a serious attempt (working code or a complete written answer, run or checked, with the remaining doubts stated). A session grading or helping must not paste solutions into the working conversation unprompted before the attempt exists; reveal hints progressively as in each project's progressive hints.

## 3. The competency ledger

`progress/LEDGER.md` (copied from `00-front/templates/LEDGER.md`) has one row for every lesson (0.1-7.2) and capstones A-E, with status: Unseen, Introduced, Practiced, Demonstrated, Retained, Applied, Production-ready, plus evidence link, date, gate score, notes. Statuses require evidence (see the table in the ledger). Reading is at most "Introduced". Retained requires a cold retest after at least 14 days. Applied requires use in real work or a later project.

## 4. State snapshot (update after each weekly review)

```
Date of last update: ____-__-__
Current week of ROADMAP: __
Current lesson/project: __
Diagnostic status: not taken / taken, graded: yes/no
Section percents A-G: __
Routing per volume: __
Ledger summary counts: Unseen __ Introduced __ Practiced __ Demonstrated __ Retained __ Applied __ Production-ready __
Open failure log categories (top 3): __
Hours last week / average sleep: __ / __
Mode violations to repeat: __
Next retests due: __
Open questions for the mentor: __
```

## 5. How to ask a new session to do each job

Always start by pointing the session at the files; do not paste large files if the session can read the folder. If the session cannot read local files, paste the specific files named below.

**Grade the diagnostic.** Provide: `DIAGNOSTIC.md`, `DIAGNOSTIC-ANSWER-KEY.md`, your `progress/diagnostic/` answer files, and your Part H self-report. Ask: "Grade each item using the key, with per-item scores and a one-line note on each missed item's underlying gap. Run my code answers where possible (A5, A7, A9, A10, B1, B2, E2, E6, E7). Compute section percentages, calibration gaps against my predictions, and the routing per volume. Produce `progress/diagnostic/summary.md`. Be strict; do not give credit for unrun code or LOOKED UP items."

**Review deliverables.** Provide: the lesson file (for its rubric and critical failures), your project directory, your failure log entries, your estimate of your own rubric score. Ask: "Score this deliverable against the lesson's rubric (100 points) and critical failures. First show your findings without the solution, ranked by severity, with evidence (file and line). Do not rewrite my code; give hints at increasing levels. Then fill the scorecard, tell me whether I pass at 80 with no critical failure, and name the single most valuable thing to fix." For capstones also: "Conduct the technical defense using the capstone's question bank, one question at a time, wait for my answer, probe, and score at the end."

**Generate remediation exercises.** Provide: the failed items or rubric lines, the failure log entries, and the lesson. Ask: "Generate three focused remedial exercises for these gaps, each a blank-file task with a Mode label, acceptance tests I can run, and a pass criterion. No rereading tasks. Do not include solutions; I will request them after an attempt."

**Adjust the curriculum.** Provide: the state snapshot, the last four weekly reviews, and the ledger. Ask: "Propose pacing and sequencing changes with reasons from the evidence: where I am slower or faster than the plan, which rows are not retained, whether I should reorder volumes because of my job, what to cut first. Show the revised schedule for the next four weeks with daily blocks and the effect on later horizons. Protect 7+ hours of sleep. Do not add content; only reorder, cut or add retests."

**Check retention.** "Select five items from lessons older than 14 days per the ledger and quiz me one at a time, Mode A, without hints, and record which I missed so the ledger can be updated."

**Audit AI use.** "Using AI-AUDIT-SCORECARD.md, review this AI-generated output against the official docs for the stated versions and find defects. Then tell me which of my verification steps were weakest."

## 6. Rules for the helping session

State these to the session if it does not already know them:
- The reader is demanding of quality; be rigorous, never insulting, no filler or motivational speeches.
- Verify before asserting: framework and language facts must match the stated versions; use `VERIFY:` when unsure; never fabricate benchmark numbers, documentation references, API names or statistics.
- Never claim any trading strategy is profitable; keep mathematical correctness separate from implementation correctness.
- Do not give full solutions before a serious attempt; escalate hints gradually.
- Defensive security only; no offensive exercises against real systems.
- Do not tell the reader outcomes are guaranteed.
- Keep Moodle/PHP, FastAPI/Python, C++, and quant tracks distinct.
- Respect the pacing and sleep protections in `ROADMAP.md`; propose cuts rather than longer days.
- Lesson authoring style and structure are defined in `00-front/STYLE-GUIDE.md`.

## 7. Continuation prompt (copy everything in the box into a new session)

```
You are continuing a self-study program called "The Elite Engineer" with me (Frank). I am a developer (Python, FastAPI, PHP, Moodle, databases, testing) who just started a new job and wants to master modern C++ and move toward quantitative development. The program is a set of Markdown files under /home/frank/Documents/engineering-book/ (if you cannot read that folder, tell me which files to paste).

First, read in this order: 00-front/CONTINUE-HERE.md (this protocol), 00-front/README.md, 00-front/ROADMAP.md, progress/LEDGER.md, my latest file in progress/reviews/, and progress/failure-log.md. Then summarize back to me in under 200 words: where I am in the roadmap, the ledger summary counts, my top three failure-log patterns, and what is due next. Do not start teaching until I confirm the summary.

Rules you must follow: be demanding about quality and never insulting; no filler or motivational speeches; verify framework and language facts against the versions stated in lessons and write VERIFY: when unsure; never invent benchmark numbers, API names or references; never claim any trading strategy is profitable; defensive security only; no promises of career outcomes. Reference solutions are in solutions/ and should only be consulted after a serious attempt by me; do not reveal them early, use progressive hints instead. Mastery requires 80/100 with no critical failure per the lesson rubric. Protect my sleep (7+ hours) and propose cuts rather than longer days.

Today I want you to: [CHOOSE ONE AND DELETE THE REST]
(a) Grade my diagnostic: files in progress/diagnostic/, key in 00-front/DIAGNOSTIC-ANSWER-KEY.md. Run my code answers, give per-item scores and gap notes, section percentages, calibration gaps, routing per volume, and write progress/diagnostic/summary.md.
(b) Review my deliverable for lesson __ at path __: score it against the lesson rubric and critical failures, give findings ranked by severity with evidence and increasing-level hints, not a rewrite, and tell me whether I pass.
(c) Generate three remedial exercises for these gaps: __ (blank-file tasks with acceptance tests, Mode labels, pass criteria, no solutions).
(d) Adjust my curriculum based on the ledger and the last four weekly reviews: propose a reordering or cuts for the next four weeks with daily blocks, with reasons from evidence.
(e) Quiz me cold (Mode A) on five items from lessons older than 14 days, one at a time, and tell me what to update in the ledger.
(f) Run a technical defense for Capstone __ using its question bank, one question at a time, and score it at the end with the capstone rubric.
(g) Continue lesson __ with me: be my tutor while I follow the lesson's sections in order; do not show section 6's Reveal or any solution before I predict or attempt.
```

## 8. Maintenance

- After each week: update the ledger, the failure log, the weekly review, and section 4 of this file.
- If you edit lessons, follow `STYLE-GUIDE.md`; reference solutions go only in `solutions/`.
- Keep a backup of `progress/` (it is the only irreplaceable part). Version control it privately.
- If this folder is moved, update the root path in the continuation prompt.

## Status at generation (2026-10-26)
- All 38 lessons (0.1-7.2), 38 solutions files, 5 capstones, front matter and templates are written.
- Most lessons exceed the 3,000-5,000 word target (5,000-8,300 raw words including code). Trim or split if wanted; 3.4 (8,300) is the first candidate.
- `00-front/VERIFY-LIST.md` lists every unverified claim. Moodle items (Vol 3) are drafts: nothing there was run against a live Moodle. Verify against moodledev.io for your actual version before relying on them.
- Not run anywhere: FastAPI snippets in 0.1, Dockerfile in 2.7, clang/gdb/perf/valgrind commands, PHPUnit files, 1.4 project suite.
