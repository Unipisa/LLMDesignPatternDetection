from datetime import datetime
from abc import ABC, abstractmethod

class AdministrativeForm(ABC):
    def __init__(self, name, date, recipient):
        self.name = name
        self.date = date
        self.recipient = recipient
        self.module = {}
    def compile(self):
        self.write_header()
        self.write_body()
        self.add_attachment()
        self.signature()
        self.send()
        return self.module
    def write_header(self):
        self.module['header'] = [self.name, self.date, self.recipient]
    @abstractmethod
    def write_body(self):
        pass
    def add_attachment(self):
        return
    def signature(self):
        self.module['signature'] = self.name
    @abstractmethod
    def send(self):
        pass

class VacationRequest(AdministrativeForm):
    def __init__(self, name, date, recipient, start, end, motivation, manager):
        super().__init__(name, date, recipient)
        self.start = start
        self.end = end
        self.motivation = motivation
        self.manager = manager
    def write_body(self):
        start = datetime.strptime(self.start, "%Y-%m-%d")
        end = datetime.strptime(self.end, "%Y-%m-%d")
        self.module['body'] = f"Vacation lasts {(end - start).days} days for {self.motivation}"
    def send(self):
        print(f"Sending email to {self.manager}")

class ExpenseReport(AdministrativeForm):
    def __init__(self, name, date, recipient, items, portal_url, receipts):
        super().__init__(name, date, recipient)
        self.items = items
        self.portal_url = portal_url
        self.receipts = receipts
    def write_body(self):
        self.module['body'] = (f"Items: {[item for item, amount in self.items]},\n"
                               f" total amount: {sum([amount for item, amount in self.items])}")
    def add_attachment(self):
        self.module['attachment'] = self.receipts
    def send(self):
        print(f"Uploading expense report on {self.portal_url}")

class ResidenceDeclaration(AdministrativeForm):
    def __init__(self, name, date, recipient, address, tax_code, town_hall_office):
        super().__init__(name, date, recipient)
        self.address = address
        self.tax_code = tax_code
        self.town_hall_office = town_hall_office
    def write_body(self):
        self.module['body'] = f"Address: {self.address}, Tax code: {self.tax_code}"
    def send(self):
        print(f"Sending declaration to {self.town_hall_office}")

def client():
    vacation_request = VacationRequest("John", "2023-01-01", "Human Resources Office",
                                       "2023-01-01", "2023-01-15", "family vacation",
                                       "mariorossi@azienda.it")
    print(vacation_request.compile())
    expense_report = ExpenseReport("Mario", "2023-01-01", "Accounting Office",
                                   [("food", 100), ("rent", 1000)],
                                   "https://www.azienda.it/expense-report",
                                   ["receipt1.pdf", "receipt2.pdf"])
    print(expense_report.compile())
    residence_declaration = ResidenceDeclaration("Mario", "2020-1-2", "Registry Office",
                                                 "123 Main Street", "12345",
                                                 "SpringField Town Hall")
    print(residence_declaration.compile())
