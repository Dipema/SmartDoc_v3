from flask import Blueprint

bp_empresa_area = Blueprint('empresa_area', __name__, url_prefix='/empresa-area')

from . import empAreaRutas