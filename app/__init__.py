from flask import Flask, current_app
from .Documento import bp_documento
from .Empresa import bp_empresas
from .Persona import bp_personas

def crear_app():
    app = Flask(__name__)

    # DAMOS DE ALTA LA CONFIGURACION DE LA APP CON LA CLASE Config
    app.config.from_object("config.Config")

    # CONFIGURAMOS LOS LOGS DE LA APP


    # DAMOS DE ALTA TODOS LOS DISTINTOS BLUEPRINTS DE LA APP
    app.register_blueprint(bp_documento)
    app.register_blueprint(bp_empresas)
    app.register_blueprint(bp_personas)
    
    @app.route('/')
    def hello_world():
        # doc = Documento('/Users/pears/Desktop/Cuenta_santander_MEX.jpg')
        # texto = doc.extraer_texto_google()
        # print(texto[0][0].description)
        return 'Hello world!!!'
    
    return app