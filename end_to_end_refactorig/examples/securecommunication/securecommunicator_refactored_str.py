from abc import ABC, abstractmethod

# Participant: Strategy
class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, plain_text: str) -> str:
        pass

# Participant: ConcreteStrategy
class ReverseCipher(EncryptionStrategy):
    def encrypt(self, plain_text: str) -> str:
        # Trivial encryption: reverses the string
        return plain_text

# Participant: ConcreteStrategy
class CaesarCipher(EncryptionStrategy):
    def encrypt(self, plain_text: str) -> str:
        # Shifts characters by 3
        return "".join(chr((ord(char) + 3) % 256) for char in plain_text)

# Participant: ConcreteStrategy
class MaskVowelsCipher(EncryptionStrategy):
    def encrypt(self, plain_text: str) -> str:
        vowels = "aeiouAEIOU"
        return "".join("*" if char in vowels else char for char in plain_text)

# Participant: Context
class SecureCommunicator:
    def __init__(self, strategy: EncryptionStrategy):
        self._strategy = strategy

    def set_encryption_strategy(self, strategy: EncryptionStrategy) -> None:
        self._strategy = strategy

    def send_message(self, message: str) -> None:
        encrypted_msg = self._strategy.encrypt(message)
        print(f"Original: {message}")
        print(f"Transmitting Encrypted Payload: {encrypted_msg}\n")