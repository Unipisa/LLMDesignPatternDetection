import unittest
from unittest.mock import patch
import os
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'securecommunicator_refactored_fm'
module_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

Cypher = module.Cypher
ReverseCipher = module.ReverseCipher
CaesarCipher = module.CaesarCipher
MaskVowelsCipher = module.MaskVowelsCipher
CypherCreator = module.CypherCreator
ReverseCipherCreator = module.ReverseCipherCreator
CaesarCipherCreator = module.CaesarCipherCreator
MaskVowelsCipherCreator = module.MaskVowelsCipherCreator


class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.reverse_creator = ReverseCipherCreator()
        self.caesar_creator = CaesarCipherCreator()
        self.mask_vowels_creator = MaskVowelsCipherCreator()

    def test_reverse_cipher(self):
        cypher = self.reverse_creator.create_cypher()
        # The code's comment says "reverses the string" but the implementation returns plain_text
        # We test the actual implementation behavior.
        self.assertEqual(cypher.encrypt("hello"), "hello")
        self.assertEqual(cypher.encrypt(""), "")
        self.assertEqual(cypher.encrypt("12345"), "12345")

    def test_caesar_cipher(self):
        cypher = self.caesar_creator.create_cypher()

        # Basic ASCII shift
        self.assertEqual(cypher.encrypt("abc"), "def")
        self.assertEqual(cypher.encrypt("ABC"), "DEF")

        # Test boundary wrapping around 256
        char_253 = chr(253)
        char_254 = chr(254)
        char_255 = chr(255)
        self.assertEqual(cypher.encrypt(f"{char_253}{char_254}{char_255}"), "\x00\x01\x02")

        # Test behavior with Unicode > 255
        # ord('€') = 8364. 8364 + 3 = 8367. 8367 % 256 = 175 -> chr(175)
        euro_shifted = chr((ord('€') + 3) % 256)
        self.assertEqual(cypher.encrypt("€"), euro_shifted)

    def test_mask_vowels_cipher(self):
        cypher = self.mask_vowels_creator.create_cypher()

        # Lowercase vowels
        self.assertEqual(cypher.encrypt("hello world"), "h*ll* w*rld")
        # Uppercase vowels
        self.assertEqual(cypher.encrypt("AEIOU aeiou"), "***** *****")
        # No vowels
        self.assertEqual(cypher.encrypt("rhythm"), "rhythm")
        # Empty string
        self.assertEqual(cypher.encrypt(""), "")


class TestCypherCreatorSendMessage(unittest.TestCase):
    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

        self.reverse_creator = ReverseCipherCreator()
        self.caesar_creator = CaesarCipherCreator()
        self.mask_vowels_creator = MaskVowelsCipherCreator()

    def test_send_message_with_reverse_cipher_creator(self):
        self.reverse_creator.send_message("hello")

        self.mock_print.assert_any_call("Original: hello")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: hello\n")

    def test_send_message_with_caesar_cipher_creator(self):
        self.caesar_creator.send_message("abc")

        self.mock_print.assert_any_call("Original: abc")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: def\n")

    def test_send_message_with_mask_vowels_cipher_creator(self):
        self.mask_vowels_creator.send_message("test message")

        self.mock_print.assert_any_call("Original: test message")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: t*st m*ss*g*\n")


if __name__ == '__main__':
    unittest.main()
