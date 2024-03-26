from flask import Blueprint

bp_empresas = Blueprint('empresa', __name__, url_prefix='/empresa')

from . import rutas_empresa