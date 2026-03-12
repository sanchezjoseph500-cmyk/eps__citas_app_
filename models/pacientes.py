from database import get_connection

def registrar_paciente(documento, nombre, apellido, telefono, correo, eps):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO pacientes (documento, nombre, apellido, telefono, correo, eps)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (documento, nombre, apellido, telefono, correo, eps))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_paciente(documento):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pacientes WHERE documento = %s", (documento,))
    paciente = cursor.fetchone()
    cursor.close()
    conn.close()
    return paciente
