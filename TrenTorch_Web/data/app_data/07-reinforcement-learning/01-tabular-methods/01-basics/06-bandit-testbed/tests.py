import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
BanditTestbed = _module.BanditTestbed


def dummy_select_greedy(q_estimates, counts, t, rng):
    """Dummy: always select the greedy action (max Q)."""
    return int(np.argmax(q_estimates))


def dummy_select_random(q_estimates, counts, t, rng):
    """Dummy: always select random."""
    return rng.integers(0, len(q_estimates))


def test_initialization():
    """Test that testbed initializes correctly."""
    testbed = BanditTestbed(num_arms=5, num_instances=10, seed=42)
    assert testbed.num_arms == 5
    assert testbed.num_instances == 10
    assert testbed.true_rewards.shape == (10, 5)
    assert len(testbed.optimal_arms) == 10


def test_optimal_arms_identified():
    """Optimal arms should be argmax of true rewards."""
    testbed = BanditTestbed(num_arms=4, num_instances=3, seed=42)
    for i in range(testbed.num_instances):
        assert testbed.optimal_arms[i] == np.argmax(testbed.true_rewards[i])


def test_run_algorithm():
    """Test running an algorithm."""
    testbed = BanditTestbed(num_arms=3, num_instances=5, seed=42)
    testbed.run_algorithm(dummy_select_greedy, num_steps=10)

    mean_rewards, optimal_counts, regrets = testbed.get_results()

    assert mean_rewards.shape == (10,)
    assert optimal_counts.shape == (10,)
    assert regrets.shape == (10,)


def test_rewards_shape():
    """Mean rewards should have shape (num_steps,)."""
    testbed = BanditTestbed(num_arms=5, num_instances=20, seed=42)
    testbed.run_algorithm(dummy_select_random, num_steps=50)

    mean_rewards, _, _ = testbed.get_results()
    assert mean_rewards.shape == (50,)


def test_optimal_counts_increase():
    """Optimal counts should be non-decreasing (only go up)."""
    testbed = BanditTestbed(num_arms=3, num_instances=10, seed=42)
    testbed.run_algorithm(dummy_select_greedy, num_steps=100)

    _, optimal_counts, _ = testbed.get_results()

    # Each step, some instances select the optimal arm
    # Cumulative count should increase (or stay same)
    for i in range(1, len(optimal_counts)):
        assert optimal_counts[i] >= optimal_counts[i - 1]


def test_regrets_increase():
    """Regrets should be non-decreasing (cumulative)."""
    testbed = BanditTestbed(num_arms=4, num_instances=10, seed=42)
    testbed.run_algorithm(dummy_select_random, num_steps=50)

    _, _, regrets = testbed.get_results()

    # Regrets are cumulative, so should be non-decreasing
    for i in range(1, len(regrets)):
        assert regrets[i] >= regrets[i - 1]


def test_determinism_with_seed():
    """Same seed should give same results."""
    testbed1 = BanditTestbed(num_arms=3, num_instances=5, seed=123)
    testbed1.run_algorithm(dummy_select_greedy, num_steps=20)
    results1 = testbed1.get_results()

    testbed2 = BanditTestbed(num_arms=3, num_instances=5, seed=123)
    testbed2.run_algorithm(dummy_select_greedy, num_steps=20)
    results2 = testbed2.get_results()

    assert np.allclose(results1[0], results2[0])
    assert np.allclose(results1[1], results2[1])
    assert np.allclose(results1[2], results2[2])


def test_error_before_run():
    """get_results() should error if no algorithm has been run."""
    testbed = BanditTestbed(num_arms=3, num_instances=5, seed=42)
    try:
        testbed.get_results()
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass


def test_single_arm():
    """Single-arm bandit: always selecting the only arm should give zero regret."""
    testbed = BanditTestbed(num_arms=1, num_instances=5, seed=42)

    def select_only_arm(q_estimates, counts, t, rng):
        return 0

    testbed.run_algorithm(select_only_arm, num_steps=20)
    _, _, regrets = testbed.get_results()

    # With one arm, no regret: we're always selecting the optimal
    assert np.allclose(regrets, 0.0)


def test_two_arms():
    """Two-arm bandit: can measure regret and optimal selection."""
    testbed = BanditTestbed(num_arms=2, num_instances=10, seed=42)
    testbed.run_algorithm(dummy_select_greedy, num_steps=30)

    mean_rewards, optimal_counts, regrets = testbed.get_results()

    # Regret should generally increase (greedy converges to best arm)
    assert regrets[-1] >= 0

    # Optimal count should be non-zero (sometimes picks the best arm)
    assert optimal_counts[-1] > 0


def test_multiple_runs_overwrite():
    """Running algorithm multiple times overwrites previous results."""
    testbed = BanditTestbed(num_arms=3, num_instances=5, seed=42)

    testbed.run_algorithm(dummy_select_greedy, num_steps=10)
    results1 = testbed.get_results()

    testbed.run_algorithm(dummy_select_random, num_steps=20)
    results2 = testbed.get_results()

    # Results2 should have 20 steps, not 10
    assert results2[0].shape == (20,)

    # Results should be different (greedy vs random)
    assert not np.allclose(results1[0], results2[0][:10])


def test_consistent_across_instances():
    """Results should be consistent: mean of instances."""
    testbed = BanditTestbed(num_arms=3, num_instances=100, seed=42)
    testbed.run_algorithm(dummy_select_random, num_steps=50)

    mean_rewards, optimal_counts, regrets = testbed.get_results()

    # With random selection on 3 arms, expected optimal rate ~ 1/3
    # After 50 steps on 100 instances, should have ~1667 optimal selections
    # (rough estimate, allow variance)
    assert 1000 < optimal_counts[-1] < 2500


def test_arms_parameter_affects_results():
    """More arms should generally lead to higher regret with random selection."""
    testbed3 = BanditTestbed(num_arms=3, num_instances=50, seed=42)
    testbed3.run_algorithm(dummy_select_random, num_steps=100)
    regrets3 = testbed3.get_results()[2]

    testbed10 = BanditTestbed(num_arms=10, num_instances=50, seed=42)
    testbed10.run_algorithm(dummy_select_random, num_steps=100)
    regrets10 = testbed10.get_results()[2]

    # More arms = worse random selection = higher regret
    assert regrets10[-1] > regrets3[-1]
