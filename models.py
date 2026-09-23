class Member:
   """Represents a MakerSpace member."""

   def __init__(self, member_id, name, email):
     self.member_id = member_id
     self.name = name
     self.email = email

   def update_email(self, new_email):
       """Update the member's email address."""
       self.email = new_email 




class Equipment:
    """Represents equipment available in the MakerSpace"""

    def __init__(self, equipment_id, name, category, serial_number, available=True):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.serial_number = serial_number
        self.available = available


    def borrow(self):
        """Mark the equipment as unavailable when it is borrowed."""
        if self.available:
            self.available = False
        else:
            print("Equipment is unavailable")    


    def return_equipment(self):
        """Mark the equipment as available when it is returned."""
        if not self.available:
            self.available = True
        else:
            print("Equipment is already available.")


    def is_available(self):
        """Return whether the equipment is currently available."""
        return self.available




class Loan:
    """Represents an equipment loan."""

    def __init__(self, loan_id, member_id, equipment_id, loan_date, return_date=None):
        self.loan_id = loan_id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.loan_date = loan_date
        self.return_date = return_date


    def is_active(self):
        """Return True if the loan has not been closed"""
        return self.return_date is None

    def close_loan(self, return_date):
        """Close the loan by recording the return date"""
        self.return_date = return_date  


