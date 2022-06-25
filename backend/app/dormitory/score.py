from flask import request, current_app
from . import dormitory
from ..response import RET, jsonRes
from ..utilities import token_required, sub_admin_required
from .. import db
# from sqlalchemy import or_, and_
from ..models import Score
from datetime import datetime


@dormitory.route("/score", methods=["POST"])
@token_required
@sub_admin_required
def add_score(current_user):
    data = request.json
    dorm_id = data.get("dorm_id")
    work_no = data.get("work_no")
    time = data.get("time")
    score = data.get("score")
    check_type = data.get("check_type")
    profile = data.get("profile")
    if not all([dorm_id, work_no, time, score, check_type]):
        return jsonRes(code=RET.PARAMERR, msg="参数不完整")

    # print("######", time, datetime.now(), datetime.fromtimestamp(time / 1000))

    score = Score(dorm_id=dorm_id,
                  work_no=work_no,
                  time=datetime.fromtimestamp(time / 1000),
                  score=score,
                  check_type=check_type,
                  profile=profile)

    try:
        db.session.add(score)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonRes(code=RET.DBERR, msg="数据库错误")
    return jsonRes(msg="打分成功")
