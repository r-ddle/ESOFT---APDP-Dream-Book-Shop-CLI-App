import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive display

import matplotlib.pyplot as plt
from typing import Dict, Any

from src.models import AnalysisResult


class ReportPresenter:
    """Handles output formatting and visualization for analysis results."""
    
    def print_summary(self, result: AnalysisResult) -> None:
        """Print the analysis summary to the CLI."""
        print("\n" + "=" * 60)
        print(f"  {result.title}")
        print("=" * 60)
        print(result.summary)
        print("=" * 60 + "\n")
    
    def plot_chart(self, result: AnalysisResult) -> None:
        """Display the appropriate chart based on the result type."""
        chart_type = result.chart_type
        chart_data = result.chart_data
        
        plt.figure(figsize=(10, 6))
        
        if chart_type == "line":
            self._plot_line_chart(chart_data, result.title)
        elif chart_type == "bar":
            self._plot_bar_chart(chart_data, result.title)
        elif chart_type == "pie":
            self._plot_pie_chart(chart_data, result.title)
        elif chart_type == "stacked_bar":
            self._plot_stacked_bar_chart(chart_data, result.title)
        
        plt.tight_layout()
        plt.show()
    
    def _plot_line_chart(self, chart_data: Dict[str, Any], title: str) -> None:
        """Plot a line chart for trend analysis."""
        labels = chart_data.get('labels', [])
        values = chart_data.get('values', [])
        x_label = chart_data.get('x_label', '')
        y_label = chart_data.get('y_label', '')
        
        plt.plot(labels, values, marker='o', linestyle='-', color='b', linewidth=2)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
    
    def _plot_bar_chart(self, chart_data: Dict[str, Any], title: str) -> None:
        """Plot a bar chart for categorical data."""
        labels = chart_data.get('labels', [])
        values = chart_data.get('values', [])
        x_label = chart_data.get('x_label', '')
        y_label = chart_data.get('y_label', '')
        
        bars = plt.bar(range(len(labels)), values, color='skyblue', edgecolor='navy')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(value), ha='center', va='bottom', fontsize=9)
    
    def _plot_pie_chart(self, chart_data: Dict[str, Any], title: str) -> None:
        """Plot a pie chart for distribution analysis."""
        labels = chart_data.get('labels', [])
        values = chart_data.get('values', [])
        percentages = chart_data.get('percentages', [])
        
        # Filter out zero values
        filtered = [(l, v, p) for l, v, p in zip(labels, values, percentages) if v > 0]
        if not filtered:
            print("No data to display in pie chart.")
            return
        
        labels, values, percentages = zip(*filtered)
        
        # Create labels with percentages
        pie_labels = [f"{l}\n({p:.1f}%)" for l, p in zip(labels, percentages)]
        
        colors = plt.cm.Set3(range(len(labels)))
        wedges, texts, autotexts = plt.pie(
            values, 
            labels=pie_labels, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 9}
        )
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('equal')
    
    def _plot_stacked_bar_chart(self, chart_data: Dict[str, Any], title: str) -> None:
        """Plot a stacked bar chart for year-language analysis."""
        years = chart_data.get('years', [])
        languages = chart_data.get('languages', [])
        data = chart_data.get('data', {})
        x_label = chart_data.get('x_label', '')
        y_label = chart_data.get('y_label', '')
        
        bottom = [0] * len(years)
        colors = plt.cm.tab20(range(len(languages)))
        
        for i, lang in enumerate(languages):
            values = data.get(lang, [0] * len(years))
            plt.bar(years, values, bottom=bottom, label=lang, color=colors[i], edgecolor='white')
            bottom = [b + v for b, v in zip(bottom, values)]
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        plt.xticks(rotation=45)