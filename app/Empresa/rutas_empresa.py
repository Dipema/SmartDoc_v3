from . import bp_empresas
from .EmpresaServicios import EmpresaSvos
from .EmpresaModelo import Empresa

from datetime import datetime
from flask import request, current_app

@bp_empresas.route('/')
def empresa_HW():
    return 'Empresa: Hello World!!!'


@bp_empresas.route('/alta-empresa/', methods=['GET', 'POST'])
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
        return alta[1]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500


@bp_empresas.route('/baja-empresa/', methods=['GET', 'POST'])
def baja_empresa():
    try:
        datos_entrada = request.form['id']

        baja = EmpresaSvos.baja_empresa(current_app, datos_entrada)
        return baja[1], 200
    except Exception as ex:
        print(ex)
        return 'ERROR', 500


@bp_empresas.route('/listar-empresas/', methods=['GET', 'POST'])
def lista_empresas():
    try:
        lista_empresas = EmpresaSvos.lista_empresa(current_app)
        return lista_empresas[1]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500
    

@bp_empresas.route('/consulta-empresa/', methods=['GET', 'POST'])
def consulta_empresas():
    try:
        datos_entrada = request.form['id']

        consulta = EmpresaSvos.consulta_empresa(current_app, datos_entrada)
        return consulta[1]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500
    
