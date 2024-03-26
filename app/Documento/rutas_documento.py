from . import bp_documento
from .DocumentoModelo import Documento
from .DocumentoServicios import DocumentoSvos
from app.Empresa.EmpresaServicios import EmpresaSvos

from flask import current_app, request
from flask_cors import CORS
import os
import datetime
from werkzeug.utils import secure_filename

cors = CORS(bp_documento, resources={fr"/documento/*": {"origins":"*"}})

@bp_documento.route('/')
def documento_HW():
    return 'Documento: Hello World!!!'

@bp_documento.route('/cargar-documento/', methods = ['POST'])
def carga_documento():
    try:
        cve_empresa = request.form['cveEmpresa'] 
        cve_persona = request.form['cvePersona']
        tipo_carga = request.form['tipoCarga']
        tipo_documento = request.form['tipoDocumento']
        archivo = request.files['image'] 

        print(f'''
            CLAVE EMPRESA:  {cve_empresa}
            NOMBRE PERSONA: {cve_persona}
            TIPO CARGA:     {tipo_carga}
            TIPO DOCUMENTO: {tipo_documento}
        ''')

        dir_carga = current_app.config['DIR_CARGAS']
        nombre_archivo = secure_filename(archivo.filename)
        ruta_temporal = os.path.join(dir_carga, nombre_archivo)
        archivo.save(ruta_temporal)

        doc = Documento(ruta_temporal, dir_carga)
        doc_json = doc.to_json()
        print(doc_json)
        texto = doc.extraer_texto_google()[0][0].description

        redis_json = {
            'nombre': doc_json['nombre'],
            'texto': texto,
            'tipo_documento': doc_json['tipo_documento'],
            'fecha_creacion': doc_json['fecha_creacion']
        }

        alta_redis = DocumentoSvos.alta_documento_redis(current_app.config, redis_json)
        #alta_postgres = DocumentoSvos.alta_documento_supabase(current_app, doc_json)
        #return [alta_postgres[1], alta_redis[1]]
        return alta_redis[1]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500
    

@bp_documento.route('/consultar-ocr/', methods = ['GET'])
def consulta_ocr():
    try:
        texto = request.form['texto']

        alta_redis = DocumentoSvos.consulta_ocr_redis(current_app.config, texto)
        return alta_redis[1]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500