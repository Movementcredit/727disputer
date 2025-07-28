from flask import Blueprint, render_template

funnel_bp = Blueprint('funnel', __name__, template_folder='templates')

@funnel_bp.route('/')
def index():
    return render_template('index.html')

@funnel_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

from flask import request, redirect, url_for, flash
from app.auth.models import User
from app import db
from werkzeug.security import generate_password_hash

@funnel_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('signup.html')
        user = User(name=name, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')
