from datetime import datetime

class PhisicalValve:
    def __init__(self):
        self._history = []

    def dispense(self, volume: float):
        self._history.append((datetime.now(), volume))
        return f"Dispensed {volume} liters of water"

    def get_recorded_usage(self):
        return self._history