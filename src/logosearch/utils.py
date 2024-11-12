import requests
from .config import REQUEST_TIMEOUT, IMAGE_EXTENSIONS, SIZE_RANGES

def verify_image_url(url):
    try:
        response = requests.head(url, timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def find_valid_image_url(results, size='small'):
    if not results:
        return None
    
    min_size, max_size = SIZE_RANGES.get(size.lower(), SIZE_RANGES['medium'])
    
    # First try to find image matching size preference
    for result in results:
        url = result.get('imageUrl', '').lower()
        width = result.get('imageWidth', 0)
        height = result.get('imageHeight', 0)
        
        if (url and 
            min_size <= max(width, height) <= max_size and 
            any(url.endswith(ext) for ext in IMAGE_EXTENSIONS)):
            if verify_image_url(url):
                return url
    
    # Fallback to any valid image
    for result in results:
        url = result.get('imageUrl', '').lower()
        if url and any(url.endswith(ext) for ext in IMAGE_EXTENSIONS):
            if verify_image_url(url):
                return url
    
    return results[0].get('imageUrl') if results else None 