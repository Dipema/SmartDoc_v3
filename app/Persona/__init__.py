from flask import Blueprint

bp_personas = Blueprint('persona', __name__, url_prefix='/persona')

from . import rutas_persona