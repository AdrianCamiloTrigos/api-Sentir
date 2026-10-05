# 🚨 API SENTIR

API REST para el reporte y consulta de **emergencias**. Permite registrar quién reporta una emergencia (personas), qué ocurrió (emergencias) y dónde (ubicaciones), y consultar toda esa información integrada.

## 📋 Descripción

El sistema maneja tres recursos relacionados:

- **Personas**: quienes reportan o participan en una emergencia.
- **Emergencias**: eventos reportados (accidentes, incendios, etc.), cada uno asociado a una persona.
- **Ubicaciones**: lugar donde ocurre la emergencia, asociada a una emergencia.

Cada recurso tiene su CRUD completo, y además hay endpoints de integración que cruzan la información de las tres tablas.

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje |
| FastAPI | Framework de la API REST |
| Uvicorn | Servidor ASGI |
| PostgreSQL | Base de datos relacional |
| psycopg2 | Conexión a PostgreSQL y consultas SQL |
| python-dotenv | Variables de entorno |
| Thunder Client | Pruebas de los endpoints |
| Git / GitHub | Control de versiones |

## 📁 Estructura del proyecto

```
api-sentir/
├── main.py            # Endpoints de la API
├── con_db.py          # Conexión a PostgreSQL
├── schema.sql         # Creación de tablas y datos de ejemplo
├── sentir_db.sql      # Respaldo de la base de datos (formato Plain)
├── requirements.txt   # Dependencias
├── .env.example       # Plantilla de variables de entorno
├── .gitignore         # Excluye .env, venv/ y __pycache__/
└── README.md
```

## 🗄️ Modelo de datos

```
personas (id_persona PK, nombre, telefono, tipo_persona)
    │
    └──< emergencias (id_emergencia PK, tipo, descripcion, fecha, estado, id_persona FK)
              │
              └──< ubicaciones (id_ubicacion PK, latitud, longitud, direccion, id_emergencia FK)
```

- Una **persona** puede reportar muchas emergencias.
- Una **emergencia** puede tener ubicaciones asociadas.

## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/didierguerreros/api-sentir
cd api-sentir
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos
En PostgreSQL (pgAdmin o psql) crea una base de datos vacía llamada `sentir_db` y elige **una** de estas dos opciones:

**Opción A: solo las tablas (vacías)**
Abre el *Query Tool* sobre `sentir_db` y ejecuta el archivo `schema.sql`.

**Opción B: tablas con datos de prueba**
Restaura el respaldo `sentir_db.sql` incluido en el repositorio:

- En pgAdmin: clic derecho sobre `sentir_db` → *Query Tool* → abrir `sentir_db.sql` → ejecutar (▶).
- O desde la terminal:
  ```bash
  psql -U postgres -d sentir_db -f sentir_db.sql
  ```

### 5. Configurar variables de entorno
Copia `.env.example` como `.env` y completa tus datos:

```env
DB_HOST=localhost
DB_NAME=sentir_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_PORT=5432
```

> ⚠️ El archivo `.env` **nunca** se sube a GitHub.

### 6. Ejecutar la API
```bash
uvicorn main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`.
Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`

## 🔗 Endpoints

### Personas

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/personas` | Consultar todas las personas |
| POST | `/personas` | Registrar una persona |
| PUT | `/personas/{id}` | Actualizar una persona |
| DELETE | `/personas/{id}` | Eliminar una persona |

Body de ejemplo:
```json
{
  "nombre": "Laura Gómez",
  "telefono": "3001234567",
  "tipo_persona": "CIUDADANO"
}
```

### Emergencias

| Método | Endpoint | Descripción | Operación SQL |
|---|---|---|---|
| GET | `/emergencias` | Consultar todas las emergencias | SELECT |
| GET | `/emergencias/{id}` | Consultar una emergencia | SELECT + WHERE |
| POST | `/emergencias` | Registrar una emergencia | INSERT |
| PUT | `/emergencias/{id}` | Actualizar una emergencia | UPDATE + WHERE |
| DELETE | `/emergencias/{id}` | Eliminar una emergencia | DELETE + WHERE |

Body de ejemplo (POST y PUT):
```json
{
  "tipo": "ACCIDENTE",
  "descripcion": "Accidente cerca de la universidad",
  "estado": "REPORTADA",
  "id_persona": 1
}
```
> La `fecha` se asigna automáticamente al registrar la emergencia.

### Ubicaciones

| Método | Endpoint | Descripción | Operación SQL |
|---|---|---|---|
| GET | `/ubicaciones` | Consultar todas las ubicaciones | SELECT |
| GET | `/ubicaciones/{id}` | Consultar una ubicación | SELECT + WHERE |
| POST | `/ubicaciones` | Registrar una ubicación | INSERT |
| PUT | `/ubicaciones/{id}` | Actualizar una ubicación | UPDATE + WHERE |
| DELETE | `/ubicaciones/{id}` | Eliminar una ubicación | DELETE + WHERE |

Body de ejemplo (POST y PUT):
```json
{
  "latitud": 8.2501234,
  "longitud": -73.3556789,
  "direccion": "Calle 10 # 5-20",
  "id_emergencia": 1
}
```

### Integración

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/emergencias/{id}/ubicacion` | Ubicación asociada a una emergencia |
| GET | `/emergencias/{id}/detalle` | Emergencia + persona que la reportó + ubicación |

Respuesta de ejemplo de `GET /emergencias/1/detalle`:
```json
{
  "emergencia": {
    "id_emergencia": 1,
    "tipo": "ACCIDENTE",
    "descripcion": "Accidente cerca de la universidad",
    "fecha": "2026-10-05T20:59:59.264354",
    "estado": "REPORTADA"
  },
  "persona": {
    "id_persona": 1,
    "nombre": "Laura Gómez",
    "telefono": "3001234567",
    "tipo_persona": "CIUDADANO"
  },
  "ubicacion": {
    "id_ubicacion": 1,
    "latitud": 8.2501234,
    "longitud": -73.3556789,
    "direccion": "Calle 10 # 5-20"
  }
}
```
Si la emergencia aún no tiene ubicación, el campo `ubicacion` es `null`.

## 📡 Códigos de respuesta

| Código | Significado |
|---|---|
| 200 | Consulta, actualización o eliminación correcta |
| 201 | Registro creado correctamente |
| 400 | Clave foránea inválida (`id_persona` o `id_emergencia` no existe) |
| 404 | El identificador solicitado no existe |
| 409 | No se puede eliminar una emergencia que aún tiene ubicaciones asociadas |

## 🔑 Manejo de claves foráneas

- No se puede crear ni actualizar una **emergencia** con un `id_persona` que no exista.
- No se puede crear ni actualizar una **ubicación** con un `id_emergencia` que no exista.
- Para eliminar una **emergencia**, primero se deben eliminar sus ubicaciones.

## 🧪 Pruebas con Thunder Client

Orden recomendado para probar todo el flujo:

| # | Petición | Resultado esperado |
|---|---|---|
| 1 | `POST /emergencias` | 201 |
| 2 | `GET /emergencias` | 200, lista con la emergencia |
| 3 | `GET /emergencias/1` | 200 |
| 4 | `PUT /emergencias/1` | 200 |
| 5 | `POST /ubicaciones` | 201 |
| 6 | `GET /ubicaciones` | 200 |
| 7 | `GET /ubicaciones/1` | 200 |
| 8 | `PUT /ubicaciones/1` | 200 |
| 9 | `GET /emergencias/1/ubicacion` | 200 |
| 10 | `GET /emergencias/1/detalle` | 200 |
| 11 | `DELETE /emergencias/1` (con ubicación) | 409 |
| 12 | `DELETE /ubicaciones/1` | 200 |
| 13 | `DELETE /emergencias/1` | 200 |

Casos de error:

| Petición | Resultado esperado |
|---|---|
| `GET /emergencias/999` | 404 |
| `PUT /emergencias/999` | 404 |
| `DELETE /emergencias/999` | 404 |
| `POST /emergencias` con `id_persona: 999` | 400 |
| `GET /ubicaciones/999` | 404 |
| `POST /ubicaciones` con `id_emergencia: 999` | 400 |
| `GET /emergencias/999/detalle` | 404 |

Las capturas de las pruebas se encuentran en la carpeta `evidencias/` *(agrégala si la incluyes en el repositorio)*.

## 🔒 Seguridad

Los archivos `.env` y la carpeta `venv/` están incluidos en `.gitignore` y **no** se suben al repositorio.

## 👥 Equipo

| Integrante | Rol |
|---|---|
| *Adrian Camilo Trigos Quintero* | *0192204* |
| *Andres Felipe Sepulveda Gaona* | *0192228* |
| *Daniel Felipe Torrado Carrascal* | *0192236* |
| *Yohan Orlando Perez Jimenez* | *0192216* |
| *Karol Daniela Manios Yañez* | *0192200* |


