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

    def parse_most_popular(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        movie_list = []
        movie_items = soup.find_all('div', class_='ipc-metadata-list-summary-item__tc')
        
        for movie in movie_items:
            try:
                # Extract the ranking
                ranking = movie.find('div', class_='meter-const-ranking').get_text(strip=True).split(' ')[0]

                # Extract the title
                title = movie.find('h3', class_='ipc-title__text').get_text(strip=True)

                # Extract release year, duration, and rating category (e.g., 'R')
                metadata_items = movie.find_all('span', class_='cli-title-metadata-item')
                release_year = metadata_items[0].get_text(strip=True) if len(metadata_items) > 0 else None
                duration = metadata_items[1].get_text(strip=True) if len(metadata_items) > 1 else None
                rating_category = metadata_items[2].get_text(strip=True) if len(metadata_items) > 2 else None

                # Extract IMDb rating
                rating = movie.find('span', class_='ipc-rating-star--imdb').get_text(strip=True).split(' ')[0]

                # Append movie information to movie_list
                movie_data = {
                    'ranking': ranking,
                    'title': title,
                    'release_year': release_year,
                    'duration': duration,
                    'rating_category': rating_category,
                    'IMDb_rating': rating
                }
                movie_list.append(movie_data)

                # Print each movie's details
                print(f"Ranking: {ranking}, Title: {title}, Year: {release_year}, Duration: {duration}, Rating Category: {rating_category}, IMDb Rating: {rating}")

            except AttributeError as e:
                # This will catch any movies that don't have complete information and print an error message
                print(f"Missing data for a movie, skipping... Error: {e}")

        return movie_list

    def parse_top_movies(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        movie_list = []
        movie_items = soup.find_all('div', class_='ipc-metadata-list-summary-item__tc')

        for movie in movie_items:
            try:
                # Extract the ranking and title
                title_with_rank = movie.find('h3', class_='ipc-title__text').get_text(strip=True)
                ranking, title = title_with_rank.split('. ', 1)

                # Extract release year, duration, and rating category (e.g., 'R')
                metadata_items = movie.find_all('span', class_='cli-title-metadata-item')
                release_year = metadata_items[0].get_text(strip=True) if len(metadata_items) > 0 else None
                duration = metadata_items[1].get_text(strip=True) if len(metadata_items) > 1 else None
                rating_category = metadata_items[2].get_text(strip=True) if len(metadata_items) > 2 else None

                # Extract IMDb rating
                rating = movie.find('span', class_='ipc-rating-star--imdb').get_text(strip=True).split(' ')[0]

                # Append movie information to movie_list
                movie_data = {
                    'ranking': ranking,
                    'title': title,
                    'release_year': release_year,
                    'duration': duration,
                    'rating_category': rating_category,
                    'IMDb_rating': rating
                }
                movie_list.append(movie_data)

                # Print each movie's details
                print(f"Ranking: {ranking}, Title: {title}, Year: {release_year}, Duration: {duration}, Rating Category: {rating_category}, IMDb Rating: {rating}")

            except AttributeError as e:
                # Catch any movies that don't have complete information and print an error message
                print(f"Missing data for a movie, skipping... Error: {e}")

        return movie_list

    


    def find_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        relevant_links = []

        # Define the specific paths you're interested in
        relevant_paths = [
            "/chart/moviemeter/",
            "/calendar/",
            "/chart/top/"
        ]

        for link in links:
            href = link['href']
            if any(path in href for path in relevant_paths):
                full_url = urljoin(self.start_url, href)
                relevant_links.append(full_url)

        return relevant_links
    
    def run(self):
        urls_to_crawl = [self.start_url]

        while urls_to_crawl:
            url = urls_to_crawl.pop(0)
            if url not in self.visited_urls:
                html = self.crawl(url)
                if html:
                    # Determine which parsing function to use based on the URL
                    if "chart/moviemeter" in url:
                        self.parse_most_popular(html)
                    elif "chart/top" in url:
                        self.parse_top_movies(html)
                    # You can add more conditions here for other types of pages

                    new_urls = self.find_links(html)
                    urls_to_crawl.extend(new_urls)
                self.visited_urls.add(url)
                print(f"Crawled URL: {url}")
                time.sleep(self.delay)


if __name__ == "__main__":
    crawler = PoliteCrawler("https://www.imdb.com", "FriendlyCrawler/1.0")
    crawler.run()
