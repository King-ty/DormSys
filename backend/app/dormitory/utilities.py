def dorm_to_dict(dorm):
    ret = {}
    ret["id"] = dorm.id
    ret["no"] = dorm.no
    ret["building"] = dorm.building.name
    ret["max_num"] = dorm.max_number

    return ret


def dorm_to_dict_select(dorm):
    ret = {}
    ret["id"] = dorm.id
    ret["no"] = dorm.no

    return ret
