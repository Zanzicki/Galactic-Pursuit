class ReusablePool():

    def __init__(self, max_size):
        self._pool = []
        self._max_size = max_size

    def acquire(self):
        if self._pool:
            return self._pool.pop()
        else:
            return None

    def release(self, obj):
        if len(self._pool) < self._max_size:
            self._pool.append(obj)    