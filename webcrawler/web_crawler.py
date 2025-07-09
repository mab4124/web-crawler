import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent
from tqdm import tqdm
import json
import csv
from colorama import Fore, Style, init
import logging
from typing import List, Dict, Set, Optional
import os
from datetime import datetime

# Initialize colorama for colored output
init()

class WebCrawler:
    """
    A comprehensive web crawler that can extract data from websites
    with features like URL filtering, data extraction, and export capabilities.
    """
    
    def __init__(self, base_url: str, max_pages: int = 10, delay: float = 1.0):
        """
        Initialize the web crawler.
        
        Args:
            base_url (str): The starting URL for crawling
            max_pages (int): Maximum number of pages to crawl
            delay (float): Delay between requests in seconds
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls: Set[str] = set()
        self.to_visit: List[str] = [base_url]
        self.scraped_data: List[Dict] = []
        
        # Set up user agent rotation
        self.ua = UserAgent()
        
        # Set up session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('crawler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Domain restriction
        self.domain = urlparse(base_url).netloc
        
    def is_valid_url(self, url: str) -> bool:
        """
        Check if the URL is valid and within the same domain.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc == self.domain and
                url not in self.visited_urls and
                url.startswith(('http://', 'https://'))
            )
        except Exception:
            return False
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse page content.
        
        Args:
            url (str): URL to fetch
            
        Returns:
            BeautifulSoup: Parsed HTML content or None if failed
        """
        try:
            # Rotate user agent
            self.session.headers['User-Agent'] = self.ua.random
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            return soup
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing {url}: {str(e)}")
            return None
    
    def extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """
        Extract all links from the current page.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            current_url (str): Current page URL
            
        Returns:
            List[str]: List of valid URLs found on the page
        """
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            
            if self.is_valid_url(full_url):
                links.append(full_url)
                
        return links
    
    def extract_data(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract data from the current page.
        Customize this method based on your scraping needs.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            url (str): Current page URL
            
        Returns:
            Dict: Extracted data
        """
        data = {
            'url': url,
            'title': '',
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'scraped_at': datetime.now().isoformat()
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            data['title'] = title_tag.get_text().strip()
        
        # Extract headings
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            for heading in headings:
                data['headings'].append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if text:
                data['paragraphs'].append(text)
        
        # Extract links
        links = soup.find_all('a', href=True)
        for link in links:
            data['links'].append({
                'text': link.get_text().strip(),
                'href': urljoin(url, link['href'])
            })
        
        # Extract images
        images = soup.find_all('img', src=True)
        for img in images:
            data['images'].append({
                'alt': img.get('alt', ''),
                'src': urljoin(url, img['src'])
            })
        
        return data
    
    def crawl(self) -> List[Dict]:
        """
        Main crawling method.
        
        Returns:
            List[Dict]: List of scraped data from all pages
        """
        print(f"{Fore.GREEN}Starting web crawl of {self.base_url}{Style.RESET_ALL}")
        print(f"Max pages: {self.max_pages}, Delay: {self.delay}s")
        
        with tqdm(total=self.max_pages, desc="Crawling pages") as pbar:
            while self.to_visit and len(self.visited_urls) < self.max_pages:
                current_url = self.to_visit.pop(0)
                
                if current_url in self.visited_urls:
                    continue
                
                self.visited_urls.add(current_url)
                
                print(f"{Fore.BLUE}Crawling: {current_url}{Style.RESET_ALL}")
                
                soup = self.get_page_content(current_url)
                if soup:
                    # Extract data from current page
                    page_data = self.extract_data(soup, current_url)
                    self.scraped_data.append(page_data)
                    
                    # Find new links to visit
                    new_links = self.extract_links(soup, current_url)
                    for link in new_links:
                        if link not in self.visited_urls and link not in self.to_visit:
                            self.to_visit.append(link)
                    
                    self.logger.info(f"Successfully scraped {current_url}")
                else:
                    self.logger.warning(f"Failed to scrape {current_url}")
                
                pbar.update(1)
                
                # Add delay between requests
                time.sleep(self.delay + random.uniform(0, 0.5))
        
        print(f"{Fore.GREEN}Crawling completed! Scraped {len(self.scraped_data)} pages{Style.RESET_ALL}")
        return self.scraped_data
    
    def export_to_json(self, filename: str = None) -> str:
        """
        Export scraped data to JSON file.
        
        Args:
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to the exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crawled_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        
        print(f"{Fore.GREEN}Data exported to {filename}{Style.RESET_ALL}")
        return filename
    
    def export_to_csv(self, filename: str = None) -> str:
        """
        Export scraped data to CSV file.
        
        Args:
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to the exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crawled_data_{timestamp}.csv"
        
        # Flatten the data for CSV export
        flattened_data = []
        for item in self.scraped_data:
            flattened_item = {
                'url': item['url'],
                'title': item['title'],
                'num_headings': len(item['headings']),
                'num_paragraphs': len(item['paragraphs']),
                'num_links': len(item['links']),
                'num_images': len(item['images']),
                'scraped_at': item['scraped_at']
            }
            flattened_data.append(flattened_item)
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"{Fore.GREEN}Data exported to {filename}{Style.RESET_ALL}")
        return filename
    
    def get_statistics(self) -> Dict:
        """
        Get crawling statistics.
        
        Returns:
            Dict: Statistics about the crawled data
        """
        if not self.scraped_data:
            return {}
        
        stats = {
            'total_pages': len(self.scraped_data),
            'total_links': sum(len(item['links']) for item in self.scraped_data),
            'total_images': sum(len(item['images']) for item in self.scraped_data),
            'total_headings': sum(len(item['headings']) for item in self.scraped_data),
            'total_paragraphs': sum(len(item['paragraphs']) for item in self.scraped_data),
            'unique_urls': len(set(item['url'] for item in self.scraped_data))
        }
        
        return stats
    
    def print_statistics(self):
        """Print crawling statistics in a formatted way."""
        stats = self.get_statistics()
        
        print(f"\n{Fore.YELLOW}=== CRAWLING STATISTICS ==={Style.RESET_ALL}")
        print(f"Total pages crawled: {stats.get('total_pages', 0)}")
        print(f"Total links found: {stats.get('total_links', 0)}")
        print(f"Total images found: {stats.get('total_images', 0)}")
        print(f"Total headings found: {stats.get('total_headings', 0)}")
        print(f"Total paragraphs found: {stats.get('total_paragraphs', 0)}")
        print(f"Unique URLs: {stats.get('unique_urls', 0)}")


def main():
    """
    Main function to demonstrate the web crawler usage.
    """
    print(f"{Fore.CYAN}=== WEB CRAWLER ==={Style.RESET_ALL}")
    print("This is a demonstration of the web crawler.")
    print("Modify the URL below to crawl your desired website.\n")
    
    # Example usage - replace with your target URL
    # Choose one of these examples or add your own:
    
    # Option 1: News site
    # base_url = "https://news.ycombinator.com"
    
    # Option 2: Blog site  
    # base_url = "https://blog.python.org"
    
    # Option 3: E-commerce demo site
    # base_url = "https://books.toscrape.com"
    
    # Option 4: Wikipedia (be very careful with max_pages!)
    # base_url = "https://en.wikipedia.org/wiki/Web_scraping"
    
    # Option 5: Your custom URL
    # base_url = "https://example.com"
    
    # Demo: Using Google.com
    base_url = "https://www.google.com"
    
    try:
        # Create crawler instance
        crawler = WebCrawler(
            base_url=base_url,
            max_pages=5,  # Limit to 5 pages for demo
            delay=1.0     # 1 second delay between requests
        )
        
        # Start crawling
        data = crawler.crawl()
        
        # Print statistics
        crawler.print_statistics()
        
        # Export data
        json_file = crawler.export_to_json()
        csv_file = crawler.export_to_csv()
        
        print(f"\n{Fore.GREEN}Crawling completed successfully!{Style.RESET_ALL}")
        print(f"JSON export: {json_file}")
        print(f"CSV export: {csv_file}")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Crawling failed: {str(e)}")


if __name__ == "__main__":
    main()
