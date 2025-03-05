from pymongo import MongoClient
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["rueda_vida"]
collection = db["empleados"]

@app.route('/guardar_p', methods=['POST'])
def guardar_p():
    print("✅ Se llamó a la función guardar_p()")  # Ver si Flask recibe el POST

    # Obtener datos del formulario
    print("🔍 Datos recibidos:", request.form)  # Ver qué datos llegan

    accion = request.form.get('accion')
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    departamento = request.form.get('departamento')
    respuestas = request.form.getlist('respuestas')

    if not respuestas:
        print("⚠️ No se recibieron respuestas.")

    respuestas = [int(r) for r in respuestas] if respuestas else []

    preguntas_rueda = {
        "Área Física": respuestas[:5],
        "Área Personal": respuestas[5:10],
        "Área Familiar": respuestas[10:15],
        "Área Económica": respuestas[15:20],
        "Área Profesional": respuestas[20:25],
        "Área Social": respuestas[25:30],
        "Área de Ocio": respuestas[30:35],
        "Área Espiritual": respuestas[35:40]
    }

    empleado = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo,
        "departamento": departamento,
        "respuestas": preguntas_rueda
    }

    print("📌 Datos listos para insertar:", empleado)  # Ver datos antes de guardar

    if accion == "Guardar":
        collection.insert_one(empleado)
        print("✅ Empleado guardado correctamente.")
    elif accion == "Editar":
        collection.update_one({"id": id}, {"$set": empleado})
        print("✅ Datos actualizados.")
    elif accion == "Borrar":
        collection.delete_one({"id": id})
        print("✅ Empleado eliminado.")

    return redirect(url_for('persona'))



if __name__ == '__main__':
    app.run(debug=True, port=5080)
