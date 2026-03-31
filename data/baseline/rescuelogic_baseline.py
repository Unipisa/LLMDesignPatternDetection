from enum import Enum

class RescueType(Enum):
    MOUNTAIN = 1
    MARITIME = 2


class RescueMission:
    def __init__(self, type_rescue: RescueType, fog, x, y, z):
        self.type = type_rescue
        self.fog = fog
        self.coordinates ={
            "x": x,
            "y": y,
            "z": z
        }
        self.log = []
    def start_rescue(self):
        if self.type == RescueType.MOUNTAIN:
            ground = True
            if not self.fog and self.coordinates["z"] > 3000:
                self.log.append("Taking off")
                ground = False
            elif not self.fog:
                self.log.append("Altitude too low for helicopter")
            if ground:
                self.log.append("Dispatch alpine rescue team")

        else:
            if self.fog:
                self.log.append("Sent maritime rescue team")
            else:
                self.log.append("Taking off")
        self.log.append("Mission completed")
        return ', '.join(self.log)

if __name__ == "__main__":
    mission = RescueMission(RescueType.MOUNTAIN, False, 100, 200, 1000)
    print(mission.start_rescue())
    miss = RescueMission(RescueType.MARITIME, True, 100, 200, 1000)
    print(miss.start_rescue())
