-- ============================================================
-- SCRIPT SQL - EPS CITAS MÉDICAS
-- Compatible con MySQL Workbench
-- Ejecutar este script completo para configurar la base de datos
-- ============================================================

-- Crear y seleccionar base de datos
CREATE DATABASE IF NOT EXISTS eps_citas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE eps_citas;

-- ============================================================
-- TABLA: pacientes
-- ============================================================
CREATE TABLE IF NOT EXISTS pacientes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    documento   VARCHAR(15) UNIQUE NOT NULL,
    nombre      VARCHAR(80) NOT NULL,
    apellido    VARCHAR(80) NOT NULL,
    telefono    VARCHAR(20),
    correo      VARCHAR(100),
    eps         VARCHAR(100)
);

-- ============================================================
-- TABLA: citas
-- ============================================================
CREATE TABLE IF NOT EXISTS citas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    documento       VARCHAR(15) NOT NULL,
    medico          VARCHAR(100) NOT NULL,
    tipo_cita       VARCHAR(50) NOT NULL,
    fecha           DATE NOT NULL,
    hora            TIME NOT NULL,
    direccion_eps   VARCHAR(150),
    FOREIGN KEY (documento) REFERENCES pacientes(documento)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ============================================================
-- DATOS DE PRUEBA (OPCIONALES)
-- ============================================================
INSERT IGNORE INTO pacientes (documento, nombre, apellido, telefono, correo, eps)
VALUES
    ('1001234567', 'Carlos',  'Rodríguez', '3001234567', 'carlos@email.com', 'Sanitas'),
    ('1009876543', 'María',   'López',     '3109876543', 'maria@email.com',  'Compensar'),
    ('1005551234', 'Andrés',  'García',    '3205551234', 'andres@email.com', 'Famisanar');

INSERT IGNORE INTO citas (documento, medico, tipo_cita, fecha, hora, direccion_eps)
VALUES
    ('1001234567', 'Dr. Juan Pérez',    'General',     '2025-07-15', '09:00:00', 'Cra 7 # 32-16, Bogotá'),
    ('1009876543', 'Dra. Ana Martínez', 'Especialista','2025-07-18', '14:30:00', 'Av. El Dorado # 68B-85'),
    ('1005551234', 'Dr. Luis Torres',   'Odontología', '2025-07-20', '11:00:00', 'Cll 72 # 10-07, Bogotá');

-- ============================================================
-- CONSULTA PRINCIPAL (JOIN) - usada en la app Flask
-- ============================================================
-- SELECT
--     pacientes.nombre,
--     pacientes.apellido,
--     citas.medico,
--     citas.tipo_cita,
--     citas.fecha,
--     citas.hora,
--     citas.direccion_eps
-- FROM pacientes
-- INNER JOIN citas ON pacientes.documento = citas.documento
-- WHERE pacientes.documento = '1001234567';

SELECT 'Base de datos eps_citas configurada correctamente ✓' AS mensaje;
