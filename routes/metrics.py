# routes/metrics.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import os

# Crear Blueprint
metrics_bp = Blueprint('metrics', __name__)

data_cache = {}  # Diccionario para almacenar temporalmente los DataFrames
computed_metrics = {}  # Diccionario para almacenar las métricas calculadas

@metrics_bp.route('/metrics/<filename>', methods=['GET', 'POST'])
def evaluate_metrics(filename):
    filepath = os.path.join('uploads', filename)

    # Cargar el DataFrame si no está en el cache
    if filename not in data_cache:
        df = pd.read_csv(filepath)
        data_cache[filename] = df
    else:
        df = data_cache[filename]

    # Cargar el modelo previamente entrenado
    model_filename = f"{filename}_model.pkl"
    if os.path.exists(model_filename):
        with open(model_filename, 'rb') as model_file:
            model = pickle.load(model_file)
        
        # Preparar datos para evaluación: se asume que la columna 'target' es la variable dependiente
        X = df.drop('target', axis=1)
        y = df['target']

        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'evaluate':
                # Calcular las métricas
                predictions = model.predict(X)
                accuracy = accuracy_score(y, predictions)
                precision = precision_score(y, predictions, average='weighted')
                recall = recall_score(y, predictions, average='weighted')
                f1 = f1_score(y, predictions, average='weighted')

                # Guardar las métricas en la cache para usarlas luego en "guardar"
                computed_metrics[filename] = {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1
                }

                return render_template('metrics.html', filename=filename,
                                       accuracy=accuracy, precision=precision,
                                       recall=recall, f1=f1)
    
    # Si no se pudo evaluar o no se envió POST, se renderiza la plantilla sin métricas
    return render_template('metrics.html', filename=filename)
