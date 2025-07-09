#!/usr/bin/env python3
"""
Advanced Web Crawler Example
This script demonstrates advanced features of the web crawler.
"""

from web_crawler import WebCrawler
from colorama import Fore, Style, init
import argparse
import sys
import os

# Initialize colorama
init()

def crawl_news_site():
    """Example: Crawl a news website and extract article data."""
    print(f"{Fore.CYAN}=== NEWS SITE CRAWLER EXAMPLE ==={Style.RESET_ALL}")
    
    # Example with a news site (replace with actual news site)
    base_url = "https://news.ycombinator.com"
    
    crawler = WebCrawler(
        base_url=base_url,
        max_pages=10,
        delay=2.0  # Be respectful with delay
    )
    
    # Crawl the site
    data = crawler.crawl()
    
    # Export results
    json_file = crawler.export_to_json("news_data.json")
    csv_file = crawler.export_to_csv("news_data.csv")
    
    # Print statistics
    crawler.print_statistics()
    
    return data

def crawl_ecommerce_site():
    """Example: Crawl an e-commerce site for product data."""
    print(f"{Fore.CYAN}=== E-COMMERCE CRAWLER EXAMPLE ==={Style.RESET_ALL}")
    
    # Example with an e-commerce site
    base_url = "https://books.toscrape.com"
    
    crawler = WebCrawler(
        base_url=base_url,
        max_pages=20,
        delay=1.5
    )
    
    # Crawl the site
    data = crawler.crawl()
    
    # Export results
    json_file = crawler.export_to_json("ecommerce_data.json")
    csv_file = crawler.export_to_csv("ecommerce_data.csv")
    
    # Print statistics
    crawler.print_statistics()
    
    return data

def crawl_blog_site():
    """Example: Crawl a blog site for article content."""
    print(f"{Fore.CYAN}=== BLOG CRAWLER EXAMPLE ==={Style.RESET_ALL}")
    
    # Example with a blog site
    base_url = "https://blog.python.org"
    
    crawler = WebCrawler(
        base_url=base_url,
        max_pages=15,
        delay=1.0
    )
    
    # Crawl the site
    data = crawler.crawl()
    
    # Export results
    json_file = crawler.export_to_json("blog_data.json")
    csv_file = crawler.export_to_csv("blog_data.csv")
    
    # Print statistics
    crawler.print_statistics()
    
    return data

def custom_crawler():
    """Interactive crawler where user can input custom parameters."""
    print(f"{Fore.CYAN}=== CUSTOM CRAWLER ==={Style.RESET_ALL}")
    
    # Get user input
    base_url = input("Enter the URL to crawl: ").strip()
    
    if not base_url:
        print(f"{Fore.RED}No URL provided. Exiting.{Style.RESET_ALL}")
        return
    
    # Add protocol if missing
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url
    
    try:
        max_pages = int(input("Enter max pages to crawl (default 10): ") or "10")
        delay = float(input("Enter delay between requests in seconds (default 1.0): ") or "1.0")
    except ValueError:
        print(f"{Fore.RED}Invalid input. Using default values.{Style.RESET_ALL}")
        max_pages = 10
        delay = 1.0
    
    # Create and run crawler
    crawler = WebCrawler(
        base_url=base_url,
        max_pages=max_pages,
        delay=delay
    )
    
    try:
        data = crawler.crawl()
        
        # Ask user about export format
        export_choice = input("Export format (json/csv/both) [default: both]: ").strip().lower()
        
        if export_choice in ['json', 'both', '']:
            json_file = crawler.export_to_json()
            print(f"JSON data saved to: {json_file}")
        
        if export_choice in ['csv', 'both', '']:
            csv_file = crawler.export_to_csv()
            print(f"CSV data saved to: {csv_file}")
        
        # Print statistics
        crawler.print_statistics()
        
    except Exception as e:
        print(f"{Fore.RED}Error during crawling: {str(e)}{Style.RESET_ALL}")

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Advanced Web Crawler Examples')
    parser.add_argument('--mode', choices=['news', 'ecommerce', 'blog', 'custom'], 
                       default='custom', help='Crawling mode')
    parser.add_argument('--url', help='URL to crawl (for custom mode)')
    parser.add_argument('--max-pages', type=int, default=10, help='Maximum pages to crawl')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests')
    
    args = parser.parse_args()
    
    if args.mode == 'news':
        crawl_news_site()
    elif args.mode == 'ecommerce':
        crawl_ecommerce_site()
    elif args.mode == 'blog':
        crawl_blog_site()
    elif args.mode == 'custom':
        if args.url:
            # Use command-line provided URL
            crawler = WebCrawler(
                base_url=args.url,
                max_pages=args.max_pages,
                delay=args.delay
            )
            data = crawler.crawl()
            crawler.export_to_json()
            crawler.export_to_csv()
            crawler.print_statistics()
        else:
            # Interactive mode
            custom_crawler()

if __name__ == "__main__":
    main()
