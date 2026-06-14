from enum import Enum

class Cypher(Enum):
    REVERSE = "reverse",
    CAESAR = "caesar",
    MASKVOWELS = "maskvowels"


class Communicator:
    def __init__(self, cypher: Cypher):
        self.cypher = cypher

    def send_message(self, message: str):
        vowels = "aeiouAEIOU"
        if self.cypher == Cypher.REVERSE:
            print(f"Original: {message}")
            print(f"Transmitting Encrypted Payload: {message}\n")
        elif self.cypher == Cypher.CAESAR:
            print(f"Original: {message}")
            print(f"Transmitting Encrypted Payload: {"".join(chr((ord(char) + 3) % 256) for char in message)}\n")
        elif self.cypher == Cypher.MASKVOWELS:
            print(f"Original: {message}")
            print(f"Transmitting Encrypted Payload: {"".join("*" if char in vowels else char for char in message)}\n")
        else:
            print("Unknown cypher. Cannot encrypt message.")