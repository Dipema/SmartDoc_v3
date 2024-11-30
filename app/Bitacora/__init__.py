from flask import Blueprint

bp_bitacora = Blueprint('bitacora', __name__, url_prefix='/bitacora')

from . import bitacoraRutas