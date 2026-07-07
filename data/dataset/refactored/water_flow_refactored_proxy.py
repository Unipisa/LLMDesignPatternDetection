from abc import ABC, abstractmethod
from datetime import datetime

class FluidOutletInterface(ABC):
    @abstractmethod
    def dispense(self, volume: float):      # volume in liters
        pass

class PhisicalValve(FluidOutletInterface):
    def dispense(self, volume: float):
        return f"Dispensed {volume} liters of water"

class WaterFlowController(FluidOutletInterface):
    def __init__(self, valve: PhisicalValve):
        self.valve = valve
        self._history = []

    def dispense(self, volume: float):
        self._history.append((datetime.now(), volume))
        if self.valve is None:
            return "No valve available"
        return self.valve.dispense(volume)

    def get_recorded_usage(self):
        return self._history