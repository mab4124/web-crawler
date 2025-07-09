#include "Crawler.h"
#include "Downloader.h"
#include "HTMLParser.h"
#include <iostream>
#include <nlohmann/json.hpp> // use for json or else simple file writing

Crawler::Crawler(const std::string& url, int depth, int threads)
    : rootUrl(url), maxDepth(depth), threadCount(threads)
{
    urlQueue.push({url, 0});
    visited.insert(url);
    outFile.open("data/sitemap.json");
    outFile << "[\n"; // start JSON array
}

void Crawler::start() {
    ThreadPool pool(threadCount);

    while (!urlQueue.empty()) {
        queueMutex.lock();
        auto [currentUrl, currentDepth] = urlQueue.front();
        urlQueue.pop();
        queueMutex.unlock();

        pool.enqueue([this, currentUrl, currentDepth]() {
            this->processUrl(currentUrl, currentDepth);
        });
    }

    pool.waitFinished();
    outFile << "{}\n]"; // close json array
    outFile.close();
}

void Crawler::processUrl(const std::string& url, int depth) {
    Downloader downloader;
    std::string html = downloader.fetchHTML(url);

    HTMLParser parser;
    auto links = parser.extractLinks(html, url);
    auto title = parser.extractTitle(html);

    outputMutex.lock();
    outFile << "  {\"url\":\"" << url << "\", \"title\":\"" << title << "\"},\n";
    outputMutex.unlock();

    if (depth + 1 > maxDepth) return;

    for (const auto& link : links) {
        visitedMutex.lock();
        if (visited.find(link) == visited.end()) {
            visited.insert(link);
            queueMutex.lock();
            urlQueue.push({link, depth + 1});
            queueMutex.unlock();
        }
        visitedMutex.unlock();
    }
}
