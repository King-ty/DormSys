from flask import request, current_app
from . import dormitory
from ..response import RET, jsonRes
from ..utilities import token_required, admin_required
# from .. import db
# from sqlalchemy import or_, and_
from ..models import Dormitory
from .utilities import dorm_to_dict, dorm_to_dict_select


@dormitory.route("/get-dorms", methods=["GET"])
@token_required
@admin_required
def get_dorms(current_user):
    data = request.args
    pagenum = int(data.get("pagenum", 1))
    pagesize = int(data.get("pagesize"))
    if not all([pagesize]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    u = current_user
    try:
        if u.role == 0:
            # debug
            paginate = (Dormitory.query.order_by(Dormitory.building.name,
                                                 Dormitory.no).paginate(
                                                     pagenum,
                                                     pagesize,
                                                     error_out=True))
            dormitories = paginate.items
            total = paginate.total
        elif u.role == 1:
            paginate = (Dormitory.query.filter(
                Dormitory.building_id == u.building_id).order_by(
                    Dormitory.building_id,
                    Dormitory.no).paginate(pagenum, pagesize, error_out=True))
            dormitories = paginate.items
            total = paginate.total
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户权限错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="数据库查询错误")
    dorms_dict = list(map(dorm_to_dict, dormitories))
    return jsonRes(msg="获取宿舍列表成功", data={"dorms": dorms_dict, "total": total})


@dormitory.route("/get-dormitorySelects", methods=["GET"])
@token_required
@admin_required
def get_dormitorySelects(current_user):
    data = request.args
    building_id = data.get("building_id")
    u = current_user
    try:
        if u.role == 0:
            dormitorys = Dormitory.query.filter(
                Dormitory.building_id == building_id).all()
        elif u.role == 1:
            if building_id != u.building_id:
                dormitorys = None
            else:
                dormitorys = Dormitory.query.filter(
                    Dormitory.building_id == building_id).all()
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户权限错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="数据库查询错误")

    dorms_dict = list(map(dorm_to_dict_select, dormitorys))
    return jsonRes(msg="获取宿舍楼列表成功", data={
        "dorms": dorms_dict,
    })
