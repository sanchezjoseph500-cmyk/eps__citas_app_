# EPS+ Citas Médicas — Guía de Instalación

## Tecnologías
Python · Flask · MySQL · HTML5 · CSS3 · Jinja2

---

## 1. Configurar la base de datos (MySQL Workbench)

1. Abrir **MySQL Workbench**.
2. Conectarse al servidor local (`localhost`, usuario `root`).
3. Ir a **File → Open SQL Script** y abrir `eps_citas_workbench.sql`.
4. Ejecutar con **Ctrl+Shift+Enter** (o el rayo ⚡).
5. Verificar que aparezca el mensaje: *Base de datos eps_citas configurada correctamente ✓*

---

## 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

---

## 3. Ajustar credenciales (si es necesario)

Editar `config.py`:
```python
MYSQL_HOST     = "localhost"
MYSQL_USER     = "root"
MYSQL_PASSWORD = ""          # ← tu contraseña de MySQL
MYSQL_DB       = "eps_citas"
```

---

## 4. Ejecutar la aplicación

```bash
python app.py
```

Abrir el navegador en: **http://127.0.0.1:5000**

---

## Estructura del proyecto

```
eps_citas_app/
├── app.py                    # Rutas principales (Flask)
├── config.py                 # Configuración BD
├── database.py               # Conexión MySQL
├── requirements.txt
├── eps_citas_workbench.sql   # Script SQL para MySQL Workbench
├── models/
│   ├── pacientes.py
│   └── citas.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── registro_paciente.html
│   ├── reservar_cita.html
│   ├── consulta_cita.html
│   ├── resultado_cita.html
│   └── actualizar_cita.html
└── static/
    └── css/
        └── style.css
```

---

## Funcionalidades CRUD

| Función            | Ruta                    | Método   |
|--------------------|-------------------------|----------|
| Inicio             | `/`                     | GET      |
| Registrar paciente | `/registro_paciente`    | GET/POST |
| Reservar cita      | `/reservar_cita`        | GET/POST |
| Consultar cita     | `/consulta_cita`        | GET      |
| Resultado cita     | `/resultado_cita`       | POST     |
| Actualizar cita    | `/actualizar_cita/<id>` | GET/POST |
