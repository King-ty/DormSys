def student_to_dict_tiny(student):
    ret = {}
    ret["no"] = student.no
    ret["name"] = student.name

    return ret


def dorm_to_dict(dorm):
    ret = {}
    ret["id"] = dorm.id
    ret["no"] = dorm.no
    ret["building"] = dorm.building.name if dorm.building else None
    ret["max_num"] = dorm.max_number
    students = dorm.students.all()
    ret["num"] = len(students)
    ret["students"] = list(map(student_to_dict_tiny, students))

    return ret


def dorm_to_dict_select(dorm):
    ret = {}
    ret["id"] = dorm.id
    ret["no"] = dorm.no

    return ret
