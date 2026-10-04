import numpy as np
from _load import load_solution


_module = load_solution(__file__)
maskgit_loss = _module.maskgit_loss


def test_basic_shape():
    logits = np.random.randn(4, 10, 256).astype(np.float32)
    targets = np.random.randint(0, 256, (4, 10))
    mask = np.ones((4, 10))
    loss = maskgit_loss(logits, targets, mask)
    assert isinstance(loss, (float, np.floating))


def test_no_mask():
    logits = np.random.randn(4, 10, 256).astype(np.float32)
    targets = np.random.randint(0, 256, (4, 10))
    mask = np.zeros((4, 10))
    loss = maskgit_loss(logits, targets, mask)
    assert loss == 0.0


def test_partial_mask():
    logits = np.random.randn(4, 10, 256).astype(np.float32)
    targets = np.random.randint(0, 256, (4, 10))
    mask = np.zeros((4, 10))
    mask[:, :5] = 1
    loss = maskgit_loss(logits, targets, mask)
    assert np.isfinite(loss)


def test_perfect_prediction():
    logits = np.zeros((4, 10, 256)).astype(np.float32)
    targets = np.zeros((4, 10), dtype=int)
    logits[:, :, 0] = 100.0
    mask = np.ones((4, 10))
    loss = maskgit_loss(logits, targets, mask)
    assert loss < 0.1


def test_worst_prediction():
    logits = np.zeros((4, 10, 256)).astype(np.float32)
    targets = np.zeros((4, 10), dtype=int)
    logits[:, :, 1:] = 100.0
    mask = np.ones((4, 10))
    loss = maskgit_loss(logits, targets, mask)
    assert loss > 5.0


def test_different_vocab_sizes():
    for vocab_size in [10, 100, 1000]:
        logits = np.random.randn(2, 8, vocab_size).astype(np.float32)
        targets = np.random.randint(0, vocab_size, (2, 8))
        mask = np.ones((2, 8))
        loss = maskgit_loss(logits, targets, mask)
        assert np.isfinite(loss)


def test_different_sequence_lengths():
    for seq_len in [5, 10, 20]:
        logits = np.random.randn(4, seq_len, 256).astype(np.float32)
        targets = np.random.randint(0, 256, (4, seq_len))
        mask = np.ones((4, seq_len))
        loss = maskgit_loss(logits, targets, mask)
        assert np.isfinite(loss)


def test_batch_averaging():
    logits = np.random.randn(4, 10, 256).astype(np.float32)
    targets = np.zeros((4, 10), dtype=int)
    logits[:, :, 0] = 10.0
    mask = np.ones((4, 10))
    loss = maskgit_loss(logits, targets, mask)
    assert np.isfinite(loss) and loss >= 0


def test_finite_outputs():
    for _ in range(10):
        logits = np.random.randn(4, 10, 256).astype(np.float32)
        targets = np.random.randint(0, 256, (4, 10))
        mask = np.random.randint(0, 2, (4, 10))
        loss = maskgit_loss(logits, targets, mask)
        assert np.isfinite(loss)


def test_all_targets_valid():
    vocab_size = 256
    logits = np.random.randn(4, 10, vocab_size).astype(np.float32)
    targets = np.random.randint(0, vocab_size, (4, 10))
    mask = np.ones((4, 10))
    loss = maskgit_loss(logits, targets, mask)
    assert np.isfinite(loss) and loss >= 0
