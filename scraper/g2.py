import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from .base import ReviewScraper
from .utils import HEADERS


class G2Scraper(ReviewScraper):

    def __init__(self):
        self.base_url = "https://www.g2.com/products/{company}/reviews?page={page}"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)



    def fetch_reviews(
        self,
        company: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:

        all_reviews = []
        page = 1

        while True:
            url = self.base_url.format(company=company, page=page)
            print(f"Fetching: {url}")

            response = requests.get(url, headers=HEADERS)
            print("Status:", response.status_code, "HTML length:", len(response.text))

            # stop if page fails
            if response.status_code != 200:
                print("No more pages or company not found.")
                break

            soup = BeautifulSoup(response.text, "lxml")

            review_cards = soup.select("div.review-card")
            if not review_cards:
                print("No more reviews found.")
                break

            for card in review_cards:

                # --- DATE ---
                date_tag = card.select_one("time")
                if not date_tag or not date_tag.get("datetime"):
                    continue

                date = datetime.fromisoformat(date_tag["datetime"]).date()

                if not (start_date.date() <= date <= end_date.date()):
                    continue

                # --- TITLE ---
                title_tag = card.select_one("h3")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # --- BODY ---
                body_tag = card.select_one(" .review-body ")
                body = body_tag.get_text(strip=True) if body_tag else ""

                # --- RATING ---
                rating = len(card.select(".star.filled"))

                # --- REVIEWER ---
                reviewer_tag = card.select_one(".user-name")
                reviewer = reviewer_tag.get_text(strip=True) if reviewer_tag else ""

                all_reviews.append({
                    "title": title,
                    "review": body,
                    "date": str(date),
                    "rating": rating,
                    "reviewer": reviewer,
                    "source": "G2"
                })

            page += 1

        return all_reviews