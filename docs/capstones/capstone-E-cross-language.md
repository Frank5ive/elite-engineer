# Capstone E: Cross-Language Integration

| Field | Value |
|---|---|
| Priority | P2: integrates the Python, C++ and (optionally) service tracks; do last. |
| Mode | Build: A/B. C allowed for binding boilerplate only, disclosed. Defense and reconstruction: A. |
| Time budget | 40-70 hours over 4-6 weeks, including packaging and debugging across the boundary. |
| Prerequisites (lessons) | 1.1-1.4, 2.6, 2.7, 4.1, 4.2, 4.3, 4.4, 5.1-5.6; Capstone C recommended (reuse its component); Capstone A or D recommended (the Python side). Helpful: 6.5, 7.2. |
| Minimum versions | Python 3.12, C++20, CMake 3.20+ (VERIFY), the binding or IPC technology you choose (VERIFY its current version and documentation before depending on it). |
| Deliverable | A working system in which Python and C++ cooperate across a boundary, with a written justification for that boundary, a measured comparison against the no-boundary alternative, tests on both sides and across, packaging and deployment instructions, and a defense. |

Attempt first. Reference notes: `../solutions/` after submission only.

## 0. The central requirement: justify the boundary

The most common mistake in multi-language systems is crossing the language boundary because it is interesting, not because it is necessary. Every boundary costs: serialization or marshalling, two build systems, two toolchains in CI, two sets of failure modes, harder debugging, harder onboarding, and an ABI or protocol that must be versioned. A capstone that does not **earn** its boundary does not pass, however well it is built.

You must submit `docs/boundary-justification.md` **before writing integration code** (milestone M0), containing:

1. **The problem and the alternatives.** At least three alternatives that avoid or reduce the crossing: (a) pure Python with the best available idiom (vectorization, a mature existing library, better algorithm or data structure); (b) pure C++ end to end; (c) a different split point. State why each is rejected or accepted, with evidence, not taste.
2. **A measured baseline.** The pure-Python implementation is written first (the reference) and profiled (4.4). The justification must show that the hot spot you want to move to C++ is the dominant cost in the profile, with the method and spread. "Python is slow" is not evidence.
3. **An expected benefit with a bound.** Using the profile, compute the **upper bound** on end-to-end improvement if the hot spot became free (the Amdahl bound; the speedup cannot exceed 1/(1-p) where p is the fraction of time spent in the moved code). If that bound does not justify the added cost in your own judgment, say so and either change the problem or stop. A defensible capstone can conclude: "the boundary is justified for these workloads only, and not for these."
4. **The costs, enumerated** (section 3 below), with your estimate of each for this project.
5. **A decision record** (ADR) with consequences, and the conditions under which you would collapse the boundary back.
6. **A non-performance justification, if that is the reason.** Valid reasons also include reusing an existing, trusted C++ library, a hard memory or latency requirement Python cannot meet, or an organizational constraint. State it. Invalid reasons: resume, curiosity, "C++ is faster" with no profile.

A negative outcome is acceptable and valued: if you measure and find the boundary is not worth it, the deliverable is the measurement, the reference implementation, a prototype of the boundary, and a reasoned recommendation not to adopt it, still with all documents and a defense. In that case, the rubric's integration-quality items are scored on the prototype, and the justification items carry the weight.

## 1. Specification: a Python service with a C++ computational kernel

The default specification uses the book's other components. Replace it with your own if the justification document supports it.

**Default:** A Python application (a FastAPI service from Capstone A, or the research pipeline from Capstone D) calls a C++ kernel (the order book from Capstone C, or a numerically intensive kernel such as pairwise distance, rolling statistics over millions of points, Monte Carlo path simulation, or a replay engine). The Python side owns I/O, validation, authorization, configuration and orchestration; the C++ side owns the compute-bound inner loop and its data structures. The interface is narrow and versioned.

### 1.1 Functional requirements

1. A defined **kernel interface** with a written contract: inputs, outputs, units, ranges, ordering guarantees, error semantics, thread-safety, ownership of memory crossing the boundary, and determinism.
2. The kernel callable from Python through one of the integration mechanisms below. You choose and justify one, and your ADR compares it with at least two others.
3. Identical results (or results within a documented tolerance, justified numerically per 6.2) between the pure-Python reference and the C++ kernel on a large randomized corpus.
4. Errors cross the boundary in a defined way: C++ failures become typed Python exceptions (or error codes) with useful messages; no C++ exception escapes into a runtime that cannot handle it; no crash of the interpreter on malformed input.
5. The system runs in a deployed form (container or a documented reproducible install) containing both components, with version pinning of both.

### 1.2 Integration mechanisms to compare (choose one, ADR the rest)

| Mechanism | Boundary cost profile | Typical risks |
|---|---|---|
| In-process extension module via a binding library (for example pybind11 or nanobind; VERIFY maintenance status and docs) | Low call overhead; conversion cost depends on type; shares address space | A kernel crash takes down the interpreter; GIL handling must be deliberate; ABI/Python version coupling; wheel building per platform |
| Plain C ABI plus `ctypes` or `cffi` | Very low abstraction; manual marshalling | Manual lifetime and layout errors; no C++ types across the boundary; easy to corrupt memory |
| Separate process with IPC (stdin/stdout, sockets, shared memory, gRPC, or a message format) | Serialization and copy costs per message; isolates crashes | Protocol versioning; deployment of two processes; latency; backpressure |
| Python buffer protocol / NumPy arrays with zero-copy views | Avoids copies for large arrays | Lifetime of the underlying buffer; strides and dtype assumptions; mutation aliasing |

State which mechanism you chose, what it copies, and what it does not.

## 2. Architecture and interface requirements

- **Narrow waist (4.1):** the boundary has few, coarse-grained calls. Many small calls multiply crossing cost; show the granularity decision with measurements (call per element versus call per batch).
- **Data representation:** specify types and layout at the boundary: fixed-width integers (never platform-dependent `long`), explicit endianness if bytes cross, explicit units for prices and timestamps, null/missing handling, string encoding (UTF-8 and explicit length). For arrays, specify dtype, shape, strides/contiguity, and whether the kernel may retain the pointer after return (it must not, unless lifetime is explicitly managed).
- **Ownership across the boundary (5.2):** for every object crossing, state who allocates, who frees, and how the lifetime is tied (for example the Python wrapper object owns the C++ object via RAII; the destructor frees it; double free impossible by construction). Show what happens when Python calls into an object after close, and when the kernel is invoked from two threads.
- **Concurrency and the GIL:** state whether the kernel releases the GIL for long calls, what that implies for the kernel's thread-safety and for Python objects it must not touch while released, and test that a long kernel call does not freeze a server's event loop (relevant if the Python side is async; a blocking call in an async handler is a defect, 2.6).
- **Errors:** an error taxonomy shared by both sides: invalid argument, resource exhausted, internal invariant violated, cancelled. Map each to a Python exception type. A C++ assertion failure in production must not corrupt state silently; define what happens.
- **Versioning:** a kernel version and an interface version exposed at runtime; the Python side refuses to start with an incompatible kernel; a documented compatibility policy.
- **Build and packaging:** one command builds the C++ part with warnings as errors and runs its tests; one command builds the Python package including the extension; wheels or an image built reproducibly in CI. Document how a developer on a clean machine goes from clone to green in under an hour.

## 3. The costs you must discuss (and measure where possible)

The design document needs a dedicated section for each.

**3.1 Serialization and marshalling.** What is converted at each call: Python object to C++ value, array copy or view, string conversion, result conversion back. Measure the **boundary overhead** by calling a no-op kernel with representative payload sizes and report time per call with spread, as a function of payload size, so the break-even payload size for the boundary is visible. For IPC mechanisms, report serialization format, schema evolution handling, and the cost of encoding and decoding at your payload sizes. Discuss precision loss (for example 64-bit integers through floating point, timestamps, decimal values) and show a test that exposes it.

**3.2 Deployment.** What must exist on the target machine: interpreter version, C++ runtime libraries, compiler ABI, CPU architecture (does the build assume instruction sets the deployment CPU might lack; VERIFY flags such as native-architecture tuning, which can make binaries non-portable), platform wheels or container base image, and how security patches to either runtime reach production. Describe the failure when the extension is built against a different interpreter than runs it. Describe rollback: can the Python side and the kernel be rolled back independently, and what does the version check do.

**3.3 Debugging.** Describe the actual procedure to debug a crash that starts in Python and ends in C++: core dumps and symbolized stack traces, running Python under a native debugger, enabling debug symbols in the extension, running the kernel's tests natively under sanitizers (5.5) separately from the Python integration, and what changes when sanitizers are loaded inside a Python process (VERIFY: preloading requirements and interpreter-allocation noise; document what you found). Demonstrate it with a seeded bug, recorded in the failure log: a memory error in the kernel triggered from Python, caught by a native sanitizer run, with the Python-side reproduction reduced to a minimal script. Describe how logging and tracing cross the boundary (correlation id passed to the kernel; kernel logs surfaced), and how profiling crosses it (a Python profiler sees the kernel as one opaque call).

**3.4 Testing.** Three layers: native kernel tests (no Python), reference-versus-kernel differential tests (the core), and end-to-end tests through the service. Property-based tests over inputs generated in Python and fed to both implementations, with seeds logged. Fuzz the boundary with malformed inputs (wrong dtype, non-contiguous arrays, empty arrays, NaN and infinity, enormous sizes, embedded NUL in strings, invalid UTF-8) and assert no interpreter crash.

**3.5 Organizational cost.** Who on a team can maintain this? What is the bus factor? What does a Python-only developer need to learn to change the kernel call? State it honestly.

## 4. Milestones with checkpoints

| # | Milestone | Checkpoint evidence |
|---|---|---|
| M0 | Boundary justification (section 0), pure-Python reference, baseline profile | Document and profile committed; Amdahl bound computed; ADR drafted |
| M1 | Interface contract and error taxonomy written; stub kernel with no-op calls | No-op overhead measured vs payload size |
| M2 | Native kernel with its own tests and sanitizer builds | Native suite green under ASan/UBSan |
| M3 | Binding/IPC layer | Round-trip tests across all supported types; ownership and lifetime tests |
| M4 | Differential and property tests, boundary fuzzing | Corpus of at least 100,000 randomized cases agreeing within stated tolerance; no interpreter crashes in fuzz run |
| M5 | Integration into the Python application with correct async/GIL handling | Event-loop-blocking test; concurrency test |
| M6 | Packaging and deployment | Clean-machine build and run; version-mismatch refusal demonstrated; rollback demonstrated |
| M7 | Cross-boundary debugging exercise (seeded bug) | Failure log entry with the full diagnosis path |
| M8 | End-to-end measurement and decision review | Measured end-to-end speedup versus the Amdahl bound; decision to keep or collapse the boundary |
| M9 | Documentation, defense preparation | Rubric self-score |

## 5. Acceptance criteria

1. The justification document exists, predates the integration code in version control, and contains the baseline profile and the bound.
2. Reference and kernel agree on the randomized corpus within the documented tolerance; tolerance is justified numerically (6.2), not tuned until green.
3. No input within the fuzzing categories crashes or hangs the interpreter; invalid inputs yield the documented exceptions.
4. A long kernel call does not block unrelated requests on the Python side (if a server) and the GIL behavior is tested.
5. The system builds and runs on a clean machine from the documentation; mismatched kernel and Python versions are rejected at startup with a clear error.
6. End-to-end measurement is reported with method and spread, compared against the bound, with an honest statement of whether the boundary paid for itself.
7. The cross-boundary debugging exercise is documented and reproducible.

## 6. Security and reliability expectations (4.3)

The boundary is a trust boundary for memory safety: Python data entering C++ is untrusted until validated on the C++ side (sizes, dtypes, alignment, overflow in size computations such as `n * element_size`). Do not trust a length supplied by the caller without checking it against the actual buffer. Do not deserialize attacker-influenced bytes with unsafe parsers; define a bounds-checked decoder. Do not use `pickle` for any cross-process or cross-trust payload. Native crashes are availability and potentially security issues: for IPC designs, show the supervisor behavior (restart, backoff, request failure semantics, idempotency of retried calls, 2.6). For in-process designs, state plainly that a kernel memory error can compromise or kill the whole service and what compensating controls you adopted (sanitized CI, fuzzing, a process-isolated fallback mode). Dependency hygiene on both sides: pinned, audited, and minimal.

## 7. Performance criteria (methodology only)

Follow Capstone C section 7 for kernel measurement and Capstone A section 7 for service measurement. Additionally:

1. Report three numbers separately, each with environment and spread: reference Python time, kernel time natively, and kernel time including the boundary crossing from Python. The difference between the last two is the boundary overhead.
2. Report a sweep over payload size and call granularity so the regime where the boundary helps and the regime where it hurts are both visible.
3. Report end-to-end time at the service level with realistic payloads. Compare against the Amdahl bound from M0. If the measured gain is far below the bound, explain where the rest went (conversion, copying, GIL contention, unmoved work).
4. Memory: report peak resident memory of both variants and describe copies at the boundary.
5. Do not generalize beyond the measured workloads, hardware and versions.

## 8. Documentation requirements

- `README.md`: architecture summary, build and run on a clean machine, version matrix.
- `docs/boundary-justification.md` (section 0) and `docs/adr/` with at least: integration mechanism; data representation at the boundary; error mapping; GIL/threading policy; versioning policy.
- `docs/interface-contract.md`: the kernel contract in section 2 terms, authoritative for both sides.
- `docs/costs.md`: sections 3.1 through 3.5 with measurements.
- `docs/debugging-guide.md`: the cross-boundary procedure and the seeded-bug case study.
- `docs/deployment.md`: environment requirements, upgrade and rollback.
- `docs/failure-log.md` and `docs/ai-use.md`: AI-generated bindings frequently contain lifetime and reference-counting errors; list any you caught.

## 9. Final technical defense

**Format.** 60 minutes, no AI. 10 minutes: present the boundary justification as if to a skeptical tech lead. 35 minutes: questions. 15 minutes: live modification (for example, change a type crossing the boundary, or diagnose a supplied crash).

**Question bank:**

1. Why does this boundary exist? What would convince you to remove it, and how would you know?
2. Show the profile that justified it. What fraction of time was in the moved code and what does the Amdahl bound say?
3. Your measured speedup is below the bound. Where did the difference go?
4. What exactly is copied at each call? Which arguments are zero-copy, and what lifetime rule makes zero-copy safe?
5. Describe the failure if Python passes a non-contiguous array or the wrong dtype.
6. Who owns the C++ object? What happens when Python's garbage collector runs finalizers during interpreter shutdown, or when two threads call into the same object?
7. Does the kernel release the GIL? What may it touch while released?
8. A production crash shows only a native stack address. Walk through your debugging steps.
9. Why does the tolerance between reference and kernel have the value it has? Show the derivation.
10. What is in the deployment image, and what happens when you upgrade Python by a minor version?
11. If this had been an IPC design instead, how would the failure semantics change?
12. Which part of the system can a Python-only teammate change safely, and which part cannot they touch?
13. The CPU in production differs from your build machine. What could go wrong?
14. Argue the opposite case: why a pure-Python or pure-C++ solution would have been better here. What evidence would settle it?
15. What AI-produced binding code did you have to fix?

A defense that cannot articulate the cost of the boundary, or treats the C++ side as automatically better, fails the justification items.

## 10. No-AI reconstruction or extension challenge

Choose one by random draw:

- **R1 reconstruction (4-5 hours, Mode A/B):** Starting from your interface contract and the C++ kernel, rebuild the binding layer with ownership, error mapping and the round-trip tests, using documentation only.
- **R2 extension (3-4 hours):** Change the boundary: add a streaming call (kernel produces results incrementally) or a new input type (for example nullable values or variable-length strings). Update contract, tests, fuzz cases, and version numbers; show the compatibility behavior for an older Python client.
- **R3 collapse (3 hours):** Argue and then demonstrate the opposite design: implement the same kernel with the best pure-Python approach (or the whole thing in C++) and measure. Produce a one-page recommendation on whether to keep the boundary, citing the measurements.

## 11. The 100-point rubric

| Area | Points | Notes |
|---|---|---|
| Boundary justification and alternatives | 15 | Written first, evidence-based, Amdahl bound, honest conclusion |
| Interface contract and data representation | 10 | Types, ownership, lifetime, errors, versioning |
| Correctness: differential and cross-boundary tests | 15 | Corpus size, tolerance justification, fuzzing, no interpreter crashes |
| Memory safety and security at the boundary | 10 | Validation, sanitizers, no unsafe deserialization |
| Costs: serialization, deployment, debugging, organizational | 15 | Each measured or reasoned; seeded-bug case study |
| Performance method and honesty | 10 | Three-way measurement, sweeps, spread, bound comparison |
| Build, packaging and deployment | 5 | Clean-machine reproducible, version check, rollback |
| Documentation | 5 | Contract, ADRs, guides |
| Technical defense | 10 | Specific, honest, argues both sides |
| No-AI reconstruction/extension | 5 | Completed and explained |
| **Total** | **100** | Pass: 80 or more and no critical failure |

**Critical failures:** no written justification or one written after the integration code; no pure-Python (or pure alternative) baseline; performance claims without profile and spread; any input class that crashes the interpreter; undefined ownership of memory crossing the boundary; unsafe deserialization of cross-boundary data; no cross-boundary test; unable to explain submitted code.

**If failed:** targeted remediation (for example, a minimal binding of a three-function kernel built from a blank directory with ownership tests and a fuzz run, or a repeated justification exercise on a different workload), then re-defense of failed topics.

Ledger update: Capstone E to `Demonstrated` on pass; `Applied` when the pattern, or a decision to avoid it, has informed a real project; `Production-ready` only after real deployment and an operational period with external review.
