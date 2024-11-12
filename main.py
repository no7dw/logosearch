import os
import json
import requests

def search_images(entity_name, num_results=10):
    url = "https://google.serper.dev/images"
    headers = {
        'X-API-Key': os.environ.get('SERPER_API_KEY'),
        'Content-Type': 'application/json'
    }
    
    search_query = f"{entity_name} logo official"
    payload = json.dumps({
        "q": search_query,
        "num": num_results
    })
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json().get('images', [])
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Error in search_images: {str(e)}")
        return None

def verify_image_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def find_valid_image_url(results, size='small'):
    if not results:
        return None
        
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    
    # Define size thresholds (in pixels)
    size_ranges = {
        'small': (0, 300),        # 0-300px
        'medium': (301, 800),     # 301-800px
        'large': (801, float('inf'))  # 801px and above
    }
    
    min_size, max_size = size_ranges.get(size.lower(), size_ranges['medium'])
    
    # First try to find image matching size preference
    for result in results:
        url = result.get('imageUrl', '').lower()
        width = result.get('imageWidth', 0)
        height = result.get('imageHeight', 0)
        
        # Check if image meets size criteria and has valid extension
        if (url and 
            min_size <= max(width, height) <= max_size and 
            any(url.endswith(ext) for ext in image_extensions)):
            if verify_image_url(url):
                return url
    
    # If no size-matching images found, fall back to any valid image
    for result in results:
        url = result.get('imageUrl', '').lower()
        if url and any(url.endswith(ext) for ext in image_extensions):
            if verify_image_url(url):
                return url
    
    # Last resort: return first image
    return results[0].get('imageUrl')

def get_logo_url(entity_name, size='small'):
    results = search_images(entity_name)
    if results:
        return find_valid_image_url(results, size)
    return None

# Example usage:
test_entities = ["nvdia","meta", "tsla"]

for entity in test_entities:
    logo_url = get_logo_url(entity)
    print(f"Logo URL for {entity}: {logo_url}")
    print("-" * 80)  # Separator for better readability

