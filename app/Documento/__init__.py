from flask import Blueprint

bp_documento = Blueprint('documento', __name__, url_prefix='/documento')

from . import rutas_documento