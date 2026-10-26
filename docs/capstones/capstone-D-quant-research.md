# Capstone D: Quantitative Research System

| Field | Value |
|---|---|
| Priority | P2: the demonstration of research discipline, separate from the P0/P1 job-readiness track. |
| Mode | Build: A/B for core math and engine; C allowed for plotting and boilerplate with disclosure. Defense and reconstruction: A. |
| Time budget | 50-90 hours over 5-8 weeks, including statistical analysis and writing. |
| Prerequisites (lessons) | 0.3, 1.1-1.4, 6.1, 6.2, 6.3, 6.4, 6.5, 4.2, 4.4. Helpful: 5.3, 5.4 (if a C++ kernel is used), 7.2. |
| Minimum versions | Python 3.12, NumPy, pandas, SciPy (VERIFY current versions and pin them), pytest. Optional C++20 kernel (Capstone C techniques). |
| Deliverable | A reproducible research repository: data pipeline, backtest engine, risk and cost model, statistical validation, a written research report with a limitations section, tests, and a defense. |

Attempt first. Reference notes: `../solutions/` after submission only.

## 0. Non-negotiable statements

1. **This capstone does not ask you to build a profitable strategy, and you must not claim that you did.** Most simple strategies tested on historical data show no edge after costs; a clean negative result with sound methodology scores higher than a fragile positive one.
2. **Forbidden claims.** The report, README, and defense must not contain statements that the strategy is or will be profitable, that it "works", that it has an "edge" demonstrated beyond the stated statistical evidence, that results predict future performance, or that it is suitable for trading real money. Phrases to use instead: "in this sample, under these assumptions, the estimated mean excess return was X with a confidence interval of Y; this is not evidence of future profitability." A submission containing a profitability claim fails with a critical failure regardless of the numbers.
3. **Stated limitations are mandatory** (section 8). A report without a substantive limitations section is not accepted for defense.
4. **Not financial advice, not for trading.** The system is an educational research tool. It does not connect to brokers or exchanges.
5. **Data honesty.** Use only data you are licensed to use. Synthetic data is permitted and encouraged for correctness tests; real or realistic historical data may be used for the research part, with its source, license, adjustments, and known problems documented.

## 1. Specification: a single-factor cross-sectional or single-asset research study

Choose one research question of this form and write it, with a pre-registered hypothesis, **before** looking at any out-of-sample data. Examples (illustrative, not endorsements): "Does a simple moving-average crossover on a daily series have a statistically distinguishable mean excess return after costs?"; "Does a 12-1 month return rank predict next-month cross-sectional return in a small universe, after costs?"; "Is realized volatility predictable one step ahead by a simple autoregressive model, and does a volatility-scaled position improve risk-adjusted return versus a constant position?" Prefer a question for which a null result is informative.

The system consists of five parts: **data layer** (ingest, clean, adjust, store, versioned snapshot); **signal layer** (pure functions from information available at time t to a position decision for t+1); **simulation layer** (event-ordered or vectorized backtest with a fill, cost and timing model); **evaluation layer** (performance and risk statistics, uncertainty quantification, multiple-testing accounting); **reporting layer** (reproducible tables, figures and a written report).

### 1.1 Functional requirements

1. **Point-in-time discipline.** Every signal at time t uses only data timestamped at or before t (account for publication lag where relevant). A deliberately leaking variant (using t+1 data) must exist in the tests to prove your leak detector catches it.
2. **Execution timing model.** State when a decision is made, when an order is assumed to fill, and at what price (for example decide at close, fill at next open; or fill at next close). Justify the assumption. Test that no fill uses information unavailable at decision time.
3. **Cost model.** Explicit commission, spread or slippage and, if shorting, a borrow-cost assumption, each as a documented parameter. Report results at zero cost and at stated costs; run a sensitivity analysis across a range of cost assumptions. Costs are assumptions, label them.
4. **Position and risk limits.** Maximum leverage, a no-short or short-allowed flag, and handling of missing data and halted instruments.
5. **Accounting.** Returns computed correctly (simple vs log, compounding, handling of cash and leverage) with a reconciliation test: portfolio value path equals the cumulative sum of per-period PnL within tolerance.
6. **Corporate actions and survivorship.** State how splits, dividends and delistings are handled, whether the data are survivorship-biased, and how that biases the result (usually upward).
7. **Reproducibility.** One command regenerates all tables and figures from a pinned data snapshot; random seeds recorded; library versions pinned; results hash recorded.

### 1.2 Statistical requirements (6.1-6.3)

- Report point estimates **with uncertainty**: confidence intervals via a method suited to autocorrelated financial series (for example a block bootstrap; VERIFY the method and the block-length rationale; do not use iid assumptions silently), and a plain statement of which assumptions each interval relies on.
- **Multiple testing accounting:** count every variant you tried (parameters, universes, filters, windows), including abandoned ones, in a research log. Apply and describe an adjustment or at minimum report the number of trials and explain how it inflates the best result's apparent significance. Hiding failed trials is a critical failure.
- **Out-of-sample protocol:** a holdout period (or walk-forward scheme) fixed before analysis and touched once per final model. Describe exactly how you prevented yourself from peeking; a record of the number of times the holdout was evaluated is required.
- **Regime and stability:** results split by sub-period and, where meaningful, by volatility regime, reported as is, including unfavorable sub-periods.
- **Benchmarks and nulls:** compare against a naive baseline (buy-and-hold, a constant position, or a randomized-signal null distribution generated by shuffling or random entries) so the result is interpreted relative to what chance and market drift alone produce.
- **Risk metrics:** volatility, maximum drawdown with duration, tail measures with the estimation method named (for example historical expected shortfall and the sample-size caveat), and the Sharpe ratio reported with its sampling error and its dependence on return frequency and autocorrelation (no annualization without stating the assumption).
- **Separate mathematical correctness from implementation correctness (STYLE-GUIDE rule):** the mathematics of an estimator (is it unbiased, what does the CLT give) and the correctness of your code for it (does it match a hand-computed small example, does it match a trusted library on random input) are verified separately and documented separately.

## 2. Architecture and interface requirements

- A package with an importable library and thin scripts; no logic in notebooks. Notebooks, if used, only call the library and display results, and are re-run top to bottom in CI or a documented check.
- Pure functions for signals and metrics (inputs: arrays/frames; outputs: arrays/frames), easy to test. Side effects (file I/O, network) only in the data layer.
- Typed interfaces (1.3): frames with documented column contracts; validation at the data layer boundary (monotonic timestamps, no duplicates, no NaN where forbidden, timezone-explicit).
- Time handling: explicit timezone, explicit calendar, no implicit local time; daylight saving and missing-session handling documented.
- Floating point (6.2): state where you rely on tolerances (`np.isclose` parameters justified), where accumulation order matters, and use stable summation or compensated methods where an error would matter; test against high-precision or exact small cases.
- Optional performance kernel: if the simulation is slow enough that you want a C++ kernel (Capstone E rules apply), you must first profile the Python version and justify.

## 3. Milestones with checkpoints

| # | Milestone | Checkpoint evidence |
|---|---|---|
| M0 | Research question, hypothesis, success/failure criteria, holdout rule, written and committed | Dated commit before any analysis; the hypothesis states what result would count as a null |
| M1 | Data layer with validation and snapshot | Validation test suite incl. malformed-data cases; data dictionary; known-issues list |
| M2 | Accounting core and cost model on synthetic data | Hand-verified toy example (3 assets, 5 days) reproduced by tests; reconciliation test |
| M3 | Signal layer and leak detector | Leaking variant fails the point-in-time test; non-leaking passes |
| M4 | Evaluation layer with uncertainty | Estimators tested against closed-form results on simulated data with known parameters (for example, recover a known mean and a known zero-edge null) |
| M5 | Null calibration | On simulated data with **no** edge, run the full pipeline many times and show the false-positive rate is near the nominal level, or explain why not |
| M6 | Real-data study on the in-sample portion | Research log complete with all trial counts |
| M7 | Single holdout evaluation | Result recorded once, whether or not it is favorable |
| M8 | Report, limitations, defense preparation | Written report per section 8; rubric self-score |

M5 is the center of the capstone: a pipeline that finds "significant" edge in pure noise is broken, no matter how good the real-data chart looks.

## 4. Acceptance criteria

1. One command reproduces every number and figure in the report from the pinned snapshot, and the results hash matches.
2. Tests pass: accounting reconciliation, point-in-time leak detection, timing model, cost model, statistical estimators against known-answer simulations.
3. The null calibration experiment (M5) is included in the report with its result, whether favorable or not.
4. The research log lists every variant tried and the number of looks at the holdout.
5. Results are shown at multiple cost assumptions and sub-periods, with uncertainty intervals.
6. The report contains the limitations section in section 8 and contains no forbidden claim from section 0.
7. Every figure has labeled axes, units, sample period and a one-sentence statement of what it does and does not show.

## 5. Testing requirements (4.2, 1.4)

- **Known-answer tests:** small hand-computed examples with exact expected values for PnL, drawdown, turnover, and cost.
- **Property tests:** invariants such as "zero positions produce zero PnL", "doubling costs never increases net return", "scaling all prices by a constant leaves returns unchanged", "permuting instrument order leaves portfolio results unchanged".
- **Simulation tests for estimators:** generate data from a known process, check that an estimator recovers parameters within sampling error over repeated draws, with seeds fixed and the tolerance justified statistically (not by trial and error until green).
- **Leak tests:** adversarial constructions in which a future-peeking signal would appear spectacular; the pipeline must flag or the test must show the discrepancy between leaking and non-leaking variants.
- **Data tests:** timezone shifts, duplicate timestamps, missing days, a split not adjusted, a NaN burst; each must raise, be repaired by a documented rule, or be reported.
- **Regression of results:** a golden-results test with tolerance, updated only intentionally with a changelog entry.
- **Mutation spot check:** break five items (off-by-one lag, wrong sign on cost, using close instead of next open, compounding vs summing, annualization factor) and record which tests catch each.

## 6. Security and reliability expectations (4.3)

Defensive scope only. Data files are untrusted inputs: validate schema and ranges, do not `eval` or unpickle untrusted files (use CSV/Parquet with explicit dtypes; VERIFY the loader's behavior), and do not store API keys in the repository. Reproducibility is the reliability property of a research system: pinned dependencies, recorded seeds, immutable snapshots, deterministic ordering, and an explicit statement of any nondeterminism (parallel reductions, library thread counts). The pipeline fails loudly on data problems rather than silently dropping rows; every dropped row is counted in a data-quality report.

## 7. Performance criteria (methodology only)

Performance is secondary to correctness here. If you optimize anything:

1. Profile the pipeline first (4.4) and report where time goes; vectorize the dominant step, not the one you suspect.
2. Report run time with environment, dataset size, repetitions and spread.
3. Prove that the optimized code produces results equal within a stated tolerance to the slow reference on the same inputs (the slow version stays in the test suite as an oracle).
4. State scaling behavior (instruments x days) from a measured sweep, not an assumption.

No claim about real-time suitability. This is a research system.

## 8. Documentation requirements, including the mandatory limitations section

- `README.md`: question, how to reproduce, data provenance and license, versions.
- `docs/report.md`: Abstract (question, method, result in one honest sentence); Data; Method; Results with uncertainty; Null calibration; Sensitivity (costs, parameters, sub-periods); Discussion; **Limitations**; Conclusion; Appendix (research log, data-quality report).
- **Limitations section requirements:** it must address, specifically for your study and not generically, each of the following, or state explicitly why one is not applicable: (a) sample size and number of independent observations; (b) multiple testing and the researcher's degrees of freedom; (c) survivorship, look-ahead and selection bias in the data; (d) the realism of the fill and cost model, market impact and capacity ignored; (e) regime dependence and non-stationarity; (f) estimator assumptions (independence, distributional) and where they are violated; (g) data quality and vendor adjustments; (h) the statement that no result here is evidence of future profitability; (i) what additional evidence would be needed before anyone should consider the idea further, and why even that would not guarantee a result.
- `docs/adr/`: at least three: execution timing model; interval estimation method; data snapshot and versioning.
- `docs/research-log.md`: every trial, with date, parameters and outcome.
- `docs/failure-log.md`: 9-field entries, including any bias you discovered in your own work.
- `docs/ai-use.md`: AI frequently produces look-ahead bias, wrong annualization, and impressive-sounding but unjustified statistics; record any you caught.

## 9. Final technical defense

**Format.** 60 minutes, no AI, repository and standard documentation. 10 minutes walkthrough of the question and method, 35 minutes questions, 15 minutes live modification or live analysis of a supplied small dataset.

**Question bank:**

1. State your null hypothesis and what result would have made you abandon the idea. Where is that written and when was it committed?
2. Walk through one trade from signal calculation to fill to PnL. Which timestamps are involved?
3. Show how your pipeline prevents look-ahead bias. Show the leak test and explain why it would fail on a leaking signal.
4. How many variants did you try? How does that number change the meaning of your best result?
5. Why this confidence interval method? Which assumption would break it, and how would the interval change?
6. What does your Sharpe ratio estimate mean, and what is its standard error approximately? Why is annualizing by the square root of 252 not always valid?
7. Your null calibration result: what did it show, and what would a failed calibration have meant?
8. Which cost assumption has the largest effect on the result? Show the sensitivity.
9. Explain survivorship bias in your dataset and the direction of its effect.
10. Distinguish a mathematical error from an implementation error with an example from your own project.
11. Where does floating-point error matter in your code, if at all? Show a test.
12. If your result is positive, give three reasons it might be spurious. If negative, give two reasons it might be a false negative.
13. What would you need to see before considering this idea worth deeper research, and what would still not make it trading-ready?
14. What did AI suggest (if used) that was statistically or logically wrong?

An answer containing a profitability claim, or a defense of the strategy as likely to make money, ends the defense with a critical failure.

## 10. No-AI reconstruction or extension challenge

Choose one by random draw:

- **R1 reconstruction (4-5 hours, Mode A/B):** From a blank directory, with only the written method section and a supplied small price file, reimplement the accounting core, cost model and one metric (drawdown and an interval estimate of mean return), and reproduce your report's headline table within tolerance.
- **R2 extension (3-4 hours):** Add a new requirement: transaction costs proportional to turnover with a quadratic impact term, or a second asset class with a different calendar. Specify semantics, update tests first, re-run null calibration, and explain how conclusions change.
- **R3 audit (2-3 hours):** Given a supplied backtest (peer-prepared or from your earlier failure log) containing at least four planted flaws (look-ahead, wrong annualization, survivorship, untracked trial count, cost omitted), find and rank them, quantify the effect of at least two by fixing them, and write the corrected conclusion.

## 11. The 100-point rubric

| Area | Points | Notes |
|---|---|---|
| Research design and pre-registration | 10 | Question, null, holdout protocol, written before analysis |
| Implementation correctness (accounting, timing, costs) | 15 | Known-answer and property tests |
| Bias control (look-ahead, survivorship, multiple testing) | 15 | Leak tests, research log, trial accounting |
| Statistical methodology and uncertainty | 15 | Intervals suited to dependence, null calibration, honest metrics |
| Reproducibility and engineering quality | 10 | One command, pinned versions, structure, tests |
| Limitations section and honesty of claims | 15 | Specific, complete, no forbidden claims |
| Documentation and reporting | 5 | Figures, report, ADRs |
| Technical defense | 10 | Specific, honest |
| No-AI reconstruction/extension | 5 | Completed and explained |
| **Total** | **100** | Pass: 80 or more and no critical failure |

**Critical failures:** any claim or implication of profitability or future performance; missing or generic limitations section; undisclosed trials or repeated holdout evaluation; look-ahead bias in the submitted pipeline; no null calibration; unreproducible results; annualized figures with no stated assumptions presented as conclusions; inability to explain code or statistics submitted as your own.

**If failed:** targeted remediation by weakest area (for example, a smaller study repeated from a blank repository with a different null question and full trial accounting, or a rebuild of the accounting core with known-answer tests), then re-defense of failed topics.

Ledger update: Capstone D to `Demonstrated` on pass. `Production-ready` is not an attainable status for a research study; the highest honest status here is `Applied` after the methods have been reused in a second study with independent review.
