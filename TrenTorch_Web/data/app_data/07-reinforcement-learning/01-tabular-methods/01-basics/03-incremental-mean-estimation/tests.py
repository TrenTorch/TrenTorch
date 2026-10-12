import numpy as np

from _load import load_solution

_module = load_solution(__file__)
update_incremental_mean = _module.update_incremental_mean


def test_first_sample():
    """First sample (count=0): estimate should become the reward."""
    old_estimate = 0.0
    count = 0
    reward = 5.0
    new_estimate = update_incremental_mean(old_estimate, count, reward)
    assert np.isclose(new_estimate, 5.0)


def test_second_sample():
    """After first sample mean is 10, second sample is 20."""
    # Q_1 = 10 (mean of [10])
    # Q_2 = 10 + (1/2) * (20 - 10) = 15 (mean of [10, 20])
    old_estimate = 10.0
    count = 1
    reward = 20.0
    new_estimate = update_incremental_mean(old_estimate, count, reward)
    assert np.isclose(new_estimate, 15.0)


def test_consistency_with_batch_mean():
    """Incremental updates should match batch mean computation."""
    rewards = [10.0, 15.0, 5.0, 20.0, 8.0]

    # Incremental approach
    estimate = 0.0
    for i, reward in enumerate(rewards):
        estimate = update_incremental_mean(estimate, i, reward)

    # Batch approach
    batch_mean = np.mean(rewards)

    assert np.isclose(estimate, batch_mean)


def test_zero_reward():
    """Should handle zero reward."""
    old_estimate = 5.0
    count = 1
    reward = 0.0
    new_estimate = update_incremental_mean(old_estimate, count, reward)
    expected = 5.0 + 0.5 * (0.0 - 5.0)
    assert np.isclose(new_estimate, expected)


def test_negative_reward():
    """Should handle negative reward."""
    old_estimate = 10.0
    count = 3
    reward = -5.0
    new_estimate = update_incremental_mean(old_estimate, count, reward)
    expected = 10.0 + (1.0 / 4.0) * (-5.0 - 10.0)
    assert np.isclose(new_estimate, expected)


def test_many_samples():
    """After many samples, new reward has small influence."""
    old_estimate = 100.0
    count = 999
    reward = 1.0
    new_estimate = update_incremental_mean(old_estimate, count, reward)
    # Step size = 1/1000 = 0.001
    expected = 100.0 + 0.001 * (1.0 - 100.0)
    assert np.isclose(new_estimate, expected)


def test_step_size_decreases():
    """Step size should decrease with count."""
    estimate = 10.0
    reward = 20.0

    # After 0 samples: step size = 1/1 = 1.0
    update1 = update_incremental_mean(estimate, 0, reward)
    change1 = abs(update1 - estimate)

    # After 9 samples: step size = 1/10 = 0.1
    update2 = update_incremental_mean(estimate, 9, reward)
    change2 = abs(update2 - estimate)

    # Change decreases
    assert change1 > change2
    assert np.isclose(change1 / change2, 10.0)


def test_all_same_rewards():
    """If all rewards are the same, estimate converges to that value."""
    reward = 7.0
    estimate = 0.0
    for i in range(100):
        estimate = update_incremental_mean(estimate, i, reward)
    assert np.isclose(estimate, 7.0, rtol=1e-10)


def test_mean_of_two():
    """Simple case: mean of [a, b]."""
    a = 10.0
    b = 20.0
    # Start with a
    estimate = a
    # Update with b (count=1 means 1 sample seen)
    estimate = update_incremental_mean(estimate, 1, b)
    assert np.isclose(estimate, (a + b) / 2.0)


def test_mean_of_three():
    """Mean of [a, b, c]."""
    values = [5.0, 15.0, 10.0]
    estimate = 0.0
    for i, val in enumerate(values):
        estimate = update_incremental_mean(estimate, i, val)
    assert np.isclose(estimate, np.mean(values))


def test_alternating_high_low():
    """Alternating high and low rewards."""
    # [100, 1, 100, 1, ...] should converge to ~50
    estimate = 0.0
    for i in range(100):
        reward = 100.0 if i % 2 == 0 else 1.0
        estimate = update_incremental_mean(estimate, i, reward)
    assert np.isclose(estimate, 50.5, rtol=1e-2)
