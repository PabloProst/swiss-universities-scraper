from scraper import scrape_universities
from pathlib import Path

def main():
    df = scrape_universities()

    output_path = Path("data/raw/swiss_universities.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False, encoding="utf-8")
    print("CSV generated successfully.")

if __name__ == "__main__":
    main()
