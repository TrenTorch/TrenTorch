def build_capstone_report(
    project_name: str, baseline_stats: dict, optimized_stats: dict, correctness_verified: bool
) -> dict:
    speedup_factor = baseline_stats["median"] / optimized_stats["median"]
    passed = correctness_verified and speedup_factor > 1.0
    summary = (
        f"{project_name}: {speedup_factor:.2f}x speedup "
        f"({'correctness verified' if correctness_verified else 'CORRECTNESS FAILED'})"
    )
    return {
        "project_name": project_name,
        "speedup_factor": speedup_factor,
        "correctness_verified": correctness_verified,
        "passed": passed,
        "summary": summary,
    }


def compare_capstone_reports(reports: list) -> dict:
    passing = [r for r in reports if r["passed"]]
    if not passing:
        return {"best_project": None, "best_speedup_factor": None, "num_passing": 0}
    best = max(passing, key=lambda r: r["speedup_factor"])
    return {
        "best_project": best["project_name"],
        "best_speedup_factor": best["speedup_factor"],
        "num_passing": len(passing),
    }
