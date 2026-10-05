import numpy as np


class BanditTestbed:
    """
    A testbed for evaluating multi-armed bandit algorithms.

    The testbed generates random bandit instances and runs algorithms on them,
    measuring cumulative regret and optimal arm selection rate.
    """

    def __init__(self, num_arms, num_instances, seed):
        """
        Initialize the testbed with random bandit instances.

        Args:
            num_arms: number of arms in each bandit
            num_instances: number of independent bandit instances
            seed: random seed for reproducibility
        """
        pass

    def run_algorithm(self, select_fn, num_steps):
        """
        Run a bandit algorithm on all instances.

        Args:
            select_fn: callable with signature select_fn(q_estimates, counts, t, rng) -> action
                      Takes current Q-value estimates, visit counts, time step, and RNG.
                      Returns the selected action (int in [0, num_arms)).
            num_steps: number of steps to run on each instance

        Returns:
            None (results stored internally)
        """
        pass

    def get_results(self):
        """
        Get aggregated results from the last run_algorithm call.

        Returns:
            mean_rewards: array of shape (num_steps,), mean reward at each step
            optimal_counts: array of shape (num_steps,), count of times optimal arm was selected
            regrets: array of shape (num_steps,), cumulative regret at each step
        """
        pass
