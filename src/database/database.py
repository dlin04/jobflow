import sqlite3
import logging
from src.database.models import Job


class Database:
    def __init__(self, db_path: str = "data/jobflow.db"):
        self.db_path = db_path

    def init_db(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                job_type TEXT CHECK(job_type IN ('intern', 'new_grad')),
                application_url TEXT UNIQUE
            )
        """
        )

        con.commit()
        con.close()

    def add_job(self, job: Job):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        try:
            cur.execute(
                "SELECT 1 FROM jobs WHERE application_url = ?", (job.application_url,)
            )
            if cur.fetchone() is not None:
                return

            cur.execute(
                "INSERT INTO jobs (title, company, job_type, application_url) VALUES (?, ?, ?, ?)",
                (job.title, job.company, job.job_type, job.application_url),
            )
            con.commit()
        except sqlite3.Error as e:
            logging.error(f"Database insert failed: {e}")
        finally:
            con.close()
