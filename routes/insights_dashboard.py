from flask import Blueprint, render_template, request, send_file
import pandas as pd
import os

# Crear Blueprint
insights_dashboard_bp = Blueprint('insights_dashboard', __name__)

data_cache = {}  # Diccionario para almacenar temporalmente los DataFrames

@insights_dashboard_bp.route('/insights/<filename>', methods=['GET'])
def show_insights(filename):
    filepath = os.path.join('uploads', filename)

    # Cargar el DataFrame si no está en el cache
    if filename not in data_cache:
        df = pd.read_csv(filepath)
        data_cache[filename] = df
    else:
        df = data_cache[filename]

    # Mostrar el DataFrame procesado con todos los cambios y métricas
    return render_template('insights_dashboard.html', filename=filename, table=df.to_html(classes='table table-striped'))

@insights_dashboard_bp.route('/download/<filename>', methods=['GET'])
def download_insights(filename):
    filepath = os.path.join('uploads', filename)
    return send_file(filepath, as_attachment=True)

