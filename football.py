from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

def scrape_football():
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the URL of the page to scrape
    url = "https://www.pro-football-reference.com/"
    driver.get(url)

# Scrape the game summaries
    game_summaries = driver.find_elements(By.CLASS_NAME, "game_summary")
    games_data = []

# Get scrape date and time
    scrape_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Iterate through each game summary
    for summary in game_summaries:
        try:
            date_element = summary.find_element(By.CSS_SELECTOR, "tr.date td")
            game_date = date_element.text if date_element else scrape_date_time

            teams = summary.find_elements(By.CSS_SELECTOR, "tr:not(.date)")
            if len(teams) >= 2:  # Ensure there are two teams
                team1 = teams[0].find_element(By.TAG_NAME, "a").text
                score1 = teams[0].find_element(By.CLASS_NAME, "right").text
                team2 = teams[1].find_element(By.TAG_NAME, "a").text
                score2 = teams[1].find_element(By.CLASS_NAME, "right").text

                game_info = {
                    'Date': game_date,
                    'Matchup': f"{team1} vs {team2}",
                    'Game Final Score': f"{score1}-{score2}",
                    'Scrape Date': scrape_date_time
                }
                games_data.append(game_info)
        except Exception as e:
            print(f"Error occurred: {e}")

# Convert data to pandas DataFrame
    df = pd.DataFrame(games_data)

# Display the DataFrame
    print(df)

# Save the DataFrame to a CSV file
    df.to_csv('football_data.csv', index=False)

# Close the driver
    driver.quit()
