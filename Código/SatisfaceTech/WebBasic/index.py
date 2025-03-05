from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo, datetime, time

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necesario para usar mensajes flash

# Conexión con MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["rueda_vida"]
    collection = db["empleados"]
    print("✅ Conexión exitosa a MongoDB")
except Exception as e:
    print("❌ Error de conexión a MongoDB:", e)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/persona')
def persona():
    return render_template('persona.html')

@app.route('/guardar_p', methods=['POST'])
def guardar_p():
    accion = request.form.get('accion')
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    departamento = request.form.get('departamento')
    respuestas = request.form.getlist('respuestas')
    respuestas = [int(r) for r in respuestas]

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
    
    if accion == "Guardar":
        collection.insert_one(empleado)
    elif accion == "Editar":
        collection.update_one({"id": id}, {"$set": empleado})
    elif accion == "Borrar":
        collection.delete_one({"id": id})
    elif accion == "Exportar":
        exportar_datos()
    
    return redirect(url_for('principal'))

@app.route('/confirmar_actualizacion', methods=['POST'])
def confirmar_actualizacion():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    departamento = request.form.get('departamento')
    
    if not id:
        flash("⚠️ Debes proporcionar un ID válido.", "warning")
        return redirect(url_for('resultados'))
    
    resultado = collection.update_one({"id": id}, {"$set": {
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo,
        "departamento": departamento
    }})
    
    if resultado.matched_count:
        flash("✅ Datos actualizados correctamente.", "success")
    else:
        flash("⚠️ No se encontró el empleado con el ID proporcionado.", "danger")
    
    return redirect(url_for('resultados'))

@app.route('/actualizar/<id>', methods=['GET'])
def actualizar(id):
    empleado = collection.find_one({"id": id})
    
    if not empleado:
        flash("⚠️ No se encontró el empleado para eliminar.", "danger")
        return redirect(url_for('resultados'))
    
    return render_template('confirmar_actualizacion.html', empleado=empleado)

@app.route('/eliminar/<id>', methods=['GET'])
def eliminar(id):
    collection.delete_one({"id": id})
    flash("✅ Empleado eliminado correctamente.", "success")
    return redirect(url_for('resultados'))

@app.route('/resultados')
def resultados():
    empleados = collection.find()
    return render_template('resultados.html', empleados=empleados)

@app.route('/ver/<id>')
def ver_detalles(id):
    empleado = collection.find_one({"id": id}, {"_id": 0})  # Evita enviar _id de MongoDB
    
    if not empleado:
        flash("⚠️ No se encontró el empleado.", "danger")
        return redirect(url_for('resultados'))

    # Convertir respuestas en porcentajes
    respuestas_porcentajes = {
        area: round((sum(valores) / 50) * 100, 2) for area, valores in empleado["respuestas"].items()
    }

    return render_template('detalles.html', empleado=empleado, respuestas_json=respuestas_porcentajes)


# Función para exportar datos a un archivo de texto
def exportar_datos():
    empleados = collection.find()
    data = "\n".join([str(emp) for emp in empleados])
    filename = f"Reports/Personas_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as file:
        file.write(data)
    print("Datos exportados a:", filename)

if __name__ == '__main__':
    app.run(debug=True, port=5080)
