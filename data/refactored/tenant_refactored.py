from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Example of cache proxy.
# The proxy intercepts data retrieval requests and checks if a local cache exists with a timestamp less than two hours old.
# If the cache is valid, it immediately returns the locally stored dataset to avoid unnecessary database queries.
# If the cache is missing or expired, it fetches the dataset from the remote source, updates the local cache and its timestamp, and returns the data.

class Tlist:
    def __init__(self, temp):
        self.tlist = temp
        self.time = datetime.now()
    def get_time(self):
        return self.time
    def get_tlist(self):
        return self.tlist

class InterfaceDB(ABC):
    @abstractmethod
    def get_tlist(self):
        pass


class DBTenant(InterfaceDB):
    def __init__(self):
        self.tlist = Tlist(["milk", "bread", "cheese", "chicken", "rice", "pasta"])
    def get_tlist(self):
        return self.tlist


class CacheProxy(InterfaceDB):
    def __init__(self, db: DBTenant):
        self.tlist = None
        self.db = db
    def get_tlist(self):
        if self.tlist is None or (datetime.now() - self.tlist.get_time()) > timedelta(hours=2):
            print("Cache miss")
            self.tlist = self.db.get_tlist()
        print("Proxy post-processing")
        return self.tlist
