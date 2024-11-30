from flask import Blueprint

bp_usuarios = Blueprint('usuario_blueprint', __name__, url_prefix='/seguridad')

from . import usuarioRutas