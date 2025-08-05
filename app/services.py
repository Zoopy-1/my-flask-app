from app import db
from .models import User, LoginLog
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class AuthService:
    @staticmethod
    def register_user(username, email, password):
        """Handles user registration logic."""
        if User.query.filter_by(username=username).first():
            return False, "用户名已存在"
        if User.query.filter_by(email=email).first():
            return False, "邮箱已存在"

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return True, "注册成功，请登录"

    @staticmethod
    def login_user(username, password, ip_address):
        """Handles user login logic."""
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return None, None

        user.last_login = datetime.utcnow()
        log = LoginLog(user_id=user.id, ip_address=ip_address)
        db.session.add(log)
        db.session.commit()

        return user, log.id

    @staticmethod
    def logout_user(log_id):
        """Handles user logout logic."""
        log = LoginLog.query.get(log_id)
        if log:
            log.logout_time = datetime.utcnow()
            db.session.commit()


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_profile_data(user_id):
        user = User.query.get(user_id)
        logs = LoginLog.query.filter_by(user_id=user_id).order_by(LoginLog.login_time.desc()).limit(10).all()
        return user, logs