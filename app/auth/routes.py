from flask import render_template, request, redirect, url_for, flash, session
from .__init__ import bp
from ..services import AuthService


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        success, message = AuthService.register_user(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password']
        )
        flash(message)
        if success:
            return redirect(url_for('auth.login'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, log_id = AuthService.login_user(
            username=request.form['username'],
            password=request.form['password'],
            ip_address=request.remote_addr
        )
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['login_log_id'] = log_id
            flash('登录成功')
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    if 'login_log_id' in session:
        AuthService.logout_user(session['login_log_id'])

    session.clear()
    flash('已登出')
    return redirect(url_for('auth.login'))