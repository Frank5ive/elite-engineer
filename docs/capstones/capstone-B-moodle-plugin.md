# Capstone B: Moodle Plugin

| Field | Value |
|---|---|
| Priority | P0/P1: directly applicable to the day job if Moodle work is part of it. |
| Mode | Build: A/B for plugin logic; C permitted for boilerplate with disclosure. Defense and reconstruction: A. |
| Time budget | 35-60 hours over 3-4 weeks, including testing and upgrade work. |
| Prerequisites (lessons) | 0.1, 0.2, 0.3, 0.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3. Helpful: 2.1, 2.3, 7.2. |
| Minimum versions | PHP 8.2+; a supported Moodle release. Pin one exact release (for example a current LTS) and write it down. VERIFY supported releases and their PHP requirements at moodledev.io before starting. |
| Deliverable | An installable plugin (zip and repository), PHPUnit and Behat suites, an upgrade path test, a privacy provider, a design doc, and a technical defense. |

Attempt first. Reference notes: `../solutions/` after submission only.

**Version honesty:** Moodle APIs change between releases (hooks replacing some callback patterns, output renderer changes, deprecations). Everything you use must be checked against the developer documentation and the core code of your pinned release. Where this document names an API, treat the name as a pointer to verify, not as a guarantee for your version.

## 1. Specification: "Learning Check-in" activity-adjacent plugin

You are building a plugin for a Moodle site that has learners, teachers and a manager role. The plugin lets a teacher publish short **check-ins** inside a course (a prompt with a due date). Learners submit a brief text response and an optional file. Teachers see a submission list, can record a private comment and a status (`acknowledged`, `needs follow-up`), and the system sends a notification to a learner when status changes. A scheduled task flags overdue check-ins and, optionally, a web service lets an external system read aggregate counts for a course.

The plugin type is your decision and must be justified in an ADR (3.2). Defensible choices: a course activity module (`mod_`), or a smaller local plugin (`local_`) that attaches to course pages. State why the other options were rejected. A `mod_` plugin has the most standard surface (gradebook, backup/restore, completion); a `local_` plugin has the least. If you pick `local_`, you must say how teachers reach it and why you are not an activity.

### 1.1 Functional requirements

1. Teacher creates, edits, deletes check-ins within a course context, with a due date and optional description in the standard editor (with file support, which obliges File API use, 3.5).
2. Learner submits and edits a response until a configurable lock time; one active submission per learner per check-in, enforced at the database level.
3. Teacher lists submissions with pagination (use core table/paging mechanisms of your release rather than hand-rolling), filters by status, and records status and comment.
4. Notification on status change using the messaging API, with a provider declared in `db/messages.php`; respects user preferences.
5. Scheduled task for overdue detection, using the task API, idempotent when run twice.
6. Event(s) triggered for created/submitted/status-changed, observed by at least one observer in your plugin that does something real (for example, updating a summary table).
7. A web service function returning aggregate counts for a course, callable by a token with the correct capability and context validation.
8. Group mode support: if the course uses separate groups, a teacher with group restrictions sees only their group's submissions (3.3).

### 1.2 Non-functional requirements

- **No core modification.** Everything lives in the plugin directory. If you believe core must change, that is a finding to document, not a patch to ship.
- Coding style conforming to Moodle's PHP coding style; run the style checker your release documents (VERIFY: moodle-plugin-ci or phpcs with Moodle standard).
- All user-facing strings in language files; none hard-coded.
- Capabilities defined with sensible archetype defaults and risk bitmasks as appropriate; no role-name checks (checking for a role shortname instead of a capability is a defect).
- Backup and restore support if you chose `mod_`; if `local_`, a written statement that user data is excluded from course backup and why.
- Privacy API implemented: metadata declaration, export, and delete for user data (3.5), including file areas.
- Database changes only through `install.xml` and `upgrade.php`, never ad hoc SQL against the DB at runtime for schema.

## 2. Architecture and interface requirements

- **Layering inside the plugin (4.1):** thin entry-point scripts (`view.php`, `index.php`) -> use-case classes in `classes/` under your plugin namespace -> persistence through the `$DB` API in a small data-access class. Business rules (can this learner still edit?) live in a class with no `$PAGE` or `$OUTPUT` dependency so they are unit-testable.
- **Access control (3.3):** For each page and each web service function, you must list in the design doc: the context used, the capability required, the `require_login` and `require_capability` (or `has_capability`) call site, and the behavior for a user without access. Use the correct context (course module or course, not system, unless justified). Test the denial paths.
- **Parameter handling (3.4):** Every request parameter read via the param API with the strictest type that fits (`required_param`/`optional_param` with `PARAM_` types), `sesskey` checks on state-changing actions, and `confirm_sesskey` on forms not using the Forms API CSRF handling. Never read `$_GET`/`$_POST` directly.
- **Forms (3.4):** Use the Forms API (moodleform) for all input, with server-side validation in `validation()`. Document which fields rely on client-side behavior only (there should be none for security-relevant rules).
- **Output (3.4):** Use renderers and Mustache templates for HTML; never echo user text unescaped. Show where each piece of user text is cleaned (`format_text`, `format_string`, `s()`/`p()` or template escaping) and the context option you passed.
- **Database (3.4):** Use the DB API with placeholders for every query. Index on the columns your queries filter on; justify each index. No `SELECT *` in hot paths. Use `get_in_or_equal` for IN clauses.
- **Events and tasks (3.5):** Event classes extend the base event with correct `objecttable`, context, and level/CRUD declared. Observers must tolerate being called during import or restore, and must not assume a web session. The scheduled task must be safe if it runs for a long time or is interrupted: process in bounded batches.
- **Caching (3.5):** Use the Cache API where you cache something, with a definition in `db/caches.php`, correct mode (application/session/request), and an invalidation story. If you cache nothing, state why that is correct.
- **Web services (3.5):** Declared in `db/services.php`; parameters and returns described with the external API classes; context validated via the API's validation helpers; capability checked; no sensitive data in returns beyond what the capability grants.
- **Upgrades (3.6):** The initial release is version 1; you must ship a second version with a schema change and an `upgrade.php` step, and test upgrading a populated database from version 1 to version 2.

## 3. Milestones with checkpoints

| # | Milestone | Checkpoint evidence |
|---|---|---|
| M0 | Environment and dossier (0.1): Moodle instance at the pinned release running locally or in containers, debugging enabled, plugin skeleton installed | Screenshot or terminal capture of plugin listed in admin notifications; documented one-command reset |
| M1 | Schema, capabilities, language strings, version.php | `install.xml` validated through the schema editor or XMLDB check; capability matrix table in docs |
| M2 | Teacher CRUD and learner submission with Forms API and templates | PHPUnit tests for the rules class; manual test script with expected results per role |
| M3 | Access control, group mode, parameter handling | Denial-path tests for each role; a table of every entry point and its checks |
| M4 | Events, observers, messaging, scheduled task | Test that triggers the event and asserts observer effect; task run twice yields identical state |
| M5 | File API and Privacy API | Privacy provider tests (export and delete); file served only through `pluginfile` callback with access checks |
| M6 | Web service | Test with tokens of different capability; invalid context rejected |
| M7 | Behat scenarios and version 2 upgrade | At least three Behat scenarios across teacher and learner journeys; upgrade test from v1 data |
| M8 | Documentation, code-style pass, defense preparation | Style checker output clean or each violation justified; rubric self-score |

## 4. Acceptance criteria

1. The plugin installs on a clean site, upgrades from v1 to v2 on a site containing real v1 data, and uninstalls cleanly (tables removed, files and config cleaned up).
2. A learner cannot view or alter another learner's submission through any URL, form, or web service function.
3. A teacher outside the course (or a teacher in another group under separate groups) cannot see the submissions.
4. Every state-changing request fails without a valid `sesskey` or form token.
5. No hard-coded strings; no role-shortname checks; no direct superglobal access; no queries by string concatenation of user input.
6. The privacy provider exports exactly the data stored for a user (including files) and deletes it for a given context, and the tests prove both.
7. Scheduled task and observers are idempotent and safe under restore/import conditions you can name.
8. PHPUnit and Behat suites pass on the pinned release in a clean environment.
9. No PHP notices, warnings or deprecation messages at the developer debug level during the Behat journeys.

## 5. Testing requirements (3.6, 4.2)

- **PHPUnit:** advanced test cases using the Moodle test data generators (courses, users, enrolments, your own plugin generator in `tests/generator/`). Each test resets state per the framework. Test the rules class with no database where possible; test the DB layer against the real test database.
- **Behat:** scenarios in the plugin's `tests/behat/` using core step definitions where available and your own only where necessary. Keep scenarios short and independent; avoid sleeps (use the framework's wait steps).
- **Security tests:** one test per denial path from the access table; one test that posts a state change without sesskey; one test that supplies another user's id.
- **Upgrade test:** create v1 data through the generator or fixture, run the upgrade step, assert the data and schema.
- **Mutation spot check:** break five critical conditions (a capability check, a lock-time comparison, a group filter, a privacy deletion, a unique constraint) and report which tests catch each.
- Bug found during the build gets a regression test and a failure log entry (0.3).

## 6. Security and reliability expectations (4.3)

- The XSS surface: list every place user-controlled text reaches output (check-in description, response text, comments, notification body, web service output) and the sanitization used at each.
- Authorization at the lowest layer that is reused: the use-case class checks capability, so a new page cannot forget it.
- File access: files served only through the file serving callback with context and capability checks; filenames and mimetypes not trusted.
- Web service tokens: least privilege; document the role and capability set for the service user.
- Reliability: scheduled task bounded and resumable; a failed notification does not roll back the status change; event observers do not throw for expected conditions; large courses (thousands of submissions) do not load everything into memory (use recordsets and paging).
- Data retention: privacy deletion semantics defined for submissions that other users' records reference (for example, a teacher comment on a deleted learner's submission): choose and document.

## 7. Performance criteria (methodology only)

Moodle performance is dominated by database queries per page and by memory in batch code. Required:

1. Use the site's performance information footer and/or query logging of your release (VERIFY the exact setting names in the admin docs) to count queries and measure page time on the submission list for a course with a seeded dataset of stated size. Record the dataset size generator and your assumption of realistic scale.
2. Identify any N+1 pattern (a query per row) and remove it with a join or an IN-set load; show queries-per-page before and after. Query count is a more portable measurement than milliseconds; report both with the environment.
3. For the scheduled task, measure peak memory with a stated batch size and show it does not grow with row count.
4. Run each measurement at least three times; report spread. Do not quote numbers you did not measure and do not assume your laptop dataset reflects production.

## 8. Documentation requirements

- `README.md` in the plugin root: purpose, supported Moodle versions (as verified), installation, configuration settings, capabilities table.
- `docs/design.md`: plugin type decision, data model diagram, access-control table, flow diagrams for submission and notification, failure modes.
- `docs/adr/`: minimum four ADRs: plugin type; where business rules live; notification mechanism; privacy deletion semantics.
- `CHANGES.md` or the project's standard changelog, with the v1 to v2 upgrade explained, including what an administrator should check before upgrading.
- `docs/test-plan.md`: manual and automated coverage; what is not tested and why.
- `docs/ai-use.md`: as in Capstone A; Moodle is a domain where AI often produces plausible but deprecated or nonexistent APIs, so record any such instance you caught.
- Failure log entries in the 9-field format.

## 9. Final technical defense

**Format.** 60 minutes, no AI, with the repository and docs.moodledev.io and the Moodle core source available (Mode B). 10 minutes architecture walkthrough, 35 minutes questions, 15 minutes live modification.

**Question bank:**

1. Trace a learner's submission from form render to database row to event to notification. Name the API at every step.
2. A user has the capability in the system context but not in the course module context. Which does Moodle check, and what does your code do? Show the call.
3. Why `require_capability` in the use-case layer instead of in `view.php` only?
4. Show every place a user-supplied string is output. How is each escaped or cleaned, and what is the difference between `format_text` and `s()` in this context?
5. What happens if the scheduled task is killed halfway through and then runs again? Prove idempotency with your test.
6. Walk through your `upgrade.php` step. What if it is interrupted? What if the site is a multi-version jump from v1 to a later release?
7. How does your plugin behave during course restore, and what must observers not do there?
8. How does the privacy provider find all of a user's data? How would you know you missed a table?
9. Why did you choose this plugin type? What would have forced you to switch?
10. Your web service is called with a token whose user lacks the course capability. Show the failure path and the message the caller sees.
11. A teacher with group restrictions views the list. Show the query and where the group filter is applied.
12. Which of your PHPUnit tests would still pass if you removed the sesskey check?
13. Where could a Moodle upgrade of core break your plugin (deprecations, changed APIs), and how would you detect it before production?
14. Which API did you first use incorrectly, how did you notice, and what does the failure log say?

## 10. No-AI reconstruction or extension challenge

Choose one by random draw:

- **R1 reconstruction (4 hours, Mode B):** From a blank plugin directory with only moodledev.io and your design doc's access table, rebuild the submission flow (capability, form, DB layer, event, privacy export) and its PHPUnit tests. No AI.
- **R2 extension (3 hours):** New requirement: teachers can assign a check-in to specific groups only; submissions from non-assigned groups are hidden and blocked. Adjust schema with an upgrade step, access checks, privacy handling, backup/restore if applicable, and tests.
- **R3 review challenge (2 hours):** Review a deliberately flawed plugin diff (a peer or you prepare it from a past mistake in your failure log) with at least five planted defects spanning access control, escaping, SQL, task idempotency, and privacy. Find them, rank them, propose fixes.

## 11. The 100-point rubric

| Area | Points | Notes |
|---|---|---|
| Functional correctness and acceptance criteria | 15 | Install, upgrade, uninstall, all journeys |
| Moodle API correctness and conventions | 15 | Forms, output, DB API, params, strings, no core hacks, no deprecated APIs for the pinned release |
| Access control and security | 20 | Capabilities, contexts, groups, sesskey, escaping, file access |
| Testing (PHPUnit, Behat, upgrade) | 15 | Generators, denial paths, regression tests |
| Privacy, backup and data lifecycle | 8 | Provider tested; restore behavior defined |
| Design, boundaries and ADRs | 7 | Testable rules class, justified plugin type |
| Reliability and performance method | 5 | Task safety, query-count measurement, spread reported |
| Documentation | 5 | Usable by an administrator and a maintainer |
| Technical defense | 7 | Specific, honest, code-grounded |
| No-AI reconstruction/extension | 3 | Done within limits and explained |
| **Total** | **100** | Pass: 80 or more and no critical failure |

**Critical failures:** any path allowing a user to read or modify data without the right capability and context; unescaped user output; SQL built from unvalidated input; a state-changing action without sesskey protection; a modified core file; a privacy provider that is missing or untested; unable to explain code submitted as your own; claiming API behavior that is not true for the pinned release.

**If failed:** targeted remediation by weakest area (for example, a smaller standalone plugin that only does capability-gated CRUD with a denial-path test matrix, rebuilt from a blank directory), then re-defense of failed topics.

Ledger update: Capstone B to `Demonstrated` on pass; `Production-ready` only after installation on a real site, one real upgrade of core with the plugin in place, and any real defect closed with a test.
