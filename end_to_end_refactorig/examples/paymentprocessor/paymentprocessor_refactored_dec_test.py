import unittest
from unittest.mock import patch
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'paymentprocessor_refactored_dec'
module_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PaymentProcessor = module.PaymentProcessor
BaseGateway = module.BaseGateway
PaymentDecorator = module.PaymentDecorator
FraudDetectionFilter = module.FraudDetectionFilter
CurrencyConverter = module.CurrencyConverter

class TestPaymentDecorators(unittest.TestCase):

    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_base_gateway(self):
        gateway = BaseGateway()
        result = gateway.process(100.0, "USD")
        self.assertTrue(result)
        self.mock_print.assert_called_once_with("Gateway: Successfully processed 100.00 USD")

    def test_fraud_detection_pass(self):
        gateway = BaseGateway()
        fraud_filter = FraudDetectionFilter(gateway)
        
        # Test boundary values below 10000
        result = fraud_filter.process(5000.0, "EUR")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Fraud Check: Analyzing transaction risk...")
        self.mock_print.assert_any_call("Fraud Check PASSED.")
        self.mock_print.assert_any_call("Gateway: Successfully processed 5000.00 EUR")

    def test_fraud_detection_exact_boundary(self):
        gateway = BaseGateway()
        fraud_filter = FraudDetectionFilter(gateway)
        
        # 10000 is not > 10000, so it should pass
        result = fraud_filter.process(10000.0, "GBP")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Fraud Check PASSED.")

    def test_fraud_detection_fail(self):
        gateway = BaseGateway()
        fraud_filter = FraudDetectionFilter(gateway)
        
        result = fraud_filter.process(15000.0, "USD")
        self.assertFalse(result)
        self.mock_print.assert_any_call("Fraud Check: Analyzing transaction risk...")
        self.mock_print.assert_any_call("Fraud Check FAILED: Amount exceeds automatic approval threshold.")
        
        # Ensure gateway wasn't called (the flow was intercepted)
        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))

    def test_currency_converter(self):
        gateway = BaseGateway()
        converter = CurrencyConverter(gateway, "EUR", 0.85)
        
        result = converter.process(100.0, "USD")
        self.assertTrue(result)
        self.mock_print.assert_any_call("Conversion: 100.00 USD -> 85.00 EUR")
        self.mock_print.assert_any_call("Gateway: Successfully processed 85.00 EUR")

    def test_multiple_decorators_success(self):
        # Stack: FraudFilter -> CurrencyConverter -> BaseGateway
        gateway = BaseGateway()
        converter = CurrencyConverter(gateway, "EUR", 0.85)
        fraud_filter = FraudDetectionFilter(converter)
        
        result = fraud_filter.process(500.0, "USD")
        self.assertTrue(result)
        
        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertEqual(calls[0], "Fraud Check: Analyzing transaction risk...")
        self.assertEqual(calls[1], "Fraud Check PASSED.")
        self.assertEqual(calls[2], "Conversion: 500.00 USD -> 425.00 EUR")
        self.assertEqual(calls[3], "Gateway: Successfully processed 425.00 EUR")

    def test_multiple_decorators_fraud_fail(self):
        # Stack: FraudFilter -> CurrencyConverter -> BaseGateway
        gateway = BaseGateway()
        converter = CurrencyConverter(gateway, "EUR", 0.85)
        fraud_filter = FraudDetectionFilter(converter)
        
        # amount > 10000, so fraud filter blocks it before currency conversion
        result = fraud_filter.process(12000.0, "USD")
        self.assertFalse(result)
        
        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertIn("Fraud Check FAILED: Amount exceeds automatic approval threshold.", calls)
        self.assertFalse(any(call.startswith("Conversion:") for call in calls))
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))

    def test_multiple_decorators_different_order(self):
        # Stack: CurrencyConverter -> FraudFilter -> BaseGateway
        gateway = BaseGateway()
        fraud_filter = FraudDetectionFilter(gateway)
        converter = CurrencyConverter(fraud_filter, "JPY", 150.0)
        
        # 100 USD converts to 15000 JPY, which triggers the FraudFilter!
        result = converter.process(100.0, "USD")
        self.assertFalse(result)
        
        calls = [call[0][0] for call in self.mock_print.call_args_list]
        self.assertEqual(calls[0], "Conversion: 100.00 USD -> 15000.00 JPY")
        self.assertEqual(calls[1], "Fraud Check: Analyzing transaction risk...")
        self.assertEqual(calls[2], "Fraud Check FAILED: Amount exceeds automatic approval threshold.")
        self.assertFalse(any(call.startswith("Gateway:") for call in calls))

if __name__ == '__main__':
    unittest.main()
