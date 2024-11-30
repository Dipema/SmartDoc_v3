from flask import Blueprint

bp_proceso = Blueprint('proceso', __name__, url_prefix='/proceso')

from . import procesoRutas