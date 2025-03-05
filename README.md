# Unicode Glyph Analysis Tool

A Python CLI tool for analyzing Unicode glyphs' readability and compatibility across different systems.

## Features

- Analyze individual Unicode characters or text strings
- Calculate readability scores based on multiple factors:
  - Character complexity
  - Display width
  - Unicode category
  - Character decomposition
- Check cross-system compatibility
- Detailed character information display
- Support for analyzing ranges of Unicode characters

## Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd unicode-glyph-analyzer

# Install dependencies
pip install click rich
```

## Usage

The tool provides two main commands:

### 1. Analyze Text

Analyze a string of text with detailed character information:

```bash
python unicode_analyzer.py analyze "Hello World! 👋" --detailed
```

This will display a table showing:
- Unicode code point
- Character name
- Readability score
- Compatibility rating
- Width information
- Unicode category
- Decomposition details

### 2. Analyze Unicode Range

Analyze a range of Unicode characters:

```bash
python unicode_analyzer.py analyze-range 0x2190 0x2195
```

This will analyze all characters in the specified range (e.g., arrow symbols ←↑→↓↔↕).

## Components

- `unicode_analyzer.py`: Main CLI interface using Click
- `glyph_scorer.py`: Implements readability scoring algorithms
- `compatibility_checker.py`: Handles cross-system compatibility analysis
- `utils.py`: Common utility functions for Unicode operations

## Example Output

```
┏━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Char ┃ Unicode ┃ Name             ┃ Readability Score ┃ Compatibility ┃
┡━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ ←    │ U+2190  │ LEFTWARDS ARROW  │ 86.00             │ High          │
│ ↑    │ U+2191  │ UPWARDS ARROW    │ 86.00             │ High          │
│ →    │ U+2192  │ RIGHTWARDS ARROW │ 86.00             │ High          │
└──────┴─────────┴──────────────────┴───────────────────┴───────────────┘
```

## License

MIT License - feel free to use and modify as needed.
