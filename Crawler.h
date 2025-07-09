#pragma once
#include <string>
#include <queue>
#include <set>
#include <mutex>
#include <fstream>
#include "ThreadPool.h"

class Crawler {
private:
    std::string rootUrl;
    int maxDepth;
    int threadCount;

    std::queue<std::pair<std::string, int>> urlQueue;
    std::set<std::string> visited;
    std::mutex queueMutex;
    std::mutex visitedMutex;
    std::mutex outputMutex;

    std::ofstream outFile;

    void processUrl(const std::string& url, int depth);

public:
    Crawler(const std::string& url, int depth, int threads);
    void start();
};
