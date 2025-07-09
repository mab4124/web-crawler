import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from bs4 import BeautifulSoup
import requests

# Add the parent directory to sys.path to import the web_crawler module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_crawler import WebCrawler

class TestWebCrawler(unittest.TestCase):
    """Test cases for the WebCrawler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://example.com"
        self.crawler = WebCrawler(self.base_url, max_pages=5, delay=0.1)
    
    def test_initialization(self):
        """Test crawler initialization."""
        self.assertEqual(self.crawler.base_url, self.base_url)
        self.assertEqual(self.crawler.max_pages, 5)
        self.assertEqual(self.crawler.delay, 0.1)
        self.assertEqual(self.crawler.domain, "example.com")
        self.assertIn(self.base_url, self.crawler.to_visit)
        self.assertEqual(len(self.crawler.visited_urls), 0)
        self.assertEqual(len(self.crawler.scraped_data), 0)
    
    def test_is_valid_url(self):
        """Test URL validation."""
        # Valid URLs
        self.assertTrue(self.crawler.is_valid_url("https://example.com/page1"))
        self.assertTrue(self.crawler.is_valid_url("https://example.com/subfolder/page2"))
        
        # Invalid URLs
        self.assertFalse(self.crawler.is_valid_url("https://other-domain.com/page"))
        self.assertFalse(self.crawler.is_valid_url("ftp://example.com/file"))
        self.assertFalse(self.crawler.is_valid_url("invalid-url"))
        
        # Already visited URL
        self.crawler.visited_urls.add("https://example.com/visited")
        self.assertFalse(self.crawler.is_valid_url("https://example.com/visited"))
    
    @patch('web_crawler.requests.Session.get')
    def test_get_page_content_success(self, mock_get):
        """Test successful page content retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.content = b"<html><body><h1>Test Page</h1></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        soup = self.crawler.get_page_content("https://example.com/test")
        
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.find('h1').text, "Test Page")
        mock_get.assert_called_once()
    
    @patch('web_crawler.requests.Session.get')
    def test_get_page_content_failure(self, mock_get):
        """Test failed page content retrieval."""
        # Mock request exception
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        soup = self.crawler.get_page_content("https://example.com/test")
        
        self.assertIsNone(soup)
        mock_get.assert_called_once()
    
    def test_extract_links(self):
        """Test link extraction from HTML."""
        html = """
        <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
            <a href="https://other-domain.com/page3">External Page</a>
            <a href="#section">Section Link</a>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'lxml')
        current_url = "https://example.com"
        
        links = self.crawler.extract_links(soup, current_url)
        
        # Should extract valid internal links only
        expected_links = [
            "https://example.com/page1",
            "https://example.com/page2"
        ]
        
        for link in expected_links:
            self.assertIn(link, links)
        
        # Should not include external links
        self.assertNotIn("https://other-domain.com/page3", links)
    
    def test_extract_data(self):
        """Test data extraction from HTML."""
        html = """
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Heading</h1>
            <h2>Sub Heading</h2>
            <p>This is a paragraph.</p>
            <p>Another paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'lxml')
        url = "https://example.com/test"
        
        data = self.crawler.extract_data(soup, url)
        
        self.assertEqual(data['url'], url)
        self.assertEqual(data['title'], "Test Page")
        self.assertEqual(len(data['headings']), 2)
        self.assertEqual(len(data['paragraphs']), 2)
        self.assertEqual(len(data['links']), 1)
        self.assertEqual(len(data['images']), 1)
        
        # Check heading structure
        self.assertEqual(data['headings'][0]['level'], 1)
        self.assertEqual(data['headings'][0]['text'], "Main Heading")
        
        # Check paragraph content
        self.assertIn("This is a paragraph.", data['paragraphs'])
        
        # Check link data
        self.assertEqual(data['links'][0]['text'], "Link 1")
        self.assertEqual(data['links'][0]['href'], "https://example.com/link1")
        
        # Check image data
        self.assertEqual(data['images'][0]['alt'], "Image 1")
        self.assertEqual(data['images'][0]['src'], "https://example.com/image1.jpg")
    
    def test_get_statistics(self):
        """Test statistics calculation."""
        # Add sample data
        self.crawler.scraped_data = [
            {
                'url': 'https://example.com/page1',
                'title': 'Page 1',
                'headings': [{'level': 1, 'text': 'Heading 1'}],
                'paragraphs': ['Para 1', 'Para 2'],
                'links': [{'text': 'Link 1', 'href': 'https://example.com/link1'}],
                'images': [{'alt': 'Image 1', 'src': 'https://example.com/img1.jpg'}]
            },
            {
                'url': 'https://example.com/page2',
                'title': 'Page 2',
                'headings': [{'level': 1, 'text': 'Heading 2'}, {'level': 2, 'text': 'Subheading'}],
                'paragraphs': ['Para 3'],
                'links': [{'text': 'Link 2', 'href': 'https://example.com/link2'}],
                'images': []
            }
        ]
        
        stats = self.crawler.get_statistics()
        
        self.assertEqual(stats['total_pages'], 2)
        self.assertEqual(stats['total_links'], 2)
        self.assertEqual(stats['total_images'], 1)
        self.assertEqual(stats['total_headings'], 3)
        self.assertEqual(stats['total_paragraphs'], 3)
        self.assertEqual(stats['unique_urls'], 2)
    
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_export_to_json(self, mock_json_dump, mock_open):
        """Test JSON export functionality."""
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Add sample data
        self.crawler.scraped_data = [{'url': 'https://example.com', 'title': 'Test'}]
        
        result = self.crawler.export_to_json("test_output.json")
        
        self.assertEqual(result, "test_output.json")
        mock_open.assert_called_once_with("test_output.json", 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(
            self.crawler.scraped_data, 
            mock_file, 
            indent=2, 
            ensure_ascii=False
        )
    
    @patch('pandas.DataFrame.to_csv')
    def test_export_to_csv(self, mock_to_csv):
        """Test CSV export functionality."""
        # Add sample data
        self.crawler.scraped_data = [
            {
                'url': 'https://example.com',
                'title': 'Test',
                'headings': [{'level': 1, 'text': 'Heading'}],
                'paragraphs': ['Para 1'],
                'links': [{'text': 'Link', 'href': 'https://example.com/link'}],
                'images': [],
                'scraped_at': '2023-01-01T00:00:00'
            }
        ]
        
        result = self.crawler.export_to_csv("test_output.csv")
        
        self.assertEqual(result, "test_output.csv")
        mock_to_csv.assert_called_once_with("test_output.csv", index=False, encoding='utf-8')

if __name__ == '__main__':
    unittest.main()
