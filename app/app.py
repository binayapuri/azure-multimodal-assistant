from flask import Flask, request, jsonify, render_template
import logging
import os
from config import Config
from bot_handler import TechMartBot

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize configuration and bot
try:
    config = Config()
    bot = TechMartBot(config)
    logging.info("✅ TechMart Bot initialized successfully")
    logging.info(f"🌐 Environment: {config.ENVIRONMENT}")
    logging.info(f"🤖 OpenAI Endpoint: {config.AZURE_OPENAI_ENDPOINT[:50]}...")
except Exception as e:
    logging.error(f"❌ Failed to initialize bot: {e}")
    bot = None

@app.route('/')
def home():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if bot else 'unhealthy',
        'bot_ready': bot is not None,
        'environment': os.getenv('ENVIRONMENT', 'unknown'),
        'services_configured': {
            'openai': bool(os.getenv('AZURE_OPENAI_ENDPOINT')),
            'speech': bool(os.getenv('AZURE_SPEECH_KEY')),
            'vision': bool(os.getenv('AZURE_CV_ENDPOINT')),
            'search': bool(os.getenv('AZURE_SEARCH_ENDPOINT')),
            'cosmos': bool(os.getenv('AZURE_COSMOS_ENDPOINT'))
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not bot:
            return jsonify({
                'success': False,
                'error': 'Bot service is not available. Please check configuration.'
            }), 503
        
        response = bot.process_message(user_id, message)
        
        return jsonify({
            'success': True,
            'response': response,
            'user_id': user_id
        })
        
    except Exception as e:
        logging.error(f"Chat error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error processing your request.'
        }), 500

@app.route('/api/image', methods=['POST'])
def image():
    """Handle image uploads"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        user_id = request.form.get('user_id', 'anonymous')
        
        if not bot:
            return jsonify({'error': 'Bot service not available'}), 503
        
        image_data = file.read()
        response = bot.process_image(user_id, image_data)
        
        return jsonify({
            'success': True,
            'response': response,
            'user_id': user_id
        })
        
    except Exception as e:
        logging.error(f"Image processing error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error processing your image.'
        }), 500

@app.route('/api/voice', methods=['POST'])
def voice():
    """Handle voice input"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio provided'}), 400
        
        file = request.files['audio']
        user_id = request.form.get('user_id', 'anonymous')
        
        if not bot:
            return jsonify({'error': 'Bot service not available'}), 503
        
        audio_data = file.read()
        response = bot.process_voice(user_id, audio_data)
        
        return jsonify({
            'success': True,
            'response': response,
            'user_id': user_id
        })
        
    except Exception as e:
        logging.error(f"Voice processing error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error processing your voice input.'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logging.info(f"🚀 Starting TechMart Bot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)