from flask import render_template, redirect, url_for, session
from app.main import bp
from app.models import User, LoginLog  # Temp import, will be removed


@bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)


@bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    login_logs = LoginLog.query.filter_by(user_id=user.id).order_by(LoginLog.login_time.desc()).limit(10).all()

    return render_template('profile.html', user=user, login_logs=login_logs)