from abc import ABC, abstractmethod
from src.database.models import Job

class BaseScraper(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def scrape(self) -> list[Job]:
        pass