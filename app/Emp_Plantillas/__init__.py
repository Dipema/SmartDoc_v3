from flask import Blueprint

bp_empresa_plantilla = Blueprint('empresa_plantilla', __name__, url_prefix='/empresa-plantilla')

from . import empPlantillaRutas