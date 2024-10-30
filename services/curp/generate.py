from models.curp import CURPGenerator
from datetime import datetime

def generar_curp(nombre, primer_apellido, segundo_apellido, fecha_nacimiento, sexo, entidad):
    """
    Función de servicio para generar una CURP.
    
    :param nombre: Nombre del usuario
    :param primer_apellido: Primer apellido del usuario
    :param segundo_apellido: Segundo apellido del usuario
    :param fecha_nacimiento: Fecha de nacimiento en formato 'YYYY-MM-DD'
    :param sexo: Sexo del usuario ('H' o 'M')
    :param entidad: Entidad federativa de nacimiento
    :return: CURP generada
    """
    try:
        # Convertir la fecha de nacimiento a formato 'DD/MM/YYYY' para CURPGenerator
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime('%d/%m/%Y')
        
        
        curp_gen = CURPGenerator(nombre, primer_apellido, segundo_apellido, fecha_nacimiento, sexo, entidad)
        return curp_gen.generar_curp()
    
    except ValueError as e:
        raise ValueError(f"Error al generar CURP: {str(e)}")
