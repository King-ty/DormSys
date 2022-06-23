def user_to_dict(user):
    ret = {}
    ret["no"] = user.no
    ret["name"] = user.name
    ret["gender"] = user.gender
    ret["tel"] = user.tel
    ret["email"] = user.email
    ret["role"] = user.role
    ret["major"] = user.major
    ret["grade"] = user.grade
    ret["classno"] = user.classno

    return ret
