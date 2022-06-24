from flask import request, current_app
from . import building
from ..utilities import token_required, admin_required, getUser


@building.route("/get-buildings", methods=["GET"])
@token_required
@admin_required
def get_buildings(current_user):
    pass