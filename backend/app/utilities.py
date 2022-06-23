from functools import wraps
from flask import jsonify, request, current_app
from .models import Student, Admin
from .response import RET
import jwt


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()
        # print("###", auth_headers)

        invalid_msg = {
            "msg":
            "无效的token",  # "Invalid token. Registeration and / or authentication required",
            "code": RET.LOGINERR,
        }
        expired_msg = {
            "msg": "过期的token",  # "Expired token. Reauthentication required.",
            "code": RET.LOGINERR,
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token,
                              current_app.config["SECRET_KEY"],
                              algorithms="HS256")  # 需要添加SECRET_KEY
            # print("data=", data)
            # TODO:不同身份
            user = Student.query.filter_by(
                id=data["sub"]).first()  # 不一定使用email
            if not user:
                raise RuntimeError("User not found")
        except jwt.ExpiredSignatureError:
            return jsonify(
                expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
        return f(user, *args, **kwargs)

    return _verify


def getUser(no):
    if (len(no) == 7):
        u = Student.query.filter_by(no=no).first()
    else:
        u = Admin.query.filter_by(no=no).first()
    return u
