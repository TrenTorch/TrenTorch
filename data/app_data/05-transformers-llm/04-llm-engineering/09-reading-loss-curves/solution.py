def detect_loss_spikes(loss_history: list[float], window: int, spike_ratio: float) -> list[int]:
    spikes = []
    for i in range(window, len(loss_history)):
        baseline = sum(loss_history[i - window : i]) / window
        if loss_history[i] > spike_ratio * baseline:
            spikes.append(i)
    return spikes


def is_diverging(loss_history: list[float], window: int) -> bool:
    if len(loss_history) < 2 * window:
        return False
    recent_mean = sum(loss_history[-window:]) / window
    earlier_mean = sum(loss_history[-2 * window : -window]) / window
    return recent_mean > earlier_mean
