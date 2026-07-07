from datetime import datetime
from enum import Enum

class FormType(Enum):
    VACATION_REQUEST = 1
    EXPENSES_REPORT = 2
    RESIDENCE_DECLARATION = 3


class Form:
    def __init__(self, form_type: FormType, name , date, recipient, start = None, end = None, motivation = None,
                 manager = None, items = None, portal_url = None, receipts= None,  address = None, tax_code = None,
                 town_hall_office = None):
        self.form_type = form_type
        self.name = name
        self.date = date
        self.recipient = recipient
        self.start = start
        self.end = end
        self.motivation = motivation
        self.manager = manager
        self.items = items
        self.portal_url = portal_url
        self.receipts = receipts
        self.address = address
        self.tax_code = tax_code
        self.town_hall_office = town_hall_office
    def compile(self):
        if self.form_type == FormType.VACATION_REQUEST:
            return {'header': [self.name, self.date, self.recipient],
                    'body': f'Vacation lasts {(datetime.strptime(self.end, "%Y-%m-%d") - 
                                               datetime.strptime(self.start, "%Y-%m-%d")).days} days for '
                            f'{self.motivation}',
                    'signature': self.name}
        elif self.form_type == FormType.EXPENSES_REPORT:
            return {
                'header': [self.name, self.date, self.recipient],
                'body': (f"Items: {[item for item, amount in self.items]},\n"
                               f" total amount: {sum([amount for item, amount in self.items])}"),
                'attachment': self.receipts,
                'signature': self.name
            }
        elif self.form_type == FormType.RESIDENCE_DECLARATION:
            return {
                'header': [self.name, self.date, self.recipient],
                'body': f"Address: {self.address}, Tax code: {self.tax_code}",
                'signature': self.name
            }
        return None
    def send(self):
        if self.form_type == FormType.VACATION_REQUEST:
            return f"Sending email to {self.manager}"
        elif self.form_type == FormType.EXPENSES_REPORT:
            return f"Uploading expense report on {self.portal_url}"
        elif self.form_type == FormType.RESIDENCE_DECLARATION:
            return f"Sending declaration to {self.town_hall_office}"
        return None