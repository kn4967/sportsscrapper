import requests
from bs4 import BeautifulSoup
from robotexclusionrulesparser import RobotExclusionRulesParser
from urllib.parse import urljoin
import time

class PoliteCrawler:
    def __init__(self, start_url, user_agent):
        self.start_url = start_url
        self.user_agent = user_agent
        self.headers = {'User-Agent': user_agent}
        self.robot_parser = RobotExclusionRulesParser()
        self.delay = 10  # Default delay between requests in seconds
        self.visited_urls = set()  # Keep track of visited URLs

    def can_fetch(self, url):
        try:
            self.robot_parser.fetch(self.start_url + "/robots.txt")
            return self.robot_parser.is_allowed(self.user_agent, url)
        except Exception as e:
            print(f"Error fetching robots.txt: {e}")
            return False

    def crawl(self, url):
        if self.can_fetch(url):
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
        else:
            print("Crawling disallowed by robots.txt")

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        urls = [urljoin(self.start_url, link['href']) for link in links]
        return urls

    def run(self):
        urls_to_crawl = [self.start_url]

        while urls_to_crawl:
            url = urls_to_crawl.pop(0)  # Get the next URL to crawl
            if url not in self.visited_urls:
                html = self.crawl(url)
                if html:
                    new_urls = self.parse(html)
                    urls_to_crawl.extend(new_urls)  # Add new URLs to the list
                self.visited_urls.add(url)  # Mark this URL as visited
                print(f"Crawled URL: {url}")
                time.sleep(self.delay)  # Respect the delay between requests

if __name__ == "__main__":
    crawler = PoliteCrawler("https://www.imdb.com", "YourCrawlerName/1.0")
    crawler.run()