import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from .base import ReviewScraper
from .utils import HEADERS


class TrustpilotScraper(ReviewScraper):

    def __init__(self):
        # Example: https://www.trustpilot.com/review/notion.so?page=1
        self.base_url = "https://www.trustpilot.com/review/{domain}?page={page}"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_reviews(
        self,
        domain: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:

        all_reviews = []
        page = 1

        while True:
            url = self.base_url.format(domain=domain, page=page)
            print(f"Fetching: {url}")

            response = self.session.get(url)

            print("Status:", response.status_code, "HTML length:", len(response.text))

            if response.status_code == 403:
                print("Access denied (403). Trustpilot may be blocking requests.")
                break

            if response.status_code != 200:
                print("Failed to fetch page:", response.status_code)
                break

            soup = BeautifulSoup(response.text, "lxml")

            # Try main selector
            review_cards = soup.select("section.styles_reviewCardInner__EwDq2")

            # Fallback selector
            if not review_cards:
                review_cards = soup.select("article")

            # If still none, stop
            if not review_cards:
                print("No more reviews found.")
                break

            for card in review_cards:

                # --- DATE ---
                date_tag = card.select_one("time")
                if not date_tag or not date_tag.get("datetime"):
                    continue

                try:
                    date = datetime.fromisoformat(date_tag["datetime"]).date()
                except Exception:
                    continue

                if not (start_date.date() <= date <= end_date.date()):
                    continue

                # --- TITLE ---
                title_tag = card.select_one("h2, h3")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # --- BODY ---
                body_tag = card.select_one("p")
                body = body_tag.get_text(" ", strip=True) if body_tag else ""

                # --- RATING ---
                rating_tag = card.select_one("img[alt$='stars']")
                rating = None
                if rating_tag:
                    rating = rating_tag["alt"].split(" ")[0]

                # --- REVIEWER ---
                author_tag = card.select_one("span.typography_heading-xxs")
                reviewer = author_tag.get_text(strip=True) if author_tag else ""

                all_reviews.append({
                    "title": title,
                    "review": body,
                    "date": str(date),
                    "rating": rating,
                    "reviewer": reviewer,
                    "source": "Trustpilot"
                })

            page += 1

        return all_reviews