def student_to_dict_brief(student):
    ret = {}
    ret["no"] = student.no
    ret["name"] = student.name
    ret["dormitory"] = student.dormitory.no
    ret["building"] = student.building.name

    return ret


def student_to_dict(student):
    ret = {}
    ret["no"] = student.no
    ret["name"] = student.name
    ret["dormitory"] = student.dormitory.no
    ret["building"] = student.building.name
    ret["gender"] = student.gender
    ret["tel"] = student.tel
    ret["email"] = student.email
    ret["role"] = student.role
    ret["major"] = student.major
    ret["grade"] = student.grade
    ret["classno"] = student.classno
    ret["profile"] = student.profile

    return ret