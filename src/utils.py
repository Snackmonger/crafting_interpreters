from data.constants import DIGITS, ALPHA_LOWER, ALPHA_UPPER



def is_digit(char: str) -> bool:
    """Test if a given character is an Indian-Arabic numeral."""
    return char in DIGITS

def is_alpha(char: str) -> bool:
    """Test if a given character is an alphabetic symbol."""
    return char in ALPHA_UPPER + ALPHA_LOWER

def is_alnum(char: str) -> bool:
    """Test if a given character is alphabetic or numeric."""
    return is_alpha(char) or is_digit(char) or char == "_"

