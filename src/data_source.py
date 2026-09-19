import csv
from abc import ABC, abstractmethod
from typing import List

from src.models import Book


class IDataSource(ABC):
    """Abstract interface for data sources."""
    
    @abstractmethod
    def load(self) -> List[Book]:
        """Load books from the data source."""
        pass


class CSVDataSource(IDataSource):
    """CSV implementation of IDataSource."""
    
    def __init__(self, file_path: str, max_rows: int = 5000) -> None:
        self._file_path = file_path
        self._max_rows = max_rows
    
    def load(self) -> List[Book]:
        """Load up to max_rows books from CSV file."""
        books = []
        row_count = 0
        
        with open(self._file_path, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                if row_count >= self._max_rows:
                    break
                
                # Extract fields from CSV row (matching the dataset column names)
                title = row.get('book', '')
                author = row.get('author', '')
                publisher = row.get('book publisher', '')
                isbn = row.get('ISBN', '')
                language = row.get('language', '')
                year = row.get('publication date', '')
                
                book = Book(
                    title=title,
                    author=author,
                    publisher=publisher,
                    isbn=isbn,
                    language=language,
                    year=year
                )
                
                books.append(book)
                row_count += 1
        
        return books