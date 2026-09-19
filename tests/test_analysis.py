#!/usr/bin/env python3
"""Unit tests for Dream Book Shop Data Analysis Application."""

import csv
import os
import tempfile
import unittest
from typing import List

from src.models import Book, AnalysisResult
from src.data_source import CSVDataSource
from src.strategies import (
    MissingIsbnAnalysis,
    TopAuthorsAnalysis,
    PublicationTrendAnalysis,
    LanguageDistributionAnalysis,
    PublisherCountAnalysis,
    YearLanguageAnalysis
)


class TestBookValidation(unittest.TestCase):
    """Tests for Book entity validation."""
    
    def test_book_with_valid_year(self) -> None:
        """Test book creation with valid year."""
        book = Book("Test Title", "Test Author", "Test Publisher", "1234567890", "English", "2023")
        self.assertEqual(book.year, 2023)
    
    def test_book_with_missing_year_empty_string(self) -> None:
        """Test book creation with empty year string defaults safely."""
        book = Book("Test Title", "Test Author", "Test Publisher", "1234567890", "English", "")
        self.assertIsNone(book.year)
    
    def test_book_with_missing_year_none(self) -> None:
        """Test book creation with None year defaults safely."""
        book = Book("Test Title", "Test Author", "Test Publisher", "1234567890", "English", None)
        self.assertIsNone(book.year)
    
    def test_book_with_invalid_year(self) -> None:
        """Test book creation with invalid year string defaults safely."""
        book = Book("Test Title", "Test Author", "Test Publisher", "1234567890", "English", "invalid")
        self.assertIsNone(book.year)
    
    def test_book_with_out_of_range_year(self) -> None:
        """Test book creation with out of range year defaults safely."""
        book = Book("Test Title", "Test Author", "Test Publisher", "1234567890", "English", "1800")
        self.assertIsNone(book.year)
        
        book2 = Book("Test Title", "Test Author", "Test Publisher", "1234567890", "English", "2200")
        self.assertIsNone(book2.year)
    
    def test_book_has_isbn_true(self) -> None:
        """Test has_isbn returns True for valid ISBN."""
        book = Book("Test", "Author", "Publisher", "1234567890", "English", "2023")
        self.assertTrue(book.has_isbn())
    
    def test_book_has_isbn_false_empty(self) -> None:
        """Test has_isbn returns False for empty ISBN."""
        book = Book("Test", "Author", "Publisher", "", "English", "2023")
        self.assertFalse(book.has_isbn())
    
    def test_book_has_isbn_false_none(self) -> None:
        """Test has_isbn returns False for None ISBN."""
        book = Book("Test", "Author", "Publisher", None, "English", "2023")  # type: ignore
        self.assertFalse(book.has_isbn())


class TestCSVDataSource(unittest.TestCase):
    """Tests for CSVDataSource."""
    
    def setUp(self) -> None:
        """Create a temporary CSV file with test data."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='')
        self.temp_file.close()
        
        # Write test CSV data
        test_data = [
            ['book', 'author', 'publication date', 'language', 'book publisher', 'ISBN', 'BNB id'],
            ['Book 1', 'Author A', '2023', 'English', 'Publisher X', '1111111111', 'GBC001'],
            ['Book 2', 'Author B', '2022', 'Spanish', 'Publisher Y', '', 'GBC002'],
            ['Book 3', 'Author A', '2023', 'English', 'Publisher X', '3333333333', 'GBC003'],
            ['Book 4', 'Author C', '2021', 'French', 'Publisher Z', '4444444444', 'GBC004'],
            ['Book 5', 'Author B', '2023', 'English', 'Publisher Y', '5555555555', 'GBC005'],
        ]
        
        with open(self.temp_file.name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)
    
    def tearDown(self) -> None:
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_returns_correct_number_of_books(self) -> None:
        """Test that load() returns correct number of Book objects."""
        data_source = CSVDataSource(self.temp_file.name, max_rows=100)
        books = data_source.load()
        
        self.assertEqual(len(books), 5)
        for book in books:
            self.assertIsInstance(book, Book)


class TestMissingIsbnAnalysis(unittest.TestCase):
    """Tests for MissingIsbnAnalysis strategy."""
    
    def test_analyse_reports_correct_percentage(self) -> None:
        """Test that analyse() correctly reports 20% missing ISBN for 2 out of 10 books."""
        books: List[Book] = []
        
        # Create 10 books, 2 without ISBN
        for i in range(10):
            isbn = "" if i < 2 else f"ISBN{i:010d}"
            books.append(Book(f"Book {i}", f"Author {i}", "Publisher", isbn, "English", "2023"))
        
        strategy = MissingIsbnAnalysis()
        result = strategy.analyse(books)
        
        # Check summary contains correct percentage
        self.assertIn("20.0%", result.summary)
        self.assertIn("Books missing ISBN: 2", result.summary)
        self.assertIn("Books with ISBN: 8", result.summary)
        
        # Check chart data
        self.assertEqual(result.chart_data['values'][0], 8)  # Has ISBN
        self.assertEqual(result.chart_data['values'][1], 2)  # Missing ISBN


class TestTopAuthorsAnalysis(unittest.TestCase):
    """Tests for TopAuthorsAnalysis strategy."""
    
    def test_analyse_returns_correct_top_5_order(self) -> None:
        """Test that analyse() returns top 5 authors in exact descending order."""
        books: List[Book] = []
        
        # Author counts: Author A=5, Author B=3, Author C=2, Author D=1, Author E=1, Author F=1
        author_counts = {
            "Author A": 5,
            "Author B": 3,
            "Author C": 2,
            "Author D": 1,
            "Author E": 1,
            "Author F": 1,
        }
        
        for author, count in author_counts.items():
            for i in range(count):
                books.append(Book(f"Book {author} {i}", author, "Publisher", f"ISBN{i}", "English", "2023"))
        
        strategy = TopAuthorsAnalysis()
        result = strategy.analyse(books)
        
        # Extract authors from chart data (top 5)
        top_authors = result.chart_data['labels']
        top_counts = result.chart_data['values']
        
        # Verify exact order and counts
        self.assertEqual(top_authors[0], "Author A")
        self.assertEqual(top_counts[0], 5)
        self.assertEqual(top_authors[1], "Author B")
        self.assertEqual(top_counts[1], 3)
        self.assertEqual(top_authors[2], "Author C")
        self.assertEqual(top_counts[2], 2)
        self.assertEqual(top_authors[3], "Author D")
        self.assertEqual(top_counts[3], 1)
        self.assertEqual(top_authors[4], "Author E")
        self.assertEqual(top_counts[4], 1)
        
        # Verify only 5 authors returned
        self.assertEqual(len(top_authors), 5)


class TestPublicationTrendAnalysis(unittest.TestCase):
    """Tests for PublicationTrendAnalysis strategy."""
    
    def test_analyse_counts_books_per_year(self) -> None:
        """Test that analyse() correctly counts books per year."""
        books: List[Book] = []
        
        # Add books with various years
        year_counts = {2020: 2, 2021: 3, 2022: 1, 2023: 4}
        for year, count in year_counts.items():
            for i in range(count):
                books.append(Book(f"Book {year}-{i}", "Author", "Publisher", f"ISBN{i}", "English", str(year)))
        
        strategy = PublicationTrendAnalysis()
        result = strategy.analyse(books)
        
        # Check chart data
        labels = result.chart_data['labels']
        values = result.chart_data['values']
        
        self.assertEqual(labels, ['2020', '2021', '2022', '2023'])
        self.assertEqual(values, [2, 3, 1, 4])


class TestLanguageDistributionAnalysis(unittest.TestCase):
    """Tests for LanguageDistributionAnalysis strategy."""
    
    def test_analyse_calculates_correct_percentages(self) -> None:
        """Test that analyse() calculates correct language percentages."""
        books: List[Book] = []
        
        # English: 6, Spanish: 3, French: 1 (total 10)
        languages = {"English": 6, "Spanish": 3, "French": 1}
        for lang, count in languages.items():
            for i in range(count):
                books.append(Book(f"Book {lang} {i}", "Author", "Publisher", f"ISBN{i}", lang, "2023"))
        
        strategy = LanguageDistributionAnalysis()
        result = strategy.analyse(books)
        
        # Check percentages
        percentages = result.chart_data['percentages']
        self.assertAlmostEqual(percentages[0], 60.0, places=1)  # English 60%
        self.assertAlmostEqual(percentages[1], 30.0, places=1)  # Spanish 30%
        self.assertAlmostEqual(percentages[2], 10.0, places=1)  # French 10%


class TestYearLanguageAnalysis(unittest.TestCase):
    """Tests for YearLanguageAnalysis strategy."""
    
    def test_analyse_cross_tabulates_year_and_language(self) -> None:
        """Test that analyse() correctly cross-tabulates year and language."""
        books: List[Book] = []
        
        # 2022: English=2, Spanish=1
        # 2023: English=3, French=2
        test_data = [
            (2022, "English"), (2022, "English"), (2022, "Spanish"),
            (2023, "English"), (2023, "English"), (2023, "English"),
            (2023, "French"), (2023, "French"),
        ]
        
        for year, lang in test_data:
            books.append(Book(f"Book {year}-{lang}", "Author", "Publisher", "ISBN", lang, str(year)))
        
        strategy = YearLanguageAnalysis()
        result = strategy.analyse(books)
        
        chart_data = result.chart_data
        years = chart_data['years']
        languages = chart_data['languages']
        data = chart_data['data']
        
        self.assertEqual(years, ['2022', '2023'])
        self.assertEqual(sorted(languages), ['English', 'French', 'Spanish'])
        
        # Check 2022 data
        self.assertEqual(data['English'][0], 2)
        self.assertEqual(data['Spanish'][0], 1)
        self.assertEqual(data['French'][0], 0)
        
        # Check 2023 data
        self.assertEqual(data['English'][1], 3)
        self.assertEqual(data['French'][1], 2)
        self.assertEqual(data['Spanish'][1], 0)


if __name__ == '__main__':
    unittest.main()