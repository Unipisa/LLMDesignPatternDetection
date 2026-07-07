from abc import ABC, abstractmethod

# Start = free
#
# Free -> assign = occupied
# Free -> report_issue = free maintanance
#
# occupied -> end_market = free
# Assigned -> report_issue = occupied maintanance
#
# occupied maintanance -> end_maintenance = occupied
# occupied maintenance -> end_market = free maintanance
#
# free maintanance -> end_maintenance = free
#
# If wrong throw error
#
# Simplified from
#
# A stall can be in one of the following states:
# - Free: From the end of the market until the next assignment.
# - Assigned
# - Occupied: During the market.
# - Under Maintenance
#
# Maintenance is triggered by a problem report made by merchants or organizers.
#
# Each report is classified with a level of urgency, determined by the state of the house:
# - High: If occupied.
# - Medium: If assigned.
# - Low: If free.
#
# Once the report is received, the system assigns a technician based on the type of intervention required and the urgency level.
#
# After the work is completed, the house returns to its previous state, unless events such as:
# - Assignment
# - The start of the market
# - The end of the market
# requires an automatic change in its state.
#
# If the technician reports the problem as unsolvable, the house remains in the maintenance state, and the system notifies the organizers to decide on any extraordinary interventions.
#
#
# should rename to avoid hints
# Refactoring with state pattern Stall Class
#
# Extension:
#
# broken -> report_issue = free maintanance


# Context Class
class Stall:
    def __init__(self):
        self.state = FreeState(self)
    
    def set_state(self, state):
        self.state = state
    
    def assign(self):
        self.state.assign()
    
    def end_market(self):
        self.state.end_market()
    
    def report_issue(self):
        self.state.report_issue()
    
    def finish_maintenance(self):
        self.state.finish_maintenance()

# State Interface
class StallState(ABC):
    def __init__(self, stall):
        self.stall = stall
    
    @abstractmethod
    def assign(self):
        pass
    
    @abstractmethod
    def end_market(self):
        pass
    
    @abstractmethod
    def report_issue(self):
        pass
    
    @abstractmethod
    def finish_maintenance(self):
        pass

# Concrete States
class FreeState(StallState):
    def assign(self):
        print("Stall assigned.")
        self.stall.set_state(OccupiedState(self.stall))
    
    def end_market(self):
        raise Exception("Market is not running.")
    
    def report_issue(self):
        print("Issue reported. Moving to maintenance.")
        self.stall.set_state(FreeMaintenanceState(self.stall))
    
    def finish_maintenance(self):
        raise Exception("Already in a free state.")

class OccupiedState(StallState):
    def assign(self):
        raise Exception("Cannot assign while occupied.")
    
    def end_market(self):
        print("Market ended. Moving to free state.")
        self.stall.set_state(FreeState(self.stall))
    
    def report_issue(self):
        print("Issue reported. Moving to maintenance.")
        self.stall.set_state(OccupiedMaintenanceState(self.stall))
    
    def finish_maintenance(self):
        raise Exception("Cannot finish maintenance in occupied state.")

class OccupiedMaintenanceState(StallState):
    def assign(self):
        raise Exception("Cannot assign. Stall is under maintenance.")
    
    def end_market(self):
        print("Market ended, changing maintenance.")
        self.stall.set_state(FreeMaintenanceState(self.stall))
    
    def report_issue(self):
        raise Exception("Already under maintenance.")
    
    def finish_maintenance(self):
        print("Maintenance finished. Moving to free state.")
        self.stall.set_state(OccupiedState(self.stall))

class FreeMaintenanceState(StallState):
    def assign(self):
        raise Exception("Cannot assign. Stall is under maintenance.")
    
    def end_market(self):
        raise Exception("Market is not running.")
    
    def report_issue(self):
        raise Exception("Already under maintenance.")
    
    def finish_maintenance(self):
        print("Maintenance finished. Moving to free state.")
        self.stall.set_state(FreeState(self.stall))