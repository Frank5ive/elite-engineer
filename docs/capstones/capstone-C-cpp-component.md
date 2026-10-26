# Capstone C: High-Performance C++ Component

| Field | Value |
|---|---|
| Priority | P1/P2: the demonstration that you can write correct, measurable systems C++ rather than C++-flavored Python. |
| Mode | Build: A/B. C allowed only for build-system boilerplate, disclosed. Defense and reconstruction: A. |
| Time budget | 45-80 hours over 4-6 weeks, including profiling and sanitizer debugging. |
| Prerequisites (lessons) | 0.1, 0.2, 0.3, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 4.2, 4.4. Helpful: 6.2 (floating point), 6.5 (market data), 7.2. |
| Minimum versions | C++20 (flag any C++23 use explicitly), CMake 3.20+ (the minimum for preset schema version 2 with test presets, per the CMake presets manual), GCC 12+ or Clang 15+ (check what you have with `--version`), Catch2 or GoogleTest, Google Benchmark or a hand-written harness. |
| Deliverable | A library with a stable public header API, tests, sanitizer and fuzz/property runs, benchmarks with methodology, a profile-driven optimization report, design doc, and a defense. |

Attempt first. Reference notes: `../solutions/` after submission only.

## 1. Specification: a limit order book matching core

Build `libbook`, a single-instrument **limit order book** with price-time priority, the standard teaching component for performance-sensitive C++. The component receives a stream of commands (`add`, `cancel`, `modify`) and emits events (`ack`, `fill`, `reject`, `cancel_ack`). It is a library, not a trading system: no networking, no persistence beyond an optional replay log, no connection to any market.

If you prefer, substitute another component of equal depth (a fixed-capacity ring-buffer pipeline, a concurrent hash map, an arena-based expression evaluator, a time-series storage engine). You must write the substitute specification with the same sections first. Do not substitute something trivial; the component must contain a non-trivial invariant-bearing data structure, a hot path, and a memory management decision.

### 1.1 Functional requirements

1. Order types: limit (GTC and IOC) at minimum. Market orders optional; if included, specify behavior when the book is empty.
2. Matching: an incoming order matches against the opposite side best price first; within a price level, earliest arrival first. A trade executes at the resting order's price. Partial fills supported.
3. Cancel by order id: O(1) amortized lookup of the order, O(1) or O(log n) removal; document and test the actual complexity.
4. Modify: define the semantics precisely. A reasonable choice: reducing quantity keeps priority, anything else is cancel-replace and loses priority. State your choice in the spec and test both branches.
5. Prices are integers in ticks; quantities are integers. **No floating point for prices or quantities.** Overflow behavior must be defined (reject or checked arithmetic; never silent wrap).
6. Deterministic: identical input sequence yields byte-identical output sequence on every run and every platform you support. No dependence on pointer values, hash iteration order, or uninitialized memory.
7. Queries: best bid/ask, depth at a price, total resting quantity, order count; all const and side-effect free.
8. Invariants checkable by a debug-mode `verify()`: no crossed book at rest, per-level queues consistent with the aggregate quantity, the id index matches the book contents, no zero-quantity resting order.

### 1.2 Non-functional requirements

- Public API in a small header set with no implementation details leaking (pimpl or a narrow interface; justify the choice and cost).
- Zero undefined behavior under sanitizers on all tests, fuzz inputs and benchmarks.
- No heap allocation on the steady-state hot path **if you claim that property**; if you claim it, prove it (allocation counting hook in tests). If you do not claim it, measure allocations per command and report.
- Exception policy declared (for example: no exceptions in the hot path, errors returned as values); the public API documents which functions can throw.
- Thread-safety statement: the component is single-threaded by contract (the recommended design) or you document and test a specific concurrency model. If you add threads, you must justify them against a single-threaded design with a measurement and use the memory model correctly (5.6).

## 2. Architecture and interface requirements

- **Data structure decision (5.4):** You must choose, justify and compare at least two designs for the price-level container and the order storage. Examples: a sorted map of levels versus a flat array indexed by price offset from a reference price; intrusive doubly-linked list per level versus a contiguous vector per level with tombstones. Implement the simpler one first as the **reference implementation** (also used as a test oracle), then the optimized one. The oracle is required: differential testing between the two is the core of the testing strategy.
- **Ownership (5.2):** Document who owns each order object, where it lives, what the lifetime is, and how a cancel invalidates handles. Prefer indices or generation-checked handles to raw pointers into containers that can reallocate. Rule of zero where possible; if you write special members, state the rule of five reasoning.
- **Memory (5.6):** Choose and justify the allocation strategy: pool/slab of order nodes, arena per session, or the default allocator. A custom allocator is not mandatory and not automatically better; measure it. If you pool, define behavior on exhaustion (reject with a reason, grow, or abort) and test it.
- **Layout (5.6):** Show the layout of your hot structs (use `static_assert` on `sizeof`/`alignof` only where you rely on it; `sizeof` and `alignof` of your structs can differ across compilers and ABIs, so build the assertions on each compiler you support before committing to them). Explain at least one decision made for cache behavior and one you declined to make for lack of evidence.
- **Types (5.3):** Strong types for price, quantity, order id (distinct types, no implicit conversion between them). Use concepts or constrained templates only where they simplify; do not template everything.
- **Interface:** A command is a small value type; output is delivered through a caller-supplied sink (a template parameter, `std::function`, or an abstract interface; justify the cost of whichever you pick and measure it if the choice matters).
- **Build (5.1):** CMake targets for the library, tests, benchmarks, sanitizer presets, and a warning policy (`-Wall -Wextra -Wpedantic` plus `-Werror` in CI; these spellings are GCC/Clang, MSVC uses `/W4 /WX`). `compile_commands.json` generation documented. No dependency beyond the test and benchmark frameworks.

## 3. Milestones with checkpoints

| # | Milestone | Checkpoint evidence |
|---|---|---|
| M0 | Spec, invariants, and API header written first | Invariant list and complexity table committed before any implementation; header compiles standalone |
| M1 | Reference implementation (simple, obviously correct) | Unit tests green; `verify()` passes after every command in a randomized test |
| M2 | Build presets and CI | Debug, Release, ASan+UBSan, and TSan (if any threading) presets all configured; warnings-as-errors green |
| M3 | Differential and property tests, fuzzing | Random command generator with seed logging; failure reproduction via seed; a fuzz or property run of stated duration with no findings or documented findings |
| M4 | Benchmark harness and baseline | Reproducible benchmark with recorded environment, repeated runs, spread; baseline of the reference implementation |
| M5 | Optimized implementation | Passes the whole test suite and the differential test against the reference, bit-for-bit on outputs |
| M6 | Profile-driven optimization cycle (at least two iterations) | Profiler output (sampling profile and/or hardware counters if available), hypothesis, change, remeasurement, decision to keep or revert |
| M7 | Hardening | Overflow, exhaustion, invalid id, duplicate id, zero quantity, extreme price edge tests; static analysis pass (clang-tidy or equivalent, with disabled checks justified) |
| M8 | Documentation and defense preparation | Design doc, benchmark report, rubric self-score |

## 4. Acceptance criteria

1. All tests pass in Debug and Release with warnings-as-errors, and under AddressSanitizer plus UndefinedBehaviorSanitizer with zero reports. Run results and compiler versions recorded.
2. The optimized implementation and the reference implementation produce identical output on at least one million randomized commands across at least ten distinct seeds, including adversarial shapes (all cancels, one deep level, alternating cross, empty-book churn).
3. Determinism: two runs, and two builds (for example GCC and Clang, if both available), produce identical output hashes for the same input file. If a platform difference exists, you can explain it.
4. `verify()` passes after every command in the debug-mode randomized test.
5. Resource safety: constructing and destroying the book repeatedly shows no leaks (sanitizer or valgrind; both checked to report leaks and uninitialized reads on Ubuntu 24.04) and handles exhaustion deterministically.
6. Every public function has documented preconditions; violating a precondition in a debug build fails loudly (assert or contract check), and in release behaves as documented.
7. The benchmark is reproducible by a stranger from the README alone.

## 5. Testing requirements (4.2, 5.5)

- **Example-based tests** for each documented semantic: price-time priority across levels, partial fills across multiple resting orders, IOC remainder discarded, cancel of a filled order is rejected, modify branches.
- **Property tests / randomized differential testing:** generate command sequences from a seeded RNG; always log the seed; shrink failing sequences manually or by a small shrinker you write (halving the sequence is enough) so failures are debuggable.
- **Fuzzing:** a libFuzzer-style or AFL-style harness over a byte-stream decoder that turns bytes into commands (libFuzzer needs clang: `-fsanitize=fuzzer,address` checked with clang 18; GCC has no libFuzzer, use AFL++ or a plain randomized driver there). Run time stated. The corpus is committed if small.
- **Sanitizers:** ASan, UBSan always; TSan if any concurrency; MSan optional (clang only; checked with clang 18 on Linux x86-64, and results depend on the optimization level).
- **Mutation spot check:** deliberately reintroduce five bugs (off-by-one in a fill quantity, wrong side comparison, priority loss on modify-down, stale index after cancel, missed level erase) and record which tests catch each.
- **Allocation test** if you claim a no-allocation hot path.
- **Failure laboratory discipline (5.5):** for each sanitizer-detected defect you actually hit, a failure log entry with the diagnostic, root cause, and regression test. If you hit none, say so, and explain why you believe that is true rather than lucky.

## 6. Security and reliability expectations (4.3)

C++ turns input validation errors into memory-safety errors. Treat all commands as untrusted input: validate id uniqueness, quantity and price ranges before touching containers; bounds-check handles; avoid signed overflow (UB) by using checked or unsigned arithmetic with defined behavior, and test boundary values (max price, max quantity, quantity sum overflow across a level). Document the maximum sizes, and what happens when they are reached. No raw owning pointers in the public API. No `reinterpret_cast`-based parsing of byte input unless you can state the aliasing and alignment rules that make it valid (otherwise use `memcpy` or `std::bit_cast`, C++20). The replay log decoder, if present, must reject truncated or malformed input without UB.

Reliability: strong exception safety guarantee where you throw; noexcept on move operations where true (and verified by `static_assert` on `std::is_nothrow_move_constructible_v` where you rely on it); a defined behavior on allocation failure.

## 7. Performance criteria (methodology only)

You are not given a target number. A claim about speed in this capstone is valid only if it comes with all of the following:

1. **Workload definition:** the command mix (for example proportions of add/cancel/modify/cross), price distribution, book depth, and why that is a defensible model. Label it a synthetic assumption. Include at least two distinct mixes; an optimization that helps one and hurts another must be reported as such.
2. **Environment:** CPU model, core pinning if used, frequency governor state, compiler and version, flags, OS. Mention noise sources you did not control.
3. **Method:** warm-up, a number of repetitions, reporting median and a spread measure (min/max or interquartile range), not a single run. Prevent the compiler from deleting the work (use the benchmark library's facility, `benchmark::DoNotOptimize` in Google Benchmark 1.8.3) and verify by inspecting that outputs are consumed.
4. **Metrics:** throughput (commands per second) and latency distribution per command including tail percentiles; state clearly how latency was timed and the timer overhead.
5. **Profile before optimizing:** a sampling profile and, if the hardware permits, counters for cache misses and branch mispredictions (`perf`, VTune, or equivalents; `perf` may be denied permission to count events in containers, as observed). Every optimization cites the profile evidence that motivated it.
6. **Keep/revert rule:** an optimization is kept only if the improvement exceeds the run-to-run spread on the relevant workloads and does not damage correctness or readability disproportionately. Reverted attempts are reported as findings.
7. **Complexity versus constants:** show a scaling run (book depth versus time per command) that matches or contradicts your complexity table.
8. **Limits of the claim:** state what the benchmark does not show: real network jitter, contention, cold caches in production, realistic order flow.

Do not paste numbers from other people's articles and do not call anything "fast" without the comparison it is fast relative to.

## 8. Documentation requirements

- `README.md`: purpose, build presets, how to run tests, fuzzers, benchmarks.
- `docs/design.md`: invariants, complexity table, data structure comparison, ownership diagram, memory layout, determinism argument, error and exhaustion behavior.
- `docs/bench.md`: the benchmark report in the format of section 7, including negative results.
- `docs/adr/`: at least four: container choice, allocation strategy, API shape (sink design), error handling policy.
- `docs/failure-log.md`: 9-field entries.
- `docs/ai-use.md`: as in the other capstones. C++ has a particularly large space of plausible-but-wrong AI output (lifetime errors, iterator invalidation, UB in "optimized" code); list any you caught, and the tool (sanitizer, test, review) that caught it.

## 9. Final technical defense

**Format.** 60 minutes, no AI, repository plus cppreference. 10 minutes walkthrough, 35 minutes questions, 15 minutes live modification, which may include writing a small test or fixing a seeded defect with the debugger.

**Question bank:**

1. State the invariants of your book. Which are enforced by types, which by `verify()`, which only by discipline?
2. A cancel arrives for an order that was just fully filled. Walk the code path. What does the caller see?
3. Which iterator or reference invalidation hazards exist in your containers? Show the line where one would bite if the container reallocated.
4. Where does your implementation have undefined behavior if the caller breaks a precondition in a release build? Is that acceptable, and where is it documented?
5. Explain your memory layout for the order node. Why that field order? How did you verify the size?
6. Your optimized version is 25% faster on mix A and 8% slower on mix B (hypothetical). What do you do?
7. What did the profiler show first, and what did you change in response? What did you try that did not help?
8. Explain false sharing, and whether it can occur in your design. If you are single-threaded, say why that choice was correct.
9. Your fuzzer found nothing in an hour. What does that tell you and what does it not?
10. Why integers for price? Give a concrete failing example for floating point.
11. How does determinism break in C++ code in general (hash order, uninitialized padding, pointer comparison, floating-point reordering)? Which did you rule out and how?
12. Show the sanitizer finding you fixed (or explain why you had none). What would TSan or MSan have added?
13. Why did you choose this sink design? What does its abstraction cost, and how would you measure it?
14. What would you change if the book needed to support 100,000 distinct price levels sparsely populated versus 200 densely populated?
15. Which parts of your code were influenced by AI, and what did you have to correct?

## 10. No-AI reconstruction or extension challenge

Choose one by random draw:

- **R1 reconstruction (4-5 hours, Mode A/B with cppreference):** From a blank directory, with your invariants list and complexity table only, rebuild the reference implementation and the randomized `verify()` test. It must pass the test suite you originally wrote.
- **R2 extension (3-4 hours):** New requirement: add iceberg orders (displayed quantity smaller than total, replenishing with loss of time priority at that level) or stop orders. Specify semantics first, extend both implementations or the optimized one with the oracle updated, and keep every existing test green.
- **R3 debugging (2-3 hours):** A peer (or you from an earlier branch) plants a lifetime or invalidation bug in the optimized implementation that shows up intermittently. Reproduce with a seed or sanitizer, locate root cause, fix, write the regression test, and write the short postmortem (7.2).

## 11. The 100-point rubric

| Area | Points | Notes |
|---|---|---|
| Correctness and semantics | 15 | Matching rules, modify/cancel semantics, determinism |
| Memory safety and UB freedom | 15 | Sanitizers clean, bounds/overflow handled, lifetimes defensible |
| Design: invariants, ownership, API | 12 | Types, boundaries, simplest sufficient design |
| Testing: differential, property, fuzz, mutation | 15 | Oracle exists, seeds logged, shrinking, mutation spot check |
| Performance method and evidence | 15 | Section 7 satisfied; negative results reported; claims bounded |
| Build and tooling | 5 | Presets, warnings, CI reproducible |
| Documentation | 5 | Design, bench, ADRs |
| Technical defense | 10 | Specific, honest |
| No-AI reconstruction/extension | 8 | Completed and explained |
| **Total** | **100** | Pass: 80 or more and no critical failure |

**Critical failures:** any sanitizer report left unexplained in the submission; no reference/oracle implementation; floating-point prices; performance claims without method; non-deterministic output; use-after-free or invalidated iterator in a tested path; inability to explain code submitted as your own.

**If failed:** targeted remediation (for example, rebuild the reference implementation and differential harness from a blank file, or repeat the profile-driven optimization cycle on a different small component), then re-defense of the failed topics.

Ledger update: Capstone C to `Demonstrated` on pass; `Applied` when the component or its techniques have been used inside another project (Capstone E counts); `Production-ready` is not claimed for a library that has never run under real load and external review.
