from flask import request, current_app
from . import user
from ..response import RET, jsonRes
from ..utilities import token_required, admin_required
from sqlalchemy import or_, and_
from ..models import Student
from .utilities import user_to_dict


@user.route("/get-users", methods=["GET"])
@token_required
@admin_required
def get_users(current_user):
    data = request.args
    query = data.get("query", "")
    pagenum = int(data.get("pagenum", 1))
    pagesize = int(data.get("pagesize"))
    if not all([pagesize]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    # print(type(pagenum), type(pagesize), '###')
    u = current_user
    try:
        if u.role == 0:
            paginate = (Student.query.filter(
                or_(
                    Student.no.like("%" + query + "%"),
                    Student.name.like("%" + query + "%"),
                )).order_by(Student.no).paginate(pagenum,
                                                 pagesize,
                                                 error_out=True))
            users = paginate.items
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
            users = paginate.items
            total = paginate.total
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户权限错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="数据库查询错误")
    users_dict = list(map(user_to_dict, users))
    return jsonRes(msg="获取用户列表成功", data={"users": users_dict, "total": total})
