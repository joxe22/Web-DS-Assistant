from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import os
from io import StringIO

# Crear Blueprint
data_processing_bp = Blueprint('data_processing', __name__)

# Carpeta de subida de archivos
UPLOAD_FOLDER = 'uploads/'

data_cache = {}  # Diccionario para almacenar temporalmente los DataFrames

@data_processing_bp.route('/process <filename>', methods=['GET', 'POST'])
def process_data(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Si el archivo no está en el cache, cargarlo
    if filename not in data_cache:
        df = pd.read_csv(filepath)
        data_cache[filename] = df
    else:
        df = data_cache[filename]

    # Acción a realizar en base al formulario enviado
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'drop_duplicates':
            df.drop_duplicates(inplace=True)
        elif action == 'drop_na':
            df.dropna(inplace=True)
        elif action == 'describe':
            stats = df.describe().to_html(classes='table table-striped')
            return render_template('data_processing.html', filename=filename, tables=[df.to_html(classes='table table-striped')], stats=stats)
        elif action == 'info':
            buffer = StringIO()  # Use StringIO instead of a list
            df.info(buf=buffer)
            info_str = buffer.getvalue()  # Get the content of the StringIO buffer
            return render_template('data_processing.html', filename=filename, tables=[df.to_html(classes='table table-striped')], info=info_str)

        # Guardar cambios temporalmente
        data_cache[filename] = df
    
    # Renderizar la plantilla con los datos
    return render_template('data_processing.html', filename=filename, tables=[df.to_html(classes='table table-striped')])
