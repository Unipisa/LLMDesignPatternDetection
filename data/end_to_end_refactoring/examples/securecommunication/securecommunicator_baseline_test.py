import importlib.util
import os
import unittest
from unittest.mock import patch

module_name = "securecommunicator_baseline"
module_path = os.path.join(os.path.dirname(__file__), f"{module_name}.py")

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

Cypher = module.Cypher
Communicator = module.Communicator


class TestCypherAlgorithms(unittest.TestCase):

    def assert_encrypted_payload(self, cypher, message, expected_payload):
        with patch("builtins.print") as mock_print:
            communicator = Communicator(cypher)
            communicator.send_message(message)

        mock_print.assert_any_call(f"Original: {message}")
        mock_print.assert_any_call(f"Transmitting Encrypted Payload: {expected_payload}\n")

    def test_reverse_cipher(self):
        self.assert_encrypted_payload(Cypher.REVERSE, "hello", "hello")
        self.assert_encrypted_payload(Cypher.REVERSE, "", "")
        self.assert_encrypted_payload(Cypher.REVERSE, "12345", "12345")

    def test_caesar_cipher(self):
        self.assert_encrypted_payload(Cypher.CAESAR, "abc", "def")
        self.assert_encrypted_payload(Cypher.CAESAR, "ABC", "DEF")

        char_253 = chr(253)
        char_254 = chr(254)
        char_255 = chr(255)
        self.assert_encrypted_payload(
            Cypher.CAESAR,
            f"{char_253}{char_254}{char_255}",
            "\x00\x01\x02",
        )

        euro_shifted = chr((ord("€") + 3) % 256)
        self.assert_encrypted_payload(Cypher.CAESAR, "€", euro_shifted)

    def test_mask_vowels_cipher(self):
        self.assert_encrypted_payload(Cypher.MASKVOWELS, "hello world", "h*ll* w*rld")
        self.assert_encrypted_payload(Cypher.MASKVOWELS, "AEIOU aeiou", "***** *****")
        self.assert_encrypted_payload(Cypher.MASKVOWELS, "rhythm", "rhythm")
        self.assert_encrypted_payload(Cypher.MASKVOWELS, "", "")


class TestCommunicator(unittest.TestCase):

    def setUp(self):
        patcher = patch("builtins.print")
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_init_and_send_message(self):
        communicator = Communicator(Cypher.MASKVOWELS)
        communicator.send_message("test message")

        self.mock_print.assert_any_call("Original: test message")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: t*st m*ss*g*\n")

    def test_set_encryption_strategy(self):
        communicator = Communicator(Cypher.REVERSE)

        communicator.send_message("hello")
        self.mock_print.assert_any_call("Original: hello")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: hello\n")

        self.mock_print.reset_mock()

        communicator.cypher = Cypher.CAESAR
        communicator.send_message("abc")
        self.mock_print.assert_any_call("Original: abc")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: def\n")


if __name__ == "__main__":
    unittest.main()