# Import classes from deepseek_python_20250727_5c42a4.py
from dataclasses import dataclass
from typing import List

@dataclass
class DisputedItem:
    bureau: str
    creditor_name: str
    account_number: str
    violation_type: str
    violation_details: str
    reported_date: str = ""
    ftc_report_number: str = ""
    correct_date: str = ""
    proof_description: str = ""

@dataclass
class PersonalInfo:
    full_name: str
    address: str
    city_state_zip: str
    ssn_last4: str
    dob: str
    phone: str
    email: str

class CreditDisputeGenerator:
    # ...existing code from deepseek_python_20250727_5c42a4.py...
    pass
