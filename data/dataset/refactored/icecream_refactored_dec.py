from abc import ABC, abstractmethod

# An icecream is made up of a cone (1.00) or a cup (1.50) and 3 scoop flavours can be added
# chocolate (0.50), (strawberry 0.75), vanilla (0.60).
# More than 1 scoop can be added, the cost is the sum of the ingredients
# Also, a description of the ice cream should be given.
#
# refactoring with decorator

class Icecream:
    def __init__(self):
        self.description = "Icecream"

    def getDescription(self):
        return self.description
    
    @abstractmethod    
    def cost(self):
        pass

#concrete component
class Cone(Icecream):
    def __init__(self):
        self.description = "Icecream Cone"

    def getDescription(self):
        return self.description
    
    def cost(self):
        return 1.00

class Cup(Icecream):
    def __init__(self):
        self.description = "Icecream Cup"

    def getDescription(self):
        return self.description

    def cost(self):
        return 1.50

#Decorator
class IcecreamDecorator(Icecream):
    def __init__(self, icecream):
        self.icecream = icecream
    
    @abstractmethod 
    def getDescription(self):         
        pass

#Concrete Decorator
class Chocolate(IcecreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.description = "Chocolate"
    
    def getDescription(self):
        return self.icecream.getDescription() + ", " + self.description
    
    def cost(self):
        return self.icecream.cost() + 0.50

class Strawberry(IcecreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.description = "Strawberry"
    
    def getDescription(self):
        return self.icecream.getDescription() + ", " + self.description
    
    def cost(self):
        return self.icecream.cost() + 0.75
class Vanilla(IcecreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.description = "Vanilla"
    
    def getDescription(self):
        return self.icecream.getDescription() + ", " + self.description
    
    def cost(self):
        return self.icecream.cost() + 0.60