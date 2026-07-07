from abc import ABC, abstractmethod

# Impementing rescue missions logic through template method

class RescueMission(ABC):
    def __init__(self, fog, x, y, z):
        self.fog = fog
        self.coordinates ={
            "x": x,
            "y": y,
            "z": z
        }
        self.log = []

    @abstractmethod
    def helicopter_takeoff(self):
        pass
    @abstractmethod
    def send_ground_team(self):
        pass

    # mini template method (hook)
    def handle_approach(self):
        if self.fog:
            self.send_ground_team()
        else:
            ris = self.helicopter_takeoff()
            if not ris:
                self.send_ground_team()

    # template method
    def start_rescue(self):
        self.handle_approach()
        self.log.append("Mission completed")
        return ', '.join(self.log)


class MountainRescue(RescueMission):
    def helicopter_takeoff(self):
        if self.coordinates["z"] > 3000:
            self.log.append("Taking off")
            return True
        else:
            self.log.append("Altitude too low for helicopter")
            return False
    def send_ground_team(self):
        self.log.append("Dispatch alpine rescue team")
        return

class MaritimeRescue(RescueMission):
    def helicopter_takeoff(self):
        self.log.append("Taking off")
        return True

    def send_ground_team(self):
        self.log.append("Sent maritime rescue team")
        return
