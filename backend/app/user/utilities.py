def user_to_dict_brief(user):
    ret = {}
    ret["no"] = user.no
    ret["name"] = user.name
    ret['building_id'] = user.building_id
    ret['building'] = user.building.name if user.building else None
    ret['dormitory_id'] = user.dorm_id
    ret['dormitory'] = user.dormitory.no if user.dormitory else None
    ret["gender"] = user.gender
    ret["tel"] = user.tel

    # ret["email"] = user.email
    # ret["major"] = user.major
    # ret["grade"] = user.grade
    # ret["classno"] = user.classno

    return ret


def user_to_dict(user):
    ret = {}
    ret["no"] = user.no
    ret["name"] = user.name
    ret['building_id'] = user.building_id
    ret['building'] = user.building.name if user.building else None
    ret['dormitory_id'] = user.dorm_id
    ret['dormitory'] = user.dormitory.no if user.dormitory else None
    ret["gender"] = user.gender
    ret["tel"] = user.tel
    ret["email"] = user.email
    ret["role"] = user.role
    ret["major"] = user.major
    ret["grade"] = user.grade
    ret["classno"] = user.classno
    ret["profile"] = user.profile

    return ret
