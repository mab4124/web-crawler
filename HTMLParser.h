#pragma once
#include <string>
#include <vector>

class HTMLParser {
public:
    std::vector<std::string> extractLinks(const std::string& html, const std::string& baseUrl);
    std::string extractTitle(const std::string& html);
};
