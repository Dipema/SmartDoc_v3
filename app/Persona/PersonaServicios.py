from app.BBDD.BaseDatosModelo import PostgresBase

class PersonaSvos():
    @classmethod
    def alta_persona(cls, arg_current_app, arg_persona):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            db = PostgresBase(arg_current_app)

            # Verifica que la persona no este registrada
            lista_personas = cls.lista_persona(arg_current_app)[1]['datos']
            if lista_personas != {}:
                for persona in lista_personas:
                    if arg_persona.identificador == persona['identificador']:
                        datos_respuesta['error'] = True
                        datos_respuesta['mensaje'] = 'Alta no exitosa, ya existe esa persona'
                        error_sistema = False
                    
                        if db.conexion:
                            db.close()
                        
                        return (False, datos_respuesta, error_sistema)

            query = f'''INSERT INTO personas 
                            (identificador, tipo_identificador, nombre, vigente, fecha_alta)
                        VALUES
                            (%s, %s, %s, %s, %s);
                    '''
            
            datos = (arg_persona.identificador, arg_persona.tipo_identificador, arg_persona.nombre, arg_persona.vigente, arg_persona.fecha_alta)
            db.execute(query, (datos))
            db.commit()
            if db.conexion:
                db.close()

            datos_respuesta['error'] = False
            datos_respuesta['mensaje'] = 'Alta realizada exitosamente'
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            print('PesonaServicios.alta_persona: ', ex)
            return (True, msg_error, error_sistema)
        

    @classmethod
    def baja_persona(cls, arg_current_app, arg_id_persona):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            # Verifica que la persona no este registrada
            lista_personas = cls.lista_persona(arg_current_app)[1]['datos']
            if lista_personas == {}:
                datos_respuesta['error'] = True
                datos_respuesta['mensaje'] = 'Baja no exitosa, no existe persona con ese ID'
                error_sistema = False
                return (False, datos_respuesta, error_sistema)
            
            for persona in lista_personas:
                if arg_id_persona == str(persona['id']):
                    db = PostgresBase(arg_current_app)

                    query = f'''UPDATE personas
                                SET vigente = False
                                WHERE id = {arg_id_persona};
                            '''
                    
                    db.execute(query)
                    db.commit()

                    if db.conexion:
                        db.close()

                    datos_respuesta['error'] = False
                    datos_respuesta['mensaje'] = f'Persona con id {arg_id_persona} ha sido dada de baja exitosamente'
                    error_sistema = False
                    return (False, datos_respuesta, error_sistema)
                
            datos_respuesta['error'] = True
            datos_respuesta['mensaje'] = 'Baja no exitosa, no existe persona con ese ID'
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            return (True, msg_error, error_sistema)


    @classmethod
    def lista_persona(cls, arg_current_app):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            db = PostgresBase(arg_current_app)

            query = f'''SELECT * FROM personas;'''
            
            db.execute(query)
            respuesta = db.fetchall()
            if db.conexion:
                db.close()

            # Valida si no se encontro nigun resultado
            if len(respuesta) <= 0:
                datos_respuesta['mensaje'] = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                datos_respuesta['datos'] = {}
                ErrorSistema = False
                return (True, datos_respuesta, ErrorSistema)
            
            lista_personas = []
            lista_valores = ['id', 'identificador', 'tipo_identidicador', 'nombre', 'valido', 'fecha_alta']
            for persona in respuesta:
                valores_persona = {}
                for i in range(0, len(lista_valores)):
                    valores_persona[lista_valores[i]] = persona[i]
                lista_personas.append(valores_persona)

            datos_respuesta['error'] = False
            datos_respuesta['mensaje'] = 'Consulta realizada exitosamente'
            datos_respuesta['datos'] = lista_personas
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            return (True, msg_error, error_sistema)
        

    @classmethod
    def consulta_persona(cls, arg_current_app, arg_id_persona):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(arg_current_app)

            query = f'''SELECT * FROM personas WHERE id = {arg_id_persona} ;'''

            db.execute(query)
            respuesta = db.fetchall()
            if db.conexion:
                db.close()

            #Valida si datosResultado esta vacio
            if (len(respuesta) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            lista_personas = []
            lista_valores = ['id', 'identidicador', 'tipo_identidicador', 'nombre', 'id_empresa', 'valido', 'fecha_alta']
            for persona in respuesta:
                valores_persona = {}
                for i in range(0, len(lista_valores)):
                    valores_persona[lista_valores[i]] = persona[i]
                lista_personas.append(valores_persona)

            mensaje = 'Consulta realizada exitosamente'
            datos_respuesta['mensaje'] = mensaje
            datos_respuesta['datos'] = lista_personas
            datos_respuesta['error'] = False
            ErrorSistema = False

            return (False, datos_respuesta, ErrorSistema)

        except Exception as ex:
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)
        
