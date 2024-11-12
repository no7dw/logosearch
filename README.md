# LogoSearch

A Python tool for searching and retrieving company logos using the Google Serper API.

## Features

- Quick logo retrieval by company name
- Size-specific image search (small, medium, large)
- Automatic image validation and verification
- Support for multiple image formats (jpg, jpeg, png, gif, webp)
- Fallback mechanisms for reliable results

## Installation

1. Install required packages:
```bash
pip install requests
```

2. Set up your API key:
```bash
export SERPER_API_KEY='your_api_key_here'
```

## Usage

### Basic Logo Search
```python
from main import get_logo_url

# Get small-sized logo (default)
logo_url = get_logo_url("nvidia")
```

### Size-Specific Search
```python
# Available sizes: "small", "medium", "large"
logo_url = get_logo_url("meta", size="medium")
```

Size specifications:
- Small: 0-300px
- Medium: 301-800px
- Large: 801px+

### Batch Processing
```python
test_entities = ["nvidia", "meta", "tesla"]
for entity in test_entities:
    logo_url = get_logo_url(entity)
    print(f"Logo URL for {entity}: {logo_url}")
```

## Requirements

- Python 3.6+
- `requests` library
- Google Serper API key

## API Setup

1. Visit [serper.dev](https://serper.dev)
2. Create an account
3. Generate your API key
4. Set the environment variable:
```bash
export SERPER_API_KEY='your_api_key_here'
```

## Error Handling

The tool includes built-in handling for:
- Network issues
- Invalid API responses
- Inaccessible image URLs
- Missing API keys

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
