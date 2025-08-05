from flask import render_template, redirect, url_for, session
from app.main import bp
from app.services import UserService


@bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = UserService.get_user_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)


@bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user, logs = UserService.get_user_profile_data(session['user_id'])
    return render_template('profile.html', user=user, login_logs=logs)