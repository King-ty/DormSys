from functools import wraps
from flask import request, current_app
from .models import Student, Admin
from .response import RET, jsonRes
import jwt


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization")
        if not auth_headers:
            return jsonRes(code=RET.LOGINERR, msg="无效的token"), 401

        try:
            token = auth_headers
            data = jwt.decode(token,
                              current_app.config["SECRET_KEY"],
                              algorithms="HS256")  # 需要添加SECRET_KEY
            no = data.get('sub')
            try:
                user = getUser(no)
            except Exception as e:
                current_app.logger.debug(e)
                return jsonRes(code=RET.DBERR, msg="数据库查询错误")

            if not user:
                raise RuntimeError("User not found")
        except jwt.ExpiredSignatureError:
            return jsonRes(code=RET.LOGINERR, msg="过期的token"), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonRes(code=RET.LOGINERR, msg="无效的token"), 401
        return f(user, *args, **kwargs)

    return _verify


def admin_required(f):
    @wraps(f)
    def wrapped_function(current_user, *args, **kwargs):
        u = current_user
        if u.role == 0:
            return f(current_user, *args, **kwargs)
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户没有此权限")

    return wrapped_function


def sub_admin_required(f):
    @wraps(f)
    def wrapped_function(current_user, *args, **kwargs):
        u = current_user
        if u.role == 0 or u.role == 1:
            return f(current_user, *args, **kwargs)
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户没有此权限")

    return wrapped_function


def getUser(no):
    if (len(no) == 7):
        u = Student.query.filter_by(no=no).first()
    else:
        u = Admin.query.filter_by(no=no).first()
    return u
