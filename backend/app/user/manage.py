from flask import request, current_app
from . import user
from .. import db, redis_client
from ..response import RET, jsonRes
from datetime import datetime, timedelta
from ..utilities import token_required, admin_required, getUser
import jwt
import random
from ..models import Student
from sqlalchemy import or_, and_


@user.route("/get-users", methods=["GET"])
@token_required
@admin_required
def get_users(current_user):
    data = request.args
    query = data.get("query", "")
    pagenum = int(data.get("pagenum", 1))
    pagesize = int(data.get("pagesize", 5))

    u = current_user

    if u.role == 0:
        paginate = (Student.query.filter(
            or_(
                Student.no.like("%" + query + "%"),
                Student.name.like("%" + query + "%"),
            )).order_by(Student.no).paginate(pagenum, pagesize,
                                             error_out=True))
        students = paginate.items
        total = paginate.total
    elif u.role == 1:
        paginate = (Student.query.filter(
            and_(
                Student.building_id == u.building_id,
                or_(
                    Student.no.like("%" + query + "%"),
                    Student.name.like("%" + query + "%"),
                ))).order_by(Student.no).paginate(pagenum,
                                                  pagesize,
                                                  error_out=True))
        students = paginate.items
        total = paginate.total
    else:
        jsonRes(code=RET.AUTHERR, msg="用户权限不够")

        return jsonRes(msg="用户登录成功", data={'token': token})  # TODO:返回身份
    return jsonRes(code=RET.LOGINERR, msg="邮箱或密码错误")
