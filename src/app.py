from typing import List

from src.data_source import IDataSource
from src.models import Book, AnalysisResult
from src.presenter import ReportPresenter
from src.strategies import (
    AnalysisStrategy,
    PublicationTrendAnalysis,
    TopAuthorsAnalysis,
    LanguageDistributionAnalysis,
    PublisherCountAnalysis,
    MissingIsbnAnalysis,
    YearLanguageAnalysis
)


class CLIApplication:
    """Main CLI application controller connecting data, analysis, and presentation layers."""
    
    def __init__(self, data_source: IDataSource, presenter: ReportPresenter) -> None:
        self._data_source = data_source
        self._presenter = presenter
        self._books: List[Book] = []
        self._strategies: dict[int, AnalysisStrategy] = {
            1: PublicationTrendAnalysis(),
            2: TopAuthorsAnalysis(),
            3: LanguageDistributionAnalysis(),
            4: PublisherCountAnalysis(),
            5: MissingIsbnAnalysis(),
            6: YearLanguageAnalysis()
        }
    
    def run(self) -> None:
        """Main application loop."""
        print("Loading book data...")
        self._books = self._data_source.load()
        print(f"Loaded {len(self._books)} books.\n")
        
        while True:
            self._display_menu()
            choice = self._get_user_choice()
            
            if choice == 7:
                print("Thank you for using Dream Book Shop Analytics. Goodbye!")
                break
            elif choice in self._strategies:
                self._run_analysis(choice)
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
    
    def _display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "=" * 50)
        print("  DREAM BOOK SHOP - DATA ANALYSIS MENU")
        print("=" * 50)
        print("  1. Publication Trend Analysis (Books per Year)")
        print("  2. Top 5 Authors Analysis")
        print("  3. Language Distribution Analysis")
        print("  4. Publisher Count Analysis")
        print("  5. Missing ISBN Analysis")
        print("  6. Year-Language Cross Analysis")
        print("  7. Exit")
        print("=" * 50)
    
    def _get_user_choice(self) -> int:
        """Get and validate user menu choice."""
        while True:
            try:
                choice = int(input("Enter your choice (1-7): ").strip())
                return choice
            except ValueError:
                print("Please enter a valid number.")
    
    def _run_analysis(self, choice: int) -> None:
        """Run the selected analysis and present results."""
        strategy = self._strategies[choice]
        
        print(f"\nRunning {strategy.__class__.__name__}...")
        result = strategy.analyse(self._books)
        
        self._presenter.print_summary(result)
        
        show_chart = input("Display chart? (y/n): ").strip().lower()
        if show_chart == 'y':
            self._presenter.plot_chart(result)