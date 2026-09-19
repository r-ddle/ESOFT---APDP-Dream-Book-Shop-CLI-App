from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Any, Tuple

from src.models import Book, AnalysisResult


class AnalysisStrategy(ABC):
    """Abstract interface for analysis strategies (Strategy Pattern)."""
    
    @abstractmethod
    def analyse(self, books: List[Book]) -> AnalysisResult:
        """Perform analysis on the list of books."""
        pass


class PublicationTrendAnalysis(AnalysisStrategy):
    """Count of books per year."""
    
    def analyse(self, books: List[Book]) -> AnalysisResult:
        year_counts: Dict[int, int] = defaultdict(int)
        
        for book in books:
            if book.year is not None:
                year_counts[book.year] += 1
        
        sorted_years = sorted(year_counts.items())
        
        summary_lines = ["Publication Trend Analysis (Books per Year):", "-" * 40]
        for year, count in sorted_years:
            summary_lines.append(f"  {year}: {count} books")
        
        total_books = sum(year_counts.values())
        summary_lines.append(f"\nTotal books with valid year: {total_books}")
        summary_lines.append(f"Year range: {min(year_counts.keys())} - {max(year_counts.keys())}")
        
        chart_data = {
            'labels': [str(year) for year, _ in sorted_years],
            'values': [count for _, count in sorted_years],
            'x_label': 'Year',
            'y_label': 'Number of Books'
        }
        
        return AnalysisResult(
            title="Publication Trend Analysis",
            summary="\n".join(summary_lines),
            chart_data=chart_data,
            chart_type="line"
        )


class TopAuthorsAnalysis(AnalysisStrategy):
    """Top 5 most prolific authors."""
    
    def analyse(self, books: List[Book]) -> AnalysisResult:
        author_counts: Dict[str, int] = defaultdict(int)
        
        for book in books:
            if book.author:
                author_counts[book.author] += 1
        
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary_lines = ["Top 5 Most Prolific Authors:", "-" * 40]
        for i, (author, count) in enumerate(top_authors, 1):
            summary_lines.append(f"  {i}. {author}: {count} books")
        
        total_authors = len(author_counts)
        summary_lines.append(f"\nTotal unique authors: {total_authors}")
        
        chart_data = {
            'labels': [author for author, _ in top_authors],
            'values': [count for _, count in top_authors],
            'x_label': 'Author',
            'y_label': 'Number of Books'
        }
        
        return AnalysisResult(
            title="Top Authors Analysis",
            summary="\n".join(summary_lines),
            chart_data=chart_data,
            chart_type="bar"
        )


class LanguageDistributionAnalysis(AnalysisStrategy):
    """Frequency count and percentage per language."""
    
    def analyse(self, books: List[Book]) -> AnalysisResult:
        language_counts: Dict[str, int] = defaultdict(int)
        
        for book in books:
            if book.language:
                language_counts[book.language] += 1
        
        total = sum(language_counts.values())
        sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
        
        summary_lines = ["Language Distribution Analysis:", "-" * 40]
        for language, count in sorted_languages:
            percentage = (count / total * 100) if total > 0 else 0
            summary_lines.append(f"  {language}: {count} books ({percentage:.1f}%)")
        
        summary_lines.append(f"\nTotal books: {total}")
        summary_lines.append(f"Unique languages: {len(language_counts)}")
        
        chart_data = {
            'labels': [lang for lang, _ in sorted_languages],
            'values': [count for _, count in sorted_languages],
            'percentages': [(count / total * 100) if total > 0 else 0 for _, count in sorted_languages]
        }
        
        return AnalysisResult(
            title="Language Distribution Analysis",
            summary="\n".join(summary_lines),
            chart_data=chart_data,
            chart_type="pie"
        )


class PublisherCountAnalysis(AnalysisStrategy):
    """Number of books published by each publisher."""
    
    def analyse(self, books: List[Book]) -> AnalysisResult:
        publisher_counts: Dict[str, int] = defaultdict(int)
        
        for book in books:
            if book.publisher:
                publisher_counts[book.publisher] += 1
        
        sorted_publishers = sorted(publisher_counts.items(), key=lambda x: x[1], reverse=True)
        
        summary_lines = ["Publisher Count Analysis:", "-" * 40]
        for publisher, count in sorted_publishers:
            summary_lines.append(f"  {publisher}: {count} books")
        
        total_books = sum(publisher_counts.values())
        summary_lines.append(f"\nTotal books: {total_books}")
        summary_lines.append(f"Unique publishers: {len(publisher_counts)}")
        
        chart_data = {
            'labels': [pub for pub, _ in sorted_publishers[:15]],  # Top 15 for readability
            'values': [count for _, count in sorted_publishers[:15]],
            'x_label': 'Publisher',
            'y_label': 'Number of Books'
        }
        
        return AnalysisResult(
            title="Publisher Count Analysis",
            summary="\n".join(summary_lines),
            chart_data=chart_data,
            chart_type="bar"
        )


class MissingIsbnAnalysis(AnalysisStrategy):
    """Count and percentage of records without an ISBN."""
    
    def analyse(self, books: List[Book]) -> AnalysisResult:
        total_books = len(books)
        missing_isbn = sum(1 for book in books if not book.has_isbn())
        has_isbn = total_books - missing_isbn
        percentage = (missing_isbn / total_books * 100) if total_books > 0 else 0
        
        summary_lines = ["Missing ISBN Analysis:", "-" * 40]
        summary_lines.append(f"  Total books: {total_books}")
        summary_lines.append(f"  Books with ISBN: {has_isbn}")
        summary_lines.append(f"  Books missing ISBN: {missing_isbn}")
        summary_lines.append(f"  Missing percentage: {percentage:.1f}%")
        
        chart_data = {
            'labels': ['Has ISBN', 'Missing ISBN'],
            'values': [has_isbn, missing_isbn],
            'percentages': [
                (has_isbn / total_books * 100) if total_books > 0 else 0,
                percentage
            ]
        }
        
        return AnalysisResult(
            title="Missing ISBN Analysis",
            summary="\n".join(summary_lines),
            chart_data=chart_data,
            chart_type="pie"
        )


class YearLanguageAnalysis(AnalysisStrategy):
    """Number of books published per year categorized by language."""
    
    def analyse(self, books: List[Book]) -> AnalysisResult:
        year_language_counts: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        for book in books:
            if book.year is not None and book.language:
                year_language_counts[book.year][book.language] += 1
        
        sorted_years = sorted(year_language_counts.keys())
        all_languages = set()
        for lang_counts in year_language_counts.values():
            all_languages.update(lang_counts.keys())
        sorted_languages = sorted(all_languages)
        
        summary_lines = ["Year-Language Cross Analysis:", "-" * 40]
        for year in sorted_years:
            summary_lines.append(f"\n  {year}:")
            for lang in sorted_languages:
                count = year_language_counts[year].get(lang, 0)
                if count > 0:
                    summary_lines.append(f"    {lang}: {count}")
        
        total_books = sum(
            sum(lang_counts.values()) 
            for lang_counts in year_language_counts.values()
        )
        summary_lines.append(f"\nTotal books with year and language: {total_books}")
        summary_lines.append(f"Year range: {min(sorted_years)} - {max(sorted_years)}")
        summary_lines.append(f"Languages found: {len(sorted_languages)}")
        
        # Prepare stacked bar chart data
        chart_data = {
            'years': [str(year) for year in sorted_years],
            'languages': sorted_languages,
            'data': {
                lang: [year_language_counts[year].get(lang, 0) for year in sorted_years]
                for lang in sorted_languages
            },
            'x_label': 'Year',
            'y_label': 'Number of Books'
        }
        
        return AnalysisResult(
            title="Year-Language Analysis",
            summary="\n".join(summary_lines),
            chart_data=chart_data,
            chart_type="stacked_bar"
        )