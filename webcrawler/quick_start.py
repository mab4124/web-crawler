#!/usr/bin/env python3
"""
Quick Start Guide for Web Crawler
This script provides a simple way to get started with the web crawler.
"""

from web_crawler import WebCrawler
from colorama import Fore, Style, init

# Initialize colorama for colored output
init()

def demo_crawler():
    """
    Demo function showing how to use the web crawler.
    This uses a safe test site that allows scraping.
    """
    print(f"{Fore.CYAN}=== WEB CRAWLER QUICK START DEMO ==={Style.RESET_ALL}")
    print("This demo will crawl a safe test website.")
    print("You can modify the URL to crawl your desired website.\n")
    
    # Using httpbin.org as a safe test site
    base_url = "https://httpbin.org"
    
    print(f"Target URL: {base_url}")
    print(f"Max pages: 3")
    print(f"Delay between requests: 1.0 seconds\n")
    
    # Create crawler instance
    crawler = WebCrawler(
        base_url=base_url,
        max_pages=3,
        delay=1.0
    )
    
    try:
        # Start crawling
        print(f"{Fore.GREEN}Starting crawl...{Style.RESET_ALL}")
        data = crawler.crawl()
        
        # Show results
        print(f"\n{Fore.GREEN}Crawling completed!{Style.RESET_ALL}")
        
        # Print statistics
        crawler.print_statistics()
        
        # Export data
        json_file = crawler.export_to_json("demo_output.json")
        csv_file = crawler.export_to_csv("demo_output.csv")
        
        print(f"\n{Fore.YELLOW}Files created:{Style.RESET_ALL}")
        print(f"- JSON: {json_file}")
        print(f"- CSV: {csv_file}")
        print(f"- Log: crawler.log")
        
        # Show sample data
        if data:
            print(f"\n{Fore.YELLOW}Sample data from first page:{Style.RESET_ALL}")
            first_page = data[0]
            print(f"URL: {first_page['url']}")
            print(f"Title: {first_page['title']}")
            print(f"Number of headings: {len(first_page['headings'])}")
            print(f"Number of paragraphs: {len(first_page['paragraphs'])}")
            print(f"Number of links: {len(first_page['links'])}")
            
    except Exception as e:
        print(f"{Fore.RED}Error during crawling: {str(e)}{Style.RESET_ALL}")
        print("This might be due to network issues or site restrictions.")

def custom_url_demo():
    """
    Interactive demo where user can specify a custom URL.
    """
    print(f"{Fore.CYAN}=== CUSTOM URL CRAWLER ==={Style.RESET_ALL}")
    
    # Get user input
    custom_url = input("Enter a URL to crawl (or press Enter for default): ").strip()
    
    if not custom_url:
        print("Using default URL: https://example.com")
        custom_url = "https://example.com"
    
    # Add protocol if missing
    if not custom_url.startswith(('http://', 'https://')):
        custom_url = 'https://' + custom_url
    
    # Create crawler
    crawler = WebCrawler(
        base_url=custom_url,
        max_pages=2,  # Keep it small for demo
        delay=1.0
    )
    
    try:
        # Crawl and show results
        data = crawler.crawl()
        crawler.print_statistics()
        
        # Export with custom filename
        json_file = crawler.export_to_json("custom_crawl.json")
        csv_file = crawler.export_to_csv("custom_crawl.csv")
        
        print(f"\nData exported to {json_file} and {csv_file}")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.CYAN}Choose a demo:{Style.RESET_ALL}")
    print("1. Demo crawler with safe test site")
    print("2. Custom URL crawler")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        demo_crawler()
    elif choice == "2":
        custom_url_demo()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice. Running default demo...")
        demo_crawler()
