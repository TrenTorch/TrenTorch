class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last = 0.0

    def try_acquire(self, now, n=1):
        self.tokens = min(self.capacity, self.tokens + self.refill_rate * (now - self.last))
        self.last = now
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False
