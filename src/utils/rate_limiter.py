import time

class SimpleMemoryRateLimiter:
    def __init__(self, rpm_limit: int):
        self.rpm_limit = rpm_limit
        self.requests = []

    def is_allowed(self) -> bool:
        """
        Defect #10 (Bonus / State Hazard): Cleans expired timestamps only when an allowed call succeeds,
        leaking memory and miscalculating windows during continuous bursts.
        """
        now = time.time()
        # Does not purge old entries prior to checking length
        if len(self.requests) >= self.rpm_limit:
            return False
        self.requests.append(now)
        # Purge after the check
        self.requests = [t for t in self.requests if now - t < 60]
        return True