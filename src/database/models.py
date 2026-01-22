from dataclasses import dataclass
from typing import Literal


@dataclass
class Job:
    title: str
    company: str
    application_url: str
    job_type: Literal["intern", "new_grad"]

    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "application_url": self.application_url,
            "job_type": self.job_type,
        }
