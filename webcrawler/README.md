# Web Crawler Project

A comprehensive Python web crawler that can extract data from websites with features like URL filtering, data extraction, and export capabilities.

## Features

- **Smart URL filtering**: Stays within the same domain and avoids revisiting pages
- **User-Agent rotation**: Prevents blocking by rotating user agents
- **Respectful crawling**: Configurable delays between requests
- **Data extraction**: Extracts titles, headings, paragraphs, links, and images
- **Multiple export formats**: JSON and CSV export options
- **Statistics tracking**: Comprehensive crawling statistics
- **Logging**: Detailed logging for debugging and monitoring
- **Error handling**: Robust error handling for network issues

## Installation

1. **Clone or download this project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- `requests` - HTTP library for making web requests
- `beautifulsoup4` - HTML parsing library
- `lxml` - Fast XML and HTML parser
- `pandas` - Data manipulation and analysis
- `colorama` - Colored terminal output
- `tqdm` - Progress bars
- `fake-useragent` - User agent rotation

## Usage

### Basic Usage

```python
from web_crawler import WebCrawler

# Create crawler instance
crawler = WebCrawler(
    base_url="https://example.com",
    max_pages=10,
    delay=1.0
)

# Start crawling
data = crawler.crawl()

# Export data
crawler.export_to_json("output.json")
crawler.export_to_csv("output.csv")

# Print statistics
crawler.print_statistics()
```

### Command Line Usage

#### Run the main crawler:
```bash
python web_crawler.py
```

#### Run examples:
```bash
# Interactive custom crawler
python examples.py --mode custom

# Crawl news site example
python examples.py --mode news

# Crawl e-commerce site example
python examples.py --mode ecommerce

# Crawl blog site example
python examples.py --mode blog

# Custom URL with parameters
python examples.py --mode custom --url https://example.com --max-pages 20 --delay 1.5
```

### Advanced Features

#### Custom Data Extraction

You can customize the `extract_data` method to extract specific data based on your needs:

```python
def extract_data(self, soup, url):
    # Your custom extraction logic here
    data = {
        'url': url,
        'custom_field': soup.find('div', class_='custom-class').text,
        # ... other fields
    }
    return data
```

#### Export Options

- **JSON Export**: `crawler.export_to_json("filename.json")`
- **CSV Export**: `crawler.export_to_csv("filename.csv")`

#### Statistics

Get comprehensive statistics about your crawl:

```python
stats = crawler.get_statistics()
print(f"Total pages: {stats['total_pages']}")
print(f"Total links: {stats['total_links']}")
```

## Configuration

### WebCrawler Parameters

- `base_url` (str): Starting URL for crawling
- `max_pages` (int): Maximum number of pages to crawl (default: 10)
- `delay` (float): Delay between requests in seconds (default: 1.0)

### Best Practices

1. **Be respectful**: Use appropriate delays between requests
2. **Check robots.txt**: Respect the website's robots.txt file
3. **Monitor your crawls**: Use the logging feature to monitor progress
4. **Handle errors gracefully**: The crawler includes comprehensive error handling

## Project Structure

```
webcrawler/
├── web_crawler.py          # Main crawler class
├── examples.py             # Usage examples and CLI interface
├── requirements.txt        # Python dependencies
├── tests/
│   └── test_web_crawler.py # Unit tests
└── README.md              # This file
```

## Testing

Run the unit tests:

```bash
python -m pytest tests/
```

Or run with unittest:

```bash
python -m unittest tests.test_web_crawler
```

## Output Files

The crawler generates several types of output:

1. **JSON files**: Complete structured data from crawled pages
2. **CSV files**: Flattened data suitable for analysis
3. **Log files**: `crawler.log` with detailed crawling information

## Example Output

### JSON Structure
```json
{
  "url": "https://example.com/page1",
  "title": "Page Title",
  "headings": [
    {"level": 1, "text": "Main Heading"},
    {"level": 2, "text": "Sub Heading"}
  ],
  "paragraphs": ["Paragraph 1", "Paragraph 2"],
  "links": [
    {"text": "Link Text", "href": "https://example.com/link"}
  ],
  "images": [
    {"alt": "Image Alt", "src": "https://example.com/image.jpg"}
  ],
  "scraped_at": "2023-01-01T12:00:00"
}
```

### CSV Structure
```csv
url,title,num_headings,num_paragraphs,num_links,num_images,scraped_at
https://example.com,Page Title,2,2,1,1,2023-01-01T12:00:00
```

## Legal and Ethical Considerations

- Always respect robots.txt files
- Don't overload servers with rapid requests
- Be mindful of copyright and terms of service
- Consider the website's bandwidth and server resources
- Use appropriate delays between requests

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
2. **Network timeouts**: Increase delay or check internet connection
3. **Access denied**: Some sites may block scrapers - respect their policies
4. **Memory issues**: Reduce max_pages for large sites

### Debug Tips

- Check the `crawler.log` file for detailed information
- Use smaller max_pages values for testing
- Increase delay if getting blocked
- Verify the target URL is accessible

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for educational purposes. Please respect website terms of service and robots.txt files when using this crawler.

## Changelog

### v1.0.0
- Initial release with basic crawling functionality
- JSON and CSV export options
- User-agent rotation
- Comprehensive error handling
- Unit tests included
