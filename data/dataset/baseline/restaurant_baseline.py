class Kitchen:
    def grill(self, order):
        return f"Grilled {order}"
    def fry(self, order):
        return f"Fried {order}"
    def pour(self, beverage):
        return f"Served {beverage}"

class Waiter:
    def __init__(self, kitchen: Kitchen):
        self.kitchen = kitchen
    def serve_grilled(self, order):
        return self.kitchen.grill(order)
    def serve_fried(self, order):
        return self.kitchen.fry(order)
    def serve_drink(self, beverage):
        return self.kitchen.pour(beverage)
    def serve_table(self, table_number, *orders):
        ready_items = []
        for action, order in orders:
            if action == "grill":
                ready_items.append(self.serve_grilled(order))
            if action == "fry":
                ready_items.append(self.serve_fried(order))
            if action == "drink":
                ready_items.append(self.serve_drink(order))
        return f"Table {table_number} ready with: {', '.join(ready_items)}"
