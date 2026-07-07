from abc import ABC, abstractmethod

# Participant: Component
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float, currency: str) -> bool:
        pass

# Participant: ConcreteComponent
class BaseGateway(PaymentProcessor):
    def process(self, amount: float, currency: str) -> bool:
        print(f"Gateway: Successfully processed {amount:.2f} {currency}")
        return True

# Participant: Decorator
class PaymentDecorator(PaymentProcessor, ABC):
    def __init__(self, processor: PaymentProcessor) -> None:
        self._processor = processor

    @abstractmethod
    def process(self, amount: float, currency: str) -> bool:
        return self._processor.process(amount, currency)

# Participant: ConcreteDecorator
class FraudDetectionFilter(PaymentDecorator):
    def process(self, amount: float, currency: str) -> bool:
        print("Fraud Check: Analyzing transaction risk...")
        if amount > 10000:
            print("Fraud Check FAILED: Amount exceeds automatic approval threshold.")
            return False
        print("Fraud Check PASSED.")
        return super().process(amount, currency)

# Participant: ConcreteDecorator
class CurrencyConverter(PaymentDecorator):
    def __init__(self, processor: PaymentProcessor, target_currency: str, rate: float) -> None:
        super().__init__(processor)
        self._target_currency = target_currency
        self._rate = rate

    def process(self, amount: float, currency: str) -> bool:
        converted_amount = amount * self._rate
        print(f"Conversion: {amount:.2f} {currency} -> {converted_amount:.2f} {self._target_currency}")
        return super().process(converted_amount, self._target_currency)
