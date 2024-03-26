from . import bp_personas
from .PersonaServicios import PersonaSvos
from app.Empresa.EmpresaServicios import EmpresaSvos
from .PersonaModelo import Persona

from flask import current_app, request
from datetime import datetime

@bp_personas.route('/')
def empresa_HW():
    return 'Persona: Hello World!!!'


@bp_personas.route('/alta-persona/', methods=['POST'])
def alta_persona():
    try:
        datos_entrada = request.get_json()

        identificador = datos_entrada['cve_persona']
        tipo_identificador = datos_entrada['tipo_cve']
        nombre = datos_entrada['nombre']
        vigente = True
        fecha_alta = datetime.today().strftime('%Y-%m-%d')

        # Verifica que el id_empresa existe en la BBDD
        # lista_empresas = EmpresaSvos.lista_empresa(current_app)[1]['datos']
        # existe_empresa = False
        # for empresa in lista_empresas:
        #     if id_empresa == empresa['id']:
        #         existe_empresa = True
        #         break
        
        # if existe_empresa:
        persona = Persona(identificador, tipo_identificador, nombre, vigente, fecha_alta)
        alta = PersonaSvos.alta_persona(current_app, persona)
        return alta[1], 200
        # else:
        #     return 'ERROR: LA EMPRESA INDICADA NO EXISTE', 500
        
    except Exception as ex:
        print(ex)
        return 'ERROR', 500   


@bp_personas.route('/baja-persona/', methods=['POST', 'GET'])
def baja_persona():
    try:
        datos_entrada = request.form['id']
        baja = PersonaSvos.baja_persona(current_app, datos_entrada)
        return baja[1], 200
    except Exception as ex:
        print(ex)
        return 'ERROR', 500


@bp_personas.route('/listar-personas/', methods=['GET'])
def listar_personas():
    try:
        lista_pnas = PersonaSvos.lista_persona(current_app)
        return lista_pnas[1]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500
    

@bp_personas.route('/consulta-persona/', methods=['GET'])
def consulta_persona():
    try:
        datos_entrada = request.form['id']

        consulta = PersonaSvos.consulta_persona(current_app, datos_entrada)
        return consulta[1]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500
    
