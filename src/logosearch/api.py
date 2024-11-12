import json
import requests
from .config import SERPER_API_URL, SERPER_API_KEY, DEFAULT_NUM_RESULTS
from .utils import find_valid_image_url

def search_images(entity_name, num_results=DEFAULT_NUM_RESULTS):
    headers = {
        'X-API-Key': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps({
        "q": f"{entity_name} logo official",
        "num": num_results
    })
    
    try:
        response = requests.post(SERPER_API_URL, headers=headers, data=payload)
        response.raise_for_status()
        return response.json().get('images', [])
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Error in search_images: {str(e)}")
        return None

def get_logo_url(entity_name, size='small'):
    results = search_images(entity_name)
    if results:
        return find_valid_image_url(results, size)
    return None 