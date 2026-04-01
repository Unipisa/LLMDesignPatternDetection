from datetime import datetime, timedelta

class Tlist:
    def __init__(self, temp):
        self.tlist = temp
        self.time = datetime.now()
    def get_time(self):
        return self.time
    def get_tlist(self):
        return self.tlist

class TenantDB:
    def __init__(self):
        self._data = ["milk", "bread", "cheese", "chicken", "rice", "pasta"]
        self._cached_data = None
        self._cache_time = None

    def get_tlist(self):
        if self._cached_data is not None and (datetime.now() - self._cache_time) < timedelta(hours=2):
            return self._cached_data
        self._cached_data = Tlist(self._data)
        self._cache_time = datetime.now()
        return self._cached_data