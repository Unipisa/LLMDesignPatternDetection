from data.dataset.baseline.formfilling_baseline import Form, FormType
from enum import Enum
from datetime import datetime
import unittest

class TestForm(unittest.TestCase):
    def setUp(self):
        self.vacation_request = Form(FormType.VACATION_REQUEST, "John", "2023-01-01", "Human Resources Office",
                    start="2023-01-01", end="2023-01-15", motivation="family vacation",
                    manager="mariorossi@azienda.it")
        self.expense_report = Form(FormType.EXPENSES_REPORT, "Mario", "2023-01-01", "Accounting Office",
                                   items = [("food", 100), ("rent", 1000)],
                                   portal_url= "https://www.azienda.it/expense-report",
                                   receipts = ["receipt1.pdf", "receipt2.pdf"]
                                   )
        self.residence_declaration = Form(FormType.RESIDENCE_DECLARATION, "Mario", "2020-1-2",
                                          "Registry Office", address="123 Main Street", tax_code="12345",
                                                 town_hall_office="SpringField Town Hall")
    def test_vacation_request(self):
        self.assertEqual(self.vacation_request.compile(), {
            'header': ['John', '2023-01-01','Human Resources Office'],
            'body': 'Vacation lasts 14 days for family vacation',
            'signature': 'John'})
    def test_send_vacation_request(self):
        self.assertEqual(self.vacation_request.send(), "Sending email to mariorossi@azienda.it")
    def test_expense_report(self):
        self.assertEqual(self.expense_report.compile(), {
            'header': ['Mario', '2023-01-01', 'Accounting Office'],
            'body': "Items: ['food', 'rent'],\n total amount: 1100",
            'attachment': ['receipt1.pdf', 'receipt2.pdf'], 'signature': 'Mario'
        })
    def test_send_expense_report(self):
        self.assertEqual(self.expense_report.send(), "Uploading expense report on https://www.azienda.it/"
                                                     "expense-report")
    def test_residence_declaration(self):
        self.assertEqual(self.residence_declaration.compile(), {
            'header': ['Mario', '2020-1-2', 'Registry Office'],
            'body': 'Address: 123 Main Street, Tax code: 12345',
            'signature': 'Mario'
        })
    def test_send_residence_declaration(self):
        self.assertEqual(self.residence_declaration.send(), "Sending declaration to SpringField Town Hall")



