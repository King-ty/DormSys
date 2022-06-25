from flask import Blueprint

dormitory = Blueprint("dormitory", __name__)

from . import manage, score
