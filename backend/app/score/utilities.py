import time


def score_to_dict(score):
    ret = {}
    ret["id"] = score.id
    ret["dormitory"] = score.dormitory.no
    ret["admin"] = score.admin.name
    ret["time"] = time.mktime(score.time.timetuple())
    ret["score"] = score.score
    ret["check_type"] = score.check_type
    ret["profile"] = score.profile

    return ret
