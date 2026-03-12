from database import get_connection

def reservar_cita(documento, medico, tipo_cita, fecha, hora, direccion_eps):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO citas (documento, medico, tipo_cita, fecha, hora, direccion_eps)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (documento, medico, tipo_cita, fecha, hora, direccion_eps))
    conn.commit()
    cursor.close()
    conn.close()

def consultar_cita(documento):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT
            pacientes.nombre,
            pacientes.apellido,
            citas.id,
            citas.medico,
            citas.tipo_cita,
            citas.fecha,
            citas.hora,
            citas.direccion_eps
        FROM pacientes
        INNER JOIN citas ON pacientes.documento = citas.documento
        WHERE pacientes.documento = %s
    """
    cursor.execute(sql, (documento,))
    citas = cursor.fetchall()
    cursor.close()
    conn.close()
    return citas

def actualizar_cita(cita_id, medico, tipo_cita, fecha, hora):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE citas
             SET medico = %s, tipo_cita = %s, fecha = %s, hora = %s
             WHERE id = %s"""
    cursor.execute(sql, (medico, tipo_cita, fecha, hora, cita_id))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_cita_por_id(cita_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM citas WHERE id = %s", (cita_id,))
    cita = cursor.fetchone()
    cursor.close()
    conn.close()
    return cita
