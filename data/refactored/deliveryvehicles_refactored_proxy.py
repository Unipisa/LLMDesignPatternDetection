from abc import ABC, abstractmethod

# Example of Protecion Proxy.
# Proxy for delivery vehicles,
# drivers have id between 10 and 999, managers have id between 0 and 10

class DeliverySystem(ABC):
    @abstractmethod
    def get_delivery_route(self, van_id):
        pass
    @abstractmethod
    def get_vehicle_status(self, van_id):
        # returns the driver associated
        pass
    @abstractmethod
    def get_traffic_status(self, van_id):
        pass
    @abstractmethod
    def set_driver(self, driver_id, van_id):
        pass
    @abstractmethod
    def set_delivery_route (self, van_id, route):
        pass


class DeliveryDB(DeliverySystem):
    def __init__(self):
        self.db = {
            # id: route, traffic, driver_id
            "AB123CD": ["Nomentana Street → East Ring Road → Tiburtina Street", "moderate traffic", 101],
            "EF456GH": ["Appia Street → Ring Road → Tuscolana Street", "heavy traffic", 203],
            "IJ789KL": ["Salaria Street → City Center → Riverside Road", "light traffic", 305],
            "MN012OP": ["A24 Highway → Industrial Area", "clear traffic", 40]
        }
    def get_delivery_route(self, van_id):
        return self.db[van_id][0]
    def get_traffic_status(self, van_id):
        return self.db[van_id][1]
    def get_vehicle_status(self, van_id):
        return self.db[van_id][2]
    def set_driver(self, driver_id, van_id):
        self.db[van_id][2] = driver_id
        return "Done"
    def set_delivery_route(self, van_id, route):
        self.db[van_id][0] = route
        return "Done"


class DeliveryProxy(DeliverySystem):
    def __init__(self, db, id_client):
        self.db = db
        self.id_client = id_client    # id client
    def get_delivery_route(self, van_id):
        if 0 <= self.id_client <= 999:
            return self.db.get_delivery_route(van_id)
        else:
            return "Access denied"
    def get_traffic_status(self, van_id):
        if 0 <= self.id_client <= 999:
            return self.db.get_traffic_status(van_id)
        else:
            return "Access denied"
    def get_vehicle_status(self, van_id):
        if 0 <= self.id_client <= 999:
            return self.db.get_vehicle_status(van_id)
        else:
            return "Access denied"
    def set_driver(self, driver_id, van_id):
        if 0 <= self.id_client <= 10:
            return self.db.set_driver(driver_id, van_id)
        else:
            return "Access denied"
    def set_delivery_route(self, van_id, route):
        if 0 <= self.id_client <= 10:
            return self.db.set_delivery_route(van_id, route)
        else:
            return "Access denied"
