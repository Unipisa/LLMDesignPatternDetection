import unittest
from unittest.mock import patch
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'paymentprocessor_refactored_str'
module_path = "/Users/alessandrofiumano/Documents/LLMDesignPatternDetection/end_to_end_refactoring/results/refactorer/paymentprocessor_strategy/paymentprocessor_e2e_str.py"

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PaymentContext = module.PaymentContext
PaymentStrategy = module.PaymentStrategy
FraudDetectionStrategy = module.FraudDetectionStrategy
CurrencyConversionStrategy = module.CurrencyConversionStrategy
PaymentProcessor = module.PaymentProcessor


class TestPaymentDecorators(unittest.TestCase):

    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_base_gateway(self):
        processor = PaymentProcessor([])
        result = processor.process(100.0, "USD")
        self.assertTrue(result)
        self.mock_print.assert_called_once_with("Gateway: Successfully processed 100.00 USD")

    def test_fraud_detection_pass(self):
        processor = PaymentProcessor([FraudDetectionStrategy()])

        # Test boundary values below 10000
        result = processor.process(5000.0, "EUR")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Fraud Check: Analyzing transaction risk...")
        self.mock_print.assert_any_call("Fraud Check PASSED.")
        self.mock_print.assert_any_call("Gateway: Successfully processed 5000.00 EUR")

    def test_fraud_detection_exact_boundary(self):
        processor = PaymentProcessor([FraudDetectionStrategy()])

        # 10000 is not > 10000, so it should pass
        result = processor.process(10000.0, "GBP")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Fraud Check PASSED.")

    def test_fraud_detection_fail(self):
        processor = PaymentProcessor([FraudDetectionStrategy()])

        result = processor.process(15000.0, "USD")
        self.assertFalse(result)
        self.mock_print.assert_any_call("Fraud Check: Analyzing transaction risk...")
        self.mock_print.assert_any_call("Fraud Check FAILED: Amount exceeds automatic approval threshold.")

        # Ensure gateway wasn't called because the flow was interrupted
        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))

    def test_currency_converter(self):
        processor = PaymentProcessor([CurrencyConversionStrategy("EUR", 0.85)])

        result = processor.process(100.0, "USD")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Conversion: 100.00 USD -> 85.00 EUR")
        self.mock_print.assert_any_call("Gateway: Successfully processed 85.00 EUR")

    def test_multiple_strategies_success(self):
        # Pipeline: FraudDetectionStrategy -> CurrencyConversionStrategy -> Gateway
        processor = PaymentProcessor([
            FraudDetectionStrategy(),
            CurrencyConversionStrategy("EUR", 0.85)
        ])

        result = processor.process(500.0, "USD")
        self.assertTrue(result)

        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertEqual(calls[0], "Fraud Check: Analyzing transaction risk...")
        self.assertEqual(calls[1], "Fraud Check PASSED.")
        self.assertEqual(calls[2], "Conversion: 500.00 USD -> 425.00 EUR")
        self.assertEqual(calls[3], "Gateway: Successfully processed 425.00 EUR")

    def test_multiple_strategies_fraud_fail(self):
        # Pipeline: FraudDetectionStrategy -> CurrencyConversionStrategy -> Gateway
        processor = PaymentProcessor([
            FraudDetectionStrategy(),
            CurrencyConversionStrategy("EUR", 0.85)
        ])

        # amount > 10000, so fraud detection blocks it before currency conversion
        result = processor.process(12000.0, "USD")
        self.assertFalse(result)

        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertIn("Fraud Check FAILED: Amount exceeds automatic approval threshold.", calls)
        self.assertFalse(any(call.startswith("Conversion:") for call in calls))
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))

    def test_multiple_strategies_different_order(self):
        # Pipeline: CurrencyConversionStrategy -> FraudDetectionStrategy -> Gateway
        processor = PaymentProcessor([
            CurrencyConversionStrategy("JPY", 150.0),
            FraudDetectionStrategy()
        ])

        # 100 USD converts to 15000 JPY, which triggers the FraudDetectionStrategy
        result = processor.process(100.0, "USD")
        self.assertFalse(result)

        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertEqual(calls[0], "Conversion: 100.00 USD -> 15000.00 JPY")
        self.assertEqual(calls[1], "Fraud Check: Analyzing transaction risk...")
        self.assertEqual(calls[2], "Fraud Check FAILED: Amount exceeds automatic approval threshold.")
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))


if __name__ == '__main__':
    unittest.main()
