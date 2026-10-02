def gradient_descent_step(x, gradient_fn, learning_rate):
    return x - learning_rate * gradient_fn(x)


def gradient_descent(x0, gradient_fn, learning_rate, num_steps):
    trajectory = [x0]
    for _ in range(num_steps):
        trajectory.append(gradient_descent_step(trajectory[-1], gradient_fn, learning_rate))
    return trajectory
