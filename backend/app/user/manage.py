from flask import request, current_app
from . import user
from .. import db
from ..response import RET, jsonRes
from ..utilities import token_required, admin_required, getUser
from ..models import Student
from sqlalchemy import or_, and_
from .utilities import student_to_dict_brief, student_to_dict


@user.route("/get-users", methods=["GET"])
@token_required
@admin_required
def get_users(current_user):
    data = request.args
    query = data.get("query", "")
    pagenum = int(data.get("pagenum", 1))
    pagesize = int(data.get("pagesize", 5))

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
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")

    students_dict = list(map(student_to_dict_brief, students))

    return jsonRes(msg="查询用户列表成功",
                   data={
                       'students': students_dict,
                       'total': total
                   })


@user.route("/user", methods=["GET"])
@token_required
def get_user(current_user):
    data = request.args
    no = data.get("no")

    if not all([no]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    u = current_user

    try:
        student = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")

    student_dict = student_to_dict(student)

    return jsonRes(msg="查询用户成功", data={
        'student': student_dict,
    })


@user.route("/user", methods=["POST"])
@token_required
@admin_required
def add_user(current_user):
    data = request.json
    no = data.get("no")
    name = data.get("name")
    password = data.get("password")
    gender = data.get("gender")
    tel = data.get("tel")
    email = data.get("email")
    major = data.get("major")
    grade = data.get("grade")
    classno = data.get("classno")
    building_id = data.get("building_id")
    dorm_id = data.get("dorm_id")

    if not all([no, name, password]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    u = current_user

    if u.role != 0:
        jsonRes(code=RET.AUTHERR, msg="用户权限不够")

    try:
        student = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")
    if student:
        return jsonRes(code=RET.DATAEXIST, msg="用户已存在")

    student = Student(no=no,
                      name=name,
                      password=password,
                      gender=gender,
                      tel=tel,
                      email=email,
                      major=major,
                      grade=grade,
                      classno=classno,
                      building_id=building_id,
                      dorm_id=dorm_id)
    try:
        db.session.add(student)
        db.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonRes(code=RET.DBERR, msg="用户添加失败")

    return jsonRes(msg="添加用户成功")


@user.route("/user", methods=["PUT"])
@token_required
@admin_required
def edit_user(current_user):
    data = request.json
    no = data.get("no")
    name = data.get("name")
    gender = data.get("gender")
    tel = data.get("tel")
    email = data.get("email")
    major = data.get("major")
    grade = data.get("grade")
    classno = data.get("classno")
    building_id = data.get("building_id")
    dorm_id = data.get("dorm_id")

    if not all([no, name]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    u = current_user

    if u.role != 0:
        jsonRes(code=RET.AUTHERR, msg="用户权限不够")

    try:
        student = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")
    if not student:
        return jsonRes(code=RET.DATANOTEXIST, msg="用户不存在")

    student.no = no
    student.name = name
    student.gender = gender
    student.tel = tel
    student.email = email
    student.major = major
    student.grade = grade
    student.classno = classno
    student.building_id = building_id
    student.dorm_id = dorm_id
    # TODO:判断宿舍满员！
    try:
        db.session.merge(student)
        db.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonRes(code=RET.DBERR, msg="用户编辑失败")

    return jsonRes(msg="编辑用户成功")


@user.route("/user/<no>", methods=["DELETE"])
@token_required
@admin_required
def del_user(current_user, no):
    if not all([no]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    no = int(no)
    u = current_user

    if u.role != 0:
        jsonRes(code=RET.AUTHERR, msg="用户权限不够")

    try:
        student = getUser(no)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="用户查询失败")

    try:
        db.session.delete(student)
        db.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonRes(code=RET.DBERR, msg="用户删除失败")

    return jsonRes(msg="删除用户成功")