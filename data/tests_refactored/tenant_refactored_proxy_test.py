from data.refactored.tenant_refactored_proxy import *
import unittest
from unittest.mock import MagicMock

class TestCacheProxy(unittest.TestCase):
    def setUp(self):
        self.db = DBTenant()
        self.db.get_tlist = MagicMock(wraps=self.db.get_tlist)
        self.proxy = CacheProxy(self.db)

    def test_resource(self):
        self.assertEqual(self.proxy.get_tlist().get_tlist(), self.db.get_tlist().get_tlist())

    def test_cache_hit(self):
        self.proxy.get_tlist()
        self.proxy.get_tlist()
        self.db.get_tlist.assert_called_once()

    def test_cache_invalidation(self):
        self.proxy.get_tlist()
        self.proxy.get_tlist().time = datetime.now() - timedelta(hours=3)
        self.proxy.get_tlist()
        self.assertEqual(self.db.get_tlist.call_count, 2)


if __name__ == "__main__":
    unittest.main()