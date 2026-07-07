from abc import ABC, abstractmethod

# There are 2 types of products: TV and remote control (RC).
# There are 2 different brands: Samsung or Philips.
# Implementation with abstract factory: a client can choose which factory is more suitable to get
# a TV and its RC, so they can be packaged together in a box.
# A Samsung TV uses a Samsung RC while a Philips TV uses a Philips RC.

# abstract products
class TV(ABC):
    @abstractmethod
    def get_description(self):
        pass

class RC(ABC):
    @abstractmethod
    def get_description(self):
        pass



# concrete products
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


# abstract factory
class CreateBox(ABC):
    @abstractmethod
    def create_tv(self):
        pass
    @abstractmethod
    def create_rc(self):
        pass

# concrete factories
class SamsungBox(CreateBox):
    def create_tv(self):
        return SamsungTV()
    def create_rc(self):
        return SamsungRC()

class PhilipsBox(CreateBox):
    def create_tv(self):
        return PhilipsTV()
    def create_rc(self):
        return PhilipsRC()
