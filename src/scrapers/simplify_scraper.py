import requests
import logging
from bs4 import BeautifulSoup
from src.scrapers.base_scraper import BaseScraper
from src.database.database import Database
from src.database.models import Job

MAX_AGE_DAYS = 14


class SimplifyScraper(BaseScraper):
    # scraper for simplifyjobs github repository
    URLS = {
        "intern": "https://github.com/SimplifyJobs/Summer2026-Internships",
        "new_grad": "https://github.com/SimplifyJobs/New-Grad-Positions",
    }

    def __init__(self, db: Database):
        super().__init__(name="SimplifyJobs")
        self.db = db

    def _parse_age_days(self, age_str: str) -> int:
        age_str = age_str.strip()
        if age_str.endswith("d"):
            return int(age_str[:-1])
        return 0

    def _scrape_repo(self, url: str, job_type: str) -> list[Job]:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []
        last_company = ""
        tables = soup.find_all("table")
        job_table = tables[1]
        rows = job_table.find_all("tr")

        for row in rows[1:]:
            cols = row.find_all("td")
            age_str = cols[4].get_text(strip=True)
            if self._parse_age_days(age_str) >= MAX_AGE_DAYS:
                logging.info(f"Reached jobs older than {MAX_AGE_DAYS} days, stopping.")
                break

            company = cols[0].get_text(strip=True)
            if company == "↳":
                company = last_company
            else:
                last_company = company
            title = cols[1].get_text(strip=True)
            details = cols[2].find("details")
            if details:
                location = ", ".join(
                    loc.strip()
                    for loc in details.get_text(separator="\n").split("\n")
                    if loc.strip() and "location" not in loc.lower()
                )
            else:
                location = cols[2].get_text(strip=True)

            apply_anchor = cols[3].find("a")
            if not apply_anchor:
                continue
            apply_url = apply_anchor["href"]

            if self.db.job_exists(apply_url):
                logging.info(f"Job already in DB: {title} at {company}, stopping.")
                break

            jobs.append(Job(
                title=title,
                company=company,
                application_url=apply_url,
                job_type=job_type,
                location=location,
            ))
        return jobs

    def scrape(self) -> list[Job]:
        jobs = []
        for job_type, url in self.URLS.items():
            jobs.extend(self._scrape_repo(url, job_type))
        return jobs