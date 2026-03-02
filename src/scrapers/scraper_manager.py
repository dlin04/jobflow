import logging
from src.database.database import Database
from src.database.models import Job
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.simplify_scraper import SimplifyScraper


class ScraperManager:
    def __init__(self, db: Database):
        self.db = db
        self.scrapers: list[BaseScraper] = []
        self._register_scrapers()

    def _register_scrapers(self):
        self.scrapers.append(SimplifyScraper(self.db))
        # add more scrapers later on

    def run(self) -> list[Job]:
        all_jobs: list[Job] = []

        for scraper in self.scrapers:
            logging.info(f"Running scraper: {scraper.name}")
            try:
                jobs = scraper.scrape()
                all_jobs.extend(jobs)
            except Exception as e:
                logging.error(f"Scraper {scraper.name} failed: {e}")

        new_jobs: list[Job] = []
        for job in all_jobs:
            if self.db.add_job(job):
                new_jobs.append(job)

        logging.info(f"Saved {len(new_jobs)} new jobs out of {len(all_jobs)} scraped")
        return new_jobs