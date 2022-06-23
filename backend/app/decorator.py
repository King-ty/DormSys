from functools import wraps
from flask import jsonify, request, current_app
from .models import User, TempRight
from .response import RET
import jwt
from sqlalchemy import and_


# def admin_required(f):
#     @wraps(f)
#     def decorated_function(current_user, *args, **kwargs):
#         u = current_user
#         if u.author != 3:
#             return f(current_user, *args, **kwargs)
#         else:
#             return jsonify(code=RET.AUTHERR, msg="用户没有此权限")

#     return decorated_function


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()
        # print("###", auth_headers)

        invalid_msg = {
            "msg": "无效的token",  # "Invalid token. Registeration and / or authentication required",
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
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )  # 需要添加SECRET_KEY
            # print("data=", data)
            user = User.query.filter_by(id=data["sub"]).first()  # 不一定使用email
            if not user:
                raise RuntimeError("User not found")
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
        return f(user, *args, **kwargs)

    return _verify


def admin_required(f):
    @wraps(f)
    def wrapped_function(current_user, *args, **kwargs):
        u = current_user
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json()
            aid = data.get("aid")
            if aid is None:
                aid = data.get("activity_id")
            if aid is None:
                tempright = None
            else:
                try:
                    tempright = TempRight.query.filter(
                        and_(
                            TempRight.user_id == current_user.id,
                            TempRight.activity_id == aid,
                        )
                    ).first()
                except Exception as e:
                    current_app.logger.debug(e)
                    return jsonify(code=RET.DBERR, msg="查询权限失败")
        else:
            tempright = None
        if u.author != 3 or tempright is not None:
            return f(current_user, *args, **kwargs)
        else:
            return jsonify(code=RET.AUTHERR, msg="用户没有此权限")

    return wrapped_function
