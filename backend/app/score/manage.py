from flask import request, current_app
from . import score
from ..response import RET, jsonRes
from ..utilities import token_required, sub_admin_required
from .. import db
# from sqlalchemy import or_, and_
from ..models import Score
from datetime import datetime
from .utilities import score_to_dict


@score.route("/get-scores", methods=["GET"])
@token_required
@sub_admin_required
def get_scores(current_user):
    data = request.args
    pagenum = int(data.get("pagenum", 1))
    pagesize = int(data.get("pagesize", 5))

    u = current_user
    try:
        if u.role == 0:
            paginate = (Score.query.order_by(Score.id.desc()).paginate(
                pagenum, pagesize, error_out=True))
            scores = paginate.items
            total = paginate.total
        elif u.role == 1:
            paginate = (Score.query.order_by(Score.id.desc()).filter_by(
                work_no=u.no).paginate(pagenum, pagesize, error_out=True))
            scores = paginate.items
            total = paginate.total
        else:
            return jsonRes(code=RET.AUTHERR, msg="用户权限错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonRes(code=RET.DBERR, msg="数据库查询错误")
    scores_dict = list(map(score_to_dict, scores))
    print(scores_dict)
    return jsonRes(msg="获取得分列表成功",
                   data={
                       "scores": scores_dict,
                       "total": total
                   })


@score.route("/score", methods=["POST"])
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
