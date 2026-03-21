from abc import ABC, abstractmethod

# Example of Virtual Proxy applied to blockchain requests

class BlockChainInterface(ABC):
    @abstractmethod
    def get_block(self, block_number):
        pass

class BlockChainDB(BlockChainInterface):
    def __init__(self):
        # memory-heavy object (simplified representation)
        self.db = {
            1: ["transaction 1", "transaction 2"],
            2: ["transaction 3", "transaction 4"],
            3: ["transaction 5", "transaction 6"],
            4: ["transaction 7", "transaction 8"]
        }
    def get_block(self, block_number):
        return self.db[block_number]

class BlockChainProxy(BlockChainInterface):
    def __init__(self):
        self.db = None
    def get_block(self, block_number):
        if self.db is None:
            self.db = BlockChainDB()        # lazy inizialization
        return self.db.get_block(block_number)

def client(servie: BlockChainInterface):
    print(f"Blockchain: {servie.get_block(1)}")
