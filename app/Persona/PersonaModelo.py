#*******************************************************************************************
#   PERSONA   
#   Definimos la clase Persona con la informacion del modelo
#*******************************************************************************************

class Persona():

    # Definimos los campos que tiene el modelo Persona
    def __init__(self, identificador, tipo_identificador, nombre, vigente, fecha_alta) -> None:
        self.identificador = identificador
        self.tipo_identificador = tipo_identificador
        self.nombre = nombre
        self.vigente = vigente
        self.fecha_alta = fecha_alta

    
    def to_str(self) -> str:
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Persona')
        print('-' * 40)
        print('         identificador: ', self.identificador)
        print('    tipo_identificador: ', self.tipo_identificador)
        print('                nombre: ', self.nombre)
        print('            id_empresa: ', self.id_empresa)
        print('               vigente: ', self.vigente)
        print('            fecha_alta: ', self.fecha_alta)
        print('=' * 40)
        print('\n') 
        

    def to_json(self):
        return {
            'identificador': self.identificador,
            'nombre': self.nombre,
            'tipo_identificador': self.tipo_identificador,
            'id_empresa': self.id_empresa,
            'vigente': self.vigente,
            'fecha_alta': self.fechaAlta, 
        }