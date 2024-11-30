from flask import Blueprint

bp_empresa_proceso = Blueprint('empresa_proceso', __name__, url_prefix='/empresa-proceso')

from . import empProcesoRutas