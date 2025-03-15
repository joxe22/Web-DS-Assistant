from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Crear Blueprint
machine_learning_bp = Blueprint('machine_learning', __name__)

data_cache = {}  # Diccionario para almacenar temporalmente los DataFrames

@machine_learning_bp.route('/machine_learning/<filename>', methods=['GET', 'POST'])
def machine_learning(filename):
    filepath = os.path.join('uploads', filename)

    # Cargar el DataFrame si no está en el cache
    if filename not in data_cache:
        df = pd.read_csv(filepath)
        data_cache[filename] = df
    else:
        df = data_cache[filename]

    columns = df.columns.tolist()

    if request.method == 'POST':
        model_type = request.form.get('model_type')
        selected_columns = request.form.getlist('columns')

        # Verificar si hay outliers
        if check_outliers(df[selected_columns]):
            return redirect(url_for('outliers.handle_outliers', filename=filename))

        # Dividir datos en variables predictoras (X) y objetivo (y)
        X = df[selected_columns[:-1]]  # Las columnas excepto la última
        y = df[selected_columns[-1]]  # La última columna es la variable objetivo

        # Dividir en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Seleccionar el modelo basado en la elección del usuario
        if model_type == 'linear_regression':
            model = LinearRegression()
        elif model_type == 'decision_tree':
            model = DecisionTreeRegressor(random_state=42)
        elif model_type == 'random_forest':
            model = RandomForestRegressor(random_state=42)
        elif model_type == 'neural_network':
            model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)

        # Entrenar el modelo
        model.fit(X_train, y_train)

        # Evaluar el modelo
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Guardar los resultados en la sesión (temporalmente)
        model_results = {'mse': mse, 'r2': r2}
        data_cache[filename]['model_results'] = model_results

        return render_template('machine_learning.html', filename=filename, columns=columns, model_results=model_results)

    return render_template('machine_learning.html', filename=filename, columns=columns)

def check_outliers(data):
    """Función para verificar si hay outliers en los datos.
       Retorna True si existe al menos un outlier, False en caso contrario."""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Se genera un DataFrame booleano, y se evalúa si existe al menos un True
    return ((data < lower_bound) | (data > upper_bound)).any().any()

