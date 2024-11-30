from app.Utilerias.BaseDatosModelo import PostgresBase, RedisBase

class EmpresaSvos():
    @classmethod
    def lista_empresa(cls, arg_current_app):
        try:
            datosRespuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(arg_current_app)

            query = f'''SELECT * FROM empresas;'''

            db.execute(query)
            respuesta = db.fetchall()
            datosResultado = respuesta
            if db.conexion:
                db.close()

            #Valida si datosResultado esta vacio
            if (len(datosResultado) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            lista_empresas = []
            lista_valores = ['id', 'nombre_empresa', 'clave_empresa', 'observaciones', 'uso_webhook', 'valido', 'fecha_alta']
            for empresa in respuesta:
                valores_empresa = {}
                for i in range(0, len(lista_valores)):
                    valores_empresa[lista_valores[i]] = empresa[i]
                lista_empresas.append(valores_empresa)

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = lista_empresas
            datosRespuesta['error'] = False
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


    @classmethod
    def alta_empresa(cls, arg_current_app, arg_empresa):
        try:
            datosRespuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(arg_current_app)

            lista_empresas = cls.lista_empresa(arg_current_app)[1]['datos']
            for empresa in lista_empresas:
                if arg_empresa.cve_empresa == empresa['clave_empresa']:
                    datosRespuesta['error'] = True
                    datosRespuesta['mensaje'] = 'Alta no exitosa, ya existe esa empresa'
                    ErrorSistema = False
                   
                    if db.conexion:
                        db.close()
                    
                    return (False, datosRespuesta, ErrorSistema)

            query = f'''INSERT INTO empresas 
                            (nombre_empresa, clave_empresa, observaciones, uso_webhook, vigente, fecha_alta)
                        VALUES
                            (%s, %s, %s, %s, %s, %s);
                    '''
        
            datos = (arg_empresa.nombre, arg_empresa.cve_empresa, arg_empresa.observaciones, arg_empresa.uso_webhook, arg_empresa.vigente, arg_empresa.fecha_alta)
            db.execute(query, (datos))
            db.commit()
            if db.conexion:
                db.close()

            datosRespuesta['error'] = False
            datosRespuesta['mensaje'] = 'Alta realizada exitosamente'
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


    @classmethod
    def consulta_empresa(cls, arg_current_app, argIdEmpresa):
        try:
            datosRespuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(arg_current_app)

            query = f'''SELECT * FROM empresas WHERE id = {argIdEmpresa} ;'''

            db.execute(query)
            respuesta = db.fetchall()
            if db.conexion:
                db.close()

            #Valida si datosResultado esta vacio
            if (len(respuesta) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            lista_empresas = []
            lista_valores = ['id', 'nombre_empresa', 'clave_empresa', 'observaciones', 'uso_webhook', 'valido', 'fecha_alta']
            for empresa in respuesta:
                valores_empresa = {}
                for i in range(0, len(lista_valores)):
                    valores_empresa[lista_valores[i]] = empresa[i]
                lista_empresas.append(valores_empresa)

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = lista_empresas
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


    @classmethod
    def baja_empresa(cls, arg_current_app, argIdEmpresa):
        try:
            datosRespuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
             
            # Conexion a la BBDD (Postgres)
            db = PostgresBase(arg_current_app)

            query = f'''UPDATE empresas
                        SET vigente = False
                        WHERE id = {argIdEmpresa};
                    '''
            
            db.execute(query)
            db.commit()

            if db.conexion:
                db.close()

            datosRespuesta['error'] = False
            datosRespuesta['mensaje'] = f'Empresa con id {argIdEmpresa} ha sido dada de baja exitosamente'

            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)
        except Exception as ex:
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

