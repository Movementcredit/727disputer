from flask import Blueprint, render_template

funnel_bp = Blueprint('funnel', __name__, template_folder='templates')

@funnel_bp.route('/')
def index():
    return render_template('index.html')

@funnel_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@funnel_bp.route('/signup')
def signup():
    return render_template('signup.html')
