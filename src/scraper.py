import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_universities_in_Switzerland"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

def fetch_page(url: str) -> BeautifulSoup:
    """Download Wikipedia page and return parsed HTML."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def extract_universities(table) -> List[Dict[str, str]]:
    """Extract university data from HTML table."""
    universities = []

    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")

        if not columns:
            continue

        uni_name = columns[0].text.strip()
        location = columns[1].text.strip() if len(columns) > 1 else "Unknown"

        universities.append({
            "University": uni_name,
            "Location": location,
        })

    return universities

def scrape_universities() -> pd.DataFrame:
    """Main scraping pipeline."""
    soup = fetch_page(WIKI_URL)
    tables = soup.find_all("table", class_="wikitable")
    universities_table = tables[1]
    data = extract_universities(universities_table)
    return pd.DataFrame(data)
