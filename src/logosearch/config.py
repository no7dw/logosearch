import os

# API Configuration
SERPER_API_URL = "https://google.serper.dev/images"
SERPER_API_KEY = os.environ.get('SERPER_API_KEY')

# Image size configurations
SIZE_RANGES = {
    'small': (0, 300),
    'medium': (301, 800),
    'large': (801, float('inf'))
}

# Valid image extensions
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

# Request configurations
REQUEST_TIMEOUT = 5
DEFAULT_NUM_RESULTS = 10