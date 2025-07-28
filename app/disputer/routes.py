from flask import Blueprint, render_template, request, flash
from .generator import CreditDisputeGenerator, PersonalInfo, DisputedItem
from flask_login import login_required, current_user

disputer_bp = Blueprint('disputer', __name__, template_folder='templates')

@disputer_bp.route('/dispute', methods=['GET', 'POST'])
@login_required
def dispute():
    if request.method == 'POST':
        # Collect form data and generate dispute letters
        personal_info = PersonalInfo(
            full_name=current_user.name,
            address=request.form['address'],
            city_state_zip=request.form['city_state_zip'],
            ssn_last4=request.form['ssn_last4'],
            dob=request.form['dob'],
            phone=request.form['phone'],
            email=current_user.email
        )
        # Example: items = [DisputedItem(...), ...]
        generator = CreditDisputeGenerator(personal_info)
        general = generator.generate_general_dispute([])
        late = generator.generate_late_payment_dispute([])
        inquiry = generator.generate_hard_inquiry_dispute([])
        generator.send_dispute_letters(general, late, inquiry)
        flash('Dispute letters generated and sent!')
    return render_template('dispute.html')
