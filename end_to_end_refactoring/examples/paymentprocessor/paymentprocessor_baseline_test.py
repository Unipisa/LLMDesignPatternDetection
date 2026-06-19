import unittest
from unittest.mock import patch
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'paymentprocessor_baseline'
module_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PaymentProcessor = module.PaymentProcessor
PaymentFeature = module.PaymentFeature



class TestPaymentProcessorBaseline(unittest.TestCase):

    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_base_gateway(self):
        processor = PaymentProcessor(features=[])
        result = processor.process(100.0, "USD")
        self.assertTrue(result)
        self.mock_print.assert_called_once_with("Gateway: Successfully processed 100.00 USD")

    def test_fraud_detection_pass(self):
        processor = PaymentProcessor(features=[PaymentFeature.FRAUD_DETECTION])

        # Test boundary values below 10000
        result = processor.process(5000.0, "EUR")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Fraud Check: Analyzing transaction risk...")
        self.mock_print.assert_any_call("Fraud Check PASSED.")
        self.mock_print.assert_any_call("Gateway: Successfully processed 5000.00 EUR")

    def test_fraud_detection_exact_boundary(self):
        processor = PaymentProcessor(features=[PaymentFeature.FRAUD_DETECTION])

        # 10000 is not > 10000, so it should pass
        result = processor.process(10000.0, "GBP")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Fraud Check PASSED.")

    def test_fraud_detection_fail(self):
        processor = PaymentProcessor(features=[PaymentFeature.FRAUD_DETECTION])

        result = processor.process(15000.0, "USD")
        self.assertFalse(result)
        self.mock_print.assert_any_call("Fraud Check: Analyzing transaction risk...")
        self.mock_print.assert_any_call("Fraud Check FAILED: Amount exceeds automatic approval threshold.")

        # Ensure gateway wasn't called (the flow was intercepted)
        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))

    def test_currency_converter(self):
        processor = PaymentProcessor(
            features=[PaymentFeature.CURRENCY_CONVERSION],
            target_currency="EUR",
            rate=0.85
        )

        result = processor.process(100.0, "USD")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Conversion: 100.00 USD -> 85.00 EUR")
        self.mock_print.assert_any_call("Gateway: Successfully processed 85.00 EUR")

    def test_multiple_decorators_success(self):
        # Baseline configuration: fraud detection + currency conversion
        processor = PaymentProcessor(
            features=[PaymentFeature.FRAUD_DETECTION, PaymentFeature.CURRENCY_CONVERSION],
            target_currency="EUR",
            rate=0.85
        )

        result = processor.process(500.0, "USD")
        self.assertTrue(result)

        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertEqual(calls[0], "Fraud Check: Analyzing transaction risk...")
        self.assertEqual(calls[1], "Fraud Check PASSED.")
        self.assertEqual(calls[2], "Conversion: 500.00 USD -> 425.00 EUR")
        self.assertEqual(calls[3], "Gateway: Successfully processed 425.00 EUR")

    def test_multiple_decorators_fraud_fail(self):
        # Baseline configuration: fraud detection + currency conversion
        processor = PaymentProcessor(
            features=[PaymentFeature.FRAUD_DETECTION, PaymentFeature.CURRENCY_CONVERSION],
            target_currency="EUR",
            rate=0.85
        )

        # amount > 10000, so fraud detection blocks it before currency conversion
        result = processor.process(12000.0, "USD")
        self.assertFalse(result)

        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertIn("Fraud Check FAILED: Amount exceeds automatic approval threshold.", calls)
        self.assertFalse(any(call.startswith("Conversion:") for call in calls))
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))


if __name__ == '__main__':
    unittest.main()
