
from models import User
from forms import SignupForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, flash, redirect, url_for, request

def auth_blueprint(login_manager,db_session):
    auth_bp = Blueprint('auth', __name__)

    #User loader function
    @login_manager.user_loader
    def load_user(user):
        return db_session.query(User).get(int(user))
    
    # Set the unauthorized handler
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash('You must be logged in to view that page.', 'warning')
        return redirect(url_for('auth.login'))

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user = db_session.query(User).filter_by(email=form.email.data).first()
                if user and check_password_hash(user.password_hash, form.password.data):
                    if login_user(user):
                        flash('Login successful!', 'success')
                        return redirect(url_for('dashboard'))
                    else:
                        flash('Failed to login. User might not be active or there was an issue with the login process.', 'error')
                else:
                    flash('Invalid email or password', 'error')
            else:
                flash('Form validation failed', 'error')
        else:
            if current_user.is_authenticated:
                return redirect(url_for('dashboard'))
        return render_template('login.html', form=form)


    @auth_bp.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        if form.validate_on_submit():
            email = form.email.data
            organization = form.organization.data
            existing_user = db_session.query(User).filter_by(email=email).first()
            if existing_user:
                flash('Email already exists. Please choose a different one.', 'danger')
                return redirect(url_for('auth.signup'))

            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(email=email, organization=organization, password_hash=hashed_password, is_active=True)
            db_session.add(new_user)
            try:
                db_session.commit()
                flash('Signup successful!', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db_session.rollback()
                flash('Signup failed. Please try again later.', 'danger')
                return redirect(url_for('auth.signup'))
        return render_template('signup.html', form=form)

    @auth_bp.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    return auth_bp
