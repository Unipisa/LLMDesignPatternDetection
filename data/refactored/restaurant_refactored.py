from abc import ABC, abstractmethod

# reciver
class Kitchen:
    def grill(self, order):
        return f"Grilled {order}"
    def fry(self, order):
        return f"Fried {order}"
    def pour(self, beverage):
        return f"Served {beverage}"

# abstract command
class OrderCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

# concrete commands
class GrillCommand(OrderCommand):
    def __init__(self, order, kitchen: Kitchen):
        self.order = order
        self.kitchen = kitchen
    def execute(self):
        return self.kitchen.grill(self.order)

class FryCommand(OrderCommand):
    def __init__(self, order, kitchen: Kitchen):
        self.order = order
        self.kitchen = kitchen
    def execute(self):
        return self.kitchen.fry(self.order)

class PourCommand(OrderCommand):
    def __init__(self, beverage, kitchen: Kitchen):
        self.beverage = beverage
        self.kitchen = kitchen
    def execute(self):
        return self.kitchen.pour(self.beverage)

class TableMacroOrder(OrderCommand):
    def __init__(self, table_number, *commands):
        self.commands = commands
        self.table_number = table_number
    def execute(self):
        ready_items = [command.execute() for command in self.commands]
        return f"Table {self.table_number} ready with: {', '.join(ready_items)}"


# invoker
class Waiter:
    def __init__(self, command: OrderCommand):
        self.command = command
    def serve(self):
        return self.command.execute()

# client
def ordering_tablet():
    kitchen = Kitchen()

    # serving a full dinner
    order = TableMacroOrder(1,
                            GrillCommand("Steak", kitchen),
                            FryCommand("Chicken", kitchen),
                            PourCommand("Cola", kitchen)
                            )
    waiter = Waiter(order)
    print(waiter.serve())

    print("-------------------------------")
    # serving a single dish
    order = TableMacroOrder(2, GrillCommand("Vegetables", kitchen))
    waiter = Waiter(order)
    print(waiter.serve())

if __name__ == "__main__":
    ordering_tablet()