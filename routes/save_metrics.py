# routes/save_metrics.py
from flask import flash, redirect, url_for
import json
import os
# Importamos el blueprint y la variable computed_metrics desde metrics.py
from metrics import metrics_bp, computed_metrics

@metrics_bp.route('/save_metrics/<filename>', methods=['POST'])
def save_metrics(filename):
    # Verificar que para el archivo exista un cálculo previo de métricas
    if filename not in computed_metrics:
        flash("No se han evaluado las métricas para guardar.", "error")
        return redirect(url_for('metrics.evaluate_metrics', filename=filename))
    
    metrics_data = computed_metrics[filename]

    # Carpeta para guardar los resultados; se crea si no existe
    save_folder = "saved_metrics"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Se genera el nombre del archivo (por ejemplo, un JSON)
    save_path = os.path.join(save_folder, f"{filename}_metrics.json")

    # Se guardan las métricas en el archivo
    with open(save_path, "w") as file:
        json.dump(metrics_data, file, indent=4)
    
    flash("Métricas guardadas exitosamente.", "success")
    return redirect(url_for('metrics.evaluate_metrics', filename=filename))
