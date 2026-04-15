from abc import ABC, abstractmethod

# Example of Virtual Proxy applied to ledger access

class LedgerInterface(ABC):
    @abstractmethod
    def get_block(self, block_number):
        pass

class LedgerDB(LedgerInterface):
    def __init__(self):
        # memory-heavy object (simplified representation)
        self.heavy_db = [f"transaction_{i}" for i in range(20000000)]
    def get_block(self, block_number):
        return self.heavy_db[block_number]

class LedgerProxy(LedgerInterface):
    def __init__(self):
        self.db = None
    def get_block(self, block_number):
        if self.db is None:
            self.db = LedgerDB()        # lazy inizialization
        return self.db.get_block(block_number)

def client(service: LedgerInterface):
    print( f"Ledger: {service.get_block(10333)}")

if __name__ == "__main__":
    client(LedgerProxy())