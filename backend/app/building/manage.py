from flask import request, current_app
from . import building
from ..response import RET, jsonRes
from ..utilities import token_required, admin_required
# from .. import db
from sqlalchemy import and_
from ..models import Building
from .utilities import building_to_dict_brief, building_to_dict


@building.route("/get-buildings", methods=["GET"])
@token_required
@admin_required
def get_buildings(current_user):
    data = request.args
    query = data.get("query", "")
    pagenum = int(data.get("pagenum", 1))
    pagesize = int(data.get("pagesize"))
    if not all([pagesize]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    u = current_user
    try:
        if u.role == 0:
            # debug
            paginate = (Building.query.filter(
                Building.name.like("%" + query + "%")).order_by(
                    Building.name).paginate(pagenum, pagesize, error_out=True))
            buildings = paginate.items
            total = paginate.total
        elif u.role == 1:
            paginate = (Building.query.filter(
                and_(Building.name.like("%" + query + "%"),
                     Building.building_id == u.building_id)).order_by(
                         Building.name).paginate(pagenum,
                                                 pagesize,
                                                 error_out=True))
            buildings = paginate.items
            total = paginate.total
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户权限错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="数据库查询错误")
    buildings_dict = list(map(building_to_dict, buildings))
    return jsonRes(msg="获取宿舍楼列表成功",
                   data={
                       "buildings": buildings_dict,
                       "total": total
                   })


@building.route("/get-buildingSelects", methods=["GET"])
@token_required
@admin_required
def get_buildingSelects(current_user):
    u = current_user
    try:
        if u.role == 0:
            buildings = Building.query.all()
        elif u.role == 1:
            buildings = Building.query.filter_by(id=u.building_id).all()
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户权限错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="数据库查询错误")
    buildings_dict = list(map(building_to_dict_brief, buildings))
    return jsonRes(msg="获取宿舍楼列表成功", data={
        "buildings": buildings_dict,
    })
