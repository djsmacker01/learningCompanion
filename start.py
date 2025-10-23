#!/usr/bin/env python3
"""
Production startup script for Learning Companion
"""

import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # Get port from environment (for cloud platforms)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=port,
        debug=False  # Always False in production
    )
