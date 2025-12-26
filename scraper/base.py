from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict


class ReviewScraper(ABC):
    """
    Base class that defines the interface for all review scrapers.
    """

    @abstractmethod
    def fetch_reviews(
        self,
        company: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Fetch reviews between start_date and end_date for a company.
        Must return a list of dicts.
        """
        pass