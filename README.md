# WebCrawler - Multi-threaded C++ Website Crawler

## Overview

This project is a high-performance, multi-threaded web crawler implemented in C++. It starts from a user-provided URL and recursively fetches linked pages up to a specified depth. The crawler extracts page titles and URLs, then outputs a structured sitemap in JSON format. It uses libcurl for HTTP requests and supports concurrency for efficient crawling.

---

## Features

- Multi-threaded crawling for faster web traversal  
- HTTP/HTTPS support via libcurl  
- Recursive link extraction and depth control  
- Extracts page titles and URLs  
- Outputs structured sitemap as JSON file  
- Robust error handling and retry mechanism  
- Command-line interface (CLI) for easy configuration  
- Modular, clean C++17 codebase  

---

## Getting Started

### Prerequisites

- C++17 compatible compiler (g++ or clang++)  
- CMake (version 3.10 or above)  
- Make (or compatible build system)  
- libcurl development libraries installed  

#### On Ubuntu/Debian:

```bash
sudo apt-get install libcurl4-openssl-dev
