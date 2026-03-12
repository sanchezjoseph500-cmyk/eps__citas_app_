from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from database import get_connection
from models.pacientes import registrar_paciente, obtener_paciente
from models.citas import reservar_cita, consultar_cita, actualizar_cita, obtener_cita_por_id
import psycopg2

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# ─────────────────────────────────────────
# CREAR TABLAS AUTOMÁTICAMENTE AL INICIAR
# ─────────────────────────────────────────
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id        SERIAL PRIMARY KEY,
            documento VARCHAR(15) UNIQUE NOT NULL,
            nombre    VARCHAR(80) NOT NULL,
            apellido  VARCHAR(80) NOT NULL,
            telefono  VARCHAR(20),
            correo    VARCHAR(100),
            eps       VARCHAR(100)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id            SERIAL PRIMARY KEY,
            documento     VARCHAR(15) NOT NULL,
            medico        VARCHAR(100) NOT NULL,
            tipo_cita     VARCHAR(50) NOT NULL,
            fecha         DATE NOT NULL,
            hora          TIME NOT NULL,
            direccion_eps VARCHAR(150),
            FOREIGN KEY (documento) REFERENCES pacientes(documento)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

with app.app_context():
    init_db()

# ─────────────────────────────────────────
# INICIO
# ─────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ─────────────────────────────────────────
# REGISTRO DE PACIENTE
# ─────────────────────────────────────────
@app.route('/registro_paciente', methods=['GET', 'POST'])
def registro_paciente():
    if request.method == 'POST':
        documento = request.form['documento'].strip()
        nombre    = request.form['nombre'].strip()
        apellido  = request.form['apellido'].strip()
        telefono  = request.form['telefono'].strip()
        correo    = request.form['correo'].strip()
        eps       = request.form['eps'].strip()

        if not all([documento, nombre, apellido]):
            flash('Los campos Documento, Nombre y Apellido son obligatorios.', 'error')
            return render_template('registro_paciente.html')

        try:
            registrar_paciente(documento, nombre, apellido, telefono, correo, eps)
            flash(f'Paciente {nombre} {apellido} registrado correctamente.', 'success')
            return redirect(url_for('index'))
        except psycopg2.errors.UniqueViolation:
            flash('Ya existe un paciente con ese número de documento.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('registro_paciente.html')

# ─────────────────────────────────────────
# RESERVAR CITA
# ─────────────────────────────────────────
@app.route('/reservar_cita', methods=['GET', 'POST'])
def reservar_cita_view():
    if request.method == 'POST':
        documento     = request.form['documento'].strip()
        medico        = request.form['medico'].strip()
        tipo_cita     = request.form['tipo_cita']
        fecha         = request.form['fecha']
        hora          = request.form['hora']
        direccion_eps = request.form['direccion_eps'].strip()

        if not all([documento, medico, tipo_cita, fecha, hora]):
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('reservar_cita.html')

        paciente = obtener_paciente(documento)
        if not paciente:
            flash('No existe un paciente con ese documento. Regístrelo primero.', 'error')
            return render_template('reservar_cita.html')

        try:
            reservar_cita(documento, medico, tipo_cita, fecha, hora, direccion_eps)
            flash('Cita médica reservada correctamente.', 'success')
            return redirect(url_for('consulta_cita'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('reservar_cita.html')

# ─────────────────────────────────────────
# CONSULTAR CITA
# ─────────────────────────────────────────
@app.route('/consulta_cita', methods=['GET', 'POST'])
def consulta_cita():
    return render_template('consulta_cita.html')

@app.route('/resultado_cita', methods=['POST'])
def resultado_cita():
    documento = request.form.get('documento', '').strip()
    if not documento:
        flash('Ingrese un número de documento.', 'error')
        return redirect(url_for('consulta_cita'))

    citas = consultar_cita(documento)
    if not citas:
        flash('No se encontraron citas para ese documento.', 'error')
        return redirect(url_for('consulta_cita'))

    return render_template('resultado_cita.html', citas=citas)

# ─────────────────────────────────────────
# ACTUALIZAR CITA
# ─────────────────────────────────────────
@app.route('/actualizar_cita/<int:cita_id>', methods=['GET', 'POST'])
def actualizar_cita_view(cita_id):
    cita = obtener_cita_por_id(cita_id)
    if not cita:
        flash('Cita no encontrada.', 'error')
        return redirect(url_for('consulta_cita'))

    if request.method == 'POST':
        medico    = request.form['medico'].strip()
        tipo_cita = request.form['tipo_cita']
        fecha     = request.form['fecha']
        hora      = request.form['hora']

        try:
            actualizar_cita(cita_id, medico, tipo_cita, fecha, hora)
            flash('Cita actualizada correctamente.', 'success')
            return redirect(url_for('consulta_cita'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('actualizar_cita.html', cita=cita)

# ─────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=False)
