from . import bp_empresas
#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from app.Utilerias.logs  import Logger
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from app.Bitacora.bitacoraModelo import Bitacora
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from app.Empresa.EmpresaModelo import Empresa
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from app.Utilerias.utileriaModelo import Operador
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from app.Bitacora.bitacoraSvosBD import BitacoraSvos
#   Servicios. Del componente EmpresaServicios.py importa la clase EmpresaSvos
from app.Empresa.empresaSvosBD import EmpresaSvos
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from app.Seguridad.seguridadSvos import Seg_TokenSvos

#   Servicios. Del componente SeguridadServicios.py importa la clase TokenSvos
#from app.admin.Servicios.SeguridadServicios import TokenSvos

from datetime import datetime
from flask import request, current_app, jsonify
import json

@bp_empresas.route('/')
def empresa_HW():
    return 'Empresa: Hello World!!!'


@bp_empresas.route('/v1/alta-empresa/', methods=['GET', 'POST'])
def alta_empresa():
    try:
        datos_entrada = request.get_json()

        cve_empresa = datos_entrada['cveEmpresa']
        nombre = datos_entrada['nombre']
        observaciones = datos_entrada['observaciones']
        uso_webhook = False
        vigente = True
        fecha_alta = datetime.today().strftime('%Y-%m-%d')
        
        empresa = Empresa(cve_empresa, nombre, observaciones, uso_webhook, vigente, fecha_alta)
        alta = EmpresaSvos.alta_empresa(current_app, empresa)
        respuesta = alta[1]
        return (respuesta, 200)
    
    except Exception as ex:
        return (traceback(ex), 500)


@bp_empresas.route('/v1/baja-empresa/', methods=['GET', 'POST'])
def baja_empresa():
    try:
        datos_entrada = request.form['id']

        baja = EmpresaSvos.baja_empresa(current_app, datos_entrada)
        respuesta = baja[1]
        return (respuesta, 200)
    
    except Exception as ex:
        return (traceback(ex), 500)


@bp_empresas.route('/v1/listar-empresas/', methods=['GET', 'POST'])
def lista_empresas():
    try:
        lista_empresas = EmpresaSvos.lista_empresa(current_app)
        respuesta = lista_empresas[1]
        return (respuesta, 200)
    
    except Exception as ex:
        return (traceback(ex), 500)

@bp_empresas.route('/v1/consulta-empresa/', methods=['GET', 'POST'])
def consulta_empresas():
    try:
        datos_entrada = request.form['id']

        consulta = EmpresaSvos.consulta_empresa(current_app, datos_entrada)
        respuesta = consulta[1]
        return (respuesta, 200)
    
    except Exception as ex:
        return (traceback(ex), 500)
    

