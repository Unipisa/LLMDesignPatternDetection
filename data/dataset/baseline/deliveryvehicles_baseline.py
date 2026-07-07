class DeliverySystem:
    def __init__(self, id_client):
        self.db = {
            # id: route, traffic, driver_id
            "AB123CD": ["Nomentana Street → East Ring Road → Tiburtina Street", "moderate traffic", 101],
            "EF456GH": ["Appia Street → Ring Road → Tuscolana Street", "heavy traffic", 203],
            "IJ789KL": ["Salaria Street → City Center → Riverside Road", "light traffic", 305],
            "MN012OP": ["A24 Highway → Industrial Area", "clear traffic", 40]
        }
        self.id_client = id_client    # id client
    def get_delivery_route(self, van_id):
        if 0 <= self.id_client <= 999:
            return self.db[van_id][0]
        else:
            return "Access denied"
    def get_traffic_status(self, van_id):
        if 0 <= self.id_client <= 999:
            return self.db[van_id][1]
        else:
            return "Access denied"
    def get_vehicle_status(self, van_id):
        if 0 <= self.id_client <= 999:
            return self.db[van_id][2]
        else:
            return "Access denied"
    def set_driver(self, driver_id, van_id):
        if 0 <= self.id_client <= 10:
            self.db[van_id][2] = driver_id
            return "Done"
        else:
            return "Access denied"
    def set_delivery_route(self, van_id, route):
        if 0 <= self.id_client <= 10:
            self.db[van_id][0] = route
            return "Done"
        else:
            return "Access denied"
