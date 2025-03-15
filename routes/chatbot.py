from flask import Blueprint, request, jsonify


chatbot_bp = Blueprint('chatbot', __name__)

UPLOAD_FOLDER = 'uploads/'

data_cache = {}

@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message", "")
    response = process_message(user_message)
    return jsonify({"response": response})

# Path: chatbot.py
# Compare this snippet from chatbot.py:
import re

def process_message(message):
    message = message.lower()

    #Basic Responses
    if "go to analytics" in message:
        return {"text": "Redirecting to analytics page", "type": "redirect", "url": "/data_analysis"}
    if "go to data processing" in message:
        return {"text": "Redirecting to data processing page", "type": "redirect", "url": "/data_processing"}
    if "go to data visualization" in message:
        return {"text": "Redirecting to data visualization page", "type": "redirect", "url": "/data_visualization"}
    if "go to machine learning" in message:
        return {"text": "Redirecting to machine learning page", "type": "redirect", "url": "/machine_learning"}
    if "go to outliers" in message:
        return {"text": "Redirecting to outliers page", "type": "redirect", "url": "/outliers"}
    if "go to metrics" in message:
        return {"text": "Redirecting to metrics page", "type": "redirect", "url": "/metrics"}
    if "go to insights dashboard" in message:
        return {"text": "Redirecting to insights dashboard page", "type": "redirect", "url": "/insights_dashboard"}
    
    #Data Analysis
    elif "describe data" in message:
        return{"text": "Here is a description of the data", "type": "data_analysis", "action": "describe_data"}
    #data visualization
    elif "scatter plot" in message:
        return{"text": "Here is a scatter plot", "type": "data_visualization", "action": "scatter_plot"}
    elif "line plot" in message:
        return{"text": "Here is a line plot", "type": "data_visualization", "action": "line_plot"}
    elif "bar plot" in message:
        return{"text": "Here is a bar plot", "type": "data_visualization", "action": "bar_plot"}
    elif "pie chart" in message:
        return{"text": "Here is a pie chart", "type": "data_visualization", "action": "pie_chart"}
    #Machine Learning
    elif "train model" in message:
        return{"text": "Training the model", "type": "machine_learning", "action": "train_model"}
    elif "predict" in message:
        return{"text": "Making predictions", "type": "machine_learning", "action": "predict"}
    #Outliers
    elif "remove outliers" in message:
        return{"text": "Removing outliers", "type": "outliers", "action": "remove_outliers"}
    #Metrics
    elif "calculate metrics" in message:
        return{"text": "Calculating metrics", "type": "metrics", "action": "calculate_metrics"}
    #Insights Dashboard
    elif "show insights" in message:
        return{"text": "Showing insights", "type": "insights_dashboard", "action": "show_insights"}
    else:
        return {"text": "I'm sorry, I don't understand that command", "type": "text"}
                  