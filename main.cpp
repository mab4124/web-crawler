#include "Crawler.h"
#include <iostream>

int main() {
    std::string startUrl = "https://google.com"; // replace
    int maxDepth = 2;
    int threadCount = 4;

    Crawler crawler(startUrl, maxDepth, threadCount);
    crawler.start();

    std::cout << "Crawling completed. Sitemap saved to data/sitemap.json\n";
    return 0;
}
