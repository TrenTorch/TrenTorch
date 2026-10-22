"""Checks the DSA-sheet questions. Run from TrenTorch_Web/:

    python data/app_data/13-dsa-sheet/_tools/dsa_tool.py check            # every question
    python data/app_data/13-dsa-sheet/_tools/dsa_tool.py check <folder>   # one question
    python data/app_data/13-dsa-sheet/_tools/dsa_tool.py fill <folder>    # write `expected` for cases that have none
    python data/app_data/13-dsa-sheet/_tools/dsa_tool.py batches [folder]  # (re)write the 300-case random batch

A question folder holds README.md, problem.json, starter.py, solution.py and an optional brute.py.
`check` runs solution.py on every case in problem.json with the same runtime the browser uses
(processes/curriculum-build/cases-runtime.py). If brute.py exists and problem.json has a "stress"
block, it also compares brute.py and solution.py on random small inputs.
"""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT.parents[2] / "processes" / "curriculum-build" / "cases-runtime.py"
sys.set_int_max_str_digits(0)


def load_runtime():
    spec = importlib.util.spec_from_file_location("cases_runtime", RUNTIME_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_function(folder, filename, name):
    path = folder / filename
    spec = importlib.util.spec_from_file_location(f"{folder.name}_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, name)


def question_folders():
    return sorted(p.parent for p in ROOT.glob("*/*/*/problem.json"))


def write_problem(path, problem):
    """Write problem.json with the header indented and one case per line, so a diff shows one
    case per changed line."""
    cases = problem["cases"]
    rest = {
        key: value for key, value in problem.items() if key not in ("cases", "stress")
    }
    head = json.dumps(rest, indent=2, ensure_ascii=False)
    lines = ",\n".join("    " + json.dumps(case, ensure_ascii=False) for case in cases)
    text = head[:-2] + ',\n  "cases": [\n' + lines + "\n  ]"
    if "stress" in problem:
        text += ',\n  "stress": ' + json.dumps(problem["stress"], ensure_ascii=False)
    path.write_text(text + "\n}\n", encoding="utf-8", newline="\n")


def fill(folder):
    runtime = load_runtime()
    path = folder / "problem.json"
    problem = json.loads(path.read_text(encoding="utf-8"))
    fn = load_function(folder, "solution.py", problem["function"]["name"])
    order = [p["name"] for p in problem["function"]["params"]]
    for case in problem["cases"]:
        if "expected" in case or "digest" in case or "batch" in case:
            continue
        args = [runtime._materialize(case["input"][name]) for name in order]
        case["expected"] = runtime._canon(fn(*args))
    write_problem(path, problem)


def batches(folder, count, seed):
    """Add (or replace) the random batch case. It uses the problem's `stress` inputs, so every
    random case is small. The digests come from solution.py."""
    runtime = load_runtime()
    path = folder / "problem.json"
    problem = json.loads(path.read_text(encoding="utf-8"))
    if not problem.get("stress") or problem.get("compare", "exact") != "exact":
        return False
    fn = load_function(folder, "solution.py", problem["function"]["name"])
    order = [p["name"] for p in problem["function"]["params"]]
    batch = {"count": count, "seed": seed}
    digests = []
    for index in range(count):
        args = runtime.batch_args(problem, batch, index)
        digests.append(runtime._digest(fn(*[args[name] for name in order]))[:6])
    case = {
        "id": "random_batch",
        "batch": {"count": count, "seed": seed},
        "digests": digests,
    }
    cases = [c for c in problem["cases"] if c["id"] != "random_batch"]
    # after the hand-written cases, before the big ones
    position = next((i for i, c in enumerate(cases) if c.get("perf")), len(cases))
    cases.insert(position, case)
    problem["cases"] = cases
    write_problem(path, problem)
    return True


def check(folder):
    runtime = load_runtime()
    problem = json.loads((folder / "problem.json").read_text(encoding="utf-8"))
    name = problem["function"]["name"]
    fn = load_function(folder, "solution.py", name)
    runtime.STATE["slow"] = False
    errors = []
    slowest = 0.0
    for case in problem["cases"]:
        try:
            slowest = max(slowest, runtime.check_case(problem, case, fn))
        except AssertionError as error:
            errors.append(f"case {case['id']}: {str(error).splitlines()[0]}")
    brute_path = folder / "brute.py"
    stress = problem.get("stress")
    if brute_path.exists() and stress:
        brute = load_function(folder, "brute.py", name)
        order = [p["name"] for p in problem["function"]["params"]]
        for run in range(stress.get("runs", 200)):
            rnd = runtime._mulberry32(900000 + run)
            args = {
                name: runtime.sample_input(stress["inputs"][name], rnd)
                for name in order
            }
            a = runtime._canon(brute(*[runtime._materialize(args[k]) for k in order]))
            b = runtime._canon(fn(*[runtime._materialize(args[k]) for k in order]))
            if not runtime._same(
                b, a, problem.get("compare", "exact"), problem.get("tolerance", 1e-9)
            ):
                errors.append(
                    f"stress run {run}: brute and solution differ on {json.dumps(args)[:200]}"
                )
                break
    return errors, slowest


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "check"
    targets = [Path(sys.argv[2]).resolve()] if len(sys.argv) > 2 else question_folders()
    if command == "fill":
        for folder in targets:
            fill(folder)
        return 0
    if command == "batches":
        done = [folder.name for folder in targets if batches(folder, 300, 1)]
        print(f"random batch written for {len(done)} of {len(targets)} questions")
        return 0
    failed = 0
    for folder in targets:
        errors, slowest = check(folder)
        status = "ok  " if not errors else "FAIL"
        print(f"{status} {folder.name:<40} slowest case {slowest:7.1f} ms (CPython)")
        for line in errors:
            print("     ", line)
        failed += bool(errors)
    print(f"{len(targets) - failed}/{len(targets)} questions pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
