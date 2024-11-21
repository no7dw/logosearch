import os
import json
import aiohttp
import asyncio

async def search_images(entity_name, num_results=10):
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
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=payload) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get('images', [])
        except Exception as e:
            print(f"Error in search_images: {str(e)}")
            return None

async def verify_image_url(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(url, timeout=5) as response:
                return response.status_code == 200
        except Exception:
            return False

async def find_valid_image_url(results, size='small'):
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
            if await verify_image_url(url):
                return url
    
    # If no size-matching images found, fall back to any valid image
    for result in results:
        url = result.get('imageUrl', '').lower()
        if url and any(url.endswith(ext) for ext in image_extensions):
            if await verify_image_url(url):
                return url
    
    # Last resort: return first image
    return results[0].get('imageUrl')

async def get_logo_url(entity_name, size='small')->str:
    results = await search_images(entity_name)
    if results:
        return await find_valid_image_url(results, size)
    return None

async def main():
    # for entity in ["china", "usa", "tesla", "meta", "btc", "usdt", "avax", "bnb" , "sui"]:
    # for entity in [ "76ers vs. Grizzlies",  "U.S. Federal Reserve", "Stock Market Trends", "Cryptocurrency Market Update"]:
    for entity in ["76ers vs. Grizzlies",  "U.S. Federal Reserve", "Stock Market Trends", "Cryptocurrency Market Update"]:
        logo_url = await get_logo_url(entity)
        print(f"{entity}: {logo_url}")
# Example usage:
if __name__ == "__main__":  
    asyncio.run(main())
