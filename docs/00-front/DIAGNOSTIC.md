# Diagnostic Assessment

**Purpose:** find out what you can actually do today so that the roadmap compresses what you know and deepens what you do not. This is not a pass/fail test. A low score means "start here", not "unsuitable".

**Rules:** Mode A. Closed-book, no AI, no internet, no running code for the *prediction* questions (predict first; you may run the code afterward for your own curiosity but do not change your answers). For the *coding challenges* you may use an editor, a Python interpreter, a PHP interpreter, a C++ compiler and a database you set up yourself, but no documentation sites, no AI, no searching. If you must look something up, write "LOOKED UP" beside the answer and score it zero for that item; that is information, not punishment.

**Time:** about 3.5 to 4.5 hours total. Take it in two sittings (sections A-D, then E-G) with a good night of sleep between. Set a timer per section; stop when it rings and mark unfinished parts. Unfinished is information.

**Do not read `DIAGNOSTIC-ANSWER-KEY.md` before finishing and writing your self-estimate (Part H).**

**Answer location:** create `progress/diagnostic/` and put your answers in files named by question id (`A7.py`, `B2.sql`, `D4.md`, and so on). Short answers can go in `answers.md`.

**Points:** A 30, B 20, C 20, D 20, E 25, F 20, G 15. Total 150 (self-report is unscored).

---

## Section A: Python and FastAPI (30 points)

**A1 (2).** Predict the exact output.
```python
def f(x, acc=[]):
    acc.append(x)
    return acc

print(f(1))
print(f(2))
print(f(3, []))
```

**A2 (2).** Predict the output and explain in one sentence.
```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])
```

**A3 (2).** Predict the output.
```python
g = (x * x for x in range(3))
print(list(g))
print(list(g))
```

**A4 (2).** Predict the output.
```python
a = [1, 2]
b = a
b += [3]
c = a
c = c + [4]
print(a, c)
```

**A5 (3). Coding.** Write a context manager `timed(label, sink)` (using `contextlib` or a class) that appends `(label, elapsed_seconds)` to the list `sink` when the block exits, **including when the block raises**, and does not suppress the exception. Include a short test (assert the entry exists after an exception propagates).

**A6 (2).** What does `g()` return, and what happens to an exception raised in the `try`?
```python
def g():
    try:
        raise ValueError("boom")
    finally:
        return "finally"
```

**A7 (4). Coding.** Using FastAPI and Pydantic v2, write an `app` with `POST /items` that accepts JSON `{"name": str, "price": number}`. Rules: `name` must be 1 to 50 characters after stripping whitespace; `price` must be greater than 0. Store items in an in-memory dict keyed by name. Return 201 with the stored item on success, 409 with a JSON error body if the name already exists. Show the Pydantic model and the endpoint. State what status FastAPI returns by default for a body that fails validation.

**A8 (3).** In FastAPI, what is the difference between declaring an endpoint with `def` and with `async def`? What happens to other requests if an `async def` endpoint calls `time.sleep(5)`? Give two ways to fix it.

**A9 (3). Coding.** Write `slugify(text: str) -> str` (lowercase, collapse runs of non-alphanumeric characters into a single hyphen, strip leading and trailing hyphens) **and** a parametrized pytest test with at least five cases including empty string and unicode letters (state what your function does with `"Café"`).

**A10 (3).** Write a FastAPI dependency `get_db` that yields a database session object and always closes it afterward, use it in an endpoint, and show how a test replaces it with a fake.

**A11 (2).** Give the conventional HTTP status code for each: resource created; request is syntactically valid JSON but fails validation (FastAPI default); missing/invalid credentials; authenticated but not allowed; conflicts with current state.

**A12 (2).** What does `python -m venv .venv` create, and why pin dependency versions in a project?

---

## Section B: Databases (20 points)

Schema for B1-B4 (PostgreSQL syntax assumed; state if you assume another):
```
students(id PK, name)
courses(id PK, title)
enrollments(student_id FK, course_id FK, status TEXT, enrolled_at TIMESTAMPTZ, PRIMARY KEY (student_id, course_id))
```

**B1 (3). Coding.** Write a query listing courses that have **no** enrollments.

**B2 (3). Coding.** Write a query returning the top 3 courses by number of enrollments with `status = 'active'`, only courses having at least 5 such enrollments, ties broken by course id.

**B3 (2).** What is the difference between `WHERE` and `HAVING`? What does `WHERE status = NULL` return and why?

**B4 (3).** The hot query is:
```sql
SELECT student_id FROM enrollments
WHERE course_id = $1 AND status = 'active'
ORDER BY enrolled_at DESC LIMIT 20;
```
Propose one index, justify the column order, and say what you would check to confirm the database uses it.

**B5 (3).** The following is an illustrative `EXPLAIN ANALYZE` excerpt (invented for this question, not a real measurement). Diagnose the issue and give your next three actions.
```
Seq Scan on enrollments  (cost=0.00..18334.00 rows=12 width=40) (actual time=0.031..95.4 rows=15 loops=1)
  Filter: (student_id = 42)
  Rows Removed by Filter: 999985
Execution Time: 95.5 ms
```

**B6 (3).** Two concurrent requests each run: read balance (100), compute balance - 30, write the result. What is the final balance, what is the anomaly called, and give two different ways to fix it.

**B7 (2).** Why is `OFFSET`-based pagination problematic on large, changing tables? Write the keyset alternative for "newest first by `(created_at, id)`, 20 per page".

**B8 (1).** In one sentence, what does the "I" in ACID promise, and why do isolation levels exist?

---

## Section C: PHP and Moodle (20 points)

**C1 (2).** Predict the output (PHP 8.x).
```php
var_dump(0 == "a");
var_dump("1" == "01");
var_dump(null ?? "x");
```

**C2 (2). Coding.** Write a PHP 8.2 class `Money` with constructor-promoted `readonly` properties `int $amountMinor` and `string $currency`, and a method `add(Money $other): Money` that throws if currencies differ.

**C3 (2).** What does PSR-4 autoloading with Composer do? Where is it configured?

**C4 (3).** In a Moodle plugin, name the file or directory used for: the plugin version/component declaration; capabilities; language strings; the database schema at install; database upgrade steps.

**C5 (3).** A plugin page must only be visible to logged-in users who may view the activity. Name the Moodle functions you would call and the context you would pass. List Moodle's context levels.

**C6 (3). Coding.** Write PHP using the Moodle `$DB` API to fetch the user with a given id, and then a `get_records_sql` call using a named placeholder to fetch all users whose lastname equals a variable. Explain why placeholders matter and how table names are written in raw SQL.

**C7 (2).** What is `sesskey` for, and name three ways Moodle code should produce safe HTML output of user-supplied text.

**C8 (3).** Describe which files and classes you create to add a scheduled task and an event observer to an existing plugin, and what you must do so Moodle registers them.

---

## Section D: Engineering practice (20 points)

**D1 (3).** You committed an API key into a feature branch. Case 1: not pushed. Case 2: pushed to a shared remote. State what you do in each case and what is different.

**D2 (3).** Explain merge versus rebase and one situation where you must not rebase. Give the commands you would use to find which commit introduced a regression using binary search.

**D3 (3). Writing.** A change adds a `retry` with exponential backoff to an outbound call and a new test. Write a pull request description (title, what, why, how tested, risks, rollback). Keep it under 150 words.

**D4 (3). Code review.** List at least five distinct problems in this snippet, most severe first.
```python
import requests, sqlite3

def get_user(name):
    conn = sqlite3.connect("app.db")
    cur = conn.execute("SELECT * FROM users WHERE name = '" + name + "'")
    row = cur.fetchone()
    try:
        r = requests.get("http://svc/profile/" + name)
        return {"row": row, "profile": r.json()}
    except:
        return None

def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

**D5 (3). Writing.** You have been blocked for two hours on a failing integration test and your lead is in meetings until afternoon. Write the message you send (under 120 words).

**D6 (3).** A test passes locally and fails in CI roughly one run in five. List your first three actions and your ordered hypotheses.

**D7 (2).** What makes a test flaky, and what does the test pyramid say about where most tests should be and why?

---

## Section E: C++ and algorithms (25 points)

(C++20 assumed. You may answer E6 and E7 in C++ or in Python; C++ answers earn the same points but record which language you chose. If you have never written C++, write "none" and skip E1-E4 and E8-E9; score honestly.)

**E1 (3).** What is wrong with this function, and what is the language-level consequence?
```cpp
const std::string& name() {
    std::string s = "abc";
    return s;
}
```

**E2 (3). Coding.** Write a class `File` owning a `FILE*` (opened in the constructor, closed in the destructor), non-copyable, movable. Show the move constructor and move assignment, leaving the source in a safe state.

**E3 (3).** What is wrong here?
```cpp
std::vector<int> v{1, 2, 3};
auto it = v.begin();
v.push_back(4);
std::cout << *it;
```

**E4 (2).** When do you choose `unique_ptr`, when `shared_ptr`, and when is a raw pointer or reference acceptable?

**E5 (3).** Give typical time complexity (average, and worst case where different) for: `std::vector` insert at front; `std::unordered_map` lookup; `std::map` lookup; `std::sort`; `std::deque::push_front`.

**E6 (4). Coding.** Given a vector of integers and a target, return the indices `i < j` of a pair summing to the target, or report none. Single pass, O(n) expected time. Handle duplicates and negative numbers. State complexity and one failure mode (what you assume about the input).

**E7 (3). Coding.** Implement `lower_bound(vec, x)`: the index of the first element not less than `x` in a sorted vector, or `size` if none. State the loop invariant in a comment. Avoid the classic overflow in the midpoint computation or say why it cannot occur in your language.

**E8 (2).** What is the difference between `const int* p` and `int* const p`?

**E9 (2).** Define undefined behavior. Give two examples and name the sanitizers that detect them.

---

## Section F: Mathematics (20 points)

**F1 (2).** Two fair six-sided dice are rolled. Probability the sum is 7?

**F2 (3).** A condition has prevalence 1%. A test has sensitivity 90% and false positive rate 5%. A person tests positive. Probability they have the condition? Show the steps.

**F3 (2).** Expected value and variance of one fair six-sided die roll.

**F4 (3).** For `A = [[2, 1], [1, 3]]` and `x = [1, 2]`, compute `Ax` and `det(A)`. What does `det(A) = 0` tell you about a square matrix?

**F5 (2).** Differentiate `f(x) = x^2 * e^x`. In one sentence, what does gradient descent do with a derivative?

**F6 (3).** Why does `0.1 + 0.2 == 0.3` fail in IEEE double precision, how should you compare floating-point numbers, and what is catastrophic cancellation (give an example)?

**F7 (2).** For independent random variables with variance s^2, what is the variance of their sum of two, and of the mean of n of them?

**F8 (3).** State precisely what a p-value is (and what it is not), what a 95% confidence interval means, and the probability of at least one false positive across 20 independent tests at the 5% level.

---

## Section G: Quantitative finance (15 points)

**G1 (2).** A price goes 100 -> 110 -> 99. Give the two simple returns, the total simple return, and the total log return. Why is the average of the two simple returns misleading?

**G2 (3).** A long European call, strike 100, premium paid 5. Give payoff and profit at expiry for S = 90, 105, 120. State put-call parity for European options without dividends.

**G3 (2).** Define the Sharpe ratio. Daily Sharpe is s; state the usual annualization with 252 days and the assumption it relies on.

**G4 (3).** List four biases or errors that inflate backtest results, and for each say in one line how it inflates them.

**G5 (2).** A researcher tried 200 parameter sets on the same historical data and reports the best, with an in-sample Sharpe of 2. What do you conclude, and what would you ask?

**G6 (3).** Order book. Bids: 100 x 10, 99 x 5. Asks: 101 x 4, 102 x 8. An incoming buy limit order for 10 at price 102 arrives. Under price-time priority, list the fills (price, quantity), the remaining order, and the book afterward.

---

## Part H: Self-report (unscored, used for routing and calibration)

Answer before reading the key.

**H1. Background.** Years of professional experience; how many weeks per year you work with each of Python, SQL, PHP, Moodle, C++, statistics: __.

**H2. Confidence (1 = no idea, 5 = can do without help).** Rate each: Python language internals __; FastAPI __; SQL and schema design __; query performance __; transactions __; PHP __; Moodle plugin dev __; Git beyond basics __; reading unfamiliar code __; debugging method __; writing tests __; C++ memory and lifetime __; algorithms __; probability __; statistics __; linear algebra __; options and risk __; backtesting __.

**H3. Predicted scores.** Predict your percentage per section A-G before grading: __. The gap between predicted and actual is your calibration error; large positive gaps in a section mean you overestimate yourself there and should treat that area more cautiously.

**H4. Habits.** Do you write tests first, after, or never? Do you keep a log of mistakes? Do you review your own diffs before pushing? Typical hours per week available: __. Typical sleep: __.

**H5. Goals.** What do you hope to do in 3 months, 12 months, 24 months (work tasks, skills, roles)? Which volume matters most to you now? __

**H6. Constraints.** Fixed commitments, known stressors, weeks you will be unavailable. __

**H7. Previous AI usage.** For which tasks do you currently reach for AI first? Which of those could you do without it? __

---

## Part I: Scoring and routing

Score each section with the answer key. Convert to a percentage per section (`section score / section maximum`). Record in `progress/diagnostic/scores.md`.

| Section | Max | Your score | Percent |
|---|---|---|---|
| A Python/FastAPI | 30 | | |
| B Databases | 20 | | |
| C PHP/Moodle | 20 | | |
| D Engineering practice | 20 | | |
| E C++/algorithms | 25 | | |
| F Mathematics | 20 | | |
| G Quant finance | 15 | | |
| Total | 150 | | |

**Routing table (applied per section, to the matching volume):**

| Section percent | Route | What to do |
|---|---|---|
| Below 40% | Foundation | Do every lesson in the matching volume in full and in order. Add the lesson's remedial exercises even if you pass the gate. Expect the high end of the time estimates. For C++ with no experience, go straight to Vol 5 only after Vol 1 is Demonstrated. |
| 40% to 69% | Standard | Do the lessons as written. Skim sections you can already state from memory, but do not skip retrieval, the failure laboratory, or the project. |
| 70% to 84% | Accelerated | Attempt each lesson's mastery gate project first (section 11) from a blank file. If you pass, mark "Demonstrated" and read only the lesson sections covering what you missed. If you fail, do the lesson in full. |
| 85% and above | Test-out | Attempt the mastery gate cold; if you pass at 80 or more with no critical failure, mark "Demonstrated" and move on. You still do the capstone for that area and still do the 14-day retest. Testing out is permission to move quickly, not to skip evidence. |

**Section-to-volume mapping:** A -> Vol 1 and 2.2, 2.6, 2.7; B -> 2.3, 2.4; C -> Vol 3; D -> Vol 0, 1.4, Vol 4; E -> Vol 5; F -> 6.1-6.3; G -> 6.4-6.5.

**Overrides:**
- Vol 0 (job readiness) is P0 and is always done in the first week regardless of score; its gates can be passed quickly.
- If your calibration error (predicted minus actual) exceeds 20 percentage points in a section, treat that section's route as one level more cautious and prefer Mode A retests.
- If your job is primarily Moodle/PHP, move Vol 3 forward as described in `ROADMAP.md` regardless of Section C, unless Section C is 85% or higher.
- Section B below 50% blocks Capstone A work: complete 2.3 and 2.4 gates first.
- Section F or G below 40% means Vol 6 starts with the foundations of 6.1 and 6.2 and you should not begin Capstone D until 6.1-6.3 are Demonstrated.

**Combine the data.** Write a one-page summary in `progress/diagnostic/summary.md`: strongest and weakest three topics, calibration gaps, routing per volume, and the first-12-weeks adjustments you propose. In a continuation session, ask for it to be reviewed (see `CONTINUE-HERE.md`).
