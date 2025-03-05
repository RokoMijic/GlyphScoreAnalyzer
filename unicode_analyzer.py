#!/usr/bin/env python3
import click
from rich.console import Console
from rich.table import Table
from rich.progress import track
from glyph_scorer import GlyphScorer
from compatibility_checker import CompatibilityChecker
from utils import get_char_info

console = Console()

@click.group()
def cli():
    """Unicode Glyph Analysis Tool - Analyze readability and compatibility of Unicode characters."""
    pass

@cli.command()
@click.argument('text', required=True)
@click.option('--detailed', '-d', is_flag=True, help='Show detailed analysis')
def analyze(text: str, detailed: bool):
    """Analyze Unicode glyphs in the provided text."""
    scorer = GlyphScorer()
    compat_checker = CompatibilityChecker()

    table = Table(show_header=True)
    table.add_column("Char")
    table.add_column("Unicode")
    table.add_column("Name")
    table.add_column("Readability Score")
    table.add_column("Compatibility")

    if detailed:
        table.add_column("Width")
        table.add_column("Category")
        table.add_column("Decomposition")

    for char in track(text, description="Analyzing characters..."):
        char_info = get_char_info(char)
        readability_score = scorer.calculate_score(char)
        compatibility = compat_checker.check_compatibility(char)

        row = [
            char,
            f"U+{ord(char):04X}",
            char_info['name'],
            f"{readability_score:.2f}",
            compatibility
        ]

        if detailed:
            row.extend([
                str(char_info['width']),
                char_info['category'],
                char_info['decomposition']
            ])

        table.add_row(*row)

    console.print(table)

@cli.command(name='analyze-range')
@click.argument('start', type=str)
@click.argument('end', type=str)
def analyze_range(start: str, end: str):
    """Analyze a range of Unicode characters."""
    try:
        start_point = int(start, 16)
        end_point = int(end, 16)
    except ValueError:
        console.print("[red]Error: Please provide hex values for range[/red]")
        return

    if end_point < start_point:
        console.print("[red]Error: End point must be greater than start point[/red]")
        return

    if end_point - start_point > 1000:
        console.print("[yellow]Warning: Large range selected. This might take a while...[/yellow]")

    table = Table(show_header=True)
    table.add_column("Char")
    table.add_column("Unicode")
    table.add_column("Name")
    table.add_column("Readability Score")
    table.add_column("Compatibility")

    scorer = GlyphScorer()
    compat_checker = CompatibilityChecker()

    # Create a list for progress tracking
    code_points = list(range(start_point, end_point + 1))

    for code_point in track(code_points, description="Analyzing range..."):
        try:
            char = chr(code_point)
            char_info = get_char_info(char)
            readability_score = scorer.calculate_score(char)
            compatibility = compat_checker.check_compatibility(char)

            table.add_row(
                char,
                f"U+{code_point:04X}",
                char_info['name'],
                f"{readability_score:.2f}",
                compatibility
            )
        except (ValueError, KeyError):
            continue

    console.print(table)

if __name__ == '__main__':
    cli()