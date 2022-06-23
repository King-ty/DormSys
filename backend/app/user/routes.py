from flask import request, current_app, make_response
from . import user
from .. import db, redis_client
from ..models import Student, Admin
from ..response import RET, jsonRes
from datetime import datetime, timedelta
from ..utilities import token_required, getUser
from ..email import send_email
import jwt
import random


@user.route("/login", methods=["POST"])
def login():
    data = request.json
    print(data)
    no = data.get("no")
    password = data.get("password")
    if not all([no, password]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")
    try:
        u = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")
    if u is not None and u.verify_password(password):
        # token
        token = jwt.encode(
            {
                "sub": u.no,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(days=1),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        # print("token=", token)
        return jsonRes(msg="用户登录成功", data={'token': token})  # TODO:返回身份
    return jsonRes(code=RET.LOGINERR, msg="邮箱或密码错误")


@user.route("/change-password", methods=["PUT"])
@token_required
def change_password(current_user):
    data = request.args
    prePassword = data.get("prePassword")
    newPassword = data.get("newPassword")
    u = current_user
    if not all([prePassword, newPassword]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")
    if u.verify_password(prePassword):
        u.password = newPassword
        try:
            db.session.commit()
            return jsonRes(msg="修改密码成功")
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()  # commit失败需要回滚
            return jsonRes(code=RET.DBERR, msg="数据库查询错误")
    else:
        return jsonRes(code=RET.PWDERR, msg="原密码错误")


@user.route("/forget-password", methods=["POST"])
def forgetpwd():
    data = request.get_json()
    no = data.get("no")

    if not all([no]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    try:
        u = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="数据库查询错误")

    if u:
        email_code = "%08d" % random.randint(0, 99999999)
        current_app.logger.debug("邮箱验证码为: " + email_code)
        # redis逻辑
        try:
            redis_client.set("AUTHCODE:" + u.email, email_code, 60)
        except Exception as e:
            current_app.logger.debug(e)
            return jsonRes(code=RET.DBERR, msg="存储邮箱验证码失败")
        # 发送邮件
        send_email(
            u.email,
            "请查收验证码",
            "mail/send_code",
            username=u.username,
            email_code=email_code,
            info="修改密码",
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return jsonRes(msg="验证码发送成功")
    else:
        return jsonRes(code=RET.DATANOTEXIST, msg="用户不存在")


# @user.route("/set-password", methods=["POST"])
# def setpwd():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
#     authcode = data.get("authcode")

#     u = User.query.filter_by(email=email).first()
#     try:
#         authcode_server = redis_client.get("AUTHCODE:" + email)
#     except Exception as e:
#         current_app.logger.debug(e)
#         return jsonify(code=RET.DBERR, msg="验证码查询失败")

#     if u:
#         if authcode_server == authcode:
#             u.password = password
#             try:
#                 db.session.commit()
#                 return jsonify({"code": RET.OK, "msg": "修改密码成功"})
#             except Exception as e:
#                 current_app.logger.debug(e)
#                 db.session.rollback()  # commit失败需要回滚
#         else:
#             return jsonify(code=RET.PARAMERR, msg="验证码错误")
#     return jsonify({"code": RET.DATANOTEXIST, "msg": "邮箱不存在或者其他错误"})
