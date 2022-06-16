from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions

class GoogleResult:
    def __init__(self, title, link, sublinks):
        self.title = title
        self.link = link
        self.sublinks = sublinks

    def add_sublink(self, link):
        self.sublinks.append(link)

    def __str__(self):
        return self.title + "\n" + self.link + "\n" + str(self.sublinks) + "\n"

class GoogleSearchResult:
    def __init__(self, results):
        self.results = results

    def add_result(self, result):
        self.results.append(result)

    def __str__(self):
        ans = ""
        for entry in self.results:
            ans += str(entry)
        return ans

#Doesn't include non alphanumeric characters however, it includes spaces and ampersan
def get_search_url(query):
    GOOGLE_URL = "https://www.google.com/search?q="
    ans = ""
    for character in query:
        if character == ' ':
            ans += '+'
        elif character == '&':
            ans += '%26'
        else:
            if character.isalnum():
                ans += character
    return GOOGLE_URL + ans

def get_links(query):
    url = get_search_url(query)

    options = ChromeOptions()
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(1.5)

    page_content = driver.page_source

    soup = BeautifulSoup(page_content, "html.parser")
    final_results = GoogleSearchResult([])
    
    results = soup.find_all("div", class_="hlcw0c")
    for result in results:
        link_container = result.find("div", class_="yuRUbf")
        if (link_container != None):
            title = link_container.find("h3").getText()
            link = link_container.find("a").get("href")
            sublinks_soup = result.find_all("div", class_="usJj9c")
            sublinks = []
            if sublinks_soup != None:
                for sublink_container in sublinks_soup:
                    header = sublink_container.find("h3")
                    sublinks.append((header.find("a").getText(), header.find("a").get("href")))
            final_results.add_result(GoogleResult(title, link, sublinks))
            
    results = soup.find_all("div", class_="g tF2Cxc")
    for result in results:
        link_container = result.find("div", class_="yuRUbf")
        if (link_container != None):
            title = link_container.find("h3").getText()
            link = link_container.find("a").get("href")
            final_results.add_result(GoogleResult(title, link, []))

    results = soup.find_all("div", class_="g")
    for result in results:
        temp = GoogleResult(None, None, [])
        link_containers = result.find_all("div", class_="yuRUbf")
        first_link = True
        sublinks = []
        for link_container in link_containers:
            if (link_container != None):
                title = link_container.find("h3").getText()
                link = link_container.find("a").get("href")
                if (len(link_containers) == 0):
                    temp.title = title
                    temp.link = link
                    final_results.add_result(temp)
                else:
                    if (first_link):
                        temp.link = link
                        temp.title = title
                    else:
                        temp.add_sublink((title, link))
                first_link = False
        final_results.add_result(temp)
    return final_results
    
print(get_links(input()))
