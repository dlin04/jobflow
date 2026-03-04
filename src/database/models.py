from dataclasses import dataclass
from typing import Literal


@dataclass
class Job:
    title: str
    company: str
    application_url: str
    job_type: Literal["intern", "new_grad"]
    location: str = ""
