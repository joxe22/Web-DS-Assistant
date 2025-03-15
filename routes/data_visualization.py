from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import base64

# Crear Blueprint
data_visualization_bp = Blueprint('data_visualization', __name__)

data_cache = {}  # Diccionario para almacenar temporalmente los DataFrames

@data_visualization_bp.route('/visualization/<filename>', methods=['GET', 'POST'])
def visualize_data(filename):
    filepath = os.path.join('uploads', filename)

    # Cargar el DataFrame si no está en el cache
    if filename not in data_cache:
        df = pd.read_csv(filepath)
        data_cache[filename] = df
    else:
        df = data_cache[filename]

    # Obtener las columnas del DataFrame
    columns = df.columns.tolist()

    if request.method == 'POST':
        plot_type = request.form.get('plot_type')
        selected_columns = request.form.getlist('columns')

        # Crear gráfico según el tipo de gráfico elegido
        if plot_type:
            fig, img_data = create_plot(plot_type, df, selected_columns)
            img_url = f"data:image/png;base64,{img_data}"

            return render_template('data_visualization.html', filename=filename, columns=columns, img_url=img_url)

    return render_template('data_visualization.html', filename=filename, columns=columns)

def create_plot(plot_type, df, selected_columns):
    """
    Función para crear los gráficos solicitados: scatter, line, bar, box, heatmap.
    """
    img = io.BytesIO()

    if plot_type == 'scatter':
        fig = plt.figure()
        sns.scatterplot(x=df[selected_columns[0]], y=df[selected_columns[1]])
        plt.title(f'Scatter plot de {selected_columns[0]} vs {selected_columns[1]}')
        plt.savefig(img, format='png')
    
    elif plot_type == 'line':
        fig = plt.figure()
        sns.lineplot(x=df[selected_columns[0]], y=df[selected_columns[1]])
        plt.title(f'Line plot de {selected_columns[0]} vs {selected_columns[1]}')
        plt.savefig(img, format='png')

    elif plot_type == 'bar':
        fig = plt.figure()
        sns.barplot(x=df[selected_columns[0]], y=df[selected_columns[1]])
        plt.title(f'Bar plot de {selected_columns[0]} vs {selected_columns[1]}')
        plt.savefig(img, format='png')

    elif plot_type == 'box':
        fig = plt.figure()
        sns.boxplot(x=df[selected_columns[0]], y=df[selected_columns[1]])
        plt.title(f'Box plot de {selected_columns[0]} vs {selected_columns[1]}')
        plt.savefig(img, format='png')

    elif plot_type == 'heatmap':
        fig = plt.figure()
        corr_matrix = df[selected_columns].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title('Heatmap de correlaciones')
        plt.savefig(img, format='png')

    else:
        # Por defecto, no genera nada si el tipo no es válido
        return None, None

    # Convertir la imagen a base64 para mostrar en la página
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode('utf-8')
    return fig, img_data

