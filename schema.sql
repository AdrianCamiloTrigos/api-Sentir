-- ============================================================
--  API SENTIR - Esquema de base de datos (PostgreSQL)
--  Ejecútalo en pgAdmin / psql SOLO si aún no tienes estas tablas.
--  Si ya las tienes, revisa que tengan estas columnas.
-- ============================================================

CREATE TABLE IF NOT EXISTS personas (
    id_persona   SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    telefono     VARCHAR(20),
    tipo_persona VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS emergencias (
    id_emergencia SERIAL PRIMARY KEY,
    tipo          VARCHAR(50)  NOT NULL,
    descripcion   TEXT,
    fecha         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado        VARCHAR(30)  NOT NULL DEFAULT 'REPORTADA',
    id_persona    INTEGER      NOT NULL REFERENCES personas(id_persona)
);

CREATE TABLE IF NOT EXISTS ubicaciones (
    id_ubicacion  SERIAL PRIMARY KEY,
    latitud       NUMERIC(10,7) NOT NULL,
    longitud      NUMERIC(10,7) NOT NULL,
    direccion     VARCHAR(200),
    id_emergencia INTEGER       NOT NULL REFERENCES emergencias(id_emergencia)
);

-- ------------------------------------------------------------
--  Datos de ejemplo (opcional, para probar con Thunder Client)
-- ------------------------------------------------------------
INSERT INTO personas (nombre, telefono, tipo_persona) VALUES
    ('Laura Gómez',  '3001234567', 'CIUDADANO'),
    ('Carlos Pérez', '3109876543', 'VOLUNTARIO');
