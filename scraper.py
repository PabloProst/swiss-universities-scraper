import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL
url = "https://en.wikipedia.org/wiki/List_of_universities_in_Switzerland"

# User-Agent to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all tables and select the second one
    tables = soup.find_all("table", class_="wikitable")
    table = tables[1] 
    
    universities = []

    # Iterate over rows, skipping the header
    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        
        if len(columns) > 0:
            # Extract name
            uni_name = columns[0].text.strip()
            
            # Extract location
            try:
                location = columns[1].text.strip()
            except IndexError:
                location = "Unknown"
            
            universities.append({
                "University": uni_name,
                "Location": location
            })
            print(f"Extracted: {uni_name}")

    # Save data to CSV
    df = pd.DataFrame(universities)
    df.to_csv("swiss_universities.csv", index=False, encoding="utf-8")
    print("Success: CSV file generated.")

else:
    print(f"Error: {response.status_code}")