from flask import request, current_app
from . import dormitory
from ..utilities import token_required, admin_required, getUser


@dormitory.route("/get-dorms", methods=["GET"])
@token_required
@admin_required
def get_dorms(current_user):
    pass