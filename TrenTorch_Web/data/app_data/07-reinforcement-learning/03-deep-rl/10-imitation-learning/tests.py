import numpy as np

from _load import load_solution

_module = load_solution(__file__)
behavioral_cloning_loss = _module.behavioral_cloning_loss


def test_basic_loss():
    """Basic behavioral cloning loss."""
    logits = [[1.0, 0.0, 0.0]]
    expert = [0]

    loss = behavioral_cloning_loss(logits, expert)

    assert isinstance(loss, float)
    assert loss >= 0


def test_perfect_prediction():
    """Perfect prediction has low loss."""
    logits = [[10.0, 0.0, 0.0]]  # Confident in action 0
    expert = [0]

    loss_good = behavioral_cloning_loss(logits, expert)

    # Wrong action
    loss_bad = behavioral_cloning_loss(logits, [1])

    assert loss_good < loss_bad


def test_uniform_logits():
    """Uniform logits give baseline loss."""
    logits = [[0.0, 0.0, 0.0]]
    expert = [0]

    loss = behavioral_cloning_loss(logits, expert)

    # log(1/3) = -ln(3)
    assert loss > 0


def test_batch_loss():
    """Batch loss averages correctly."""
    logits = [
        [10.0, 0.0],  # Expert correct
        [0.0, 10.0]   # Expert wrong
    ]
    expert = [0, 0]

    loss = behavioral_cloning_loss(logits, expert)

    # Should be between 0 (first correct) and high (second wrong)
    assert loss > 0


def test_multi_action():
    """Multiple action space."""
    logits = np.random.randn(32, 5)
    expert = np.random.randint(0, 5, size=32)

    loss = behavioral_cloning_loss(logits, expert)

    assert loss >= 0
    assert np.isfinite(loss)
