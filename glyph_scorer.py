import unicodedata
from typing import Dict, Optional

class GlyphScorer:
    def __init__(self):
        # Weights for different scoring factors
        self.weights = {
            'complexity': 0.3,
            'width': 0.2,
            'category': 0.3,
            'decomposition': 0.2
        }

        # Category scores (normalized between 0 and 1)
        self.category_scores = {
            'Lu': 1.0,  # Uppercase Letter
            'Ll': 1.0,  # Lowercase Letter
            'Nd': 0.9,  # Decimal Number
            'No': 0.8,  # Other Number
            'Po': 0.7,  # Other Punctuation
            'Sm': 0.6,  # Math Symbol
            'So': 0.5,  # Other Symbol
            'Mn': 0.4,  # Non-spacing Mark
            'Me': 0.3,  # Enclosing Mark
            'Mc': 0.3,  # Spacing Mark
            'Cf': 0.2,  # Format
            'Co': 0.1,  # Private Use
            'Cn': 0.0   # Unassigned
        }

    def calculate_score(self, char: str) -> float:
        """Calculate the readability score for a given character."""
        if not char:
            return 0.0

        complexity_score = self._calculate_complexity_score(char)
        width_score = self._calculate_width_score(char)
        category_score = self._calculate_category_score(char)
        decomposition_score = self._calculate_decomposition_score(char)

        final_score = (
            complexity_score * self.weights['complexity'] +
            width_score * self.weights['width'] +
            category_score * self.weights['category'] +
            decomposition_score * self.weights['decomposition']
        )

        return min(max(final_score * 100, 0), 100)  # Normalize to 0-100 range

    def _calculate_complexity_score(self, char: str) -> float:
        """Calculate complexity score based on the character's properties."""
        try:
            # Get the number of combining marks
            combining_marks = len([c for c in unicodedata.normalize('NFD', char)
                                if unicodedata.combining(c)])
            # Penalize characters with many combining marks
            complexity_penalty = max(0, 1 - (combining_marks * 0.2))
            
            # Additional penalty for unusual Unicode blocks
            code_point = ord(char)
            if code_point > 0xFFFF:  # Characters outside BMP
                complexity_penalty *= 0.8
                
            return complexity_penalty
        except Exception:
            return 0.0

    def _calculate_width_score(self, char: str) -> float:
        """Calculate score based on the character's display width."""
        try:
            # East Asian Width property
            width = unicodedata.east_asian_width(char)
            width_scores = {
                'Na': 1.0,  # Narrow
                'H': 1.0,   # Halfwidth
                'W': 0.8,   # Wide
                'F': 0.8,   # Fullwidth
                'A': 0.9,   # Ambiguous
                'N': 1.0    # Neutral
            }
            return width_scores.get(width, 0.5)
        except Exception:
            return 0.5

    def _calculate_category_score(self, char: str) -> float:
        """Calculate score based on the character's Unicode category."""
        try:
            category = unicodedata.category(char)
            return self.category_scores.get(category, 0.5)
        except Exception:
            return 0.0

    def _calculate_decomposition_score(self, char: str) -> float:
        """Calculate score based on character decomposition."""
        try:
            decomposition = unicodedata.decomposition(char)
            if not decomposition:
                return 1.0  # No decomposition needed
            
            # Penalize complex decompositions
            components = decomposition.count('<')
            return max(0, 1 - (components * 0.2))
        except Exception:
            return 0.0
