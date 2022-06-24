def building_to_dict(building):
    ret = {}
    ret["id"] = building.id
    ret["name"] = building.name
    ret["gender"] = building.gender
    ret["is_bed_on_table"] = building.is_bed_on_table
    ret["is_independent_bathroom"] = building.is_independent_bathroom
    ret["profile"] = building.profile

    return ret


def building_to_dict_brief(building):
    ret = {}
    ret["id"] = building.id
    ret["name"] = building.name

    return ret
