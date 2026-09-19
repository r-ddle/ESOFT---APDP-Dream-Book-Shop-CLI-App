#!/usr/bin/env python3
"""Entry point for Dream Book Shop CLI Data Analysis Application."""

from src.data_source import CSVDataSource
from src.presenter import ReportPresenter
from src.app import CLIApplication


def main() -> None:
    """Main entry point - sets up dependencies and runs the application."""
    # Configuration
    data_file = "data/sample_books.csv"
    max_rows = 5000
    
    # Dependency injection
    data_source = CSVDataSource(data_file, max_rows)
    presenter = ReportPresenter()
    
    # Create and run application
    app = CLIApplication(data_source, presenter)
    app.run()


if __name__ == "__main__":
    main()