from fastapi import FastAPI, HTTPException
from psycopg2 import errors
from con_db import obtener_conexion

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Sentir - FastAPI"}

#Consultar personas en la base de datos
@app.get("/personas")
def consultar_personas():
    # Lógica para consultar personas
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_persona, nombre, telefono, tipo_persona
        FROM personas
    """)

    personas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return personas

#Guardar persona en la base de datos
@app.post("/personas")
def guardar_persona(persona: dict):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO personas (nombre, telefono, tipo_persona)
        VALUES (%s, %s, %s)
    """, (persona["nombre"], persona["telefono"], persona["tipo_persona"]))

    conexion.commit()
    cursor.close()
    conexion.close()

    return {"message": "Persona guardada correctamente"}

#Actualizar persona en la base de datos
@app.put("/personas/{id_persona}")
def actualizar_persona(id_persona: int, persona: dict):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE personas
        SET nombre = %s, telefono = %s, tipo_persona = %s
        WHERE id_persona = %s
    """, (persona["nombre"], persona["telefono"], persona["tipo_persona"], id_persona))

    conexion.commit()
    cursor.close()
    conexion.close()

    return {"message": "Persona actualizada correctamente"}

#Eliminar persona en la base de datos
@app.delete("/personas/{id_persona}")
def eliminar_persona(id_persona: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM personas
        WHERE id_persona = %s
    """, (id_persona,))

    conexion.commit()
    cursor.close()
    conexion.close()

    return {"message": "Persona eliminada correctamente"}


# =====================================================================
#  EMERGENCIAS
#  tabla: emergencias (id_emergencia, tipo, descripcion, fecha, estado, id_persona)
# =====================================================================

#Consultar todas las emergencias
@app.get("/emergencias")
def consultar_emergencias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_emergencia, tipo, descripcion, fecha, estado, id_persona
        FROM emergencias
        ORDER BY id_emergencia
    """)

    emergencias = cursor.fetchall()
    cursor.close()
    conexion.close()

    return emergencias

#Consultar una emergencia por id
@app.get("/emergencias/{id_emergencia}")
def consultar_emergencia(id_emergencia: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_emergencia, tipo, descripcion, fecha, estado, id_persona
        FROM emergencias
        WHERE id_emergencia = %s
    """, (id_emergencia,))

    emergencia = cursor.fetchone()
    cursor.close()
    conexion.close()

    if emergencia is None:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    return emergencia

#Registrar una emergencia
@app.post("/emergencias", status_code=201)
def guardar_emergencia(emergencia: dict):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO emergencias (tipo, descripcion, fecha, estado, id_persona)
            VALUES (%s, %s, NOW(), %s, %s)
            RETURNING id_emergencia
        """, (emergencia["tipo"], emergencia["descripcion"],
              emergencia["estado"], emergencia["id_persona"]))
        nuevo_id = cursor.fetchone()[0]
        conexion.commit()
    except errors.ForeignKeyViolation:
        # id_persona no existe en la tabla personas
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La persona indicada (id_persona) no existe")
    finally:
        cursor.close()
        conexion.close()

    return {"message": "Emergencia guardada correctamente", "id_emergencia": nuevo_id}

#Actualizar una emergencia
@app.put("/emergencias/{id_emergencia}")
def actualizar_emergencia(id_emergencia: int, emergencia: dict):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE emergencias
            SET tipo = %s, descripcion = %s, estado = %s, id_persona = %s
            WHERE id_emergencia = %s
        """, (emergencia["tipo"], emergencia["descripcion"],
              emergencia["estado"], emergencia["id_persona"], id_emergencia))
        filas = cursor.rowcount
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La persona indicada (id_persona) no existe")
    finally:
        cursor.close()
        conexion.close()

    if filas == 0:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    return {"message": "Emergencia actualizada correctamente"}

#Eliminar una emergencia
@app.delete("/emergencias/{id_emergencia}")
def eliminar_emergencia(id_emergencia: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            DELETE FROM emergencias
            WHERE id_emergencia = %s
        """, (id_emergencia,))
        filas = cursor.rowcount
        conexion.commit()
    except errors.ForeignKeyViolation:
        # todavía tiene ubicaciones asociadas
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar: la emergencia tiene ubicaciones asociadas. Elimínalas primero")
    finally:
        cursor.close()
        conexion.close()

    if filas == 0:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    return {"message": "Emergencia eliminada correctamente"}


# =====================================================================
#  UBICACIONES
#  tabla: ubicaciones (id_ubicacion, latitud, longitud, direccion, id_emergencia)
# =====================================================================

#Consultar todas las ubicaciones
@app.get("/ubicaciones")
def consultar_ubicaciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_ubicacion, latitud, longitud, direccion, id_emergencia
        FROM ubicaciones
        ORDER BY id_ubicacion
    """)

    ubicaciones = cursor.fetchall()
    cursor.close()
    conexion.close()

    return ubicaciones

#Consultar una ubicación por id
@app.get("/ubicaciones/{id_ubicacion}")
def consultar_ubicacion(id_ubicacion: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_ubicacion, latitud, longitud, direccion, id_emergencia
        FROM ubicaciones
        WHERE id_ubicacion = %s
    """, (id_ubicacion,))

    ubicacion = cursor.fetchone()
    cursor.close()
    conexion.close()

    if ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    return ubicacion

#Registrar una ubicación
@app.post("/ubicaciones", status_code=201)
def guardar_ubicacion(ubicacion: dict):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO ubicaciones (latitud, longitud, direccion, id_emergencia)
            VALUES (%s, %s, %s, %s)
            RETURNING id_ubicacion
        """, (ubicacion["latitud"], ubicacion["longitud"],
              ubicacion["direccion"], ubicacion["id_emergencia"]))
        nuevo_id = cursor.fetchone()[0]
        conexion.commit()
    except errors.ForeignKeyViolation:
        # id_emergencia no existe en la tabla emergencias
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La emergencia indicada (id_emergencia) no existe")
    finally:
        cursor.close()
        conexion.close()

    return {"message": "Ubicación guardada correctamente", "id_ubicacion": nuevo_id}

#Actualizar una ubicación
@app.put("/ubicaciones/{id_ubicacion}")
def actualizar_ubicacion(id_ubicacion: int, ubicacion: dict):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE ubicaciones
            SET latitud = %s, longitud = %s, direccion = %s, id_emergencia = %s
            WHERE id_ubicacion = %s
        """, (ubicacion["latitud"], ubicacion["longitud"],
              ubicacion["direccion"], ubicacion["id_emergencia"], id_ubicacion))
        filas = cursor.rowcount
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La emergencia indicada (id_emergencia) no existe")
    finally:
        cursor.close()
        conexion.close()

    if filas == 0:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    return {"message": "Ubicación actualizada correctamente"}

#Eliminar una ubicación
@app.delete("/ubicaciones/{id_ubicacion}")
def eliminar_ubicacion(id_ubicacion: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM ubicaciones
        WHERE id_ubicacion = %s
    """, (id_ubicacion,))
    filas = cursor.rowcount

    conexion.commit()
    cursor.close()
    conexion.close()

    if filas == 0:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    return {"message": "Ubicación eliminada correctamente"}


# =====================================================================
#  INTEGRACIÓN
# =====================================================================

#Consultar la ubicación asociada a una emergencia
@app.get("/emergencias/{id_emergencia}/ubicacion")
def consultar_ubicacion_de_emergencia(id_emergencia: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1) ¿existe la emergencia?
    cursor.execute("""
        SELECT id_emergencia FROM emergencias WHERE id_emergencia = %s
    """, (id_emergencia,))
    if cursor.fetchone() is None:
        cursor.close()
        conexion.close()
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    # 2) su ubicación
    cursor.execute("""
        SELECT id_ubicacion, latitud, longitud, direccion, id_emergencia
        FROM ubicaciones
        WHERE id_emergencia = %s
        ORDER BY id_ubicacion
        LIMIT 1
    """, (id_emergencia,))
    ubicacion = cursor.fetchone()
    cursor.close()
    conexion.close()

    if ubicacion is None:
        raise HTTPException(status_code=404, detail="La emergencia no tiene ubicación registrada")

    return ubicacion

#Consultar emergencia + persona que la reportó + ubicación
@app.get("/emergencias/{id_emergencia}/detalle")
def consultar_detalle_emergencia(id_emergencia: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # JOIN con personas (siempre existe por la FK) y LEFT JOIN con ubicaciones
    # (una emergencia puede no tener ubicación todavía)
    cursor.execute("""
        SELECT e.id_emergencia, e.tipo, e.descripcion, e.fecha, e.estado,
               p.id_persona, p.nombre, p.telefono, p.tipo_persona,
               u.id_ubicacion, u.latitud, u.longitud, u.direccion
        FROM emergencias e
        JOIN personas p ON p.id_persona = e.id_persona
        LEFT JOIN ubicaciones u ON u.id_emergencia = e.id_emergencia
        WHERE e.id_emergencia = %s
        ORDER BY u.id_ubicacion
        LIMIT 1
    """, (id_emergencia,))

    fila = cursor.fetchone()
    cursor.close()
    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    ubicacion = None
    if fila[9] is not None:
        ubicacion = {
            "id_ubicacion": fila[9],
            "latitud": fila[10],
            "longitud": fila[11],
            "direccion": fila[12],
        }

    return {
        "emergencia": {
            "id_emergencia": fila[0],
            "tipo": fila[1],
            "descripcion": fila[2],
            "fecha": fila[3],
            "estado": fila[4],
        },
        "persona": {
            "id_persona": fila[5],
            "nombre": fila[6],
            "telefono": fila[7],
            "tipo_persona": fila[8],
        },
        "ubicacion": ubicacion,
    }