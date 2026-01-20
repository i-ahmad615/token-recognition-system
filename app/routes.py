"""
Flask Routes for Token Recognition System
"""

from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.lexer import TokenRecognitionSystem

# Allowed file extensions
ALLOWED_EXTENSIONS = {'c', 'cpp', 'py', 'txt', 'java', 'js', 'h', 'hpp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_routes(app):
    """Initialize all routes"""
    
    lexer = TokenRecognitionSystem()
    
    @app.route('/')
    def index():
        """Render main page"""
        return render_template('index.html')
    
    @app.route('/tokenize', methods=['POST'])
    def tokenize():
        """Tokenize code from text input"""
        try:
            data = request.get_json()
            
            if not data or 'code' not in data:
                return jsonify({
                    'success': False,
                    'error': 'No code provided'
                }), 400
            
            code = data['code']
            
            if not code. strip():
                return jsonify({
                    'success': False,
                    'error': 'Empty code input'
                }), 400
            
            # Tokenize the code
            result = lexer.tokenize(code)
            
            return jsonify({
                'success':  True,
                'tokens': result['tokens'],
                'errors':  result['errors'],
                'total_tokens': result['total_tokens']
            })
        
        except Exception as e: 
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        """Handle file upload and tokenization"""
        try: 
            # Check if file is present
            if 'file' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No file uploaded'
                }), 400
            
            file = request.files['file']
            
            # Check if file is selected
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400
            
            # Check file extension
            if not allowed_file(file.filename):
                return jsonify({
                    'success': False,
                    'error': f'Invalid file type.  Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
                }), 400
            
            # Read file content
            try:
                code = file.read().decode('utf-8')
            except UnicodeDecodeError:
                return jsonify({
                    'success': False,
                    'error': 'File encoding not supported.  Please use UTF-8 encoded files.'
                }), 400
            
            # Tokenize the code
            result = lexer. tokenize(code)
            
            return jsonify({
                'success': True,
                'filename': secure_filename(file.filename),
                'tokens': result['tokens'],
                'errors': result['errors'],
                'total_tokens':  result['total_tokens']
            })
        
        except Exception as e: 
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle file too large error"""
        return jsonify({
            'success': False,
            'error': 'File too large. Maximum size is 16MB.'
        }), 413
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500