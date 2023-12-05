from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime


def scrape_basketball():
# Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the URL of the page to scrape
    url = "https://www.basketball-reference.com/"

# Use the driver to get the page
    driver.get(url)

# Wait for the specific element to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "game_summary"))
        )
    except Exception as e:
        print("Timed out waiting for page to load")
        driver.quit()

# Extract game data
    game_divs = driver.find_elements(By.CLASS_NAME, "game_summary")
    data = []
    scrape_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for game_div in game_divs:
        try:
            teams = game_div.find_elements(By.CSS_SELECTOR, ".teams tbody tr")
            if len(teams) >= 2:  # Ensure there are two teams (one game)
                team1 = teams[0].find_element(By.TAG_NAME, "a").text
                score1 = teams[0].find_element(By.CLASS_NAME, "right").text
                team2 = teams[1].find_element(By.TAG_NAME, "a").text
                score2 = teams[1].find_element(By.CLASS_NAME, "right").text
                data.append({"Game": f"{team1} vs {team2}", "Final Score": f"{score1}-{score2}",'Scrape Date': scrape_date_time})
        except Exception as e:
            print(f"Error occurred: {e}")

# Convert data to DataFrame
    df = pd.DataFrame(data)

# Display the DataFrame
    print(df)

# Save the DataFrame to a CSV file
    df.to_csv('basketball_data.csv', index=False)

# Close the driver
    driver.quit()
