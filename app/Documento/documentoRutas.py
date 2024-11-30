from . import bp_documento
from .documentoModelo import Documento
from .documentoSvosBD import DocumentoSvos
from app.Empresa.empresaSvosBD import EmpresaSvos
from app.Persona.PersonaServicios import PersonaSvos

from flask import current_app, request
from flask_cors import CORS
import os
import json
from io import BytesIO
from PIL import Image
import requests
from werkzeug.utils import secure_filename

cors = CORS(bp_documento, resources={fr"/documento/*": {"origins":"*"}})

@bp_documento.route('/')
def documento_HW():
    return 'Documento: Hello World!!!'


@bp_documento.route('/cargar-documento/', methods = ['POST'])
def carga_documento():
    try:
        # RECIBIMOS LOS DATOS DEL REQUEST
        id_empresa= request.form['idEmpresa']
        id_persona= request.form['idPersona']
        tipo_carga= request.form['tipoCarga']
        tipo_documento= request.form['tipoDocumento']
        archivo= request.files['imagen']

        print(f'''
            ID EMPRESA:     {id_empresa}
            ID PERSONA:     {id_persona}
            TIPO CARGA:     {tipo_carga}
            TIPO DOCUMENTO: {tipo_documento}
        ''')

        # GUARDAMOS EL ARCHIVO EN UN DIRECTORIO LOCAL
        dir_carga = current_app.config['DIR_CARGAS']
        nombre_archivo = secure_filename(archivo.filename)
        ruta_temporal = os.path.join(dir_carga, nombre_archivo)
        archivo.save(ruta_temporal)

        # CREAMOS UN OBJETO DEL TIPO DOCUMENTO
        doc = Documento(ruta_temporal, dir_carga)
        doc_json = doc.to_json()
        texto = doc.extraer_texto_google()[0][0].description

        # CHECAMOS LAS EMPRESAS PARA VER LA CVE QUE COINCIDE CON EL ID
        cve_empresa = ''
        lista_empresas = EmpresaSvos.lista_empresa(current_app)[1]['datos']
        for empresa in lista_empresas:
            if str(empresa['id']) == id_empresa:
                #print(empresa)
                cve_empresa = empresa['clave_empresa']
                break

        # CHECAMOS LAS PERSONAS PARA VER LA CVE QUE COINCIDE CON EL ID
        cve_persona = ''
        lista_personas = PersonaSvos.lista_persona(current_app)[1]['datos']
        for persona in lista_personas:
            if str(persona['id']) == id_persona:
                #print(persona)
                cve_persona = persona['identificador']
                break

        # GUARDAMOS EL ARCHIVO EN GOOGLE STORAGE
        gs_json = {
            'cve_empresa': cve_empresa,
            'cve_persona': cve_persona,
            'tipo_carga': tipo_carga,
            'tipo_documento': tipo_documento,
            'nombre': nombre_archivo,
            'ruta': ruta_temporal
        }
        alta_gs = DocumentoSvos.alta_bucket_GS(current_app, gs_json)

        # GUARDAMOS DATOS EN REDIS
        redis_json = {
            'nombre': doc_json['nombre'],
            'id_persona': 1,
            'id_empresa': 1,
            'texto': texto,
            'tipo_documento': doc_json['tipo_documento'],
            'ruta_gs': alta_gs['datos'],
            'fecha_creacion': doc_json['fecha_creacion'],
        }
        alta_redis = DocumentoSvos.alta_documento_redis(current_app.config, redis_json)

        # GUARDAMOS DATOS EN POSTGRES
        post_json ={
            'id_persona': id_persona,
            'id_empresa': id_empresa,
            'tipo_carga': tipo_carga,
            'texto': texto,
            'ruta_gs': alta_gs['datos'],
            'ext': doc_json['ext'],
            'informacion': json.dumps({}),
            'vigente': True,
            'fecha_alta': doc_json['fecha_creacion'],
            'tipo_documento': tipo_documento
        }
        alta_supabase = DocumentoSvos.alta_documento_supabase(current_app, post_json)
        return [alta_supabase[1], alta_redis[1]]
    except Exception as ex:
        print(ex)
        return 'ERROR', 500
    

@bp_documento.route('/cargar-documento-url/', methods=['POST'])
def carga_documento_url():
    try:
        id_empresa = request.form['idEmpresa'] 
        id_persona = request.form['idPersona']
        tipo_carga = request.form['tipoCarga']
        tipo_documento = request.form['tipoDocumento']
        url_imagen = request.form['urlImagen'] 

        print(f'''
            CLAVE EMPRESA:  {id_empresa}
            NOMBRE PERSONA: {id_persona}
            TIPO CARGA:     {tipo_carga}
            TIPO DOCUMENTO: {tipo_documento}
        ''')
        
        # DESCARGAMOS EL DOCUMENTO DE LA URL EN UN ARCHIVO LOCAL
        dir_carga = current_app.config['DIR_CARGAS']
        respuesta = requests.get(url_imagen)
        nombre_archivo = os.path.split(url_imagen)[1]
        ruta_temporal = os.path.join(dir_carga, nombre_archivo)
        ext_archivo = os.path.splitext(nombre_archivo)[-1].lower()
        if ext_archivo == '.pdf':
            with open(ruta_temporal, 'wb') as f:
                f.write(respuesta.content)
        else:
            imagen = Image.open(BytesIO(respuesta.content))
            imagen.save(ruta_temporal)

        # CREAMOS UN OBJETO DEL TIPO DOCUMENTO
        doc = Documento(ruta_temporal, dir_carga)
        doc_json = doc.to_json()
        texto = doc.extraer_texto_google()[0][0].description

        # CHECAMOS LAS EMPRESAS PARA VER LA CVE QUE COINCIDE CON EL ID
        cve_empresa = ''
        lista_empresas = EmpresaSvos.lista_empresa(current_app)[1]['datos']
        for empresa in lista_empresas:
            if str(empresa['id']) == id_empresa:
                #print(empresa)
                cve_empresa = empresa['clave_empresa']
                break

        # CHECAMOS LAS PERSONAS PARA VER LA CVE QUE COINCIDE CON EL ID
        cve_persona = ''
        lista_personas = PersonaSvos.lista_persona(current_app)[1]['datos']
        for persona in lista_personas:
            if str(persona['id']) == id_persona:
                #print(persona)
                cve_persona = persona['identificador']
                break

        # GUARDAMOS EL ARCHIVO EN GOOGLE STORAGE
        gs_json = {
            'cve_empresa': cve_empresa,
            'cve_persona': cve_persona,
            'tipo_carga': tipo_carga,
            'tipo_documento': tipo_documento,
            'nombre': nombre_archivo,
            'ruta': ruta_temporal
        }
        alta_gs = DocumentoSvos.alta_bucket_GS(current_app, gs_json)

        # GUARDAMOS DATOS EN REDIS
        redis_json = {
            'nombre': doc_json['nombre'],
            'id_persona': 1,
            'id_empresa': 1,
            'texto': texto,
            'tipo_documento': doc_json['tipo_documento'],
            'ruta_gs': alta_gs['datos'],
            'fecha_creacion': doc_json['fecha_creacion'],
        }
        alta_redis = DocumentoSvos.alta_documento_redis(current_app.config, redis_json)

        # GUARDAMOS DATOS EN POSTGRES
        post_json ={
            'id_persona': id_persona,
            'id_empresa': id_empresa,
            'tipo_carga': tipo_carga,
            'texto': texto,
            'ruta_gs': alta_gs['datos'],
            'ext': doc_json['ext'],
            'informacion': json.dumps({}),
            'vigente': True,
            'fecha_alta': doc_json['fecha_creacion'],
            'tipo_documento': tipo_documento
        }
        alta_supabase = DocumentoSvos.alta_documento_supabase(current_app, post_json)
        return [alta_supabase[1], alta_redis[1]]
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

