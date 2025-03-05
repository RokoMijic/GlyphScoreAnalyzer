import unicodedata
from typing import Dict, Any

def get_char_info(char: str) -> Dict[str, Any]:
    """
    Get detailed information about a Unicode character.
    """
    try:
        return {
            'name': unicodedata.name(char, 'UNKNOWN'),
            'category': unicodedata.category(char),
            'combining': unicodedata.combining(char),
            'bidirectional': unicodedata.bidirectional(char),
            'decomposition': unicodedata.decomposition(char) or 'N/A',
            'decimal': unicodedata.decimal(char, ''),
            'digit': unicodedata.digit(char, ''),
            'numeric': unicodedata.numeric(char, ''),
            'width': unicodedata.east_asian_width(char),
            'mirrored': unicodedata.mirrored(char)
        }
    except Exception as e:
        return {
            'name': 'UNKNOWN',
            'category': 'Unknown',
            'combining': 0,
            'bidirectional': 'Unknown',
            'decomposition': 'N/A',
            'decimal': '',
            'digit': '',
            'numeric': '',
            'width': 'N',
            'mirrored': False
        }

def is_valid_hex(s: str) -> bool:
    """
    Check if a string is a valid hexadecimal number.
    """
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def get_block_name(code_point: int) -> str:
    """
    Get the Unicode block name for a code point.
    """
    blocks = [
        (0x0000, 0x007F, "Basic Latin"),
        (0x0080, 0x00FF, "Latin-1 Supplement"),
        (0x0100, 0x017F, "Latin Extended-A"),
        (0x0180, 0x024F, "Latin Extended-B"),
        (0x0250, 0x02AF, "IPA Extensions"),
        (0x02B0, 0x02FF, "Spacing Modifier Letters"),
        (0x0300, 0x036F, "Combining Diacritical Marks"),
        (0x0370, 0x03FF, "Greek and Coptic"),
        (0x0400, 0x04FF, "Cyrillic"),
        (0x0500, 0x052F, "Cyrillic Supplement"),
    ]
    
    for start, end, name in blocks:
        if start <= code_point <= end:
            return name
    return "Unknown Block"

def format_code_point(code_point: int) -> str:
    """
    Format a code point as a Unicode escape sequence.
    """
    return f"U+{code_point:04X}"
