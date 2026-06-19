from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple


class PaymentStrategy(ABC):
    @abstractmethod
    def execute(self, amount: float, currency: str) -> Tuple[float, str, bool]:
        """Process the payment step.

        Returns a tuple of (amount, currency, continue_processing).
        """
        pass


class FraudDetectionStrategy(PaymentStrategy):
    def execute(self, amount: float, currency: str) -> Tuple[float, str, bool]:
        print("Fraud Check: Analyzing transaction risk...")
        if amount > 10_000:
            print(
                "Fraud Check FAILED: Amount exceeds automatic approval threshold."
            )
            return amount, currency, False
        print("Fraud Check PASSED.")
        return amount, currency, True


class CurrencyConversionStrategy(PaymentStrategy):
    def __init__(self, target_currency: str, rate: float) -> None:
        self._target_currency = target_currency
        self._rate = rate

    def execute(self, amount: float, currency: str) -> Tuple[float, str, bool]:
        converted_amount = amount * self._rate
        print(
            f"Conversion: {amount:.2f} {currency} -> {converted_amount:.2f} "
            f"{self._target_currency}"
        )
        return converted_amount, self._target_currency, True


class PaymentContext:
    def __init__(self, strategies: List[PaymentStrategy]) -> None:
        self._strategies = strategies

    def process(self, amount: float, currency: str) -> bool:
        for strategy in self._strategies:
            amount, currency, continue_processing = strategy.execute(amount, currency)
            if not continue_processing:
                return False
        print(f"Gateway: Successfully processed {amount:.2f} {currency}")
        return True


class PaymentProcessor:
    def __init__(self, strategies: List[PaymentStrategy] | None = None) -> None:
        self._context = PaymentContext(strategies or [])

    def process(self, amount: float, currency: str) -> bool:
        return self._context.process(amount, currency)