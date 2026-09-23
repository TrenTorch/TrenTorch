def run_model_tests(model_fn, test_cases: list) -> list:
    """
    Runs a suite of model tests, exactly like a normal code test
    suite: each test_case is (test_name, input_value, check_fn), where
    check_fn(model_output) returns True/False. Any exception raised
    while running a test (a genuinely broken model call) counts as
    that test FAILING, not as a crash of the whole suite.
    """
    # TODO: loop over test_cases. For each, try calling
    # model_fn(input_value) and check_fn(output); on any exception,
    # mark passed=False instead of letting it propagate. Append
    # {"test_name": test_name, "passed": passed} to results. Return
    # results.
    pass


def pass_rate(results: list) -> float:
    """
    The fraction of tests that passed -- an empty test suite is
    treated as vacuously passing (1.0), since there were no failures.
    """
    # TODO: if results is empty, return 1.0. Otherwise, count how many
    # entries have passed=True, divide by len(results).
    pass


def gate_deployment(results: list, min_pass_rate: float) -> bool:
    """
    Real ML model tests are often APPROXIMATE (a model's exact output
    can shift slightly between valid retrains), so unlike ordinary
    code CI, deployment is gated on a PASS RATE threshold rather than
    requiring literally every single test to pass.
    """
    # TODO: pass_rate(results) >= min_pass_rate
    pass
