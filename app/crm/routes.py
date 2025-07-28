from flask import Blueprint, render_template
from flask_login import login_required

crm_bp = Blueprint('crm', __name__, template_folder='templates')

@crm_bp.route('/clients')
@login_required
def clients():
    # List clients for agency
    return render_template('clients.html')
