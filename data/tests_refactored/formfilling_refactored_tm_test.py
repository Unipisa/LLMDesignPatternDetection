import unittest
from data.refactored.formfilling_refactored_tm import VacationRequest,ExpenseReport, ResidenceDeclaration


class TestVacationRequest(unittest.TestCase):
    def setUp(self):
        self.vacation_request = VacationRequest("John", "2023-01-01", "Human Resources Office",
                                       "2023-01-01", "2023-01-15", "family vacation",
                                       "mariorossi@azienda.it")
    def test_compile(self):
        self.assertEqual(self.vacation_request.compile(), {
            'header': ['John', '2023-01-01','Human Resources Office'],
            'body': 'Vacation lasts 14 days for family vacation', 'signature': 'John'})
    def test_send(self):
        self.assertEqual(self.vacation_request.send(), "Sending email to mariorossi@azienda.it")

class TestExpenseReport(unittest.TestCase):
    def setUp(self):
        self.expense_report = ExpenseReport("Mario", "2023-01-01", "Accounting Office",
                                       [("food", 100), ("rent", 1000)],
                                       "https://www.azienda.it/expense-report",
                                       ["receipt1.pdf", "receipt2.pdf"])
    def test_compile(self):
        self.assertEqual(self.expense_report.compile(), {
            'header': ['Mario', '2023-01-01', 'Accounting Office'],
            'body': "Items: ['food', 'rent'],\n total amount: 1100",
            'attachment': ['receipt1.pdf', 'receipt2.pdf'], 'signature': 'Mario'
        })
    def test_send(self):
        self.assertEqual(self.expense_report.send(), "Uploading expense report on https://www.azienda.it/"
                                                     "expense-report")

class TestResidenceDeclaration(unittest.TestCase):
    def setUp(self):
        self.residence_declaration = ResidenceDeclaration("Mario", "2020-1-2", "Registry Office",
                                                 "123 Main Street", "12345",
                                                 "SpringField Town Hall")
    def test_compile(self):
        self.assertEqual(self.residence_declaration.compile(), {
            'header': ['Mario', '2020-1-2', 'Registry Office'],
            'body': 'Address: 123 Main Street, Tax code: 12345',
            'signature': 'Mario'})
    def test_send(self):
        self.assertEqual(self.residence_declaration.send(), "Sending declaration to SpringField Town Hall")