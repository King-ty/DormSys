from flask import jsonify


class RET:
    OK = "00"
    LOGINERR = "01"
    PARAMERR = "02"
    DBERR = "03"
    DATAEXIST = "04"
    PWDERR = "05"
    DATANOTEXIST = "06"
    COPY = "07"
    TIMEOUT = "08"
    AUTHERR = "09"  # 权限错误，请求的用户没有此操作的权限


def jsonRes(code=RET.OK, msg="成功", data=None):
    meta = {'code': code, 'msg': msg}
    return jsonify(meta=meta, data=data)
