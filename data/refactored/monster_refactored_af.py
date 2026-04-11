from abc import ABC, abstractmethod

class Leg(ABC):
    def __init__(self, base_speed, speed_modifier):
        self.base_speed = base_speed
        self.speed_modifier = speed_modifier

    def get_speed(self):
        return self.base_speed * self.speed_modifier

    def __str__(self):
        return f"Speed: {self.get_speed():.2f}"


class Arm(ABC):
    def __init__(self, base_attack, attack_modifier):
        self.base_attack = base_attack
        self.attack_modifier = attack_modifier

    def get_attack_power(self):
        return self.base_attack * self.attack_modifier

    def __str__(self):
        return f"Attack: {self.get_attack_power():.2f}"

# ------------------------------
# Concrete Leg Classes
# ------------------------------

class ZombieLeg(Leg):
    def __init__(self):
        super().__init__(base_speed=5, speed_modifier=0.75)

class SkeletonLeg(Leg):
    def __init__(self):
        super().__init__(base_speed=8, speed_modifier=1.00)

# ------------------------------
# Concrete Arm Classes
# ------------------------------

class ZombieArm(Arm):
    def __init__(self):
        super().__init__(base_attack=10, attack_modifier=0.85)

class SkeletonArm(Arm):
    def __init__(self):
        super().__init__(base_attack=15, attack_modifier=1.25)


class MonsterFactory(ABC):
    # These methods will now return mixed legs and arms
    @abstractmethod
    def create_right_leg(self):
        pass

    @abstractmethod
    def create_left_leg(self):
        pass

    @abstractmethod
    def create_right_arm(self):
        pass

    @abstractmethod
    def create_left_arm(self):
        pass
    @abstractmethod

    def create_name(self):
        pass
# Concrete Factory for Mixed Monsters
class SkeletonFactory(MonsterFactory):
    def create_right_leg(self):
        return SkeletonLeg()

    def create_left_leg(self):
        return SkeletonLeg()

    def create_right_arm(self):
        return SkeletonArm()

    def create_left_arm(self):
        return SkeletonArm()

    def create_name(self):
        return "Skeleton"


class ZombieFactory(MonsterFactory):
    def create_right_leg(self):
        return ZombieLeg()

    def create_left_leg(self):
        return ZombieLeg()

    def create_right_arm(self):
        return ZombieArm()

    def create_left_arm(self):
        return ZombieArm()

    def create_name(self):
        return "Zombie"


class GhoulFactory(MonsterFactory):
    def create_right_leg(self):
        return ZombieLeg()

    def create_left_leg(self):
        return SkeletonLeg()

    def create_right_arm(self):
        return ZombieArm()

    def create_left_arm(self):
        return SkeletonArm()

    def create_name(self):
        return "Ghoul"


# It is the client's responsibility to create the monster using the appropriate factory.
class Monster:
    def __init__(self, name, legs, arms):
        self.name = name
        self.legs = legs
        self.arms = arms

    def get_total_speed(self):
        return sum(leg.get_speed() for leg in self.legs) / len(self.legs)

    def get_total_attack(self):
        return sum(arm.get_attack_power() for arm in self.arms)

    def __str__(self):
        legs_str = ", ".join(str(leg) for leg in self.legs)
        arms_str = ", ".join(str(arm) for arm in self.arms)
        return (f"{self.name}:\n"
                f"  Legs: {legs_str}\n"
                f"  Arms: {arms_str}\n"
                f"  Total Speed: {self.get_total_speed():.2f}\n"
                f"  Total Attack: {self.get_total_attack():.2f}")


