from data.baseline.tenant_baseline import *
from datetime import datetime, timedelta
import unittest


class TestTenantDB(unittest.TestCase):
    def setUp(self):
        self.db = TenantDB()
    def test_resource(self):
        self.assertEqual(self.db.get_tlist().get_tlist(), self.db._data)

    def test_cache_hit(self):
        first_call = self.db.get_tlist()
        second_call = self.db.get_tlist()
        self.assertIs(first_call, second_call)  # verifica il riferimento allo stesso oggetto

    def test_cache_invalidation(self):
        first_call = self.db.get_tlist()
        self.db._cache_time = datetime.now() - timedelta(hours=3)
        second_call = self.db.get_tlist()   # quando scaduta, in cache viene ricreata una nuova Tlist
        self.assertIsNot(first_call, second_call)

