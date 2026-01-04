import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

URL = "https://en.wikipedia.org/wiki/List_of_universities_in_Switzerland"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

def scrape_universities_basic():
    """Scrape only the basic info table from Wikipedia."""
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table", class_="wikitable")
    info_table = tables[0]  # basic info table

    # Extract headers from the first row only
    headers = [th.text.strip() for th in info_table.find("tr").find_all("th")]

    rows = []
    for tr in info_table.find_all("tr")[1:]:
        cells = tr.find_all("td")
        if not cells:
            continue
        row = [cell.text.strip() for cell in cells]
        # Ensure row has same number of columns as headers
        while len(row) < len(headers):
            row.append(None)
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)

    # Keep only relevant columns
    columns_needed = ['Institution', 'Abbreviation', 'Location', 'Founded', 'Language', 'Type', 'Enrollment']
    df = df[columns_needed]

    # Rename first column to 'University'
    df.rename(columns={'Institution': 'University'}, inplace=True)

    # Strip spaces from column names
    df.columns = [col.strip() for col in df.columns]

    return df
    
def main():
    df = scrape_universities_basic()
    
    # Ensure folder exists
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    
    # Save CSV
    df.to_csv("data/raw/swiss_universities_basic.csv", index=False, encoding="utf-8")
    print("CSV with basic university info generated successfully!")
    print(df.head())

if __name__ == "__main__":
    main()
