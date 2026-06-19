import abc
from dataclasses import dataclass


class BaseGateway:
    """Concrete component that performs the actual payment processing."""

    def process(self, amount: float, currency: str) -> bool:
        print(f"Gateway: Successfully processed {amount:.2f} {currency}")
        return True


class PaymentDecorator(BaseGateway, abc.ABC):
    """Abstract decorator that forwards calls to a wrapped component."""

    def __init__(self, component: BaseGateway) -> None:
        self._component = component

    @abc.abstractmethod
    def process(self, amount: float, currency: str) -> bool:
        pass


class FraudDetectionFilter(PaymentDecorator):
    """Concrete decorator that performs fraud detection before delegating."""

    def process(self, amount: float, currency: str) -> bool:
        print("Fraud Check: Analyzing transaction risk...")
        if amount > 10000:
            print(
                "Fraud Check FAILED: Amount exceeds automatic approval threshold."
            )
            return False
        print("Fraud Check PASSED.")
        return self._component.process(amount, currency)


class CurrencyConverter(PaymentDecorator):
    """Concrete decorator that converts the amount to a target currency."""

    def __init__(
        self,
        component: BaseGateway,
        target_currency: str,
        rate: float,
    ) -> None:
        super().__init__(component)
        self._target_currency = target_currency
        self._rate = rate

    def process(self, amount: float, currency: str) -> bool:
        converted_amount = amount * self._rate
        print(
            f"Conversion: {amount:.2f} {currency} -> {converted_amount:.2f} {self._target_currency}"
        )
        return self._component.process(converted_amount, self._target_currency)