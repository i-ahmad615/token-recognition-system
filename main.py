"""
Token Recognition System - Web Application
Main entry point for the Flask application
"""

from flask import Flask
from app.routes import init_routes
import os

# Create Flask app
# Point templates to the package templates directory
app = Flask(__name__, template_folder=os.path.join('app', 'templates'), static_folder='static')

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize routes
init_routes(app)

if __name__ == '__main__': 
    print("=" * 70)
    print("          TOKEN RECOGNITION SYSTEM - WEB APP")
    print("=" * 70)
    print("\n🚀 Starting server...")
    print("📍 Open your browser and navigate to:  http://localhost:5000")
    print("🛑 Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)