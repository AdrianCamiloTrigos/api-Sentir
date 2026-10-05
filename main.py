from fastapi import FastAPI
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