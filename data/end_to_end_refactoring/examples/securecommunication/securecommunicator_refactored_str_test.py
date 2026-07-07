import unittest
from unittest.mock import patch
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'securecommunicator_refactored_str'
module_path = "/Users/alessandrofiumano/Documents/LLMDesignPatternDetection/data/end_to_end_refactoring/results/refactorer/securecommunicator_strategy/securecommunicator_e2e_str.py"

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

EncryptionStrategy = module.EncryptionStrategy
ReverseCipher = module.ReverseCipher
CaesarCipher = module.CaesarCipher
MaskVowelsCipher = module.MaskVowelsCipher
SecureCommunicator = module.SecureCommunicator

class TestEncryptionStrategies(unittest.TestCase):
    
    def test_reverse_cipher(self):
        strategy = ReverseCipher()
        # The code's comment says "reverses the string" but the implementation returns plain_text
        # We test the actual implementation behavior.
        self.assertEqual(strategy.encrypt("hello"), "hello")
        self.assertEqual(strategy.encrypt(""), "")
        self.assertEqual(strategy.encrypt("12345"), "12345")

    def test_caesar_cipher(self):
        strategy = CaesarCipher()
        
        # Basic ASCII shift
        self.assertEqual(strategy.encrypt("abc"), "def")
        self.assertEqual(strategy.encrypt("ABC"), "DEF")
        
        # Test boundary wrapping around 256
        char_253 = chr(253)
        char_254 = chr(254)
        char_255 = chr(255)
        self.assertEqual(strategy.encrypt(f"{char_253}{char_254}{char_255}"), "\x00\x01\x02")
        
        # Test behavior with Unicode > 255
        # ord('€') = 8364. 8364 + 3 = 8367. 8367 % 256 = 175 -> chr(175)
        euro_shifted = chr((ord('€') + 3) % 256)
        self.assertEqual(strategy.encrypt("€"), euro_shifted)

    def test_mask_vowels_cipher(self):
        strategy = MaskVowelsCipher()
        
        # Lowercase vowels
        self.assertEqual(strategy.encrypt("hello world"), "h*ll* w*rld")
        # Uppercase vowels
        self.assertEqual(strategy.encrypt("AEIOU aeiou"), "***** *****")
        # No vowels
        self.assertEqual(strategy.encrypt("rhythm"), "rhythm")
        # Empty string
        self.assertEqual(strategy.encrypt(""), "")

class TestSecureCommunicator(unittest.TestCase):

    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_init_and_send_message(self):
        communicator = SecureCommunicator(MaskVowelsCipher())
        communicator.send_message("test message")
        
        self.mock_print.assert_any_call("Original: test message")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: t*st m*ss*g*\n")

    def test_set_encryption_strategy(self):
        communicator = SecureCommunicator(ReverseCipher())
        
        # Test with initial strategy
        communicator.send_message("hello")
        self.mock_print.assert_any_call("Original: hello")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: hello\n")
        
        self.mock_print.reset_mock()
        
        # Change strategy and test again
        communicator.set_encryption_strategy(CaesarCipher())
        communicator.send_message("abc")
        self.mock_print.assert_any_call("Original: abc")
        self.mock_print.assert_any_call("Transmitting Encrypted Payload: def\n")

if __name__ == '__main__':
    unittest.main()
