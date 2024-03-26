import json
from google.cloud import storage
from app.BBDD.BaseDatosModelo import PostgresBase, RedisBase

class DocumentoSvos():
    #===================================
    #   SERVICIOS DE POSTGRES
    #===================================
    @classmethod
    def alta_documento_supabase(cls, arg_current_app, arg_doc_post):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            db = PostgresBase(arg_current_app)

            # Verifica que la persona no este registrada
            query = f'''INSERT INTO expediente 
                            (id_empresa, id_persona, tipo_carga, texto, ruta_google_storage, ext, informacion, vigente, fecha_alta)
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''
            
            datos = (arg_doc_post.id_empresa, arg_doc_post.id_persona, arg_doc_post.tipo_carga, arg_doc_post.texto, arg_doc_post.ruta_google_storage, arg_doc_post.ext, arg_doc_post.informacion, arg_doc_post.vigente, arg_doc_post.fecha_alta)
            db.execute(query, (datos))
            db.commit()
            if db.conexion:
                db.close()

            datos_respuesta['error'] = False
            datos_respuesta['mensaje'] = 'Alta de documento en POSTGRES realizada exitosamente'
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            print('PesonaServicios.alta_documento_supabase: ', ex)
            return (True, msg_error, error_sistema)
    

    @classmethod
    def baja_documento_supabase(cls, arg_current_app, arg_documento):
        return
        

    #===================================
    #   SERVICIOS DE REDIS
    #===================================
    @classmethod
    def alta_documento_redis(cls, arg_current_app, arg_doc_redis: dict):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            redis_con = RedisBase(arg_current_app)

            nombre = arg_doc_redis.pop('nombre')
            redis_con.cargar_json(nombre, arg_doc_redis)

            datos_respuesta['error'] = False
            datos_respuesta['mensaje'] = 'Alta de documento en REDIS realizada exitosamente'
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            print('PesonaServicios.alta_documento_redis: ', ex)
            return (True, msg_error, error_sistema)
    

    @classmethod
    def baja_documento_redis(cls, arg_current_app, arg_doc_redis):
        return
    

    @classmethod
    def consulta_ocr_redis(cls, arg_current_app, query):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            redis_con = RedisBase(arg_current_app)
            consulta = redis_con.consultar()
            resultados = []
            for r in consulta:
                resultados.append(json.loads(r.json))

            datos_respuesta['datos'] = resultados
            datos_respuesta['error'] = False
            datos_respuesta['mensaje'] = 'Consulta de documento en REDIS realizada exitosamente'
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            print('PesonaServicios.consulta_ocr_redis: ', ex)
            return (True, msg_error, error_sistema)
    

    #===================================
    #   SERVICIOS DE GOOGLE CLOUD
    #===================================
    @classmethod
    def alta_bucket_GS(cls, arg_current_app, arg_documento):
        try:
            bucket_name = arg_current_app['GOOGLE_CLOUD_BUCKET']
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob_name = f"{arg_documento.cve_empresa}/{arg_documento.cve_persona}/{arg_documento.tipo_documento}/{arg_documento.nombre}"
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(arg_documento.ruta)
            return True
        except Exception as e:
            print(e)
            return False