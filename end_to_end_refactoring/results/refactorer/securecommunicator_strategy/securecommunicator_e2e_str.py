from abc import ABC, abstractmethod


class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        """Return the encrypted form of plaintext."""
        pass


class ReverseCipher(EncryptionStrategy):
    def encrypt(self, plaintext: str) -> str:
        # The original implementation did not reverse; keep behavior.
        return plaintext


class CaesarCipher(EncryptionStrategy):
    def encrypt(self, plaintext: str) -> str:
        return "".join(chr((ord(ch) + 3) % 256) for ch in plaintext)


class MaskVowelsCipher(EncryptionStrategy):
    VOWELS = "aeiouAEIOU"

    def encrypt(self, plaintext: str) -> str:
        return "".join("*" if ch in self.VOWELS else ch for ch in plaintext)


class SecureCommunicator:
    def __init__(self, strategy: EncryptionStrategy):
        self._strategy = strategy

    def set_encryption_strategy(self, strategy: EncryptionStrategy) -> None:
        self._strategy = strategy

    def send_message(self, message: str) -> None:
        encrypted = self._strategy.encrypt(message)
        print(f"Original: {message}")
        print(f"Transmitting Encrypted Payload: {encrypted}\n")