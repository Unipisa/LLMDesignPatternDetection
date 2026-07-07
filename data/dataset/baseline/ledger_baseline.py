class LedgerDB:
    def __init__(self):
        self.heavy_db = [f"transaction_{i}" for i in range(20000000)]
    def get_block(self, block_number):
        return self.heavy_db[block_number]