"""Wyze Light Control Web Interface."""
from flask import Flask, render_template, jsonify, request
import logging
from config import app_config
from wyze_manager import WyzeManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder=app_config.template_dir)
wyze = WyzeManager()

@app.route('/')
def home():
    """Render home page with list of bulbs."""
    try:
        # Just get basic bulb info without status
        bulbs = wyze.get_bulb_names()
        return render_template('index.html', bulbs=bulbs)
    except Exception as e:
        logger.error(f"Error rendering home page: {e}") 
        return render_template('index.html', error=str(e))

@app.route('/status/<mac>')
def get_bulb_status(mac):
    """Get the current status of a specific bulb."""
    try:
        status = wyze.get_bulb_status(mac)
        return jsonify({'success': True, **status})
    except Exception as e:
        logger.error(f"Error getting bulb status: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/toggle/<mac>')
def toggle_bulb(mac):
    """Toggle the state of a specific bulb."""
    try:
        result = wyze.toggle_bulb(mac)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error toggling bulb: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/brightness/<mac>', methods=['POST'])
def set_brightness(mac):
    """Set the brightness of a specific bulb."""
    try:
        brightness = request.json.get('brightness')
        if brightness is None:
            return jsonify({'success': False, 'error': 'Brightness value required'}), 400
            
        result = wyze.set_brightness(mac, brightness)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error setting brightness: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    logger.info("=== Starting Wyze Light Control Web Server ===")
    app.run(
        debug=app_config.debug,
        host=app_config.host,
        port=app_config.port
    )
