#pragma once
#include <string>

class Downloader {
public:
    std::string fetchHTML(const std::string& url);
};
