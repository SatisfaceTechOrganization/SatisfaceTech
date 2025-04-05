# 1. Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 2. Cargar el dataset Iris
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df["target"] = iris.target

# 3. Seleccionar variables predictoras (X) y la variable objetivo (y)
X = df.drop(columns=["sepal length (cm)"])  # Predeciremos el largo del sépalo
y = df["sepal length (cm)"]

# 4. Dividir los datos en conjuntos de entrenamiento y prueba (80% - 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Entrenar un modelo de Regresión Lineal
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# 6. Hacer predicciones en los datos de prueba
y_pred = modelo.predict(X_test)

# 7. Evaluar el modelo
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"📊 Evaluación del modelo:")
print(f"🔹 MAE (Error Absoluto Medio): {mae:.4f}")
print(f"🔹 MSE (Error Cuadrático Medio): {mse:.4f}")
print(f"🔹 R² (Coeficiente de Determinación): {r2:.4f}")

# 8. Graficar resultados
plt.scatter(y_test, y_pred, color="blue", alpha=0.6)
plt.plot(y_test, y_test, color="red", linestyle="--")  # Línea ideal
plt.xlabel("Valores reales")
plt.ylabel("Predicciones")
plt.title("Regresión Lineal - Predicción del largo del sépalo")
plt.show()

# 9. Guardar los resultados en un archivo Excel
resultados = pd.DataFrame({"Real": y_test, "Predicción": y_pred})
resultados.to_excel("resultados_regresion.xlsx", index=False)
print("📁 Archivo 'resultados_regresion.xlsx' guardado correctamente.")
