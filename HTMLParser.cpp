#include "HTMLParser.h"
#include <regex>

std::vector<std::string> HTMLParser::extractLinks(const std::string& html, const std::string& baseUrl) {
    std::vector<std::string> links;
    std::regex hrefRegex("<a\\s+(?:[^>]*?\\s+)?href=[\"']([^\"']*)", std::regex::icase);
    auto linksBegin = std::sregex_iterator(html.begin(), html.end(), hrefRegex);
    auto linksEnd = std::sregex_iterator();

    for (std::sregex_iterator i = linksBegin; i != linksEnd; ++i) {
        links.push_back(i->str(1));
    }
    return links;
}

std::string HTMLParser::extractTitle(const std::string& html) {
    std::regex titleRegex("<title>(.*?)</title>", std::regex::icase);
    std::smatch match;
    if (std::regex_search(html, match, titleRegex)) {
        return match[1];
    }
    return "";
}
