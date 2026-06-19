from abc import ABC, abstractmethod


class PaymentContext:
    def __init__(self, amount: float, currency: str) -> None:
        self.amount = amount
        self.currency = currency


# Strategy
class PaymentStrategy(ABC):
    @abstractmethod
    def apply(self, context: PaymentContext) -> bool:
        pass


# ConcreteStrategy
class FraudDetectionStrategy(PaymentStrategy):
    def apply(self, context: PaymentContext) -> bool:
        print("Fraud Check: Analyzing transaction risk...")

        if context.amount > 10000:
            print("Fraud Check FAILED: Amount exceeds automatic approval threshold.")
            return False

        print("Fraud Check PASSED.")
        return True


# ConcreteStrategy
class CurrencyConversionStrategy(PaymentStrategy):
    def __init__(self, target_currency: str, rate: float) -> None:
        self._target_currency = target_currency
        self._rate = rate

    def apply(self, context: PaymentContext) -> bool:
        converted_amount = context.amount * self._rate

        print(f"Conversion: {context.amount:.2f} {context.currency} -> {converted_amount:.2f} {self._target_currency}")

        context.amount = converted_amount
        context.currency = self._target_currency
        return True


class PaymentProcessor:
    def __init__(self, strategies: list[PaymentStrategy]) -> None:
        self._strategies = strategies

    def process(self, amount: float, currency: str) -> bool:
        context = PaymentContext(amount, currency)

        for strategy in self._strategies:
            if not strategy.apply(context):
                return False

        print(f"Gateway: Successfully processed {context.amount:.2f} {context.currency}")
        return True