import unicodedata
from typing import Dict, Set

class CompatibilityChecker:
    def __init__(self):
        # Common Unicode blocks that are widely supported
        self.common_blocks = {
            (0x0000, 0x007F),  # Basic Latin
            (0x0080, 0x00FF),  # Latin-1 Supplement
            (0x0100, 0x017F),  # Latin Extended-A
            (0x0180, 0x024F),  # Latin Extended-B
            (0x0370, 0x03FF),  # Greek and Coptic
            (0x0400, 0x04FF),  # Cyrillic
            (0x2000, 0x206F),  # General Punctuation
            (0x20A0, 0x20CF),  # Currency Symbols
            (0x2100, 0x214F),  # Letterlike Symbols
            (0x2190, 0x21FF),  # Arrows
        }

        # Problematic categories that might cause compatibility issues
        self.problematic_categories = {
            'Co',  # Private Use
            'Cn',  # Unassigned
            'Cf',  # Format
        }

    def check_compatibility(self, char: str) -> str:
        """
        Check the compatibility of a Unicode character across systems.
        Returns a human-readable compatibility status.
        """
        try:
            code_point = ord(char)
            category = unicodedata.category(char)
            
            # Check if character is in common blocks
            in_common_block = any(start <= code_point <= end 
                                for start, end in self.common_blocks)
            
            # Check for potential compatibility issues
            if category in self.problematic_categories:
                return "Low"
            
            if not in_common_block:
                if code_point > 0xFFFF:  # Outside BMP
                    return "Limited"
                return "Moderate"
            
            # Check for combining characters
            if unicodedata.combining(char):
                return "Variable"
            
            # Check decomposition
            decomposition = unicodedata.decomposition(char)
            if decomposition and decomposition.startswith('<compat>'):
                return "Moderate"
            
            # If all checks pass, it's likely highly compatible
            return "High"
            
        except Exception as e:
            return "Unknown"

    def get_detailed_compatibility(self, char: str) -> Dict[str, bool]:
        """
        Get detailed compatibility information for a character.
        """
        code_point = ord(char)
        return {
            "in_basic_multilingual_plane": code_point <= 0xFFFF,
            "in_common_block": any(start <= code_point <= end 
                                 for start, end in self.common_blocks),
            "has_name": bool(unicodedata.name(char, '')),
            "is_normalized_nfc": char == unicodedata.normalize('NFC', char),
            "is_normalized_nfd": char == unicodedata.normalize('NFD', char),
            "is_printable": char.isprintable(),
            "has_compatibility_decomposition": bool(unicodedata.decomposition(char))
        }
