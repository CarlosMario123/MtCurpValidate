from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.curp.generate import generar_curp
from services.curp.validate import validar_curp

#blueprint
curp_bp = Blueprint('curp', __name__, template_folder='templates')


@curp_bp.route('/')
def consulta_curp():
    return render_template('curp.html')

@curp_bp.route('/generar', methods=['POST'])
def generar_curp_view():
    # Obtener los datos del formulario
    nombre = request.form.get('nombre')
    primer_apellido = request.form.get('primer_apellido')
    segundo_apellido = request.form.get('segundo_apellido')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    sexo = request.form.get('sexo')
    entidad = request.form.get('entidad')

    try:
        
        curp = generar_curp(nombre, primer_apellido, segundo_apellido, fecha_nacimiento, sexo, entidad)

        flash(f'Tu CURP es: {curp}', 'success')
    except ValueError as e:
        flash(str(e), 'error')

    
    return redirect(url_for('curp.consulta_curp'))

@curp_bp.route('/validar', methods=['GET', 'POST'])
def validar_curp_view():
    if request.method == 'POST':
        curp = request.form.get('curp')

        print("CURP recibida:", curp) 
        
      
        if curp:
            resultado = validar_curp(curp)
            if resultado is True:
                flash("La CURP es válida.", "success")
            elif resultado is False:
                flash("La CURP es inválida.", "error")
            else:
                flash(resultado, "error")  # Mensaje de error específico
        else:
            flash("Por favor, ingresa una CURP para validar.", "error")
        
        return redirect(url_for('curp.validar_curp_view'))

    return render_template('validar_curp.html')