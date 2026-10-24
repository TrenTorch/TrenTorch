"""Checks the DSA-sheet questions. Run from TrenTorch_Web/:

    python data/app_data/13-dsa-sheet/_tools/dsa_tool.py check            # every question
    python data/app_data/13-dsa-sheet/_tools/dsa_tool.py check <folder>   # one question
    python data/app_data/13-dsa-sheet/_tools/dsa_tool.py fill <folder>    # write `expected` for cases that have none

A question folder holds README.md, problem.json, starter.py, solution.py and an optional brute.py.
`check` runs solution.py on every case in problem.json with the same runtime the browser uses
(processes/curriculum-build/cases-runtime.py). If brute.py exists and problem.json has a "stress"
block, it also compares brute.py and solution.py on random small inputs.
"""

import importlib.util
import json
import random
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


def sample(runtime, spec, rng):
    """One random value for a stress spec: an int, a choice, or a generator with any size field given as {min, max}."""
    kind = spec["type"]
    if kind == "int":
        return rng.randint(spec["lo"], spec["hi"])
    if kind == "choice":
        return rng.choice(spec["values"])
    gen = dict(spec)
    for key, value in spec.items():
        if isinstance(value, dict) and set(value) == {"min", "max"}:
            gen[key] = rng.randint(value["min"], value["max"])
    gen["seed"] = rng.randint(1, 2**31)
    return runtime._gen(gen)


def fill(folder):
    runtime = load_runtime()
    path = folder / "problem.json"
    problem = json.loads(path.read_text(encoding="utf-8"))
    fn = load_function(folder, "solution.py", problem["function"]["name"])
    order = [p["name"] for p in problem["function"]["params"]]
    for case in problem["cases"]:
        if "expected" in case or "digest" in case:
            continue
        args = [runtime._materialize(case["input"][name]) for name in order]
        case["expected"] = runtime._canon(fn(*args))
    path.write_text(
        json.dumps(problem, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


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
        rng = random.Random(12345)
        for run in range(stress.get("runs", 200)):
            args = {
                key: sample(runtime, spec, rng)
                for key, spec in stress["inputs"].items()
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
