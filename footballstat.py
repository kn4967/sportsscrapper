from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

def scrape_football_stats():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.pro-football-reference.com/"
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "all_passing")))

    # Locate the table by id
    table = driver.find_element(By.ID, "all_passing")  # Replace 'all_passing' with the correct ID
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Initialize data container
    data = []

    # Iterate through each row, extracting data
    for row in rows:
        if 'thead' in row.get_attribute('class'):  # Skip header row
            continue
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:  # This checks that it's a data row, not a header or empty row
            data.append({
                "Player": cols[0].text,
                "Date": cols[1].text,
                "Team": cols[2].text,
                "Opponent": cols[4].text,
                "Outcome": cols[5].text,
                "Cmp": cols[6].text,
                "Att": cols[7].text,
                "Yds": cols[8].text,
                "TD": cols[9].text,
                "Int": cols[10].text,
                "Rate": cols[11].text
            })

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('football_data.csv', index=False)

    # Close the driver
    driver.quit()
    return df  # Make sure to return the DataFrame if you want to use it outside this function

# Call the function
scrape_football_stats()
