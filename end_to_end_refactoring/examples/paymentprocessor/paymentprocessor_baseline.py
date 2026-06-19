from enum import Enum

class PaymentFeature(Enum):
    FRAUD_DETECTION = "fraud_detection"
    CURRENCY_CONVERSION = "currency_conversion"


class PaymentProcessor:
    def __init__(self, features: list[PaymentFeature], target_currency: str | None = None, rate: float | None = None) -> None:
        self._features = features
        self._target_currency = target_currency
        self._rate = rate

    def process(self, amount: float, currency: str) -> bool:
        if PaymentFeature.FRAUD_DETECTION in self._features:
            print("Fraud Check: Analyzing transaction risk...")
            if amount > 10000:
                print("Fraud Check FAILED: Amount exceeds automatic approval threshold.")
                return False
            print("Fraud Check PASSED.")

        if PaymentFeature.CURRENCY_CONVERSION in self._features:
            converted_amount = amount * self._rate
            print(f"Conversion: {amount:.2f} {currency} -> {converted_amount:.2f} {self._target_currency}")
            amount = converted_amount
            currency = self._target_currency

        if (self._rate is None and self._target_currency is not None) or (self._rate is not None and self._target_currency is None):
            print("Error, create new payment processor")
            return False

        print(f"Gateway: Successfully processed {amount:.2f} {currency}")
        return True
