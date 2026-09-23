def run_model_tests(model_fn, test_cases: list) -> list:
    results = []
    for test_name, input_value, check_fn in test_cases:
        try:
            output = model_fn(input_value)
            passed = bool(check_fn(output))
        except Exception as error:
            passed = False
            output = None
        results.append({"test_name": test_name, "passed": passed})
    return results


def pass_rate(results: list) -> float:
    if not results:
        return 1.0
    return sum(1 for r in results if r["passed"]) / len(results)


def gate_deployment(results: list, min_pass_rate: float) -> bool:
    return pass_rate(results) >= min_pass_rate
