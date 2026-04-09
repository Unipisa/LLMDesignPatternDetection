from abc import abstractmethod, ABC

class TV(ABC):
    @abstractmethod
    def get_description(self):
        pass

class RC(ABC):
    @abstractmethod
    def get_description(self):
        pass

class SamsungTV(TV):
    def get_description(self):
        return "Samsung TV"

class PhilipsTV(TV):
    def get_description(self):
        return "Philips TV"

class SamsungRC(RC):
    def get_description(self):
        return "Samsung RC"

class PhilipsRC(RC):
    def get_description(self):
        return "Philips RC"

class Box:
    def __init__(self, tv: TV, rc: RC):
        self.tv = tv
        self.rc = rc

    def get_description(self):
        return f"Box with {self.tv.get_description()} and {self.rc.get_description()}"

class CreateBox(ABC):
    @abstractmethod
    def create_box(self):
        pass

class CreateSamsungBox(CreateBox):
    def create_box(self):
        return Box(SamsungTV(), SamsungRC())

class CreatePhilipsBox(CreateBox):
    def create_box(self):
        return Box(PhilipsTV(), PhilipsRC())