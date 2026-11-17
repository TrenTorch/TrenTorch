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
        self.num_arms = num_arms
        self.num_instances = num_instances
        self.rng = np.random.default_rng(seed)

        # Generate true arm rewards for each instance
        # Shape: (num_instances, num_arms)
        self.true_rewards = self.rng.standard_normal(
            size=(num_instances, num_arms)
        )

        # Identify the optimal arm for each instance (highest true reward)
        self.optimal_arms = np.argmax(self.true_rewards, axis=1)
        self.optimal_values = np.max(self.true_rewards, axis=1)

        # Storage for results
        self.last_rewards = None
        self.last_optimal_counts = None
        self.last_regrets = None

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
        # Track results for each instance
        instance_rewards = []
        instance_optimal_counts = []
        instance_regrets = []

        for instance_idx in range(self.num_instances):
            # Initialize Q-value estimates and visit counts
            q_estimates = np.zeros(self.num_arms)
            counts = np.zeros(self.num_arms, dtype=int)

            # Create an RNG for this instance (to ensure reproducibility)
            instance_rng = np.random.default_rng(
                seed=self.rng.integers(0, 2**32 - 1)
            )

            # Storage for this instance
            step_rewards = []
            step_optimal_counts = []
            step_regrets = []
            cumulative_regret = 0.0

            optimal_arm = self.optimal_arms[instance_idx]
            optimal_value = self.optimal_values[instance_idx]
            true_arms = self.true_rewards[instance_idx]

            for step in range(num_steps):
                # Select an action using the algorithm
                action = select_fn(q_estimates, counts, step + 1, instance_rng)

                # Observe reward: sample from N(true_reward[action], 1)
                observed_reward = instance_rng.normal(
                    loc=true_arms[action], scale=1.0
                )

                # Update Q-value estimate incrementally
                counts[action] += 1
                q_estimates[action] += (
                    1.0 / counts[action] * (observed_reward - q_estimates[action])
                )

                # Record results for this step
                step_rewards.append(observed_reward)

                # Check if we selected the optimal arm
                is_optimal = 1 if action == optimal_arm else 0
                step_optimal_counts.append(is_optimal)

                # Compute regret for this step
                regret = optimal_value - true_arms[action]
                cumulative_regret += regret
                step_regrets.append(cumulative_regret)

            instance_rewards.append(step_rewards)
            instance_optimal_counts.append(step_optimal_counts)
            instance_regrets.append(step_regrets)

        # Average results across instances
        instance_rewards = np.array(instance_rewards)  # (num_instances, num_steps)
        instance_optimal_counts = np.array(instance_optimal_counts)
        instance_regrets = np.array(instance_regrets)

        self.last_rewards = np.mean(instance_rewards, axis=0)
        self.last_optimal_counts = np.sum(instance_optimal_counts, axis=0)
        self.last_regrets = np.mean(instance_regrets, axis=0)

    def get_results(self):
        """
        Get aggregated results from the last run_algorithm call.

        Returns:
            mean_rewards: array of shape (num_steps,), mean reward at each step
            optimal_counts: array of shape (num_steps,), count of times optimal arm was selected
            regrets: array of shape (num_steps,), cumulative regret at each step
        """
        if self.last_rewards is None:
            raise RuntimeError(
                "No algorithm has been run yet. Call run_algorithm() first."
            )
        return self.last_rewards, self.last_optimal_counts, self.last_regrets
