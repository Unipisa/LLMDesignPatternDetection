from abc import abstractmethod, ABC
# Products

class Cypher(ABC):
    @abstractmethod
    def encrypt(self, message: str) -> str:
        pass

class ReverseCipher(Cypher):
    def encrypt(self, plain_text: str) -> str:
        # Trivial encryption: reverses the string
        return plain_text

class CaesarCipher(Cypher):
    def encrypt(self, plain_text: str) -> str:
        # Shifts characters by 3
        return "".join(chr((ord(char) + 3) % 256) for char in plain_text)

class MaskVowelsCipher(Cypher):
    def encrypt(self, plain_text: str) -> str:
        vowels = "aeiouAEIOU"
        return "".join("*" if char in vowels else char for char in plain_text)

# Creator

class CypherCreator(ABC):
    @abstractmethod
    def create_cypher(self) -> Cypher:
        pass
  
    def send_message(self, message: str) -> None:
        cypher = self.create_cypher()
        print(f"Original: {message}")
        print(f"Transmitting Encrypted Payload: {cypher.encrypt(message)}\n")

class ReverseCipherCreator(CypherCreator):
    def create_cypher(self) -> Cypher:
        return ReverseCipher()

class CaesarCipherCreator(CypherCreator):
    def create_cypher(self) -> Cypher:
        return CaesarCipher()

class MaskVowelsCipherCreator(CypherCreator):
    def create_cypher(self) -> Cypher:
        return MaskVowelsCipher()
