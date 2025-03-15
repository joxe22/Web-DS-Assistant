from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import os

# Crear Blueprint
data_analysis_bp = Blueprint('data_analysis', __name__)

data_cache = {}  # Diccionario para almacenar temporalmente los DataFrames

@data_analysis_bp.route('/analysis/<filename>', methods=['GET', 'POST'])
def analyze_data(filename):
    filepath = os.path.join('uploads', filename)

    # Cargar el DataFrame si no está en el cache
    if filename not in data_cache:
        df = pd.read_csv(filepath)
        data_cache[filename] = df
    else:
        df = data_cache[filename]

    # Obtener las columnas del DataFrame
    columns = df.columns.tolist()

    # Acciones del análisis
    if request.method == 'POST':
        selected_columns = request.form.getlist('columns')
        question = request.form.get('question')

        # Aquí podrías implementar lógica para responder preguntas sobre los datos
        response = analyze_question(df, selected_columns, question)

        # Guardar cambios temporales
        data_cache[filename] = df

        return render_template('data_analysis.html', filename=filename, columns=columns, response=response)

    return render_template('data_analysis.html', filename=filename, columns=columns)

# Función para analizar preguntas (ejemplo simple)
def analyze_question(df, selected_columns, question):
    if "Correlation" in question:
        correlation = df[selected_columns].corr()
        return f"Correlación entre las columnas: {correlation}",
    elif "Group by" in question:
        grouped = df.groupby(selected_columns).sum()
        return f"Resultado de la agrupación y suma: {grouped}",
    elif "Count" in question:
        grouped = df.groupby(selected_columns).count()
        return f"Resultado de la agrupación y conteo: {grouped}",
    elif "Mean" in question:
        grouped = df.groupby(selected_columns).mean()
        return f"Resultado de la agrupación y promedio: {grouped}",
    elif "Standard deviation" in question:
        grouped = df.groupby(selected_columns).std()
        return f"Resultado de la agrupación y desviación estándar: {grouped}",
    elif "Min" in question:
        grouped = df.groupby(selected_columns).min()
        return f"Resultado de la agrupación y mínimo: {grouped}",
    elif "Max" in question:
        grouped = df.groupby(selected_columns).max()
        return f"Resultado de la agrupación y máximo: {grouped}",
    else:
        return "Pregunta no reconocida. Intenta con otra."