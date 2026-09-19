from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class AnalysisResult:
    """Container for analysis results including summary text and chart data."""
    title: str
    summary: str
    chart_data: Dict[str, Any]
    chart_type: str


class Book:
    """Entity class representing a book record with encapsulated attributes."""
    
    def __init__(
        self,
        title: str,
        author: str,
        publisher: str,
        isbn: str,
        language: str,
        year: Optional[str] = None
    ) -> None:
        self._title = title.strip() if title else ""
        self._author = author.strip() if author else ""
        self._publisher = publisher.strip() if publisher else ""
        self._isbn = isbn.strip() if isbn else ""
        self._language = language.strip() if language else ""
        self._year = self._validate_year(year)
    
    def _validate_year(self, year: Optional[str]) -> Optional[int]:
        """Validate and convert year to integer, handling missing/invalid values gracefully."""
        if year is None or year == "":
            return None
        try:
            year_int = int(year)
            if 1900 <= year_int <= 2100:
                return year_int
            return None
        except (ValueError, TypeError):
            return None
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def author(self) -> str:
        return self._author
    
    @property
    def publisher(self) -> str:
        return self._publisher
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @property
    def language(self) -> str:
        return self._language
    
    @property
    def year(self) -> Optional[int]:
        return self._year
    
    def has_isbn(self) -> bool:
        """Check if the book has a valid ISBN."""
        return bool(self._isbn and self._isbn.strip())
    
    def __repr__(self) -> str:
        return f"Book(title='{self._title}', author='{self._author}', year={self._year})"