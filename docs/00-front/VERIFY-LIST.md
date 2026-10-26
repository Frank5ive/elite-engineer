# Consolidated VERIFY list

501 markers at generation time. Check each against official docs before relying on it. Moodle items first (job-critical).

## 04-vol3-php-moodle/3.1-modern-php.md
9:| Minimum versions | PHP 8.2 (language features used: readonly properties, enums, `never`, first-class callable syntax, constructor promotion). Examples were executed on PHP 8.4.27 CLI. Composer 2.x. PHPUnit 10 or 11 (
83:- Moodle core files do **not** all use `declare(strict_types=1);`. Moodle's coding style does not mandate it (VERIFY against current coding style page before deciding for a Moodle plugin; new code in recent core uses 
103:Python comparison: Python is strongly typed at runtime (`"5" + 5` raises) but ignores type hints. PHP's declarations are **enforced by the engine** at call time (for scalar/class types) but there is no static checker
181:- **`readonly` properties** (8.1) can be initialized once, from inside the class scope, and require a type; modifying afterwards throws `Error` ("Cannot modify readonly property ..."; I ran this). `readonly` classes 
203:Case matters on Linux; a class `Submission` in `submission.php` works on macOS/Windows (case-insensitive FS) and breaks in Linux production. Moodle has its own autoloader for `classes/` (lesson 3.2), which follows a 
220:PDO is PHP's database abstraction extension. A **prepared statement** sends the SQL template and the parameter values separately: the DB parses the structure first, so values cannot change the SQL grammar. **[runtime
242:`composer.json` declares requirements and autoload rules; `composer.lock` pins exact versions (commit it for applications); `vendor/autoload.php` is the generated autoloader. Commands: `composer require [--dev] pkg`,
246:PHPUnit runs `test*` methods (or `#[Test]`-attributed ones, PHPUnit 10+) in `*Test.php` classes. Prefer `assertSame` (strict) to `assertEquals` (loose); use `expectException` and data providers (`#[DataProvider('name
275:(The PHPUnit constraint `^11.0` is an example; run `composer require --dev phpunit/phpunit` and let Composer write the constraint it resolves. VERIFY.) Then `composer dump-autoload`. Add `vendor/` to `.gitignore`.
489:Repository tests (you write them in the Project): in-memory SQLite, then a payload such as `"Robert'); DROP TABLE grades;--"` stored and read back, and `findByStudent("1 OR 1=1")` expecting `TypeError` (types stop it
495:**Correctness.** Turn on `declare(strict_types=1)`, run static analysis (PHPStan/Psalm: VERIFY team tooling), avoid `==`. In `php.ini` development: `error_reporting=E_ALL`, `display_errors=On`; production: `display_e
612:| **Quality requirements** | PSR-12-style formatting (run `phpcs`/`php-cs-fixer` if the team uses them: VERIFY, otherwise manual); each public method has a PHPDoc where types cannot express the contract (e.g., `list<
616:| **Progressive hints** | H1 (least): If autoload fails, print `get_class()` and compare with the path and case; `composer dump-autoload`. H2: Use `PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION`; `fetchAll(PDO::FETCH_A
678:P0 lesson; optional reading: PHP internals book on zvals and copy-on-write (VERIFY current URL), `opcache.preload` and JIT (measure; do not assume gains), Fibers (8.1), static analysis levels in PHPStan.
## 04-vol3-php-moodle/3.2-moodle-architecture-and-plugins.md
9:| Minimum versions | **Verified against Moodle 5.3 (LTS, released 5 October 2026; moodledev.io "main (5.3)" docs and the GitHub `main` branch, which is already 6.0dev).** Moodle 5.2 requires PHP 8.3.0+ (verified; PHP 8
14:**Reading convention for this lesson.** Every fact is labelled. **[Stable]** = a principle that has held across many Moodle versions and will probably survive. **[5.3]** = verified against official 5.3-era docs or the
62:- **Globals are the API surface.** `$CFG` (config), `$DB` (database), `$USER` (current user), `$PAGE` (page setup), `$OUTPUT` (renderer), `$COURSE`. They exist because the request is single-user, single-process. Insid
65:- **Versioning.** Each component has a `version` integer in `version.php` (format `YYYYMMDDXX`, by convention; the official page shows only placeholders: VERIFY the convention on the Plugin files page for your version
75:A component name is `<plugintype>_<pluginname>`. The type is a fixed prefix from the list Moodle defines; the name is chosen by the author. **[Stable principle]**: lowercase letters and digits; the name part must not 
86:| DB tables | `local_greetings_*` by convention | (convention; XMLDB editor enforces prefix rules: VERIFY) |
107:Subplugins live inside a parent plugin; their type is declared by the parent in `db/subplugins.json` (VERIFY on moodledev.io before using).
137:All of these file names are verified on the "Plugin files" page except `templates/` and `tests/`, which that page does not describe (the testing guide verifies `tests/*_test.php`; `templates/` is standard but VERIFY 
143:Moodle registers an autoloader. **[Stable]** A class named `\<component>\<rest>` is found in `<component directory>/classes/<rest as path>.php`, where namespace separators after the component become directory separat
146:- The autoloader **caches the class map**; after adding a new class in a *new* directory or moving classes, purge caches (`php admin/cli/purge_caches.php`) before concluding the code is wrong. VERIFY on your version 
152:`config.php` (site root, generated by the installer or copied from `config-dist.php`/a template) defines `$CFG->dbtype`, `dbhost`, `dbname`, `dbuser`, `dbpass`, `prefix`, `wwwroot`, `dataroot`, `admin`, and ends with
173:Facts verified on moodledev.io: bump the version after changing `db/access.php` (capabilities reload on upgrade) and after adding or changing `db/tasks.php`; hook registrations are cached so bump the version or purge
175:The CLI route for dev and production deployments: `php admin/cli/upgrade.php --non-interactive` (VERIFY flags with `--help`; on 5.1+ the script path may be `admin/cli/upgrade.php` at the root or under `public/`: the 
201:`<MOODLE_BRANCH>` is the branch name for your target release: use the stable branch naming from the Moodle GitHub repository (branches are named like `MOODLE_405_STABLE`; for 5.3 expect `MOODLE_503_STABLE`: VERIFY wi
228:$plugin->requires  = 2026100200;       // VERIFY: set to the $version in your core's public/version.php minimum you support
233:`$plugin` is predefined by Moodle's plugin loader (the file is included in a scope that defines it). `component` must equal the frankenstyle name or Moodle reports a mismatch. `requires` is the minimum core version n
248:`pluginname` is mandatory (verified). `{$a}` is Moodle's string placeholder, filled by `get_string('greeting', 'local_greetings', $name)`. Why strings and not literals: internationalization, and admins can override s
289:Reasoning: `config.php` first (bootstrap); `require_login()` before anything else touches user data (verified signature: `require_login($courseorid = null, $autologinguest = true, $cm = null, $setwantsurltome = true,
331:(`mtrace` is Moodle's output function for CLI/cron logging: VERIFY name in the Task API.) The file path is `classes/task/purge.php` for class `\local_greetings\task\purge` - the autoloader rule from 3.5.
381:(VERIFY both script paths and flags in your checkout; on 5.1+ some CLI scripts may live under `public/`.) Then log in as admin: Site administration -> Plugins -> Plugins overview should list "Greetings" (local plugin
387:**Maintainability.** One plugin, one repository, semantic release strings, `UPGRADING.md`-style notes for API changes you consume. Follow Moodle coding style (lesson 3.6); run `phpcs` with the Moodle standard if the 
391:**Performance.** Pages run after the whole core bootstrap; the cost is in your queries and loops. Use the DB API's recordsets and `IN` helpers (e.g. `get_in_or_equal`, verified signature), never a query in a loop wit
395:**Failure handling.** Moodle throws `moodle_exception` / `dml_exception`; do not catch broadly. For tasks, throw to mark failure so it appears in the task log and retries (VERIFY semantics in Task API).
434:- **Lab A.** The plugin is not installed cleanly: Moodle expects the component in `version.php` to match the plugin's directory-derived component (`local_greetings`); a mismatch is reported as an error during the plu
486:| **Extension challenge** | Register an event observer in `db/events.php` that logs when a course is deleted and removes that course's notes (verify the event class name in the Events API docs first; `\core\event\cou
538:Read `public/lib/classes/component.php` (component and plugin-type resolution) and trace how the plugin list is built: VERIFY the file path in your checkout. Compare `mod_choice` with a newer activity (e.g., read the
## 04-vol3-php-moodle/3.3-capabilities-contexts-roles.md
9:| Minimum versions | **Verified against Moodle 5.3 (LTS, released 5 October 2026): moodledev.io 5.3 docs and the 5.x/`main` sources on GitHub (`public/lib/accesslib.php`, `public/lib/enrollib.php`, `public/mod/choice/d
14:**Labelling.** **[Stable]** = principle that has held across Moodle versions. **[5.3]** = verified against 5.3-era docs/source in the way stated. **[VERIFY]** = not confirmed; check as written. Names of functions belo
57:(Level numbers 10, 30, 40, 50, 70, 80 verified in source. The tree position of `context_user` and `context_block` is simplified here: `context_user` is directly under system; blocks attach to the context they are disp
119:**Permission values [5.3, verified]:** `CAP_INHERIT` 0, `CAP_ALLOW` 1, `CAP_PREVENT` -1, `CAP_PROHIBIT` -1000. **Resolution [Stable, per Roles docs]:** for each of the user's roles, walk from system down to the targe
167:(`required_param_array`/`optional_param_array` exist for array inputs: VERIFY signatures; `PARAM_*` list below is verified from `moodlelib.php`.) The `$type` is a `PARAM_*` constant that both validates and cleans. Ty
244:$course = get_course($note->courseid);          // VERIFY name in the course API (widely used helper)
254:echo \html_writer::div(s($note->note));          // s(): escape for HTML output (VERIFY helper name/behavior)
264:- Output uses an escaping helper; the full output and format APIs are lesson 3.4. (`s()` is the commonly used escape helper in Moodle code: VERIFY in the output docs.)
280:if ($_SERVER['REQUEST_METHOD'] !== 'POST') {              // VERIFY: Moodle may offer a helper; a form is better
281:    throw new \moodle_exception('invalidrequest');       // VERIFY: string key exists; else use another error string
289:Points: order matches the pipeline; deletion deletes the **loaded** note's id; `delete_records` signature `($table, array $conditions = null)` verified (mind: passing an empty conditions array deletes all rows; alway
314:        $gen->enrol_user($teacherA->id, $courseA->id, 'editingteacher');   // role-shortname argument: VERIFY
374:Test design notes: (1) Users are enrolled only in course A; the note is in course B: the capability exists in A but not in B, so denial proves the *context* is derived from the note. (2) A student in the right course
378:**Correctness.** Authorization is a function of (user, action, object). Tests must vary all three. Cache effects: capability checks are cached per request; changes in the same request in tests may need `accesslib_cle
382:**Security.** Defense in depth: capability + sesskey + parameter typing + output escaping + prepared queries through `$DB`. Log denied attempts? Moodle logs events, not denials by default (VERIFY); for sensitive data
392:**Diagnosing "permission denied" for a legitimate user.** (1) What context was checked? Print `$context->contextlevel` and id. (2) Role assignments: Site administration -> Users -> Permissions -> "Check permissions" 
426:- **Lab C.** Expected answer: **no**. The docs state "Prohibit always wins" (verified): a Prohibit reached by any of the user's roles on the path to the context denies the capability, even though the `editingteacher`
## 04-vol3-php-moodle/3.4-forms-output-database-api.md
14:Version discipline for this lesson. Moodle's *principles* (never trust input, escape on output, parameterise SQL, check capability, use the DB abstraction, keep strings out of code) have been stable for over a decade.
16:Directory layout note (`VERIFY`): from Moodle 5.1 onward the web-accessible code is served from a `public/` subdirectory, and the developer documentation for PHPUnit already shows `php public/admin/tool/phpunit/cli/in
84:What: every value from outside the process (query string, POST body, form submission) is untrusted text. A `PARAM_*` constant is a *declared type* with a cleaning function behind it. `required_param($name, $type)` fet
88:How it behaves internally: `clean_param($param, $type)` applies a type-specific transformation (for example `PARAM_INT` casts to integer; `PARAM_ALPHANUMEXT` strips every character except letters, digits, underscore a
146:Passing data into the form constructor: `new item_form($url, ['courseid' => $courseid, 'id' => $id])`; inside, `$this->_customdata['courseid']`. (`VERIFY:` the `_customdata` property name in `lib/formslib.php`.) Hidd
153:- `$PAGE` is the `moodle_page` instance describing the page being built: `set_url`, `set_title`, `set_heading`, `set_context` (and layout, which the page I fetched did not cover; `VERIFY:` `$PAGE->set_pagelayout('sta
158:- `render_from_template('component/name', $context)` renders a Mustache template directly. Templates live in the plugin's `templates/` folder as `name.mustache` (the page I fetched did not state the folder; this is e
162:Language strings: `get_string('identifier', 'component', $a)`. Strings live in `lang/en/<component>.php` as `$string['identifier'] = '...';`. The coding-style page requires that strings are complete sentences (no con
193:Portability. Moodle supports several database engines and the set changes between releases. `VERIFY:` read the "Moodle requirements" for your exact release in Site administration > Server > Environment, or docs.moodl
201:Verified `version.php` fields (docs main/5.3): `component` (required, frankenstyle), `version` (YYYYMMDDXX integer, must increase), `requires` (minimum core version, recommended), `supported` (since 3.9, lowest and h
203:Verified DDL methods (docs): `$dbman = $DB->get_manager();` then `table_exists`, `create_table`, `field_exists`, `add_field`, `drop_field`, `index_exists`, `add_index`, `change_field_*`, `rename_field`. Objects: `new
258:$plugin->requires  = 2025041400;      // VERIFY: replace with the $version from your target Moodle's version.php.
293:Design choices: plain integer timestamps (`timecreated`, `timemodified`) are the Moodle convention; `char` for bounded text and `text` for unbounded (`VERIFY:` the 1333 length for URLs: it is a convention used in cor
382:Review notes you should be able to give: the search term uses a named placeholder and `sql_like_escape` so `%` and `_` typed by the user are literals; `sql_like` with `casesensitive = false, accentsensitive = false` 
442:            $errors['status'] = get_string('invaliddata', 'error');   // VERIFY: string key exists in your version.
455:require(__DIR__ . '/../../config.php');   // VERIFY: depth on 5.1+ where plugins live under public/.
510:Reasons, in order: `require_login` before anything; capability before input is acted on; `$PAGE` set before `header()`; the id read from the request is *re-checked* against the course because `PARAM_INT` only guarant
549:Mechanism: the object is loaded first, and the capability is checked in the *item's own course context* (not a context supplied by the request). `$OUTPUT->confirm()` builds POST buttons; `VERIFY:` that your version a
695:and bump `$plugin->version = 2026102601;` in `version.php`. The `field_exists` guard makes the step safe to rerun after a partial failure. Run upgrades with the admin UI or `php admin/cli/upgrade.php` (`VERIFY:` the 
705:Security: see 3.7. Add `defined('MOODLE_INTERNAL') || die();` to non-entry PHP files that could otherwise be executed directly (the coding-style page requires it for non-class scripts with side effects; class files i
798:| 3 | Requirements | R1 Create, read (list with search), update, delete items with title, URL, note, status. R2 Capabilities `view` and `manage` declared in `db/access.php` (designed per 3.3) and enforced on every sc
803:| 8 | Deliverables | Plugin directory as a git repository with at least 8 meaningful commits; `README.md` for the plugin (install steps, capabilities, URL); a short `NOTES.md` listing every `VERIFY:` you resolved, ho
806:| 11 | Progressive hints | H1: Start from the tables, not the pages: write install.xml with the XMLDB editor, install, then check the table exists. H2: Write the repository class and prove each method works from a th
807:| 12 | Evaluation rubric (100) | Correct CRUD behaviour on A1-A10: 30. Security (cleaning, escaping once, sesskey, capability, IDOR): 25. DB design and `$DB` usage (placeholders, portability, upgrade): 15. Output API
809:| 14 | Reflection questions | Which of your `VERIFY:` resolutions surprised you? Where did you first put authorisation logic and why did you move it? What would break first if the site changed from MariaDB to Postgre
830:Pass = 80/100 on the project rubric with no critical failure. Required evidence: the plugin repository, the `NOTES.md` with resolved `VERIFY` items and tested Moodle version, the A1-A10 demonstration log, and a 10-mi
853:- Moodle Developer Resources, Forms API: https://moodledev.io/docs/5.3/apis/subsystems/form (moodleform structure, element types, is_cancelled/get_data pattern). `VERIFY:` the exact docs path version segment if it mo
## 04-vol3-php-moodle/3.5-events-tasks-webservices-files-privacy.md
9:| Minimum versions | PHP 8.2. Moodle: **API names checked against moodledev.io docs for main/5.3 (5.3 "current stable, LTS", released 5 October 2026 per moodledev.io/general/releases, read 2026-10-26)**. Items marked `
16:Layout note: on Moodle 5.1+ plugins are placed under `public/` (`VERIFY:` as in 3.4).
53:Class shape (names from the Events API documentation; the documentation page I could read is the archived docs.moodle.org/dev page, last edited 2021, and notes itself as stale, so treat the details as `VERIFY:` agains
90:Rules from the documentation: the class name encodes `object_action`; `objecttable` is required when `objectid` is used; the description should begin with the user id in quotes; `other` must be JSON-serialisable and s
114:`VERIFY:` an `observer` class under `classes/` named in the callback string, and the exact event object type hint. Documented behaviour you must design for: `internal` defaults to true, meaning the observer runs imme
139:`db/tasks.php` (documented keys: `classname`, `blocking`, `minute`, `hour`, `day`, `month`, `dayofweek`; `R` picks a random value; `blocking` is documented as `0` in the example and blocking support was removed in 4.
170:Design rules (principles): tasks must be idempotent (retries and double execution will happen), must record progress in the database not in memory, must handle partial failure, must emit output with `mtrace()` for th
218:            'title' => \core_external\util::format_string($i->title, $context),  // VERIFY: helper name in your version
235:The documented example uses the method names `execute_parameters`, `execute`, `execute_returns`, the `core_external\...` namespace, `self::validate_parameters`, `self::validate_context` and `require_capability`. The 
241:Backward compatibility for services: a published function is a public API. Never rename it, change a parameter's type, make an optional parameter required, remove or retype a returned field. Add optional parameters a
243:Enabling a service for testing: site admin enables web services and creates a token (Site administration > Server > Web services). `VERIFY:` the current menu path for your version.
287:Serving: Moodle calls `<component>_pluginfile($course, $cm, $context, $filearea, $args, $forcedownload, array $options = [])` in your `lib.php`. It must return `false` when the file is not found and must call `send_s
315:Uploading through forms uses `filemanager`/`filepicker` form elements and helper functions to move files from the user's draft area. The helper names (`file_prepare_standard_filemanager`, `file_postupdate_standard_fi
317:Security principles: a pluginfile URL is guessable; the callback is the only gate. Always check the object, not just the context. Never serve files by path from the filesystem. Delete files when the owning record is 
416:The interface names, `add_database_table`, `add_subsystem_link`, `contextlist::add_from_sql`, `userlist::add_from_sql`, `writer::with_context`, `get_in_or_equal` and the method list come from the Privacy API page for
424:Principles (stable): published identifiers are contracts: event class names and their data fields, web service names, parameters and returns, capability names, language string keys that other plugins use, database co
436:Step 4: adhoc task. Add a nullable `reminded` timestamp to items via an upgrade step (3.4 pattern). The scheduled task `send_reminders` selects courses with unread items older than 7 days and queues `notify_course::i
438:Step 5: web service. `local_readinglist_list_items` as in 3.3. Naive version: reading `$courseid` straight from the arguments and querying. Improved: `validate_parameters`, `validate_context`, `require_capability`, r
458:Testing: event observed via an event sink in PHPUnit (`$sink = $this->redirectEvents()`, `VERIFY:` method name in your version's `advanced_testcase`); tasks tested by calling `execute()` directly; privacy via `provid
527:No hints beyond moodledev.io. Evidence: green tests (3.6 shows how to run them) and a table listing every file and the Moodle API it uses, with each `VERIFY` resolved.
538:| 4 | Constraints | No core changes. No new third-party libraries. Backward compatible: v1 URLs keep working. Mode B. PHP 8.2+. Each `VERIFY` item you use must be resolved in `NOTES.md` with source and Moodle version
542:| 8 | Deliverables | Updated plugin repository, `NOTES.md` with VERIFY resolutions and tested Moodle version, a sequence diagram (Mermaid) of the delete flow including event, observer and cache, and a table of public
545:| 11 | Progressive hints | H1: Do one mechanism at a time; commit after each, with a version bump. H2: For the observer, first log the event class and `objectid` with `debugging()` or `mtrace()` in a dev copy to prov
556:Pass = 80/100, no critical failure. Evidence: repository, tests output (or manual scripts), NOTES.md with VERIFY resolutions, contract table, diagram, 10-minute defence. Critical failures: a service function lacking 
## 04-vol3-php-moodle/3.6-testing-style-upgrades.md
9:| Minimum versions | PHP 8.2. Moodle: **docs verified for main/5.3 (5.3 "current stable, LTS", 5 Oct 2026, moodledev.io/general/releases, read 2026-10-26)**. PHPUnit: the docs state Moodle 5.0 uses PHPUnit 11.4 and Moo
59:- PHPUnit is a Composer dependency, not part of Moodle: run `php composer.phar install` in the Moodle root (or `composer install`; `VERIFY:` the exact incantation in the page for dev dependencies).
69:- Messages and email: `preventResetByRollback()` then `redirectMessages()`; unset `noemailever` then `redirectEmails()`. Not verified in the page I read but used in core and plausible for events: `redirectEvents()`; `
110:Notes: `@covers` here is the pre-5.0 style (keep it only if you support 4.5; on 5.0+ the documentation says to use attributes, `VERIFY:` whether both are accepted); the test names state the behaviour; arrange, act, a
131:`enrol_user($userid, $courseid, $roleidorshortname)`: the third argument accepting a shortname is how core tests do it; `VERIFY:` in `lib/testing/generator/data_generator.php`. This test depends on the capability def
133:Event test (sink name `VERIFY`):
145:External function test: call `list_items::execute($course->id)` after `setUser($student)`, compare with `\core_external\external_api::clean_returnvalue(list_items::execute_returns(), $result)` (that helper exists in 
147:Privacy test: extend `provider_testcase`; create two users, items; use `provider::get_contexts_for_userid($user->id)`, then export with `approved_contextlist` and read the writer with `writer::with_context($context)`
149:Cache pitfalls in tests: caches may be warm; call `\cache_helper::purge_all()` (`VERIFY:`) or use `\cache::make(...)->purge()` in setup of cache-sensitive tests. Test that the invalidation exists by reading, editing,
151:Time: tests that depend on `time()` are flaky; compare relative timestamps with a tolerance or inject time. `VERIFY:` presence of a clock mock (`mock_clock_with_frozen()` in `\advanced_testcase`) in 5.3 docs before r
171:Use: `$this->getDataGenerator()->get_plugin_generator('local_readinglist')->create_item(['courseid' => $c->id])`. The class-naming convention for plugin generators is `<component>_generator` in the file `tests/genera
175:Documented: Behat features are Given/When/Then scenarios in a component's `tests/behat/` folder; tests run against a separate Behat site configured with `$CFG->behat_wwwroot`, `$CFG->behat_prefix`, `$CFG->behat_datar
177:Scenario skeleton (step wording follows long-standing Moodle conventions; `VERIFY:` exact step phrasing in `lib/tests/behat/` of your version, especially the "following ... exist" generator step and the `Given I log 
201:    And I am on the "C1" "Course" page   # VERIFY: page-resolver step syntax in your version
212:Rules: generate state with generator steps, not by clicking; one journey per scenario; no sleeps (Moodle steps wait); tag with the component. Decide Behat versus PHPUnit by asking "does a user-visible interaction (JS
218:Checking: moodle-plugin-ci (maintained by Moodle HQ) runs, per its documentation, PHPUnit, Behat, Moodle Code Checker (phpcs with the Moodle standard), Moodle PHPdoc check, Mustache linting, Grunt tasks, PHP Parallel
232:Run style before pushing; do not argue with the standard; never add `// phpcs:ignore` to hide a violation without an explicit justification comment and a reviewer agreeing. Fix violations by editing code. A style fai
240:Version scheme: `YYYYMMDDXX`; on a stable branch keep the date and increment `XX` (documented). `requires` and `supported` are compatibility declarations; set them from what you tested, not what you hope (`VERIFY:` `
242:Core upgrade cadence: Moodle ships major versions every six months (4.5 LTS Oct 2024, 5.1 Oct 2025, 5.2 Apr 2026, 5.3 LTS Oct 2026 per the releases page). Support table from the same page: 4.5 LTS security until 4 Oc
244:Backward compatibility checklist when releasing: identifiers published to others (events, services, capabilities, strings, DB columns, settings keys, file areas) unchanged or deprecated; database changes additive; a 
259:`VERIFY:` on the Moodle docs "Debugging" page that these lines are still the current recommendation for 5.x; use them only on dev and staging, never in production because it discloses internals and paths. Other docum
261:Xdebug (php.net/xdebug docs; Xdebug 3 settings): `xdebug.mode=debug`, `xdebug.start_with_request=trigger` or `yes`, `xdebug.client_host`, `xdebug.client_port` (Xdebug 3 default 9003), IDE path mappings from the web r
269:Version and metadata; style and static checks green; tests green on every supported Moodle/PHP/DB combination you claim; Behat journey green; upgrade from previous release and from the oldest supported release tested
297:Correctness: test across database engines you claim to support; the DB differences described in 3.4 (case sensitivity, empty string versus null) show up here first. Do not claim portability on one engine's evidence. 
305:Operations: upgrade in maintenance mode with a backup; read upgrade notes; run `php admin/cli/upgrade.php` (path under `public/` on 5.1+, `VERIFY:`) on staging first. Provide an administrator-facing upgrade note list
352:1: the documentation lists `resetAfterTest` in a shared `setUp()` as banned; it hides which test modified data and resets after tests that did not need it. Call it in the test that changes data. 2 and 3: test order d
396:| 4 | Constraints | No core modifications. No suppressed style errors unless justified in writing. Tests must pass in any order and alone. Every `VERIFY` item you rely on must be resolved in NOTES.md. Mode B. |
400:| 8 | Deliverables | Repository with tests, CI config, upgrade code, CHANGES, README, release tag; NOTES.md with VERIFY resolutions and measured suite runtimes; debugging report (symptom, hypotheses, evidence, root c
404:| 12 | Evaluation rubric (100) | Test quality and coverage of contracts: 25. Negative/security tests and red-then-green proof: 10. Style and static checks clean without suppression: 10. CI configuration correct and g
412:Checklist: can each test fail (you saw it fail)? Does each test have exactly one reason to fail? Is state created by generators? Is time, cache and order handled? Are negative cases included? Zero suppressed style vi
434:P2: study how core organises `tests/behat` contexts and `lib/tests/behat` step definitions; read `lib/phpunit/classes/advanced_testcase.php` for the full helper list (do not copy, learn what exists); investigate cove
## 01-vol0-job-readiness/0.1-day-one-protocol.md
9:| Minimum versions | Python 3.12 (for `repo_map.py`), Git 2.28+, PHP 8.2 (reading only), any recent pytest. Framework facts are labelled with a version where I am confident, and `VERIFY:` where you must check. |
75:A baseline turns "the tests fail" from an accusation into a dated fact, and tells you the feedback-loop length. pytest selection flags (check `pytest --version`): `--collect-only -q` lists tests; `path::test_name` run
110:In the classic layout a plugin page such as `/local/hello/index.php` is a PHP file executed directly by the web server; there is no single front controller. `ASSUMPTION:` Moodle 4.x. Moodle 5.1 moved web-served code 
130:Other entry paths may host the bug instead of a page: AJAX/external functions (`db/services.php`), scheduled and ad hoc tasks (`db/tasks.php`, `classes/task/`), event observers (`db/events.php`), CLI scripts (`admin/
134:Behaviour changes without code changes; configuration is the usual cause of "works on my machine" and the usual place secrets leak. Python/FastAPI sources: `os.environ["X"]` (KeyError if unset), `os.environ.get`, `os
156:You are given a small FastAPI service. This worked example is a **walkthrough on code I wrote for this lesson**; I did not execute it in the authoring environment (FastAPI was not installed there), so treat it as an 
263:Header naming: FastAPI converts the parameter `x_api_token` to the header `x-api-token` (underscores become hyphens) by default; HTTP header names are case-insensitive. This is documented FastAPI behaviour; `VERIFY` 
330:- **Observability:** find where logs go and how to raise verbosity locally (uvicorn has `--log-level`; application loggers are configured by the project: `grep -rn logging`). Moodle debugging is controlled by `$CFG->
343:| Moodle change invisible | Old output persists | Caches; `php admin/cli/purge_caches.php` (`VERIFY` on your version) |
430:| 2. Context | Monday: your employer's repository. Before Monday, practise on public repositories. `ASSUMPTION:` Moodle core (`VERIFY:` official URL on moodle.org/dev; a GitHub mirror exists under `github.com/moodle`
496:Rebuild the Python scanner with the `ast` module and compare which false positives disappear and which failure modes (syntax errors, version-specific grammar) appear; measure rather than assume. Read "Working Effecti
## 01-vol0-job-readiness/0.2-git-workflow.md
9:| Minimum versions | Git 2.28+ (`git init -b`); `git switch`/`git restore` need 2.23+; `zdiff3` conflict style needs about 2.35 (`VERIFY:` `git --version`). Labs were run with Git 2.47.3. Bash for the lab scripts. |
14:Assumption notice. Your employer's branching model, commit style, merge strategy, and review tool are unknown. This lesson teaches the mechanics every model shares, then how to discover and follow local conventions (3
126:Setting `git config merge.conflictStyle zdiff3` (newer Git; `diff3` on older versions, `VERIFY` your version) additionally shows the common ancestor in the markers, which often makes the intent obvious. It changes yo
157:The reflog keeps entries for a limited time (defaults are about 90 days for reachable entries and 30 days for unreachable ones; `VERIFY:` `gc.reflogExpire` and `gc.reflogExpireUnreachable` in `git help gc`). It is lo
415:| 13. Extension challenge | A drill for `git rebase --onto` (branch created from the wrong base), and one for a dropped stash (`git fsck --unreachable`; `VERIFY` the procedure). |
422:Checklist: every destructive command has a safety net; every "recoverable" claim was demonstrated, not assumed; scripts never reach outside the lab directory (run one from a different working directory and from a pat
459:- git-scm.com/docs/git-config, `merge.conflictStyle` and `rerere.enabled`: conflict markers and reuse of resolutions (`VERIFY` availability).
461:- `git help gc`, reflog expiry settings: how long recovery windows last (`VERIFY` defaults).
## 01-vol0-job-readiness/0.3-debugging-and-failure-log.md
92:Chained exceptions: "The above exception was the direct cause of the following exception" means `raise X from Y`; "During handling of the above exception, another exception occurred" means an error inside an `except` 
94:FastAPI: an unhandled exception in an endpoint becomes a generic HTTP 500; the traceback is in the **server** log (first question: where do logs go? Lesson 0.1). `HTTPException` is a deliberate response, not a crash. 
107:| Test order / shared state | Module-level state, mutable defaults, caches, leftover database rows | Run the test alone, then after its predecessors; reverse or randomise order if your runner supports it (`VERIFY`) |
145:- **Never log** passwords, tokens, keys, full personal data (names with grades, emails), or payment details. In Moodle the privacy implications are real (`VERIFY:` your organisation's policy).
149:`breakpoint()` (Python 3.7+) opens `pdb` at that line; `python -m pdb script.py`; `pytest --pdb` stops at failures (`VERIFY` your version). Debuggers are best for state you do not yet know to ask about; logs are best
379:- **Security.** Logs are an attack surface and a privacy liability. Never log secrets; truncate or hash identifiers where policy requires; keep debug display off in production (Moodle: `$CFG->debugdisplay`; `VERIFY` 
509:- Zeller, "Why Programs Fail" (book): systematic debugging and delta debugging. `VERIFY:` edition details before citing; read for the formal version of Section 3.3.
513:Property-based testing (the `hypothesis` library, a third-party dependency, so only with team agreement) automates input shrinking in a way similar to `halve`. Read about deterministic simulation and record-and-repla
## 01-vol0-job-readiness/0.4-communication.md
424:- Atlassian or GitHub documentation on writing pull request descriptions and templates (docs.github.com, "About pull requests" and "Creating a pull request template"): read for the mechanics of templates in your host
431:Blameless postmortem writing (Lesson 7.2), estimation under uncertainty (read about reference-class forecasting and use your failure log as the reference class), and written communication in remote teams. `VERIFY:` a
## 02-vol1-python/1.1-object-model.md
228:`tuple`: fixed record, hashable if its elements are. `list`: growable ordered sequence (amortised O(1) append, O(n) membership and front insertion). `dict`: key lookup, average O(1), insertion-ordered since 3.7 (lang
266:(CPython implementation detail; PyPy and others differ. Free-threaded builds of 3.13 change internals; VERIFY with `python3 -VV` and the docs for your interpreter.)
420:Vocabulary only, before Lessons 2.6 and 4.4. **GIL**: in the standard CPython build one thread runs Python bytecode at a time, so threads help I/O-bound work, not CPU-bound Python (3.13 has an experimental free-threa
516:| **Quality requirements** | Docstrings stating mutation and thread-safety behavior. Tests named for behavior. Each test makes one assertion-worthy claim. No test depends on another's side effects (check by running t
## 02-vol1-python/1.2-iterators-generators-context-managers-exceptions.md
259:6. **Never** write bare `except:` (catches `KeyboardInterrupt`/`SystemExit`), `except Exception: pass`, or `return` in `finally` (it silently discards the in-flight exception; Python 3.14 emits a warning for this, PE
567:| **Progressive hints** | Hint 1: Write the failure-semantics table first; each row becomes a test. Hint 2: Make each stage a function from iterable to iterator; compose them in `run`, and keep `run` short. Hint 3: F
## 02-vol1-python/1.3-types-packaging-config-logging.md
40:This is *gradual typing*: you can type part of a codebase. `mypy --strict` turns on the strictest practical set (no untyped defs, no implicit `Any`, no unused ignores, and more: VERIFY the exact flag set with `mypy --
98:- **`TYPE_CHECKING`** guards imports needed only for hints and can break import cycles; `from __future__ import annotations` makes annotations lazy strings (Pydantic and dataclasses have rules about that: VERIFY in th
407:- Intentionally small: `structlog` or `python-json-logger` exist; choosing one is a team decision (VERIFY maintenance status). Understand the stdlib mechanics first.
416:**Security.** Env vars are the *delivery mechanism*, not a vault: same-user processes and crash reporters can read them (`/proc/<pid>/environ`). Supply chain: pin, review, use hashes, run an audit tool such as `pip-a
594:- PEP 735 (dependency groups) and PEP 751 (lock file format): compare with your tool's lockfile (VERIFY current status).
## 02-vol1-python/1.4-pytest-fixtures-mocking.md
65:- Useful flags: `-x`, `-k expr`, `-q`, `-ra`, `--lf`, `-s`, `--tb=short`, `--pdb` (VERIFY with `pytest --help`).
145:| Current time | Inject a `Clock` (Lessons 1.1, 1.3); never `sleep` in tests. Time-travel libraries such as freezegun exist (VERIFY maintenance and compatibility before adopting); injection is the dependency-free def
147:| Test order | No shared mutable state; function-scoped fixtures; run the suite in random or reverse order periodically (a plugin such as pytest-randomly exists: VERIFY before adding a dependency to a team repo) |
199:3. Cover branches: run coverage (`pytest --cov` needs the pytest-cov plugin; VERIFY) and add inputs until the branches you intend to change are exercised.
436:**Suite speed.** Measure with `pytest --durations=10`; parallelize only after tests are order-independent (VERIFY pytest-xdist).
564:| **Constraints** | Python 3.12+; dev dependencies limited to pytest and hypothesis (coverage plugin allowed if you VERIFY and document it). No `time.sleep` in tests. No test may depend on another. Do not change the 
565:| **Acceptance criteria** | Suite passes in normal, reversed (`pytest` with the file order reversed by naming or explicit paths) and single-test order. Each of the two bug-fix tests fails on the pre-fix commit (evide
664:- Michael Feathers, "Working Effectively with Legacy Code" (book): characterization tests and seams; read the chapters on seams and characterization testing (VERIFY chapter numbers in your edition).
668:- Mutation testing tools (for example mutmut or cosmic-ray: VERIFY maintenance status) to automate the hand mutation check.
## 03-vol2-fastapi-backend/2.1-http-rest-contracts.md
70:2. **Idempotency is a property of the semantics you implement, not the verb you pick.** A `PUT` that appends to a list violates the contract and breaks retry libraries. You can make a POST retry-safe with an idempoten
140:A contract states paths, methods, parameters, bodies, responses (including errors), auth, and semantics. **OpenAPI** (3.1 aligns its schema dialect with JSON Schema 2020-12) is the standard format; FastAPI generates 
144:Versioning: URI (`/v1`: visible, simple routing), header or media type (clean URLs, harder to test), or additive-only evolution with deprecation signals (`Deprecation` and `Sunset` headers; VERIFY their RFC numbers b
## 03-vol2-fastapi-backend/2.2-fastapi-lifecycle-pydantic-di.md
9:| Minimum versions | Python 3.12; FastAPI, Pydantic 2.x, Starlette, Uvicorn, pytest. Verified here with FastAPI 0.162.0, Pydantic 2.14.1, Starlette 1.10.0, Uvicorn 0.54.0, pytest 9.1.1. VERIFY your versions with `pip l
48:Process model: `uvicorn app.main:app` runs one process with one event loop. For multiple CPU cores you run multiple worker processes (Uvicorn `--workers`, or a process manager such as Gunicorn with Uvicorn workers; VE
97:- **Lax mode (default) coerces.** `"4"` becomes `4` for an `int` field. In lax mode Python-side validation also accepts `True` for an `int` field and gives `1` (observed in this lesson's testing). Use `Field(strict=Tr
131:`APIRouter(prefix=..., tags=[...])` groups related operations; `app.include_router(router)` mounts it. Suggested layout: `app/main.py` (assemble), `app/routers/` (HTTP layer), `app/schemas.py` (Pydantic), `app/deps.p
265:Choices: we return only `loc`, `msg`, `type` from validation errors (Pydantic's error dict can include `input` and `ctx`, which may echo user data back; omitting them is a deliberate security/privacy decision, review
498:4. Add a catch-all `Exception` handler returning 500 problem+json with no internals, and a test that proves a deliberately raised `RuntimeError("secret")` does not leak "secret". VERIFY: with `TestClient`, unhandled 
512:| Requirements | 1. Resource `/bookmarks`: create (201 + Location), list (paginated envelope, `tag` filter, `q` substring search on title, enforced limit max 100), read, replace (PUT), patch (PATCH with correct omitt
516:| Quality requirements | Type hints everywhere; `ruff check` clean if your team uses ruff (VERIFY the team's tool, do not introduce one unprompted); no business logic in routers beyond orchestration; no global mutabl
541:Pass = 80/100 and no critical failure. Evidence: repository link or archive; `pytest` output with random order (for example `pytest -p randomly`, VERIFY plugin name) or three runs in different orders; the committed `
## 03-vol2-fastapi-backend/2.3-sql-schema-indexes-explain.md
9:| Minimum versions | PostgreSQL 15+ (all queries and plans below were run on PostgreSQL 18.6 in the `postgres:18-alpine` image). MySQL 8.0+/MariaDB 10.5+ differences are noted and marked VERIFY. SQLite 3.25+ for window
113:- `WHERE submitted_at > '2025-10-01'` alone on that composite index: a `Bitmap Index Scan` using the composite index (the second column). I had expected a sequential scan from the leading-prefix rule. PostgreSQL 18 a
121:Workflow: (1) capture the real slow query with its parameters (from a slow query log, `pg_stat_statements`, or the APM; VERIFY availability on your setup); (2) `EXPLAIN (ANALYZE, BUFFERS)` on production-shaped data; 
125:Moodle supports PostgreSQL, MariaDB and MySQL (VERIFY the supported versions for your Moodle release at moodledev.io before relying on any of this). Differences that bite:
128:- **No partial indexes**; functional indexes exist in MySQL 8.0.13+ (VERIFY); MariaDB has virtual columns that can be indexed.
132:- **Window functions and CTEs**: MySQL 8.0+, MariaDB 10.2+ (windows) and 10.2+ (CTEs). Older installations lack them (VERIFY).
133:- **Plan tools**: MySQL 8.0 has `EXPLAIN ANALYZE` (since 8.0.18; VERIFY) and `EXPLAIN FORMAT=TREE`; MariaDB uses `ANALYZE <statement>` and `EXPLAIN`. Output formats differ from PostgreSQL's, but the reading skill (ro
135:- **Moodle specifics**: tables are prefixed (default `mdl_`), and Moodle code uses its own database abstraction (`$DB`, Lesson 3.4) and XMLDB schema definitions rather than raw SQL, so portability is handled for you 
247:**Performance.** Index for the queries you have, not those you imagine. For each index record: the query it serves, the plan before/after, the write cost. Remove indexes that no query uses (`pg_stat_user_indexes` sho
251:**Operations.** Index creation on a large table locks writes unless you use `CREATE INDEX CONCURRENTLY` (PostgreSQL; cannot run inside a transaction block; VERIFY details in the docs); it takes longer but avoids bloc
253:**Observability.** Slow query logging (`log_min_duration_statement`) and `pg_stat_statements` identify the top offenders by total time, not just single slow calls (VERIFY extension availability). Track queries per re
331:| Requirements | 1. `schema.sql` in 3NF with PKs, FKs (with chosen ON DELETE per relationship), unique, not null and check constraints (score range, status enums, due date after open date). 2. `seed.sql` or a Python 
340:| Evaluation rubric (100) | Schema correctness and constraint completeness 20; query correctness incl. NULL/zero handling 20; measurement discipline (before/after, estimate vs actual) 25; index selection and rejected
363:Critical failures: an index justified by intuition rather than a recorded plan; a LEFT JOIN silently turned inner in a delivered query; string-concatenated SQL; missing FK or PK in the core entities; a reported speed
## 03-vol2-fastapi-backend/2.4-transactions-migrations-pagination.md
34:7. State, for a given change, what lock a migration takes and whether it is safe on a large live table, citing PostgreSQL documentation (VERIFY) rather than memory.
65:The SQL standard's table differs from PostgreSQL's implementation (for example, PostgreSQL's REPEATABLE READ is snapshot isolation). MySQL/InnoDB's default is REPEATABLE READ with different locking behaviour (gap lock
80:Transaction A locks row 1 then wants row 2; B locks row 2 then wants row 1. Neither can proceed. PostgreSQL detects the cycle (after `deadlock_timeout`, default 1s; VERIFY) and aborts one with `DeadlockDetected` (SQLS
122:Lock facts to look up before any DDL on a big table (PostgreSQL docs "Explicit Locking" and `ALTER TABLE` notes; VERIFY for your version, since improvements land often): adding a column with a constant default has be
136:The row-value comparison with a matching composite index `(submitted_at DESC, id DESC)` gives a bounded index range scan (verified plan: `Index Only Scan` with `Index Cond: ROW(submitted_at, id) < ROW(...)`, no sort)
335:Be honest about what this does *not* do: Alembic runs the whole migration in one transaction by default on PostgreSQL, so these batches are not separately committed, and locks and WAL accumulate for the full run. For
384:**Performance.** Hold transactions open as briefly as possible; no network calls, no `sleep`, no user waiting inside. Long transactions block vacuum and bloat tables, and keep locks. Keep connection pool size in mind
401:| Autogenerate applied unreviewed | Dropped tables, dropped columns (rename seen as drop+add) | Read the generated file before running; run `alembic upgrade --sql` to see SQL (VERIFY option) |
473:| Requirements | 1. Schema (SQLAlchemy 2.x models) with constraints: unique `(event_id, seat_label)`, `bookings` with unique `(seat_id)` as the last line of defence, check constraints, FKs. 2. `book(event_id, seat_la
481:| Progressive hints | 1: Write the invariants as sentences first ("a seat has at most one booking"); then map each to the cheapest mechanism. 2: A unique constraint plus catching `IntegrityError` is often the simples
529:- Online schema change tools for MySQL (gh-ost, pt-online-schema-change) for Moodle-era deployments; VERIFY current maintenance status.
## 03-vol2-fastapi-backend/2.5-authn-authz-passwords-secrets.md
28:The user was authenticated (the token was valid). Nobody asked whether *this* user may see *this* row. That is **broken object-level authorization** (BOLA, also called IDOR), and it is the top item in the OWASP API Se
86:- **Argon2id**: winner of the Password Hashing Competition; the usual recommendation today (OWASP Password Storage Cheat Sheet lists Argon2id first; VERIFY current parameters there).
92:Skip composition rules. Enforce a minimum length (NIST SP 800-63B: at least 8; many teams choose 12+; VERIFY), reject known-breached passwords where feasible, and cap the maximum (e.g. 128) to bound hashing cost (unbo
146:What your **backend** typically does: it is the *resource server*. It verifies bearer access tokens from the identity provider: fetch the provider's public keys (JWKS), cache them, verify signature/`iss`/`aud`/`exp`,
313:I ran the full set (10 tests) green. `TestClient` emitted a Starlette deprecation warning about `httpx` in my environment (see VERIFY below).
347:| Secret in repo | `git log -S` ; a scanner such as gitleaks (VERIFY usage at github.com/gitleaks/gitleaks); rotate, then purge |
## 03-vol2-fastapi-backend/2.6-async-background-jobs-idempotency.md
62:| `def` endpoint/dependency | in a threadpool worker thread | May block, but each blocked call consumes a pool thread; the pool is finite (AnyIO's default limiter is 40 threads; VERIFY in the AnyIO docs for your versi
66:**Mixing.** From async code, call blocking code via `await anyio.to_thread.run_sync(fn, *args)` or `await asyncio.to_thread(fn, *args)`. From threads, you cannot `await`; use `anyio.from_thread.run`. For CPU-heavy wor
72:Without a timeout, a dead dependency holds your resources forever; slow failures consume every worker. Every network call needs a **bound**. For `httpx`, the default is a 5 second timeout (framework behavior; VERIFY i
92:An operation is **idempotent** if performing it N times has the same effect as once. `PUT /users/7 {…}` and `DELETE /users/7` are idempotent by definition of the method; `POST /payments` is not. Make it so with an *
114:| arq | asyncio-native Redis queue | Async codebases wanting light weight | Smaller ecosystem; check maintenance status before adopting (VERIFY at github.com/python-arq/arq) |
235:Design choices: `sleep` and `rng` are injected so tests are instant and deterministic (1.4); only transient exceptions are retried, so 4xx propagates at once. `httpx.TimeoutException` is a subclass of `httpx.Transpor
320:I ran the three tests green, three times in a row. Honest caveats: SQLite serializes writers, so this proves the *logic*; on PostgreSQL the duplicate waits on the unique index entry of the uncommitted first transacti
344:| `requests`/`time.sleep`/sync ORM in `async def` | Latency spikes and failing health checks with idle CPU. Run a lag monitor task (sleep 100 ms, log overshoot); enable asyncio debug mode (`PYTHONASYNCIODEBUG=1`), wh
400:3. Find the blocker: `py-spy dump --pid <pid>` shows the stack of the main thread (VERIFY tool installation); or run with asyncio debug.
## 03-vol2-fastapi-backend/2.7-observability-deploy-reliability.md
9:| Minimum versions | Python 3.12, FastAPI 0.115+ (checked on 0.162.0), Starlette (checked on 1.10.0), uvicorn (checked on 0.54.0), prometheus-client, pydantic-settings 2.x, Docker 24+ (VERIFY on your machine) |
63:- Python's `logging` is global and thread-safe; use `contextvars.ContextVar` for the request id so concurrent requests on one event loop (and the threadpool, since contextvars propagate through AnyIO's thread dispatch
79:A **trace** is the story of one request; a **span** is one timed operation with a name, start/end, attributes and a parent, forming a tree. Context (trace id, parent span id) crosses process boundaries in headers (W3C
95:On deploy, the orchestrator sends `SIGTERM`, waits a grace period (K8s default 30 s), then `SIGKILL`. A graceful process: (1) **stops being routed to** (readiness goes false; the load balancer needs time to notice, so
121:# Dockerfile (VERIFY: build and run on your machine; I did not build this image in the authoring environment)
145:Notes. Pin dependencies. Multi-stage builds pay off only when compiling wheels. Never copy `.env` (use `.dockerignore`). One worker per container is the orchestrator-friendly default; scale by replicas. With multiple
153:Traps: **coordinated omission** (a closed-loop generator waits for each response, so when the server stalls it stops sending and under-records the slow period; use constant-rate open-loop tools for latency claims; te
191:Why a **pure ASGI middleware** rather than `@app.middleware("http")` (which uses `BaseHTTPMiddleware`)? `BaseHTTPMiddleware` has documented limitations around `contextvars` propagation and background tasks in some ve
227:Decisions: status defaults to 500 so an exception that escapes is counted as an error; `scope["route"]` is set by the router after matching (observed on Starlette 1.10.0; VERIFY on your version, since older versions 
284:The test drives a fake clock: three failures open it; calls fail fast; after the cooldown one probe passes and a concurrent second is refused; a failed probe reopens; a successful probe closes. Caveat: it is not thre
296:**Security.** Redact logs; decide deliberately whether `/metrics` and `/docs` are public; non-root containers; scan images and dependencies (VERIFY tooling such as `pip-audit`, `trivy`); no secrets in image layers (`
302:**Testing.** Test that: the request id round-trips and appears on every log line; metrics labels stay bounded; readiness flips false at shutdown; the breaker transitions; configuration fails fast; the Docker image st
367:3. With shell-form `CMD`, `/bin/sh -c` may be PID 1 and not forward `SIGTERM` (shell-dependent; check `ps` in the container; VERIFY), so the app is killed with `SIGKILL` after the grace period and in-flight requests 
422:| Progressive hints | **H1:** Write the cardinality test first: request 1,000 random paths and assert the number of distinct label sets on `http_requests_total` is under a small constant. **H2:** For the pool gauge u
## 05-vol4-engineering/4.1-architecture-and-boundaries.md
129:Anything crossing a boundary and outliving a deploy (queue JSON, stored events, public APIs, a column another module reads) is a contract, and old and new versions coexist. Compatible: add an optional field with a de
287:Real adapters: `SqlAlchemyOrders` with explicit row-to-`Order` conversion functions (so the domain class never imports SQLAlchemy; VERIFY imperative-mapping details in the SQLAlchemy 2.x docs before choosing it over 
356:CI asserts `violations(Path("src/shop/domain")) == []`. An unenforced boundary decays. Limit: dynamic imports are invisible. For richer rules see import-linter (VERIFY current status and config) or, for PHP, PHPStan/
446:| Context | A FastAPI service beside a Moodle site. Completion data arrives through a port you define; do NOT assume exact Moodle web-service names (if you wire a real one, VERIFY on moodledev.io for your Moodle vers
451:| Quality requirements | Type hints on public functions; mypy-clean if available (VERIFY, else say it was not run). Each ADR under 400 words. Domain vocabulary in names. |
470:Critical failures: domain imports a web framework, ORM or HTTP client; uniqueness enforced only in application code; event published outside the transaction with no outbox while the report claims safety; a test claim
491:- Michael Nygard, "Documenting Architecture Decisions" (cognitect blog, 2011): the original ADR format. Read for the minimal template. VERIFY the URL is still live.
## 05-vol4-engineering/4.2-testing-strategy-review-refactoring.md
76:Instead of hand-picking examples, state a property and let a generator produce many inputs; on failure, the tool **shrinks** the input to a minimal counterexample. Python: Hypothesis. PHP options exist (VERIFY: curren
104:Good property sources: round-trips, idempotence, commutativity, "same result as a slow obvious implementation" (a **model** or **oracle**), and "output satisfies the invariant". Hypothesis stores failing examples in 
140:Mutation testing makes small automated changes ("mutants": `>=` to `>`, `+` to `-`, delete a statement) to the code and reruns the suite. A mutant that passes (**survives**) shows a behavior no test pins down. The **
220:Moodle-specific caution: core code and the global `$DB`, `$CFG`, `$USER`, `$PAGE` make unit testing hard; Moodle's PHPUnit setup provides database reset between tests (`resetAfterTest()`; VERIFY in moodledev.io for y
327:This is inheritance used *for testing*, which section 3 of 4.1 told you to distrust; here it is a deliberate, temporary scaffold with a clear exit: once tests exist, inject a `Clock` interface and delete the subclass
382:- Test order dependence: passes alone, fails in the suite. Diagnosis: run with randomized order (VERIFY the pytest plugin options, e.g. pytest-randomly) and bisect the order.
537:- Google Engineering Practices, "How to do a code review" (google.github.io/eng-practices/review): reviewer and author guidance. VERIFY the URL is current.
544:- Mutation testing tools for Python and PHP (VERIFY maintenance status), and the research literature on the coupling effect hypothesis.
## 05-vol4-engineering/4.3-security-and-reliability.md
48:The categories below follow the OWASP Top 10 (2021 edition: A01 Broken Access Control, A03 Injection which includes XSS, A10 Server-Side Request Forgery; VERIFY the current edition and numbering at owasp.org when you 
76:PHP: PDO prepared statements with named placeholders; Moodle code uses the `$DB` API with `?` or `:named` placeholders and never string-built SQL (VERIFY placeholder rules and the `$DB->get_records_sql` signature for 
82:**What:** attacker-controlled text is interpreted as markup or script in another user's browser. **Why:** output built by concatenation into HTML/JS/URL contexts. **Fix:** context-aware output encoding by default (aut
86:**What:** a malicious page makes the victim's browser send an authenticated request (cookies attached automatically) to your site. **Applies when** authentication is carried by something the browser sends on its own (
139:Tested against injected resolutions to `127.0.0.1`, `10.0.0.5`, `169.254.169.254`, `::1`, `192.168.1.1` (all rejected), plus `http://`, `file:///` and a host-less URL (rejected). Caveat: `is_global` follows the `ipad
143:Logs are copied to ticket systems, chat and third-party vendors; treat them as a data-egress channel. Rules: never log credentials, tokens, session ids, full card numbers, or request bodies of auth endpoints; log ide
164:Your code includes thousands of other people's lines. Controls: pin versions with a lockfile; run an audit tool in CI (Python: `pip-audit`; PHP: `composer audit`; VERIFY availability and flags for your tool versions)
246:Verified tests: a function failing twice succeeds on the third attempt with two jittered sleeps each in `[0, cap]`; a `Permanent` error is not retried; after two failures with threshold 2 the next call raises `Circui
278:For PostgreSQL the analogous tools are logical dumps (`pg_dump`/`pg_restore`) and physical base backups with WAL archiving for point-in-time recovery; for MySQL/MariaDB (common under Moodle) `mysqldump` or physical t
334:PHP/Moodle slice, as a checklist for any plugin entry point: `require_login()` first; `require_capability()` in the correct context; `required_param`/`optional_param` with a strict `PARAM_*` type; `require_sesskey()`
424:| Context | Start from a blank repository. Build (or reuse from earlier lessons) a FastAPI service with SQLite or PostgreSQL: `users`, `grades` (owner, course, value), `webhooks` (user-supplied URL to be called when 
425:| Requirements | (1) Vulnerable v0 with at least: SQL string-built query, IDOR on grades, unescaped HTML in a teacher comment page, SSRF-prone webhook fetch, token logged. (2) Threat model (DFD, STRIDE table, residua
434:| Evaluation rubric (100) | Threat model quality and honest residual risk: 12; fix correctness with fail-then-pass evidence for each class: 25; policy matrix and access-control tests: 8; SSRF depth (pinning, redirect
475:- OWASP Top 10 and Cheat Sheet Series (owasp.org): category definitions and per-topic defensive cheat sheets (SQL injection prevention, XSS prevention, CSRF prevention, SSRF prevention, session management, logging, s
484:- AWS Architecture Blog, "Exponential Backoff and Jitter": the analysis behind full jitter (VERIFY URL).
## 05-vol4-engineering/4.4-performance-engineering-method.md
87:**`py-spy`** (sampling, external): attaches to a running Python process without code changes. Typical commands: `py-spy top --pid <PID>` (live view), `py-spy record -o profile.svg --pid <PID>` (flame graph), `py-spy d
91:**PHP profiling options (VERIFY each against current docs and your PHP/Moodle version):**
94:- **XHProf / Tideways** extensions: sampling or lightweight instrumenting profilers designed to be lower overhead; Moodle has had admin-level profiling integration for XHProf-compatible extensions (Site administration
95:- **SPX** (a simple profiling extension) and **Blackfire** (commercial service): other options (VERIFY maintenance and licensing).
96:- Moodle also provides performance-oriented debug facilities such as the performance info footer and DB query counts (VERIFY `$CFG->perfdebug` and related settings for your version). For Moodle, query count and cache 
98:**Database profiling.** Application profilers show time waiting on the DB as one opaque cost; to look inside use the database: slow query log or `pg_stat_statements` (PostgreSQL; VERIFY enablement), `EXPLAIN`, and `EX
175:Sources of noise: other processes, CPU frequency scaling and thermal throttling, shared cloud hosts, garbage collection and allocator state, JIT or warmup (OS file cache, DB buffer cache, import costs, Python's speci
183:- **Statistical care**: with few samples, differences under the noise floor mean nothing. A significance test or bootstrap helps (VERIFY chosen method; for a first cut, the rule below is a defensible heuristic).
210:**Open versus closed models.** A *closed* generator (N users, each waits for a response before the next request) slows down when the server slows, which masks the problem; an *open* generator (requests arrive at a fi
214:Tools (VERIFY current versions and features): `wrk`/`wrk2`, `k6`, `locust`, `hey`, `ab` (limited), JMeter. Use throwaway environments you own; never aim a load test at a system you do not own.
218:A cache trades **staleness and complexity** for **speed and reduced load**. Before adding one: confirm with a profile that the cached work is the bottleneck; estimate hit rate (a cache with a 10% hit rate is mostly o
237:Performance regresses silently. Defenses: **benchmarks in CI** on stable hardware with the noise-aware rule above, run nightly rather than per commit if they are slow; **budgets on cheap deterministic proxies** (quer
267:**PHP/Moodle variant.** Same loop: baseline with Moodle's performance info and DB query counts for the page; locate with an Xdebug/XHProf-style profile on a development site (VERIFY tools); typical hypotheses are per
289:- Adding indexes everywhere. Diagnose: write cost and plan; check unused indexes in database statistics (VERIFY view names).
355:**8.3 (Mode B, 90 min). Query plan investigation.** In SQLite (or PostgreSQL if available), create `users`, `courses`, `enrolments`, `grades` tables with a seeded generator at two data sizes (for example 1,000 and 10
364:| Context | Start from a blank repository. Build a small FastAPI app (Python 3.12, Pydantic v2, SQLAlchemy 2.x, SQLite or PostgreSQL) with endpoint `GET /teachers/{id}/dashboard` returning, per course, learner count 
374:| Evaluation rubric (100) | Requirement quality and reproducible baseline harness: 15; profiling and plan reading used to locate cost correctly: 15; hypotheses recorded before and tested one change at a time: 15; res
415:- `py-spy` README (github.com/benfred/py-spy): installation, permissions, commands. VERIFY it is still the maintained location.
416:- Brendan Gregg, "Flame Graphs" and "Systems Performance": reading flame graphs and the USE method. VERIFY URLs.
418:- Gil Tene, "How NOT to Measure Latency" (conference talk): coordinated omission. VERIFY the talk's current location.
424:- Statistical methods for benchmark comparison: bootstrap confidence intervals and the Mann-Whitney U test; Chen and Revels on robust benchmarking (VERIFY citation) and the documentation of tools such as `pyperf` (VE
425:- The Python interpreter's adaptive specialization (PEP 659) and its consequences for warmup (VERIFY current details).
## 06-vol5-cpp/5.1-build-types-lifetime-const.md
9:| Minimum versions | C++20 (`-std=c++20`), GCC 11+ or Clang 14+, CMake 3.20+. Verified in preparing this lesson with GCC 14.2.0 and CMake 4.4.4 (CMake installed via `pip`; the system had none). Clang was not available 
114:- C++26 turns reads of uninitialized locals into "erroneous behavior" (`VERIFY: P2795` on cppreference). Do not depend on it.
323:- `std::span<char*>` over `argv` replaces unchecked `argv[i]` arithmetic with range-for and `subspan(1)`. `subspan(1)` on an empty span is UB; the `size() == 1` branch above only covers `argc >= 1`. A launcher can st
## 06-vol5-cpp/5.2-raii-copy-move-smart-pointers.md
9:| Minimum versions | C++20 (`-std=c++20`); `std::expected` is C++23 (`-std=c++23`, GCC 12+; flagged where used). Verified with GCC 14.2.0 and CMake 4.4.4. Clang was not available: Clang-specific behavior is marked `VER
149:Convention, not law: exceptions for failures you cannot handle locally; `expected`/codes for failures the caller branches on, like bad input. Follow the team standard (Lesson 4.1); inconsistent mixing is worse than e
253:`g++ -std=c++20 -Wall -Wextra -Wpedantic -fsanitize=address,undefined -g test_buffer.cpp -o tb && ./tb` exited 0 with no sanitizer output. The tests (same `EXPECT` idea as Lesson 5.1) cover: a copy is independent (`b
335:| Use after move | stale or empty values | review; clang-tidy `bugprone-use-after-move` (`VERIFY` availability) |
## 06-vol5-cpp/5.3-stl-lambdas-templates-concepts.md
9:| Minimum versions | C++20 (`-std=c++20`): ranges, concepts, `std::erase_if`, `contains`. C++23 items are labelled. Verified with GCC 14.2.0 (`-Wall -Wextra -Wpedantic`, ASan+UBSan where relevant) and CMake 4.4.4. Clan
44:| `std::deque<T>` | chunked | `[i]` O(1) | both ends O(1); middle O(n) | insertion invalidates iterators; whether references survive depends on where you insert (`VERIFY` on the cppreference `deque` page) |
48:| `std::flat_map` (C++23) | sorted vectors | O(log n) | O(n) | availability in your library: `VERIFY` (`__cpp_lib_flat_map`) |
50:(Table facts for associative/unordered complexity and invalidation were confirmed against the cppreference container page; sequence-container complexities are the standard's operation requirements, `VERIFY` details on
73:Views borrow from their source: if the source is destroyed or modified, the view is invalid. (Rvalue containers piped into a view are moved into an `owning_view` in GCC 14; `VERIFY` your library's C++20 conformance le
121:| `std::move_only_function` (C++23) | type-erased | like `std::function` | like `std::function` | store move-only callables (`std::function` requires copyable ones); availability: `VERIFY` |
407:Program B (verified): the first loop printed nothing, only `|`. A view is lazy: the filter runs when iterated, after `v` was replaced with `{1, 3, 5}`, which has no even element. (Modifying the underlying container a
448:| 2 | Context | Quant and trading code often keeps small, read-mostly maps (symbol to config, tenor to rate). A sorted vector gives contiguous iteration and fast lookup but costs O(n) insertion and invalidates iterat
## 06-vol5-cpp/5.4-data-structures-and-algorithms.md
49:Doubling array, inserting `n` elements. Growth copies happen at sizes 1, 2, 4, ..., so total copies are below 2n; with n writes the total is below 3n, so the average cost per push is at most 3 = O(1) amortized. The si
195:Invariants: **I1** capacity is a power of two. **I2** `used_*4 <= capacity*3` after every insert (`used_` = Full + Deleted), so at least one `Empty` slot always exists and every probe loop terminates. **I3** every `F
511:`std::flat_map`/`std::flat_set` are C++23 (VERIFY library support in cppreference's compiler support table; not in the g++ 14.2 used here).
644:- Why do databases (lesson 2.3) use B-trees? Compare a B-tree node search with `lower_bound` on a sorted vector. Read about Swiss-table designs (VERIFY details in Abseil's docs).
## 06-vol5-cpp/5.5-sanitizers-ub-debugging-profiling.md
9:| Minimum versions | C++20. Everything marked "observed" was run with g++ 14.2 on x86-64 Linux (ASan, UBSan, TSan, gprof, `-fanalyzer`, `-S` assembly output). NOT available where this lesson was written, therefore mark
27:4. Produce a core dump, state how you would open it in gdb or lldb, and use `bt`/`frame`/`print`/watchpoint commands (VERIFY, not runnable where this was written).
54:| Violating strict aliasing | read a `float` through an `int*` | `-Wstrict-aliasing`; no reliable runtime tool in GCC (VERIFY) |
55:| Invalid comparator (not strict weak ordering) | `a <= b` in `std::sort` | ASan sometimes, `-D_GLIBCXX_DEBUG` (VERIFY) |
64:| ASan (+LSan on Linux x86-64) | `-fsanitize=address` | heap/stack/global overflow, use-after-free, double free, leaks (observed: `LeakSanitizer: detected memory leaks`) | typically 2x slowdown and several times the m
67:| MSan | `-fsanitize=memory` | uninitialized reads | **clang only**; needs all linked code instrumented (VERIFY); not testable with the g++-only setup used here |
69:Useful environment options (observed to work): `UBSAN_OPTIONS=print_stacktrace=1`. Others (`ASAN_OPTIONS=detect_stack_use_after_return=1`, `halt_on_error`) - VERIFY in the sanitizer documentation for your compiler ver
75:`g++ -fanalyzer` (GCC 10+; observed in 14.2) found the same uninitialized use with a CWE tag; GCC's documentation describes C++ support as limited (VERIFY the current statement), so treat silence as no evidence. **cla
77:### 3.4 Debuggers and core dumps (VERIFY: no gdb/lldb where this was written)
79:Build with `-g -O0` (or `-Og`) for debugging; at `-O2` variables are optimized away, lines jump. gdb basics: `gdb ./prog`, `break file.cpp:42`, `run args`, `bt` (stack), `frame N`, `info locals`, `print expr`, `next`/
81:Core dumps: `ulimit -c unlimited; ./prog` writes a core file if the kernel policy allows. Observed here: after `abort()`, a file named `core.<pid>` appeared in the working directory (`/proc/sys/kernel/core_pattern` wa
83:**valgrind** (VERIFY): `valgrind --leak-check=full ./prog` needs no recompile, runs far slower than native, reports uninitialized reads (memcheck) - the practical substitute for MSan on a g++-only toolchain. Do not co
88:- **perf** (Linux; VERIFY, not installed here): build `-O2 -g -fno-omit-frame-pointer`; `perf record -F 99 -g ./prog`; `perf report`; `perf stat ./prog` for counters (hardware counters may be unavailable in VMs/contai
94:Compiler Explorer (godbolt.org; VERIFY the UI): pick "C++", an "x86-64 gcc 14.x" compiler, flags `-std=c++20 -O2`; the right pane maps source lines to instructions; add `-fsanitize=address` to see instrumentation. Loc
253:**Security.** Memory errors are the major source of exploitable bugs in C++ code (language-level fact: no bounds checking by default). Defensive measures: sanitizers in CI, hardened standard-library assertions (`_GLI
315:**Bug 4.** Observed: `-Wall -Wextra` gave **no** warning at `-O0` and `warning: 'result' may be used uninitialized [-Wmaybe-uninitialized]` at `-O2`; `-fanalyzer` reported `use of uninitialized value 'result' [CWE-45
333:9. What is the difference between a profile from `gprof -pg` and from `perf record` (mechanism, overhead, blind spots)? (perf part: VERIFY.)
335:11. In gdb, how do you stop when a variable changes? How do you inspect a crash from a core file? (VERIFY on your machine.)
355:| 4. Constraints | C++20; g++ or clang++; no AI; every claim about a tool's output must be an observed excerpt or labelled VERIFY; fixes must keep behavior identical for valid input. |
364:| 13. Extension | Add a fuzzing target (libFuzzer needs clang: VERIFY) or a randomized stress test for your containers from 5.4 under ASan+UBSan, and report any finding. |
374:- Is the evidence observed output, not remembered output? Are VERIFY items clearly marked?
407:- https://perfwiki.github.io/main/ - perf documentation (VERIFY it is the current home).
411:- Read a real ASan report on a larger program and trace the shadow-memory encoding (the `fa`, `fd` bytes in the report); read the `-O2` assembly of a loop to see auto-vectorization (`-fopt-info-vec` for GCC, VERIFY).
## 06-vol5-cpp/5.6-cache-allocators-concurrency-memory-model.md
9:| Minimum versions | C++20 (`std::jthread`, `std::pmr` is C++17). Verified with g++ 14.2 on x86-64 Linux, 4 physical cores (8 logical). Google Benchmark was not installed where this was written (VERIFY its API against 
62:3. **Prevent dead-code elimination**: the compiler may delete work whose result is unused. Consume results through an optimizer barrier (`do_not_optimize` below uses a GCC/Clang `asm volatile`; Google Benchmark provid
68:9. Control the environment: AC power and performance governor if you can (VERIFY: `cpupower frequency-set -g performance` needs root and the tool), pin to a core (`taskset -c 2 ./prog`), close other work, same compile
73:Hand-rolled harness (used below). Google Benchmark is the usual tool in teams; it adds automatic iteration counts, statistics and output formats, and is a dependency to be agreed with the team (VERIFY installation: pa
76:// file: bench.hpp  (C++20)  Hand-rolled harness. GCC/Clang inline asm; see VERIFY note for other compilers.
87:    static volatile const void* sink;  // VERIFY: weaker fallback; MSVC needs its own mechanism
189:Rules of thumb: start with `seq_cst`; relax only with a proof of the happens-before edges you need and a measurement that shows the gain (on x86-64 many orders compile to the same instructions for loads/stores, so ga
230:constexpr std::size_t kLine = 64;  // typical x86-64 line; VERIFY with: getconf LEVEL1_DCACHE_LINESIZE
422:**Performance.** Measure before restructuring: AoS to SoA changes every call site. Prefer fixing the biggest structural cost first: allocation counts (`reserve`, arenas), pointer-heavy structures, then layout, then t
428:**Observability.** Expose queue depth, task latency histogram, and rejected-task counts; log thread names. Operations: pin cores and set thread count from `std::thread::hardware_concurrency()` (a hint that may return
434:**Beginner mistakes and diagnosis.** (1) Benchmarking `-O0` or unused results: look at the assembly or vary the code and see no change. (2) `wait` without a predicate: sporadic hangs or spurious wakeup bugs; add the 
504:| 13. Extension | Work-stealing per-thread queues, or a `parallel_for` built on the pool with chunking; compare with C++17 parallel algorithms (`std::execution::par`, VERIFY toolchain support: libstdc++ typically req
546:- https://github.com/google/benchmark - Google Benchmark README (VERIFY API names and install steps for your version).
553:- C++23: `std::mdspan` for strided/SoA-friendly views (VERIFY library support in your toolchain).
## 07-vol6-quant/6.1-probability-and-distributions.md
14:Scope note: mathematical correctness first, implementation correctness second. Every number below was produced by running the code shown (Python 3.13.5, stdlib `random`). Simulated values are single runs at a stated s
383:- Gigerenzer and Hoffrage (1995), "How to improve Bayesian reasoning without instruction: frequency formats", Psychological Review - why natural-frequency tables work (VERIFY details before quoting).
## 07-vol6-quant/6.2-linear-algebra-calculus-numerics.md
9:| Minimum versions | C++20 (`<span>`, `<numbers>`, concepts not required); GCC 14.2 used to verify (clang/MSVC: VERIFY by compiling). Python 3.12 + numpy >= 1.26 only for cross-checks |
87:Computation: Jacobi's method applies plane rotations that each zero one off-diagonal entry; the matrix converges to diagonal while the rotations accumulate into the eigenvector matrix. It is simple and accurate for sm
130:Whether C++ `double` is IEEE binary64 is implementation-defined; check `std::numeric_limits<double>::is_iec559` (VERIFY on your toolchain). Compilers may also fuse multiply-add (`-ffp-contract`), changing last bits b
150:Idea: keep a running correction c holding the low-order bits lost by each addition. Neumaier's variant compares magnitudes, so it also works when a new term exceeds the running sum: for {1e100, 1, -1e100} naive gives
247:**Performance and operations.** Dense O(n^3) kernels are memory-bound at scale; production code uses BLAS/LAPACK (Eigen, Armadillo, MKL are options; VERIFY team standards before adding a dependency). Measure before o
366:- GCC documentation, "Optimize Options" (`-ffast-math`, `-ffp-contract`), https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html - what fast-math permits (VERIFY exact flag descriptions for your version).
## 07-vol6-quant/6.3-statistics-timeseries-montecarlo.md
14:Every number below was produced by running code (Python 3.13.5, numpy 2.5.4, scipy 1.18.1) with the stated seeds; they are single runs and your digits will differ if your numpy version changes the stream (`default_rng
112:Pseudo-random generators are deterministic given a seed. Rules: (1) seed explicitly and log the seed; (2) use `numpy.random.default_rng(seed)` (a `Generator`), not the legacy global `np.random.seed` state; (3) for pa
284:- Wasserstein and Lazar (2016), "The ASA statement on p-values" (The American Statistician) - official statement on p-value misuse (VERIFY citation details).
286:- Granger and Newbold (1974), "Spurious regressions in econometrics" (Journal of Econometrics) - the original warning on regressing non-stationary series (VERIFY details).
## 07-vol6-quant/6.4-markets-returns-options-risk.md
9:| Minimum versions | Python 3.12 (standard library only: `math`, `random`, `statistics.NormalDist`, `unittest`), or C++20 (g++ 13+ / clang 16+; VERIFY with `g++ --version`) |
147:- **Volatility is not constant.** Implied vol varies with strike and maturity (smile/skew); practitioners quote prices as implied vols. VERIFY on data you are licensed to use; do not assert a shape from memory.
191:VaR fails in specific ways: it ignores losses beyond the threshold; it is not subadditive in general (ES is); it depends heavily on window and sample size. ES is harder to backtest. The Basel market-risk framework (F
426:- Hull, J., *Options, Futures, and Other Derivatives* (Pearson): standard text for instruments, parity, Greeks, VaR/ES; use the chapter index to find each topic (edition-dependent; VERIFY chapter numbers in your edit
429:- Basel Committee on Banking Supervision, "Minimum capital requirements for market risk" (bis.org): official source for the VaR to Expected Shortfall change (VERIFY the confidence level and wording before quoting).
## 07-vol6-quant/6.5-backtesting-orderbook-marketdata.md
9:| Minimum versions | C++20 (g++ 13+ or clang 16+; VERIFY with `g++ --version`); Python 3.12 standard library for the backtester |
70:- **Overfitting / data snooping**: with enough tries a noise strategy looks good; the best of m no-edge parameter sets has an upward-biased Sharpe growing with m. Defences: an untouched OOS set, walk-forward, reportin
92:Caveats: Sharpe from one path has a large standard error (roughly proportional to 1/sqrt(years of data); the usual approximation is in Lo (2002), VERIFY the exact expression). Annualising by `sqrt(252)` assumes indepe
96:A limit order: side, price, quantity, (id, timestamp). Rules of an exchange with **price-time priority**: better prices match first; at the same price, earlier orders match first (FIFO). An incoming order that crosses
133:A feed delivers messages: add order (id, side, price, qty), reduce/cancel, delete, execute, replace (vocabulary resembling Nasdaq ITCH-style feeds; VERIFY any protocol against the venue's document). Handle: **sequenc
226:Choices: one template serves both sides (`bids_` uses `std::greater`, `asks_` uses `std::less`, so `begin()` is always the best price); the index entry is erased exactly when the maker leaves the list; `has_limit` le
234:5. **Repetitions**: discard a warm-up, then at least 30 runs; report median and spread (min, p90, max). State CPU model, OS, compiler version, frequency governor; pin to a core if possible (VERIFY: `taskset`).
386:- Bailey, D. and Lopez de Prado, M., "The Deflated Sharpe Ratio" (2014): multiple-testing correction for Sharpe; VERIFY the formula in the paper.
390:- Exchange ITCH-style protocol specifications (e.g. Nasdaq TotalView-ITCH, published by Nasdaq): real message vocabulary and sequencing; VERIFY the current spec.
## 08-vol7-independence/7.1-ai-independence-and-audits.md
74:- **Fabricated or misremembered APIs**: functions, parameters, flags or config keys that do not exist or exist in another version. Check: run it, `help()`/`dir()`, official docs for your exact version. In the lab, `ma
167:Rewrite following 3.2: "FastAPI 0.x (VERIFY exact version with `pip show fastapi`), Python 3.12, Postgres via SQLAlchemy 2.x. `GET /orders?customer=...` takes about 2 s for a customer with 40k orders; others are fast
395:- OWASP Cheat Sheet Series, Password Storage and SQL Injection Prevention (cheatsheetseries.owasp.org): current recommendations; VERIFY parameter values at time of use.
400:- Property-based testing (Hypothesis), mutation testing tools (VERIFY maintenance status of any tool you pick) and static analysis (`bandit`, `ruff`) as a first-pass reviewer, and what they miss.
## 08-vol7-independence/7.2-design-docs-adrs-postmortems.md
385:- Google, *Site Reliability Engineering* book, chapter "Postmortem Culture: Learning from Failure" (sre.google/sre-book): blameless postmortem practice; VERIFY chapter title in the current online edition.
