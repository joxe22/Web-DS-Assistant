import os
import sys
from routes.data_processing import data_processing_bp
from flask import Flask
from routes.principal import principal_bp
from routes.data_analysis import data_analysis_bp
from routes.data_visualization import data_visualization_bp
from routes.machine_learning import machine_learning_bp
from routes.outliers import outliers_bp
from routes.metrics import metrics_bp
from routes.insights_dashboard import insights_dashboard_bp
from routes.chatbot import chatbot_bp

# Agregar al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Carpeta para guardar archivos CSV

# Registro de Blueprints
app.register_blueprint(principal_bp)
app.register_blueprint(data_processing_bp)
app.register_blueprint(data_analysis_bp)
app.register_blueprint(data_visualization_bp)
app.register_blueprint(machine_learning_bp)
app.register_blueprint(outliers_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(insights_dashboard_bp)
app.register_blueprint(chatbot_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5150)
