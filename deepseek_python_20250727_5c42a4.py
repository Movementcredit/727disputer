import datetime
from dataclasses import dataclass
from typing import List, Dict
from flask import current_app
from app import mail
from flask_mail import Message

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
    def __init__(self, personal_info: PersonalInfo):
        self.personal_info = personal_info
        self.date = datetime.datetime.now().strftime("%m/%d/%Y")
        self.case_laws = {
            "outdated": "Guimond v. Trans Union Credit Information Co., 45 F.3d 1329 (9th Cir. 1995)",
            "reaging": "Bryant v. TRW, Inc., 689 F.2d 72 (6th Cir. 1982)",
            "identity_theft": "Dennis v. BEH-1, LLC, 520 F.3d 1066 (9th Cir. 2008)",
            "unverified": "Cushman v. Trans Union Corp., 115 F.3d 220 (3d Cir. 1997)",
            "unauthorized_inquiry": "Phillips v. Grendahl, 312 F.3d 357 (8th Cir. 2002)",
            "duplicate": "Koropoulos v. Credit Bureau, Inc., 734 F.2d 37 (D.C. Cir. 1984)",
            "incomplete_investigation": "Gorman v. Wolpoff & Abramson, LLP, 584 F.3d 1147 (9th Cir. 2009)"
        }
        self.fcra_statutes = {
            "outdated": "15 U.S.C. § 1681c(a)(5)",
            "reaging": "15 U.S.C. § 1681s-2(a)(5)",
            "identity_theft": "15 U.S.C. § 1681c-2",
            "unverified": "15 U.S.C. § 1681s-2(a)(1)(A)",
            "unauthorized_inquiry": "15 U.S.C. § 1681b(c)",
            "duplicate": "15 U.S.C. § 1681e(b)",
            "incomplete_investigation": "15 U.S.C. § 1681i(a)"
        }

    def generate_header(self) -> str:
        return f"""{self.personal_info.full_name}
{self.personal_info.address}
{self.personal_info.city_state_zip}
{self.date}

VIA CERTIFIED MAIL (RETURN RECEIPT REQUESTED)

Experian | Equifax | TransUnion
[Respective Bureau Addresses]
"""

    def generate_general_dispute(self, items: List[DisputedItem]) -> str:
        letter = self.generate_header()
        letter += f"""RE: FORMAL DISPUTE & DEMAND FOR DELETION OF INACCURATE INFORMATION
Credit Report File #: [Your File #]
SSN: XXX-XX-{self.personal_info.ssn_last4} | DOB: {self.personal_info.dob}

NOTICE OF WILLFUL FCRA VIOLATIONS

To Whom It May Concern:

This letter serves as formal notice that your agency is currently violating the FCRA by reporting inaccurate, fraudulent, and obsolete information on my credit file. Below is a detailed list of violations across all three bureaus. FAILURE TO CORRECT THESE ERRORS WITHIN 10 DAYS will result in immediate legal action.

🚨 DISPUTED ITEMS & LEGAL DEMANDS
"""

        for item in items:
            violation_text = ""
            demand_text = ""
            
            if item.violation_type == "outdated":
                violation_text = f"- Violation: 7+ years old ({self.fcra_statutes['outdated']})"
                demand_text = "- Demand: DELETE IMMEDIATELY."
            elif item.violation_type == "reaging":
                violation_text = f"- Violation: Fraudulent date change ({self.fcra_statutes['reaging']})"
                demand_text = f"- Demand: CORRECT DATE TO {item.correct_date} OR DELETE."
            elif item.violation_type == "identity_theft":
                violation_text = f"- Violation: FTC Report # {item.ftc_report_number} ({self.fcra_statutes['identity_theft']})"
                demand_text = "- Demand: REMOVE NOW OR FACE $100,000 IN PUNITIVE DAMAGES."
            elif item.violation_type == "unverified":
                violation_text = f"- Violation: Unverified account ({self.fcra_statutes['unverified']})"
                demand_text = "- Demand: DELETE IMMEDIATELY OR FACE $10,000 IN STATUTORY DAMAGES."
            
            letter += f"""\n{len(items)}. {item.creditor_name} (#{item.account_number})
  {violation_text}
  - Case Law: {self.case_laws[item.violation_type]} – {item.violation_details}
  {demand_text}
"""

        letter += """
⚠️ FINAL WARNING: 10-DAY DEADLINE
You have 10 calendar days from receipt of this letter to:
1. Delete ALL disputed items.
2. Send written confirmation of corrections.
3. Cease ALL unlawful reporting.

FAILURE TO COMPLY WILL RESULT IN:
✔ Lawsuit for $1,000 per violation (15 U.S.C. § 1681n).
✔ Punitive damages (up to $100,000+).
✔ CFPB/FTC/State AG complaints.

Attached: Credit reports, ID proof, FTC report (if applicable).

Sincerely,
"""
        letter += f"{self.personal_info.full_name}\n{self.personal_info.phone} | {self.personal_info.email}"
        return letter

    def generate_late_payment_dispute(self, late_payments: List[DisputedItem]) -> str:
        letter = self.generate_header()
        letter += f"""RE: FORMAL DISPUTE OF INACCURATE LATE PAYMENTS
File #: [Your Credit Report #]
SSN: XXX-XX-{self.personal_info.ssn_last4} | DOB: {self.personal_info.dob}

NOTICE OF FCRA VIOLATIONS & DEMAND FOR DELETION

To Whom It May Concern:

This letter serves as formal notice that your agency is willfully violating the FCRA by reporting inaccurate late payments on my credit file. Below is a list of fraudulent lates and the legal basis for their immediate deletion.

🚨 DISPUTED LATE PAYMENTS
"""

        for i, payment in enumerate(late_payments, 1):
            violation_text = ""
            if payment.violation_type == "outdated":
                violation_text = f"- Error: Older than 7 years (violates {self.fcra_statutes['outdated']})"
            elif payment.violation_type == "incorrect":
                violation_text = f"- Error: Never late (see attached {payment.proof_description})"
            elif payment.violation_type == "creditor_error":
                violation_text = f"- Error: Creditor admitted error (see attached {payment.proof_description})"
            
            letter += f"""{i}. {payment.creditor_name} (Account #: {payment.account_number})
  Reported Late: {payment.reported_date}
  {violation_text}
  - Case Law: {self.case_laws['unverified']} – Unverified lates must be deleted.
  - Threat: Delete or face $1,000 statutory damages.
"""

        letter += """
⚠️ FINAL WARNING: 10-DAY DEADLINE
You have 10 calendar days to:
1. Delete ALL disputed late payments.
2. Send written confirmation of corrections.

FAILURE TO ACT WILL RESULT IN:
✔ Lawsuit for $1,000 per violation (15 U.S.C. § 1681n).
✔ Punitive damages (state consumer laws).
✔ CFPB/FTC/State AG complaints.

Attached: Payment records, creditor letters, ID proof.

Sincerely,
"""
        letter += f"{self.personal_info.full_name}\n{self.personal_info.phone} | {self.personal_info.email}"
        return letter

    def generate_hard_inquiry_dispute(self, inquiries: List[DisputedItem]) -> str:
        letter = self.generate_header()
        letter += f"""RE: FORMAL DISPUTE OF UNAUTHORIZED HARD INQUIRIES
FCRA § 1681b(c) VIOLATIONS
FILE #: [Your Report #]

NOTICE OF WILLFUL NON-COMPLIANCE

To Whom It May Concern:

The following hard inquiries on my credit report lack permissible purpose and violate FCRA § 1681b(c). Per Phillips v. Grendahl, each violation carries $1,000 in statutory damages.

🚨 UNAUTHORIZED INQUIRIES DEMANDING REMOVAL
"""

        for i, inquiry in enumerate(inquiries, 1):
            violation_text = ""
            if inquiry.violation_type == "unauthorized":
                violation_text = "- Violation: No application submitted"
            elif inquiry.violation_type == "freeze_violation":
                violation_text = "- Violation: Pull occurred during active security freeze"
            elif inquiry.violation_type == "expired":
                violation_text = "- Violation: Expired permissible purpose (>12 months old)"
            
            letter += f"""{i}. {inquiry.creditor_name}
  Date: {inquiry.reported_date}
  {violation_text}
  - Legal Threat: Delete or face $4,000 lawsuit (4 violations)
"""

        letter += """
⚠️ 10-DAY DEADLINE
You have 10 calendar days to:
1. Delete ALL unauthorized inquiries
2. Provide sworn affidavit confirming removal

FAILURE TO COMPLY WILL RESULT IN:
✔ Federal lawsuit ($1,000 per violation)
✔ CFPB complaint (Case # will be cited in court)
✔ State AG action ([Your State] Consumer Protection Act)

Attached:
- Credit report (highlighted inquiries)
- Security freeze confirmation (if applicable)
- Government-issued ID

Sincerely,
"""
        letter += f"{self.personal_info.full_name}\n{self.personal_info.phone} | {self.personal_info.email}"
        return letter

    def send_dispute_letters(self, general_dispute, late_payment_dispute, hard_inquiry_dispute):
        msg = Message(
            subject="Your Movement Credit A.I. Dispute Letters",
            sender=current_app.config['MOVEMENT_EMAIL'],
            recipients=[self.personal_info.email],
            body="Please find attached your dispute letters."
        )
        
        msg.attach("general_dispute.txt", "text/plain", general_dispute)
        msg.attach("late_payment_dispute.txt", "text/plain", late_payment_dispute)
        msg.attach("hard_inquiry_dispute.txt", "text/plain", hard_inquiry_dispute)
        
        mail.send(msg)