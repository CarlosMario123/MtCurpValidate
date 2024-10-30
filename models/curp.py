import random
import string
from datetime import datetime

class CURPGenerator:
    def __init__(self, nombre, primer_apellido, segundo_apellido, fecha_nacimiento, sexo, entidad):
        # Validar y limpiar los datos de entrada
        self.nombre = self.limpiar_texto(nombre)
        self.primer_apellido = self.limpiar_texto(primer_apellido)
        self.segundo_apellido = self.limpiar_texto(segundo_apellido)
        self.fecha_nacimiento = self.validar_fecha(fecha_nacimiento)
        self.sexo = self.validar_sexo(sexo)
        self.entidad = self.validar_entidad(entidad)
        
        # Inicializar la CURP como una lista de caracteres
        self.curp = [''] * 18  # Cambiar '_' por '' para evitar caracteres de relleno no deseados
    
    def limpiar_texto(self, texto):
        """ Elimina caracteres no deseados y convierte el texto a mayúsculas. """
        texto_limpio = ''.join(e for e in texto.upper() if e in string.ascii_uppercase + 'Ñ ')
        return texto_limpio.strip()
    
    def obtener_vocal_interna(self, apellido):
        """ Obtiene la primera vocal interna del apellido. """
        vocales = 'AEIOU'
        for letra in apellido[1:]:
            if letra in vocales:
                return letra
        return 'X'  # Si no encuentra vocal interna
    
    def validar_fecha(self, fecha):
        """ Valida y convierte la fecha de nacimiento a objeto datetime en formato 'DD/MM/YYYY'. """
        try:
            return datetime.strptime(fecha, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Fecha de nacimiento inválida. Formato esperado 'DD/MM/YYYY'.")
    
    def validar_sexo(self, sexo):
        """ Valida el sexo. Espera 'H' o 'M'. """
        sexo = sexo.upper()
        if sexo not in ['H', 'M']:
            raise ValueError("Sexo inválido. Debe ser 'H' para hombre o 'M' para mujer.")
        return sexo
    
    def validar_entidad(self, entidad):
        """ Valida la entidad de nacimiento. """
        entidad = entidad.upper()
        codigos_entidades = {
            'AS', 'BC', 'BS', 'CC', 'CL', 'CM', 'CS', 'CH', 'DF', 'DG',
            'GT', 'HG', 'JC', 'MC', 'MN', 'MS', 'NT', 'NL', 'OC', 'PL',
            'QT', 'QR', 'SP', 'SL', 'SR', 'TC', 'TS', 'TL', 'VZ', 'YN',
            'ZS', 'NE'  # NE para nacimiento en el extranjero
        }
        if entidad not in codigos_entidades:
            raise ValueError(f"Entidad inválida. Debe ser uno de los siguientes códigos: {', '.join(codigos_entidades)}.")
        return entidad
    
    def evitar_palabras_ofensivas(self):
        """ funcion para palabras ofensiva """
        palabras_ofensivas = {
            'BACA', 'BAKA', 'BUEI', 'BUEY', 'CACA', 'CACO', 'CAGA', 'CAGO',
            'CAKA', 'CAKO', 'COGE', 'COGI', 'COJA', 'COJE', 'COJI', 'COJO',
            'CULO', 'FETO', 'GUEI', 'GUEY', 'JOTO', 'KACA', 'KACO', 'KAGA',
            'KAGO', 'KOJO', 'KULO', 'MAME', 'MAMO', 'MEAR', 'MEAS', 'MEON',
            'MION', 'MOCO', 'MULA', 'PEDA', 'PEDO', 'PENE', 'PUTA', 'PUTO',
            'QULO', 'RATA', 'ROBA', 'ROBE', 'ROBO', 'RUIN'
        }
        iniciales = ''.join(self.curp[0:4])
        if iniciales in palabras_ofensivas:
            # Reemplazar la segunda inicial (vocal interna) con 'X'
            self.curp[1] = 'X'
    
    def generar_homoclave(self):
        """ Genera la homoclave completa de 2 caracteres alfanuméricos. """
        caracteres = string.ascii_uppercase + string.digits
        return random.choice(caracteres) + random.choice(caracteres)
    
    def calcular_digito_verificador(self):
        """ Calcula el dígito verificador de la CURP completa. """
        valores = {char: idx for idx, char in enumerate("0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")}
        suma = sum(valores.get(c, 0) * (18 - idx) for idx, c in enumerate(self.curp[:17]))
        digito_verificador = (10 - (suma % 10)) % 10
        return str(digito_verificador)
    
    def generar_curp(self):
        """ Genera la CURP completa siguiendo las reglas establecidas. """
        # Generar las iniciales
        self.curp[0] = self.primer_apellido[0]
        self.curp[1] = self.obtener_vocal_interna(self.primer_apellido)
        self.curp[2] = self.segundo_apellido[0] if self.segundo_apellido else 'X'
        self.curp[3] = self.nombre[0]
        
        # Evitar palabras ofensivas
        self.evitar_palabras_ofensivas()
        
        # Generar la fecha de nacimiento en formato AAMMDD
        fecha = self.fecha_nacimiento
        año = fecha.strftime('%y')
        mes = fecha.strftime('%m')
        dia = fecha.strftime('%d')
        self.curp[4:10] = list(año + mes + dia)
        
        # Asignar el sexo
        self.curp[10] = self.sexo
        
       
        self.curp[11:13] = list(self.entidad)
        
        # Generar la homoclave
        homoclave = self.generar_homoclave()
        self.curp[13:15] = list(homoclave)
        
       
        self.curp[16] = self.calcular_digito_verificador()
        
        return ''.join(self.curp)
    
    def mostrar_curp(self):
        """ Retorna la CURP generada como una cadena de texto. """
        return ''.join(self.curp)
