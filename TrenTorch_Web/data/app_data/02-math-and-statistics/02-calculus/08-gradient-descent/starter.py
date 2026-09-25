def gradient_descent_step(x, gradient_fn, learning_rate):
    """
    x: current position (scalar float or NumPy array)
    gradient_fn: function taking x, returning the gradient at x (same
        shape as x)
    learning_rate: a small positive float

    Returns:
        The next position, one gradient-descent update from x.
    """
    # TODO: Implement x - learning_rate * gradient_fn(x) from Theory.
    pass


def gradient_descent(x0, gradient_fn, learning_rate, num_steps):
    """
    x0: starting position
    gradient_fn, learning_rate: same as gradient_descent_step
    num_steps: number of update steps to run

    Returns:
        A list of length num_steps + 1: x0, followed by the position
        after each update.
    """
    # TODO: Implement the loop using gradient_descent_step, from Theory.
    pass
