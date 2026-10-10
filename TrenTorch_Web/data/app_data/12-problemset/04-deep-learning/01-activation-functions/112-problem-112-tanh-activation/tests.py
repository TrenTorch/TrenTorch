"""Tests with varied inputs. Expected values were checked against independent references (SciPy, scikit-learn, PyTorch or a first-principles formula)."""
import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def _close(actual, expected, rtol=1e-6, atol=1e-8):
    if isinstance(expected, dict):
        assert set(actual) == set(expected)
        for k in expected:
            _close(actual[k], expected[k], rtol, atol)
        return
    if isinstance(expected, (tuple, list)) and not (len(expected) and isinstance(expected[0], (int, float, np.number)) and not isinstance(expected, tuple)):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            _close(a, e, rtol, atol)
        return
    a, e = np.asarray(actual), np.asarray(expected)
    assert a.shape == e.shape, (a.shape, e.shape)
    if a.dtype.kind in "biufc" and e.dtype.kind in "biufc":
        np.testing.assert_allclose(a, e, rtol=rtol, atol=atol, equal_nan=True)
    else:
        assert a.tolist() == e.tolist()


def test_01_readme_example_1():
    _close(solve([-2.0, 0.0, 2.0]), np.array([-0.9640275800758169, 0.0, 0.9640275800758169]))


def test_02_readme_example_2():
    _close(solve([20.0, -20.0]), np.array([1.0, -1.0]))


def test_03_random_valid_case_1():
    _close(solve([4.67, 0.21, 4.38, 0.81, 0.96, 2.46, 0.48, -4.3]), np.array([0.999824336558004, 0.20696649972945258, 0.9996862800006663, 0.6695902596187708, 0.7442768673618373, 0.9855075208083371, 0.4462436102487796, -0.9996318561900731]))


def test_04_random_valid_case_2():
    _close(solve([0.74, -4.2, 0.5, 2.37, -0.42, 0.13, -1.66, 3.2]), np.array([0.6291451614140354, -0.9995503664595334, 0.46211715726000974, 0.9826741124303737, -0.39693043200507755, 0.12927258360605834, -0.9302171829365263, 0.9966823978396512]))


def test_05_random_valid_case_3():
    _close(solve([2.2, 4.75, 1.07, 4.65, -3.46, -2.94, 2.56, 1.97]), np.array([0.9757431300314515, 0.9998503075449787, 0.7894612209549805, 0.9998171682522956, -0.9980262898089581, -0.9944260075619155, 0.9881189556033193, 0.9618456053694837]))


def test_06_random_valid_case_4():
    _close(solve([-2.89, 1.2, -4.03, -1.48, 4.1, -0.96, 0.85, 1.1]), np.array([-0.9938415907570455, 0.8336546070121552, -0.9993683459458442, -0.9014679878319467, 0.9994508436877974, -0.7442768673618373, 0.6910694698329306, 0.8004990217606297]))


def test_07_random_valid_case_5():
    _close(solve([3.55, -2.73, -2.29, 1.73, -1.64, 3.2, 3.1, 1.83]), np.array([0.9983511506272034, -0.9915289207183132, -0.9796983982280146, 0.9390559334707117, -0.9274725672507034, 0.9966823978396512, 0.9959493592219002, 0.9498260756930405]))


def test_08_random_valid_case_6():
    _close(solve([0.2, -1.96, -2.12, 2.85, 4.6, 3.19, -0.28, 3.71]), np.array([0.197375320224904, -0.961089830863614, -0.9715940772546178, 0.9933303853851734, 0.9997979416121844, 0.9966154912452405, -0.27290508056313273, 0.9988024192384614]))


def test_09_random_valid_case_7():
    _close(solve([-1.33, 3.26, 2.56, 3.11, 3.57, 2.59, -4.8, -0.63]), np.array([-0.8692493331488548, 0.9970569988052209, 0.9881189556033193, 0.9960294080465228, 0.9984157517232097, 0.9888069815508205, -0.9998645517007604, -0.5580522155596244]))


def test_10_random_valid_case_8():
    _close(solve([0.55, -3.5, 2.9, -1.61, 1.14, -1.28, -3.21, 2.43]), np.array([0.5005202111902353, -0.9981778976111987, 0.9939631673505832, -0.9231600289968693, 0.814414093765686, -0.8564849154724973, -0.9967479839466443, 0.9846182482369834]))


def test_11_random_valid_case_9():
    _close(solve([-2.69, -3.4, -0.79, 1.39, 2.98, 2.79, -2.37, 2.44]), np.array([-0.9908266254165919, -0.9977749279342794, -0.658409035955251, 0.8831708889152075, 0.9948534536923793, 0.9924832264829985, -0.9826741124303737, 0.9849205308832533]))


def test_12_random_valid_case_10():
    _close(solve([2.22, 4.75, -1.04, 2.23, -0.74, -1.06, 3.89, 0.21]), np.array([0.9766831668903339, 0.9998503075449787, -0.7778880665771849, 0.9771395937470586, -0.6291451614140354, -0.7856638590269437, 0.9991643249731132, 0.20696649972945258]))
