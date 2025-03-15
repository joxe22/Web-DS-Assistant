import os
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from scipy.stats import zscore

# Crear Blueprint
outliers_bp = Blueprint('outliers', __name__)

data_cache = {}  # Diccionario para almacenar temporalmente los DataFrames

@outliers_bp.route('/outliers/<filename>', methods=['GET', 'POST'])
def handle_outliers(filename):
    filepath = os.path.join('uploads', filename)

    # Cargar el DataFrame si no está en el cache
    if filename not in data_cache:
        df = pd.read_csv(filepath)
        data_cache[filename] = df
    else:
        df = data_cache[filename]

    columns = df.columns.tolist()

    if request.method == 'POST':
        method = request.form.get('method')
        selected_columns = request.form.getlist('columns')

        # Aplicar el método seleccionado para tratar outliers
        if method == 'winsorization':
            df[selected_columns] = df[selected_columns].apply(lambda x: winsorize(x))
        elif method == 'iqr':
            df[selected_columns] = df[selected_columns].apply(lambda x: iqr_outliers(x))
        elif method == 'random':
            df[selected_columns] = df[selected_columns].apply(lambda x: random_outliers(x))

        # Guardar los cambios temporales en el cache
        data_cache[filename] = df

        return render_template('outliers.html', filename=filename, columns=columns, tables=[df.to_html(classes='table table-striped')])

    return redirect('machine_learning.html', filename=filename, columns=columns)

def winsorize(series):
    """Aplicar Winsorization a la serie de datos"""
    lower = series.quantile(0.05)
    upper = series.quantile(0.95)
    series = np.clip(series, lower, upper)
    return series

def iqr_outliers(series):
    """Detectar y tratar outliers usando IQR"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    series = series.apply(lambda x: x if lower_bound <= x <= upper_bound else np.nan)
    return series

def random_outliers(series):
    """Reemplazar outliers con valores aleatorios en el rango"""
    lower = series.quantile(0.05)
    upper = series.quantile(0.95)
    series = series.apply(lambda x: np.random.uniform(lower, upper) if x < lower or x > upper else x)
    return series
