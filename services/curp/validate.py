# services/curp_validation.py
from models.turingMachine import TuringMachineCURP
def validar_curp(curp):
    """Valida la CURP usando la máquina de Turing."""
    try:
        machine = TuringMachineCURP(curp)
        return machine.validate()  
    except ValueError as e:
        return str(e)  
