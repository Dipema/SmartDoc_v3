from flask import Blueprint

bp_seguridad = Blueprint('seguridad', __name__, url_prefix='/seguridad')

from . import seguridadRutas