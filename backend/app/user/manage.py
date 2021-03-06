from flask import request, current_app
from . import user
from .. import db
from ..response import RET, jsonRes
from ..utilities import token_required, admin_required, sub_admin_required, getUser
from sqlalchemy import or_, and_
from ..models import Student, Dormitory
from .utilities import user_to_dict, user_to_dict_brief


@user.route("/get-users", methods=["GET"])
@token_required
@sub_admin_required
def get_users(current_user):
    data = request.args
    query = data.get("query", "")
    pagenum = int(data.get("pagenum", 1))
    pagesize = int(data.get("pagesize", 5))
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
    users_dict = list(map(user_to_dict_brief, users))
    return jsonRes(msg="获取用户列表成功", data={"users": users_dict, "total": total})


@user.route("/user", methods=["GET"])
@token_required
def get_user(current_user):
    data = request.args
    no = data.get("no")

    if not all([no]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")
    try:
        u = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")

    if u:
        return jsonRes(msg="查询用户成功", data=user_to_dict(u))

    return jsonRes(code=RET.DATANOTEXIST, msg="用户不存在")


@user.route("/user", methods=["POST"])
@token_required
@admin_required
def add_user(current_user):
    data = request.json
    no = data.get("no")
    name = data.get("name")
    password = data.get("password")
    gender = data.get("gender")
    email = data.get("email")
    tel = data.get("tel")
    major = data.get("major")
    grade = data.get("grade")
    classno = data.get("classno")
    building_id = data.get("building_id")
    dorm_id = data.get("dormitory_id")

    if not all([no, name, password]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")
    try:
        u = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")

    if u:
        return jsonRes(code=RET.DATAEXIST, msg="用户已存在")
    if dorm_id:
        dormitory = Dormitory.query.filter_by(id=dorm_id).first()
        students_in = dormitory.students.all()
        if len(students_in) >= dormitory.max_number:
            return jsonRes(code=RET.LIMIT, msg="该宿舍已满员")
    u = Student(no=no,
                name=name,
                password=password,
                gender=gender,
                email=email,
                tel=tel,
                major=major,
                grade=grade,
                classno=classno,
                building_id=building_id,
                dorm_id=dorm_id)
    try:
        db.session.add(u)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonRes(code=RET.DBERR, msg="数据库错误")
    return jsonRes(msg="添加用户成功")


@user.route("/user", methods=["PUT"])
@token_required
@admin_required
def edit_user(current_user):
    data = request.json
    # print(data)
    no = data.get("no")
    name = data.get("name")
    gender = data.get("gender")
    email = data.get("email")
    tel = data.get("tel")
    major = data.get("major")
    grade = data.get("grade")
    classno = data.get("classno")
    building_id = data.get("building_id")
    dorm_id = data.get("dormitory_id")

    if not all([no, name]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")
    try:
        u = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")

    if not u:
        return jsonRes(code=RET.DATANOTEXIST, msg="用户不存在")

    if dorm_id and u.dorm_id != dorm_id:
        dormitory = Dormitory.query.filter_by(id=dorm_id).first()
        students_in = dormitory.students.all()
        if len(students_in) >= dormitory.max_number:
            return jsonRes(code=RET.LIMIT, msg="该宿舍已满员")

    u.name = name
    u.gender = gender
    u.email = email
    u.tel = tel
    u.major = major
    u.grade = grade
    u.classno = classno
    u.building_id = building_id
    u.dorm_id = dorm_id
    try:
        db.session.merge(u)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonRes(code=RET.DBERR, msg="数据库错误")
    return jsonRes(msg="编辑用户成功")


@user.route("/user/<no>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(current_user, no):
    # 删除有点特殊！
    # print(request.args, no)

    if not all([no]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")
    try:
        u = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")

    if not u:
        return jsonRes(code=RET.DATANOTEXIST, msg="用户不存在")
    try:
        db.session.delete(u)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonRes(code=RET.DBERR, msg="数据库错误")
    return jsonRes(msg="删除用户成功")
