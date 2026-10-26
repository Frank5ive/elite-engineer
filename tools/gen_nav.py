"""Regenerates the nav block of mkdocs.yml with short sidebar titles. Run from repo root: python3 tools/gen_nav.py"""
import glob, os, re, json
os.chdir("docs")
SHORT = {
"0.1":"Day-one protocol","0.2":"Git workflow","0.3":"Debugging & failure log","0.4":"Communication",
"1.1":"Python object model","1.2":"Iterators, generators, contexts","1.3":"Types, packaging, logging","1.4":"pytest & mocking",
"2.1":"HTTP, REST & contracts","2.2":"FastAPI & Pydantic","2.3":"SQL & indexes","2.4":"Transactions & pagination",
"2.5":"AuthN, AuthZ, secrets","2.6":"Async, jobs, idempotency","2.7":"Observability & deploy",
"3.1":"Modern PHP","3.2":"Moodle architecture","3.3":"Capabilities & roles","3.4":"Forms, output, DB API",
"3.5":"Events, tasks, web services","3.6":"Testing & upgrades",
"4.1":"Architecture","4.2":"Testing & refactoring","4.3":"Security & reliability","4.4":"Performance method",
"5.1":"Build, types, lifetime","5.2":"RAII & ownership","5.3":"STL, lambdas, templates","5.4":"Data structures & algorithms",
"5.5":"Sanitizers & debugging","5.6":"Cache & concurrency",
"6.1":"Probability","6.2":"Linear algebra & numerics","6.3":"Statistics & Monte Carlo","6.4":"Markets & options",
"6.5":"Backtesting & order books","7.1":"AI independence","7.2":"Design docs & postmortems"}
CAP = {"A":"A: Production backend","B":"B: Moodle plugin","C":"C: C++ component","D":"D: Quant research","E":"E: Cross-language"}
FRONT = {"README":"How to use this book","DIAGNOSTIC":"Diagnostic","ROADMAP":"Roadmap","CONTINUE-HERE":"Continue in a new session","VERIFY-LIST":"Verification status"}
def h1(f):
    for l in open(f):
        if l.startswith("# "): return l[2:].strip()
    return os.path.basename(f)
def lid(f):
    m = re.match(r"(\d\.\d)-", os.path.basename(f)); return m.group(1) if m else None
def label(f):
    n = os.path.basename(f)
    if n.startswith("capstone-"): return CAP[n.split("-")[1]]
    if "/solutions/" in "/"+f:
        i = lid(f); return f"{i}  {SHORT[i]}" if i else h1(f)
    i = lid(f)
    if i: return f"{i}  {SHORT[i]}"
    k = n[:-3]
    return FRONT.get(k) or h1(f)
vols = [("Start here", [f"00-front/{k}.md" for k in FRONT]),
("0 · Job readiness", sorted(glob.glob("01-*/*.md"))), ("1 · Python", sorted(glob.glob("02-*/*.md"))),
("2 · FastAPI & backend", sorted(glob.glob("03-*/*.md"))), ("3 · PHP & Moodle", sorted(glob.glob("04-*/*.md"))),
("4 · Engineering judgment", sorted(glob.glob("05-*/*.md"))), ("5 · Modern C++", sorted(glob.glob("06-*/*.md"))),
("6 · Quant", sorted(glob.glob("07-*/*.md"))), ("7 · Independence", sorted(glob.glob("08-*/*.md"))),
("Capstones", sorted(glob.glob("capstones/*.md"))),
("Templates", sorted(glob.glob("00-front/templates/*.md"))),
("Solutions (attempt first)", sorted(glob.glob("solutions/*.md")) + ["00-front/DIAGNOSTIC-ANSWER-KEY.md"])]
nav = ["  - Home: index.md"]; lessons = []
for v, fs in vols:
    nav.append(f'  - "{v}":')
    for f in fs:
        lab = "Diagnostic answer key" if f.endswith("ANSWER-KEY.md") else label(f)
        nav.append(f'      - "{lab}": {f}')
        if re.match(r"0\d-vol|capstones", f): lessons.append({"path": f, "title": h1(f)})
os.chdir("..")
t = open("mkdocs.yml").read()
t = re.sub(r"nav:\n(?:  .*\n)+", "nav:\n" + "\n".join(nav) + "\n", t)
open("mkdocs.yml", "w").write(t)
open("docs/assets/lessons.json", "w").write(json.dumps(lessons))
print(len(lessons), "lessons")
