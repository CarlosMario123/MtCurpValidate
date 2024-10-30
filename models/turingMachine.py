class TuringMachineCURP:
    def __init__(self, curp):
        
        if len(curp) != 18:
            raise ValueError("La CURP debe tener exactamente 18 caracteres.")
        
        # CURP en cinta extendida con espacios en blanco
        self.cinta = list(curp) + [' '] * 50  
        self.head_position = 0  # Posición inicial del cabezal
        self.state = 'q0'       # Estado inicial
        self.is_bisiesto = False  # Indicador para años bisiestos
    
    def read_symbols(self, count=1):
        """Lee 'count' símbolos desde la posición actual del cabezal."""
        symbols = self.cinta[self.head_position:self.head_position+count]
        return ''.join(symbols)
    
    def write_symbols(self, symbols):
        """Escribe una cadena de símbolos en la posición actual del cabezal."""
        for symbol in symbols:
            if self.head_position < len(self.cinta):
                self.cinta[self.head_position] = symbol
                self.head_position += 1
            else:
                # Expande la cinta si es necesario
                self.cinta.append(symbol)
                self.head_position += 1
    
    def move_right(self, steps=1):
        """Mueve el cabezal a la derecha."""
        self.head_position += steps
    
    def move_left(self, steps=1):
        """Mueve el cabezal a la izquierda."""
        self.head_position = max(0, self.head_position - steps)
    
    def transition(self):
        """Define las transiciones para validar la CURP."""
        if self.state == 'q0':
            # Estado inicial para validar las primeras 4 letras
            if self.head_position < 4:
                symbol = self.read_symbols()
                if not symbol.isalpha():
                    self.state = 'q_reject'
                else:
                    self.move_right()
            else:
                self.state = 'q_year'
        
        elif self.state == 'q_year':
            # Estado para verificar el año de nacimiento
            year_str = self.read_symbols(2)
            if not year_str.isdigit():
                self.state = 'q_reject'
                return
            year_digits = int(year_str)
            
            # Determinar el siglo basado en los dígitos del año
            # Asumiendo que YY <= 24 pertenece al siglo 2000, de lo contrario al 1900
            current_year_suffix = 24  # Ajusta este valor según el año actual si es necesario
            if year_digits <= current_year_suffix:
                full_year = 2000 + year_digits
            else:
                full_year = 1900 + year_digits
            
            # Verificar si el año es bisiesto
            if (full_year % 4 == 0):
                self.is_bisiesto = True
                if (full_year % 100 == 0) and (full_year % 400 != 0):
                    self.is_bisiesto = False
            else:
                self.is_bisiesto = False
            
            # Mover el cabezal dos posiciones a la derecha
            self.move_right(2)
            self.state = 'q_month'
        
        elif self.state == 'q_month':
            # Estado para validar el mes
            month_str = self.read_symbols(2)
            if not month_str.isdigit():
                self.state = 'q_reject'
                return
            month = int(month_str)
            
            if not (1 <= month <= 12):
                self.state = 'q_reject'
            elif month == 2:
                self.state = 'q_day_feb'
            elif month in [4, 6, 9, 11]:
                self.state = 'q_day_30'
            else:
                self.state = 'q_day_31'
            
            # Mover el cabezal dos posiciones a la derecha
            self.move_right(2)
        
        elif self.state == 'q_day_feb':
            # Estado para validar el día en febrero
            day_str = self.read_symbols(2)
            if not day_str.isdigit():
                self.state = 'q_reject'
                return
            day = int(day_str)
            
            if self.is_bisiesto:
                if 1 <= day <= 29:
                    self.state = 'q_sexo'
                else:
                    self.state = 'q_reject'
            else:
                if 1 <= day <= 28:
                    self.state = 'q_sexo'
                else:
                    self.state = 'q_reject'
            
            # Mover el cabezal dos posiciones a la derecha
            self.move_right(2)
        
        elif self.state == 'q_day_31':
            # Estado para validar el día en meses con 31 días
            day_str = self.read_symbols(2)
            if not day_str.isdigit():
                self.state = 'q_reject'
                return
            day = int(day_str)
            
            if 1 <= day <= 31:
                self.state = 'q_sexo'
            else:
                self.state = 'q_reject'
            
            # Mover el cabezal dos posiciones a la derecha
            self.move_right(2)
        
        elif self.state == 'q_day_30':
            # Estado para validar el día en meses con 30 días
            day_str = self.read_symbols(2)
            if not day_str.isdigit():
                self.state = 'q_reject'
                return
            day = int(day_str)
            
            if 1 <= day <= 30:
                self.state = 'q_sexo'
            else:
                self.state = 'q_reject'
            
            # Mover el cabezal dos posiciones a la derecha
            self.move_right(2)
        
        elif self.state == 'q_sexo':
            # Estado para validar el sexo (H o M)
            sexo = self.read_symbols()
            if sexo not in ['H', 'M']:
                self.state = 'q_reject'
            else:
                self.move_right()
                self.state = 'q_entidad'
        
        elif self.state == 'q_entidad':
            # Estado para validar la entidad federativa (2 letras)
            entidad = self.read_symbols(2).upper()
            entidades_validas = [
                'AS', 'BC', 'BS', 'CC', 'CL', 'CM', 'CS', 'CH', 'DF', 'DG',
                'GT', 'GR', 'HG', 'JC', 'MC', 'MN', 'MS', 'NT', 'NL', 'OC',
                'PL', 'QT', 'QR', 'SP', 'SL', 'SR', 'TC', 'TS', 'TL', 'VZ',
                'YN', 'ZS', 'NE'  # NE para nacimiento en el extranjero
            ]
            if entidad not in entidades_validas:
                self.state = 'q_reject'
            else:
                self.move_right(2)
                self.state = 'q_consonantes'
        
        elif self.state == 'q_consonantes':
            # Estado para validar las consonantes internas 3 caracteres
            consonantes = self.read_symbols(3).upper()
            if not consonantes.isalpha():
                self.state = 'q_reject'
            else:
                self.move_right(3)
                self.state = 'q_homoclave'
        
        elif self.state == 'q_homoclave':
            # Estado para validar la homoclave (1 carácter alfanumérico)
            homoclave = self.read_symbols()
            if not homoclave.isalnum():
                self.state = 'q_reject'
            else:
                self.move_right()
                self.state = 'q_digito_verificador'
        
        elif self.state == 'q_digito_verificador':
            # Estado para validar el digito verificador (1 dígito)
            digito = self.read_symbols()
            if not digito.isdigit():
                self.state = 'q_reject'
            else:
                self.state = 'q_accept'
        
        # Estados de Aceptación y Rechazo
        elif self.state == 'q_accept':
            pass  # Máquina se detiene en estado de aceptación
        
        elif self.state == 'q_reject':
            pass  # Máquina se detiene en estado de rechazo
    
    def validate(self):
        """Ejecuta las transiciones de la máquina para validar la CURP."""
        while self.state not in ['q_accept', 'q_reject']:
            self.transition()
        
        return self.state == 'q_accept'

# Ejemplo de uso

"""
Ejemplo de uso de la clase TuringMachineCURP 

machine = TuringMachineCURP(curp) Ingresamos una cadena curp

machine.validate() --> validda retorna false O true dependiendo del resultado
"""

