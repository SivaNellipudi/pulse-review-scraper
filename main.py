from scraper.trustpilot import TrustpilotScraper
from scraper.g2 import G2Scraper
from scraper.capterra import CapterraScraper
from scraper.utils import parse_date
import json


def main():
    print("\nSelect Review Source:")
    print("1. Trustpilot")
    print("2. G2")
    print("3. Capterra")

    choice = input("\nEnter 1 / 2 / 3: ")

    start = parse_date(input("Enter start date (YYYY-MM-DD): "))
    end = parse_date(input("Enter end date (YYYY-MM-DD): "))

    reviews = []

    if choice == "1":
        domain = input("Enter company domain (example: notion.so): ")
        scraper = TrustpilotScraper()
        reviews = scraper.fetch_reviews(domain, start, end)
        filename = "trustpilot_reviews.json"

    elif choice == "2":
        company = input("Enter G2 company slug (example: notion): ")
        scraper = G2Scraper()
        reviews = scraper.fetch_reviews(company, start, end)
        filename = "g2_reviews.json"

    elif choice == "3":
        product_id = input("Enter Capterra product ID: ")
        scraper = CapterraScraper()
        reviews = scraper.fetch_reviews(product_id, start, end)
        filename = "capterra_reviews.json"

    else:
        print("Invalid choice")
        return

    print(f"\nTotal reviews fetched: {len(reviews)}")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {filename}")


if __name__ == "__main__":
    main()