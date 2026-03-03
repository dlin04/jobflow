import json
import logging
import requests
from bs4 import BeautifulSoup
from src.scrapers.base_scraper import BaseScraper
from src.database.database import Database
from src.database.models import Job


class YCScraper(BaseScraper):
    URL = "https://www.ycombinator.com/internships"

    def __init__(self, db: Database):
        super().__init__(name="YCombinator")
        self.db = db

    def scrape(self) -> list[Job]:
        try:
            response = requests.get(self.URL)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {self.URL}: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        data_div = soup.find(attrs={"data-page": True})
        if not data_div:
            logging.error("Could not find data-page attribute — page structure may have changed.")
            return []

        data = json.loads(data_div["data-page"])
        postings = data.get("props", {}).get("jobPostings", [])

        jobs = []
        for posting in postings:
            title = posting.get("title", "").strip()
            company = posting.get("companyName", "").strip()
            location = posting.get("location", "").strip()
            relative_url = posting.get("url", "")
            apply_url = "https://www.ycombinator.com" + relative_url if relative_url else ""

            if not title or not apply_url:
                continue

            if self.db.job_exists(apply_url):
                logging.info(f"Job already in DB: {title} at {company}, stopping.")
                return jobs

            jobs.append(Job(
                title=title,
                company=company,
                application_url=apply_url,
                job_type="intern",
                location=location,
            ))

        return jobs