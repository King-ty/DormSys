from flask import Blueprint

building = Blueprint("building", __name__)

from . import manage
