import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from .base import ReviewScraper
from .utils import HEADERS


class CapterraScraper(ReviewScraper):

    def __init__(self):
        # example:
        # https://www.capterra.com/p/152234/Notion/reviews/
        self.base_url = "https://www.capterra.com/p/{product_id}/reviews/?page={page}"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_reviews(
        self,
        product_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:

        all_reviews = []
        page = 1

        while True:
            url = self.base_url.format(product_id=product_id, page=page)
            print(f"Fetching: {url}")

            response = self.session.get(url)
            print("Status:", response.status_code, "HTML length:", len(response.text))
        

            if response.status_code != 200:
                print("No more pages or product not found.")
                break

            soup = BeautifulSoup(response.text, "lxml")

            review_cards = soup.select("div[data-testid='review-card']")
            if not review_cards:
                print("No more reviews found.")
                break

            for card in review_cards:

                # --- DATE ---
                date_tag = card.select_one("span[data-testid='review-date']")
                if not date_tag:
                    continue

                date = datetime.strptime(date_tag.text.strip(), "%B %d, %Y").date()

                if not (start_date.date() <= date <= end_date.date()):
                    continue

                # --- TITLE ---
                title_tag = card.select_one("h3")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # --- BODY ---
                body_tag = card.select_one("p")
                body = body_tag.get_text(" ", strip=True) if body_tag else ""

                # --- RATING ---
                rating = len(card.select("svg[aria-label='Filled star']"))

                # --- REVIEWER ---
                reviewer_tag = card.select_one("span[data-testid='reviewer-name']")
                reviewer = reviewer_tag.get_text(strip=True) if reviewer_tag else ""

                all_reviews.append({
                    "title": title,
                    "review": body,
                    "date": str(date),
                    "rating": rating,
                    "reviewer": reviewer,
                    "source": "Capterra"
                })

            page += 1

        return all_reviews