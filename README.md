# Wyze Light Control Web Interface

A responsive web application for controlling Wyze smart bulbs. Built with Flask and the Wyze SDK.

## Features

- Real-time control of Wyze bulbs
- Responsive design that works on desktop and mobile
- Optimized API usage with staged loading
- Dynamic status updates
- Individual bulb control
- Clear online/offline status indicators

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export WYZE_EMAIL="your.email@example.com"
export WYZE_PASSWORD="your-password"
export WYZE_KEY_ID="your-key-id"  # Optional
export WYZE_API_KEY="your-api-key"  # Optional
```

3. Run the application:
```bash
python web_control.py
```

4. Access the web interface at `http://localhost:5001`

## Project Structure

- `web_control.py` - Flask application and route handlers
- `wyze_manager.py` - Wyze SDK integration and device management
- `config.py` - Configuration management
- `templates/index.html` - Web interface template

## Implementation Details

### Frontend
- Built with Tailwind CSS for styling
- Uses jQuery for AJAX interactions
- Implements staged loading for better UX
- Real-time status updates

### Backend
- Flask web framework
- Wyze SDK for device control
- Environment-based configuration
- Optimized API usage

## Development

The application runs in debug mode by default. Configuration can be modified in `config.py`.

Default server settings:
- Host: 0.0.0.0
- Port: 5001
- Debug: Enabled

## Security Notes

- Credentials are managed via environment variables
- Debug mode should be disabled in production
- API keys should be kept secure

## Dependencies

- Flask 2.0.1
- Wyze SDK 1.0.0
- Tailwind CSS (via CDN)
- jQuery 3.6.0 (via CDN)
