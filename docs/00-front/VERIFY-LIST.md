# Verification status

Generated after a verification pass (2026-10-26) against primary sources and by running code where possible. The original 501 `VERIFY` markers were resolved: confirmed items had the marker removed, wrong items were corrected, and items that cannot be confirmed from a primary source were reworded to say so or left marked below.

## Known remaining gaps

- **Moodle (Vol 3):** checked against a clone of the real Moodle source (MOODLE_503_STABLE and main) and the developer docs, but never run against a live Moodle install. Run the labs on your actual version; the version your employer uses may differ from 5.3.
- Whether Moodle logs permission denials by default (3.3): no primary source found.
- Exact in-place 'component mismatch' error text (3.2 Lab A): needs a real install.
- Moodle plugins-directory submission rules (3.6): not checkable from code or developer docs.
- Whether a PHPUnit test that renders via get_renderer() needs $PAGE->set_url() (3.6 solutions): untested.
- Locust and coordinated omission (4.4): no documentation found; treat its tail latencies as suspect.
- Exchange queue priority on size reduction (6.5): venue-specific, unconfirmed.
- Deflated Sharpe formula (6.5): checked only against secondary implementations, not the paper.
- `perf` output and `coredumpctl` behaviour (5.5): not run (container restrictions).
- Library tested versions: Python 3.13, g++ 14.2, clang 18, PostgreSQL 18, PHP 8.4. Behaviour on other versions may differ.
- Lessons are still longer than the 3,000-5,000 word target (3.4 is about 8,300 words, 4.2-4.4 about 6,300-7,000). Trimming is not done.

## Remaining VERIFY markers in the text

| File | Line | Text |
|---|---|---|
| 04-vol3-php-moodle/3.2-moodle-architecture-and-plugins.md | 14 | **Reading convention for this lesson.** Every fact is labelled. **[Stable]** = a principle that has held across many Moodle versions and will probably survive. **[5.3]** = verified against official 5. |
| 04-vol3-php-moodle/3.2-moodle-architecture-and-plugins.md | 201 | `<MOODLE_BRANCH>` is the branch name for your target release: use the stable branch naming from the Moodle GitHub repository (branches are named like `MOODLE_405_STABLE`; `MOODLE_503_STABLE` exists, c |
| 04-vol3-php-moodle/3.3-capabilities-contexts-roles.md | 14 | **Labelling.** **[Stable]** = principle that has held across Moodle versions. **[5.3]** = verified against 5.3-era docs/source in the way stated. **[VERIFY]** = not confirmed; check as written. Names  |
| 04-vol3-php-moodle/3.3-capabilities-contexts-roles.md | 382 | **Security.** Defense in depth: capability + sesskey + parameter typing + output escaping + prepared queries through `$DB`. Log denied attempts? Moodle logs events, not denials by default (VERIFY); fo |
| 04-vol3-php-moodle/3.4-forms-output-database-api.md | 14 | Version discipline for this lesson. Moodle's *principles* (never trust input, escape on output, parameterise SQL, check capability, use the DB abstraction, keep strings out of code) have been stable f |
| 04-vol3-php-moodle/3.4-forms-output-database-api.md | 803 | / 8 / Deliverables / Plugin directory as a git repository with at least 8 meaningful commits; `README.md` for the plugin (install steps, capabilities, URL); a short `NOTES.md` listing every `VERIFY:`  |
| 04-vol3-php-moodle/3.4-forms-output-database-api.md | 807 | / 12 / Evaluation rubric (100) / Correct CRUD behaviour on A1-A10: 30. Security (cleaning, escaping once, sesskey, capability, IDOR): 25. DB design and `$DB` usage (placeholders, portability, upgrade) |
| 04-vol3-php-moodle/3.4-forms-output-database-api.md | 809 | / 14 / Reflection questions / Which of your `VERIFY:` resolutions surprised you? Where did you first put authorisation logic and why did you move it? What would break first if the site changed from Ma |
| 04-vol3-php-moodle/3.4-forms-output-database-api.md | 830 | Pass = 80/100 on the project rubric with no critical failure. Required evidence: the plugin repository, the `NOTES.md` with resolved `VERIFY` items and tested Moodle version, the A1-A10 demonstration  |
| 04-vol3-php-moodle/3.5-events-tasks-webservices-files-privacy.md | 9 | / Minimum versions / PHP 8.2. Moodle: **API names checked against moodledev.io docs for main/5.3 (5.3 "current stable, LTS", released 5 October 2026 per moodledev.io/general/releases, read 2026-10-26) |
| 04-vol3-php-moodle/3.5-events-tasks-webservices-files-privacy.md | 527 | No hints beyond moodledev.io. Evidence: green tests (3.6 shows how to run them) and a table listing every file and the Moodle API it uses, with each `VERIFY` resolved. |
| 04-vol3-php-moodle/3.5-events-tasks-webservices-files-privacy.md | 538 | / 4 / Constraints / No core changes. No new third-party libraries. Backward compatible: v1 URLs keep working. Mode B. PHP 8.2+. Each `VERIFY` item you use must be resolved in `NOTES.md` with source an |
| 04-vol3-php-moodle/3.5-events-tasks-webservices-files-privacy.md | 542 | / 8 / Deliverables / Updated plugin repository, `NOTES.md` with VERIFY resolutions and tested Moodle version, a sequence diagram (Mermaid) of the delete flow including event, observer and cache, and a |
| 04-vol3-php-moodle/3.5-events-tasks-webservices-files-privacy.md | 556 | Pass = 80/100, no critical failure. Evidence: repository, tests output (or manual scripts), NOTES.md with VERIFY resolutions, contract table, diagram, 10-minute defence. Critical failures: a service f |
| 04-vol3-php-moodle/3.6-testing-style-upgrades.md | 269 | Version and metadata; style and static checks green; tests green on every supported Moodle/PHP/DB combination you claim; Behat journey green; upgrade from previous release and from the oldest supporte |
| 04-vol3-php-moodle/3.6-testing-style-upgrades.md | 396 | / 4 / Constraints / No core modifications. No suppressed style errors unless justified in writing. Tests must pass in any order and alone. Every `VERIFY` item you rely on must be resolved in NOTES.md. |
| 04-vol3-php-moodle/3.6-testing-style-upgrades.md | 400 | / 8 / Deliverables / Repository with tests, CI config, upgrade code, CHANGES, README, release tag; NOTES.md with VERIFY resolutions and measured suite runtimes; debugging report (symptom, hypotheses,  |
| 04-vol3-php-moodle/3.6-testing-style-upgrades.md | 404 | / 12 / Evaluation rubric (100) / Test quality and coverage of contracts: 25. Negative/security tests and red-then-green proof: 10. Style and static checks clean without suppression: 10. CI configurati |
| 04-vol3-php-moodle/3.6-testing-style-upgrades.md | 412 | Checklist: can each test fail (you saw it fail)? Does each test have exactly one reason to fail? Is state created by generators? Is time, cache and order handled? Are negative cases included? Zero sup |
| solutions/3.6-testing-style-upgrades-solutions.md | 3 | Docs basis: main/5.3 as read 2026-10-26. PHPUnit versions per docs: 11.4 on Moodle 5.0, 9.6 on 4.4-4.5; the 5.3 `composer.lock` pins 11.5.x. Names checked against the Moodle 5.3 source and moodle-plug |
| solutions/3.6-testing-style-upgrades-solutions.md | 32 | 3. `test_hostile_title_is_escaped_in_rendered_output`: render the renderable via `$PAGE->get_renderer(...)`/`render()` (needs `$PAGE->set_url` in the test; `VERIFY:`), assert the output contains `&lt; |
