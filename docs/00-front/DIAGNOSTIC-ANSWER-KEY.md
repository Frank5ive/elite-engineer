# Diagnostic Answer Key and Grading Guide

**Do not open this before finishing `DIAGNOSTIC.md` and recording your predicted scores (Part H3).**

## Grading principles

- Grade from the answer files, not from memory of what you meant.
- Award partial credit as indicated. A correct answer with a wrong explanation earns at most half.
- For coding items: run them. Code that was not run, or that fails its own test, caps at 50% of the item. Items marked LOOKED UP score zero.
- Self-grading bias is real. If grading yourself, be strict, and where unsure give the lower score; then ask for an independent grading in a continuation session (CONTINUE-HERE.md), which should be told the answer files only, not your estimate.
- Where the key marks a version-dependent fact, check it in official docs when it matters.
- Record per-item scores in `progress/diagnostic/scores.md`, with a one-line note on every missed item stating the underlying gap (this feeds remediation exercises).

---

## Section A (30)

**A1 (2).** Output:
```
[1]
[1, 2]
[3]
```
Default value is evaluated once at `def` time and shared. 1 point for correct output, 1 for the reason (when stated: or demonstrated understanding in the answer). The third call passes its own list.

**A2 (2).** `[2, 2, 2]`. Closures capture the variable `i`, not its value; by the time the lambdas run, `i` is 2. Fix: `lambda i=i: i`. 1 + 1.

**A3 (2).** `[0, 1, 4]` then `[]`. A generator is exhausted after one pass. 1 + 1.

**A4 (2).** `[1, 2, 3] [1, 2, 3, 4]`. `+=` on a list mutates in place (and `b` aliases `a`); `c = c + [4]` builds a new list bound to `c`. 1 for each correct value; the explanation is needed for full marks only if the output is right.

**A5 (3).** Reference:
```python
from contextlib import contextmanager
import time

@contextmanager
def timed(label, sink):
    start = time.perf_counter()
    try:
        yield
    finally:
        sink.append((label, time.perf_counter() - start))
```
Test: use `pytest.raises` around a block that raises and assert one entry in `sink`. Scoring: 1 uses `finally` (or `__exit__` always recording), 1 does not suppress the exception (a class `__exit__` must return a falsy value), 1 working test. Using `time.time()` instead of a monotonic clock: allowed but note it (no deduction, remark only). Common failure: placing the append after `yield` without `finally`, which skips recording on exceptions.

**A7 (4).** Reference (Pydantic v2):
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()
items: dict[str, "Item"] = {}

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def strip_and_check(cls, v: str) -> str:
        v = v.strip()
        if not 1 <= len(v) <= 50:
            raise ValueError("name must be 1-50 characters")
        return v

@app.post("/items", status_code=201, response_model=Item)
def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=409, detail="item exists")
    items[item.name] = item
    return item
```
Default validation failure status: 422. Scoring: 1 model with constraints (v2 syntax: `field_validator`, `Field(gt=0)`; v1 `@validator` or `constr` usage with v2 mismatch loses half), 1 correct 201, 1 correct 409, 1 correct 422 statement and working code. Valid alternatives: `Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]` (Pydantic v2; `from pydantic import StringConstraints` imports on Pydantic 2.14, checked); `Decimal` for price (a good answer, mention that money should not be float); a lock or note about thread-safety of the shared dict (bonus remark, no points).

**A8 (3).** `def` endpoints run in a threadpool, so blocking calls do not stop the event loop (up to the pool size); `async def` endpoints run on the event loop, so a blocking call stops all other requests handled by that loop for its duration. Fixes: use `await asyncio.sleep` or an async client/driver; or declare the endpoint with `def`; or `run_in_threadpool` / `anyio.to_thread.run_sync`; or move to a background worker. 1 + 1 + 1 (two fixes needed for the last point).

**A9 (3).** Reference:
```python
import re

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
```
This maps `"Café"` to `"caf"`, dropping the accent; a better design normalizes with `unicodedata.normalize("NFKD", ...)` and drops combining marks to produce `"cafe"`, or uses `\w` with the Unicode flag to keep letters. Either is acceptable if stated and tested. Scoring: 1 correct behavior including empty string returning `""`, 1 parametrized test (`@pytest.mark.parametrize`) with at least five cases, 1 explicit and tested statement of the unicode behavior.

**A10 (3).**
```python
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/things")
def things(db = Depends(get_db)): ...

app.dependency_overrides[get_db] = lambda: FakeDb()
```
1 for `yield` with `try/finally`, 1 for `Depends`, 1 for `dependency_overrides` (and clearing it afterward in the test teardown: remark).

**A11 (2).** 201; 422; 401; 403; 409. 0.4 each, round to the nearest half point at the end. 400 accepted for the second only if the answerer clarifies that FastAPI's default is 422.

**A12 (2).** `venv` creates an isolated environment directory with its own interpreter links and `site-packages`, so project dependencies do not collide with system or other projects. Pinning gives reproducible builds and prevents surprise upgrades breaking behavior; a lock file (hashes optional) records the resolved set. 1 + 1.

## Section B (20)

**B1 (3).**
```sql
SELECT c.id, c.title
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
WHERE e.course_id IS NULL;
```
or `WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.course_id = c.id)`. Wrong: `NOT IN` against a nullable column without discussing NULL (1 point at most; here `course_id` is a key so acceptable if noted). 3 for correct and run; 2 for correct but unrun; 1 for join without null test.

**B2 (3).**
```sql
SELECT c.id, c.title, COUNT(*) AS n
FROM courses c
JOIN enrollments e ON e.course_id = c.id
WHERE e.status = 'active'
GROUP BY c.id, c.title
HAVING COUNT(*) >= 5
ORDER BY n DESC, c.id
LIMIT 3;
```
1 filter before grouping, 1 `HAVING`, 1 order/limit with tiebreak.

**B3 (2).** `WHERE` filters rows before aggregation; `HAVING` filters groups after aggregation. `status = NULL` evaluates to unknown, so it returns no rows; use `IS NULL`. 1 + 1.

**B4 (3).** Index `(course_id, status, enrolled_at DESC)` (or `(course_id, status, enrolled_at)` since a b-tree can be read backward; PostgreSQL 11+ can add `student_id` as a `INCLUDE` column for an index-only scan; other engines differ). Reason: equality columns first, then the ordering column so the order is served by the index and `LIMIT 20` stops early. Confirm with `EXPLAIN (ANALYZE, BUFFERS)` looking for an index scan without a separate sort, and a low actual row count. 1 index, 1 reasoning, 1 verification step. A partial index on `status = 'active'` is a valid, better-for-this-query alternative and earns the reasoning point if justified.

**B5 (3).** A sequential scan reads about a million rows to return 15; no usable index on `student_id`. Actions: (1) create an index on `enrollments(student_id)` (concurrently on a production table; check lock behavior), (2) rerun `EXPLAIN ANALYZE` and confirm the plan changed and the rows removed dropped, (3) check statistics (`ANALYZE`) and whether the query is frequent enough to justify the write cost of the index. Note that the composite primary key `(student_id, course_id)` in the schema above already has `student_id` as its leading column, so an index likely exists in this schema; award a bonus remark if the answerer notices that and says the plan in the question implies the schema differs (the excerpt is illustrative). 1 diagnosis, 1 fix, 1 verification or cost awareness.

**B6 (3).** Final balance 70 (or 70 from one update lost), not 40: a **lost update**. Fixes (any two): single atomic statement `UPDATE accounts SET balance = balance - 30 WHERE id = ? AND balance >= 30`; `SELECT ... FOR UPDATE` row lock; serializable (or repeatable read in PostgreSQL) with retry on serialization failure; optimistic concurrency with a version column. 1 value, 1 anomaly name, 1 two fixes (0.5 each). Note: the anomaly shown yields 70 and one withdrawal is lost.

**B7 (2).** OFFSET makes the database walk and discard offset rows, so cost grows with page number; and concurrent inserts or deletes shift rows so pages can duplicate or skip items. Keyset:
```sql
SELECT * FROM t
WHERE (created_at, id) < ($1, $2)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```
1 + 1.

**B8 (1).** Concurrent transactions do not see each other's partial work; the strength depends on the isolation level, which trades anomaly protection against concurrency and retry cost.

## Section C (20)

**C1 (2).** `bool(false)`, `bool(true)`, `string(1) "x"`. In PHP 8, `0 == "a"` is false (numeric strings are compared as numbers; non-numeric strings compare with the number as string). `"1" == "01"` is true (both numeric strings). 0.5 + 0.5 + 1 distribution: 0.5 for each of the first two, 1 for the third. Checked by running PHP 8.4.27: `var_dump(0 == "a")` gives `bool(false)` and `var_dump("1" == "01")` gives `bool(true)`; the third line prints `string(1) "x"`. See the PHP 8 comparison table at php.net if disputing.

**C2 (2).**
```php
final class Money {
    public function __construct(
        public readonly int $amountMinor,
        public readonly string $currency,
    ) {}

    public function add(Money $other): Money {
        if ($this->currency !== $other->currency) {
            throw new InvalidArgumentException('Currency mismatch');
        }
        return new Money($this->amountMinor + $other->amountMinor, $this->currency);
    }
}
```
1 for promotion + readonly syntax, 1 for check and immutable return. `declare(strict_types=1)` mention is a bonus remark.

**C3 (2).** Maps namespace prefixes to directories so classes load on demand via the Composer-generated autoloader; configured in `composer.json` under `autoload.psr-4`, regenerated with `composer dump-autoload`. Moodle also has its own autoloader for `classes/` directories keyed by component (Frankenstyle) namespace; mention earns the second point more strongly. 1 + 1.

**C4 (3).** `version.php`; `db/access.php`; `lang/en/<component>.php`; `db/install.xml`; `db/upgrade.php`. 0.6 each, round at the end.

**C5 (3).** `require_login($course, false, $cm)` (course and course module as applicable), `require_capability('mod/foo:view', $context)` or `has_capability` for a soft check, with `$context = context_module::instance($cm->id)`. Context levels: system, user, course category, course, activity module, block. 1 + 1 + 1.

**C6 (3).**
```php
$user = $DB->get_record('user', ['id' => $id], '*', MUST_EXIST);
$users = $DB->get_records_sql(
    'SELECT id, firstname, lastname FROM {user} WHERE lastname = :ln',
    ['ln' => $lastname]
);
```
Placeholders prevent SQL injection and handle quoting; table names are written in braces `{user}` so the configured prefix is applied. 1 + 1 + 1.

**C7 (2).** `sesskey` is a CSRF token that must be checked (`require_sesskey()` / `confirm_sesskey()`) on state-changing requests. Safe output: `s()` / `p()`, `format_string()`, `format_text()` with the right options and context, `html_writer` and Mustache templates with default escaping `{{ }}` (not triple braces for untrusted data), `clean_param` on input. 1 + 1 (three named).

**C8 (3).** Task: `classes/task/<name>.php` extending `\core\task\scheduled_task` (implement `get_name()` and `execute()`), and `db/tasks.php` declaring it; language string for the name. Observer: `db/events.php` listing `eventname` and `callback`, and a class in `classes/` with a static callback. Then bump `version.php` and run the upgrade so Moodle registers them; clear caches during development. 1 + 1 + 1.

## Section D (20)

**D1 (3).** Case 1 (not pushed): remove the secret and rewrite the commit (amend, or rebase to drop/edit it) so it never reaches the remote; also consider revoking the key anyway because it exists in reflog and possibly in other places such as editor backups. Case 2 (pushed): treat the key as compromised: **revoke/rotate it immediately** and then clean history if policy requires (history rewrite requires coordination and does not un-leak it; forks, clones and CI logs may already have it); inform the relevant owner per team process. Key insight: rotation, not deletion, is the fix once pushed. 1 + 1 + 1 (rotation emphasis).

**D2 (3).** Merge preserves history with a merge commit; rebase replays commits onto a new base, producing a linear history and new commit hashes. Do not rebase commits that others have based work on (shared or published branches) unless coordinated. Regression search: `git bisect start`, `git bisect bad`, `git bisect good <commit>`, then mark each step, or `git bisect run <test-command>`. 1 + 1 + 1.

**D3 (3).** Look for: a clear title; what changed and why (the problem: transient failures); how it was tested (including the new test and manual check); risks (retry amplification, idempotency of the call, timeout budget) and rollback (revert, config toggle). Under 150 words, scannable. 1 content, 1 risks/rollback, 1 clarity and brevity.

**D4 (3).** Problems (1 point for severe items found, up to 5 distinct needed for full marks; each 0.6 rounding): SQL injection by string concatenation (most severe); connection never closed / no context manager; `requests.get` with no timeout (can hang); bare `except:` swallowing all errors including `KeyboardInterrupt` and hiding failures (returns `None` silently); `http://` plain text and URL built from unescaped user input (path injection); mutable default argument in `add_tag`; `SELECT *`; no error handling for `r.json()` or status (`raise_for_status`); no types or tests; a possible leak of `row` data. The bonus remark: a hard-coded database path.

**D5 (3).** A good message: states what you are trying to do, what fails (exact error), what you tried (2-3 items), what you suspect, what you need (a specific question or a 15-minute pairing), and whether anything is blocked by the delay. No "it doesn't work". Under 120 words. 1 context and exact symptom, 1 what was tried, 1 clear ask and impact.

**D6 (3).** First actions: (1) get the CI failure logs and the exact failing test and error, and compare with a passing run; (2) try to reproduce locally by repeating the test many times, in random order, in a clean container matching CI (versions, env vars, CPU count, locale, timezone); (3) check for shared state, ordering dependencies, time or randomness, network or port conflicts, parallelism and resource limits. Hypotheses ordered by likelihood: test order or shared state, timing/async races, environment differences, external dependency. Do not "just rerun". 1 + 1 + 1.

**D7 (2).** Flaky causes: shared mutable state, time, randomness, concurrency or timing assumptions, network or external services, test order, resource limits. Pyramid: many fast, isolated unit tests; fewer integration tests; very few end-to-end tests; because speed, determinism and localization of failure fall as scope grows. 1 + 1. (The pyramid is a heuristic; an answer that notes cases where more integration coverage is wise earns the point equally.)

## Section E (25)

If the answerer has never written C++ and wrote "none", score E1-E4, E8-E9 as zero and route as Foundation for Vol 5; do not penalize further.

**E1 (3).** Returns a reference to a local that is destroyed when the function returns: dangling reference; using it is undefined behavior. (Return by value; a compiler warning is likely; note: temporaries and lifetime extension do not apply here.) 2 + 1.

**E2 (3).**
```cpp
class File {
    FILE* f_ = nullptr;
public:
    explicit File(const char* path, const char* mode) : f_(std::fopen(path, mode)) {
        if (!f_) throw std::runtime_error("open failed");
    }
    ~File() { if (f_) std::fclose(f_); }
    File(const File&) = delete;
    File& operator=(const File&) = delete;
    File(File&& o) noexcept : f_(std::exchange(o.f_, nullptr)) {}
    File& operator=(File&& o) noexcept {
        if (this != &o) { if (f_) std::fclose(f_); f_ = std::exchange(o.f_, nullptr); }
        return *this;
    }
};
```
1 destructor release plus deleted copy, 1 move constructor leaves source null, 1 move assignment releases the old resource and handles self-assignment. Missing `noexcept` on moves: remark.

**E3 (3).** `push_back` may reallocate, which invalidates all iterators, pointers and references; dereferencing `it` afterward is undefined behavior (even if it often "works" when capacity suffices). Fix: reserve first, or re-acquire the iterator, or use indices. 2 + 1.

**E4 (2).** `unique_ptr` for exclusive ownership (default); `shared_ptr` only when ownership is genuinely shared and lifetimes cannot be nested simply (and consider the cost and cycle risk, `weak_ptr`); raw pointers or references for non-owning observation where the pointee outlives the use. 1 + 1.

**E5 (3).** Vector insert at front O(n); `unordered_map` lookup average O(1), worst O(n); `std::map` O(log n); `std::sort` O(n log n) comparisons (the worst-case O(n log n) requirement for `std::sort` applies since C++11 via LWG 713; cppreference notes that earlier wording allowed quicksort with O(n^2) worst case, and that libc++ only implemented the corrected requirement in LLVM 14); `deque::push_front` amortized O(1) (constant time). 0.6 each.

**E6 (4).** Reference approach: hash map from value to index; for each `j`, look up `target - a[j]`; return `(i, j)` if found, else insert `a[j]`. O(n) expected time, O(n) space. Duplicates handled because lookup precedes insertion (e.g. `[3, 3]`, target 6). Failure modes or assumptions: integer overflow of `target - a[j]` for extreme values (use wider type), hash worst case O(n^2) under adversarial input, multiple valid answers (state which is returned). 1 correct algorithm, 1 handles duplicates and negatives with tests, 1 stated complexity, 1 stated failure mode. Code not run: cap at 2.

**E7 (3).**
```cpp
size_t lower_bound(const std::vector<int>& v, int x) {
    size_t lo = 0, hi = v.size();           // invariant: all v[i] < x for i < lo; all v[i] >= x for i >= hi
    while (lo < hi) {
        size_t mid = lo + (hi - lo) / 2;
        if (v[mid] < x) lo = mid + 1; else hi = mid;
    }
    return lo;
}
```
1 correct on tests including empty, all less, all greater, duplicates; 1 invariant stated correctly; 1 midpoint safe (`lo + (hi - lo)/2`) or reasoned. A half-open interval `[lo, hi)` is the cleanest; closed intervals with `hi = size-1` are fine if correct.

**E8 (2).** `const int* p`: pointer to const int (cannot modify `*p`; can reseat `p`). `int* const p`: const pointer to int (can modify `*p`; cannot reseat `p`). 1 + 1.

**E9 (2).** Behavior for which the standard imposes no requirements: anything may happen. Examples: signed integer overflow, out-of-bounds access, use after free, data race, null dereference. AddressSanitizer (memory errors), UndefinedBehaviorSanitizer (overflow, misaligned access, etc.), ThreadSanitizer (data races). 1 definition and examples, 1 sanitizers.

## Section F (20)

**F1 (2).** 6/36 = 1/6, about 0.1667.

**F2 (3).** P(D|+) = 0.01*0.90 / (0.01*0.90 + 0.99*0.05) = 0.009 / (0.009 + 0.0495) = 0.009/0.0585 ≈ 0.154 (about 15.4%). 1 setup (Bayes), 1 correct arithmetic, 1 interpretation of why it is low (base rate). 

**F3 (2).** E = 3.5. Var = E[X^2] - E[X]^2 = 91/6 - 12.25 = 35/12 ≈ 2.917. 1 + 1.

**F4 (3).** `Ax = [2*1 + 1*2, 1*1 + 3*2] = [4, 7]`. `det(A) = 2*3 - 1*1 = 5`. `det = 0` means the matrix is singular: not invertible, columns linearly dependent, the map collapses a dimension. 1 + 1 + 1.

**F5 (2).** `f'(x) = (2x + x^2) e^x` by the product rule. Gradient descent moves parameters in the direction opposite the gradient to decrease the function, scaled by a step size. 1 + 1.

**F6 (3).** 0.1, 0.2 and 0.3 have no exact binary representation, so the sum differs from the nearest double of 0.3 by a rounding error. Compare with a tolerance (absolute and relative, e.g. `math.isclose`) chosen from the problem's scale, or use integers/decimals for exact quantities such as money. Catastrophic cancellation: subtracting nearly equal numbers wipes out leading digits, leaving mostly rounding noise, e.g. `(1 + 1e-16) - 1` returns 0 in double precision, or `sqrt(x+1) - sqrt(x)` for large x (rewrite as `1/(sqrt(x+1)+sqrt(x))`). 1 + 1 + 1.

**F7 (2).** Sum of two independent: 2 s^2 (variances add). Mean of n: s^2 / n (standard error s/sqrt(n)). 1 + 1.

**F8 (3).** p-value: the probability, assuming the null hypothesis and the model are true, of data at least as extreme as observed; it is not the probability that the null is true or that the result is due to chance alone. 95% CI: an interval produced by a procedure that covers the true parameter in 95% of repeated samples (under assumptions); it does not mean a 95% probability that this specific interval contains the parameter (in the frequentist framing). Multiple tests: 1 - 0.95^20 ≈ 0.642. 1 + 1 + 1.

## Section G (15)

**G1 (2).** Simple returns: +10% (100 to 110) and -10% (110 to 99, since 11/110 = 0.10). Total: 99/100 - 1 = -1%. Log returns: ln(1.1) = 0.0953, ln(0.9) = -0.1054; sum -0.0101 = ln(0.99). The average of simple returns (0%) hides the loss because simple returns do not add across time; compounding matters. 1 + 1.
**G2 (3).** Payoff = max(S - K, 0): 0, 5, 20. Profit = payoff - 5: -5, 0, 15. Put-call parity: C - P = S - K e^(-rT) (European, no dividends, same strike and expiry). 1 payoffs, 1 profits, 1 parity.

**G3 (2).** Sharpe = (mean excess return) / (standard deviation of excess returns). Annualized = s * sqrt(252), assuming independent and identically distributed returns (no autocorrelation) and stable parameters. 1 + 1. Bonus remark: the estimate has sampling error and autocorrelation can make the scaling wrong.

**G4 (3).** Four of: look-ahead bias (uses information not yet available); survivorship bias (only assets that survived are tested); overfitting / data snooping / multiple testing (the best of many trials looks good by chance); ignoring costs and slippage/impact; unrealistic fills; using adjusted data inconsistently; selection of the sample period; non-stationarity; small sample. 0.75 each, round at the end.

**G5 (2).** The best of 200 trials on noise will look good by selection; the in-sample Sharpe is biased upward and the evidence for an edge is weak without correction. Ask: how many variants were tried in total; what is the out-of-sample or walk-forward result; transaction costs; whether adjustments for multiple testing (e.g. deflating the Sharpe ratio, a holdout touched once) were applied; economic rationale. 1 + 1.

**G6 (3).** Incoming buy 10 @ 102 limit crosses the asks: fill 4 @ 101 (the best ask), then 6 @ 102 (partial fill of the 8 resting). Trades occur at the resting order's price. Remaining incoming quantity 0. Book afterward: bids 100 x 10, 99 x 5; asks 102 x 2. 1 fills with prices and quantities, 1 trade at the resting price/priority, 1 book after.

---

## Interpreting results

1. Compute section percentages and apply the routing table in `DIAGNOSTIC.md`.
2. For each missed item, write the underlying gap in one line (for example "default evaluation time", "did not run code", "did not know `HAVING`") and group them. Three or more misses in one cluster justify a targeted remedial exercise before the relevant lesson. In a continuation session, ask for exercises generated from your cluster list (CONTINUE-HERE.md).
3. Compare predicted versus actual percentages (Part H3). Overconfidence (predicted well above actual) in a section means self-assessment there is unreliable: favor Mode A retests and external review in that volume. Underconfidence is also useful: you may be moving too slowly there.
4. Process signals matter as much as scores: items marked LOOKED UP, untested code, timing, and which sections you avoided.

## Limits of this diagnostic

It samples a small slice of each domain with short items. A high score can result from familiarity with common textbook problems; a low score can result from a bad day or an unfamiliar notation. Treat it as a first estimate and let the lesson mastery gates and the 14-day retests correct it. It is not a hiring-grade or certification instrument.
