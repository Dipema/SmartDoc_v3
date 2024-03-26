#*******************************************************************************************
#   EMPRESA   
#   Definimos la clase Empresa con la informacion del modelo
#*******************************************************************************************

class Empresa():

    # Definimos los campos que tiene el modelo Empresa
    def __init__(self, cve_empresa, nombre, observaciones, uso_webhook, vigente, fecha_alta) -> None:
        self.cve_empresa = cve_empresa
        self.nombre = nombre
        self.observaciones = observaciones
        self.uso_webhook = uso_webhook
        self.vigente = vigente
        self.fecha_alta = fecha_alta

    # Metodo para imprimir los valores de la Clase
    def to_str(self) -> str:
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Empresa')
        print('-' * 40)
        print('                id: ', self.id)
        print('      cve_empresa: ', self.cve_empresa)
        print('           nombre: ', self.nombre)
        print('    observaciones: ', self.observaciones)
        print('       usoWebhook: ', self.uso_webhook)
        print('     usuario_alta: ', self.UsuarioAlta)
        print('       fecha_alta: ', self.fecha_alta)
        print('=' * 40)
        print('\n')

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'cve_empresa': self.cveEmpresa,
            'nombre': self.nombre,
            'observaciones': self.observaciones,
            'uso_webhook': self.usoWebhook,
            'vigente': self.vigente,
            'fecha_alta': self.fechaAlta, 
        }
    
