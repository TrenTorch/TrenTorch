class CircuitBreaker:
    def __init__(self, failure_threshold, cooldown):
        self.failure_threshold = failure_threshold
        self.cooldown = cooldown
        self.state = "closed"
        self.failures = 0
        self.opened_at = None
        self._trial_out = False

    def allow(self, now):
        if self.state == "closed":
            return True
        if self.state == "open":
            if now - self.opened_at >= self.cooldown:
                self.state = "half_open"
                self._trial_out = True
                return True
            return False
        if self._trial_out:
            return False
        self._trial_out = True
        return True

    def record_success(self, now):
        self.failures = 0
        self.state = "closed"
        self._trial_out = False

    def record_failure(self, now):
        if self.state == "half_open":
            self.state = "open"
            self.opened_at = now
            self._trial_out = False
            return
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = "open"
            self.opened_at = now
