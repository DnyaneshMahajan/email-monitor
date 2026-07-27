import html

ZERO_WIDTH_CHARACTERS = {
    "\u200B": "ZERO WIDTH SPACE",
    "\u200C": "ZERO WIDTH NON-JOINER",
    "\u200D": "ZERO WIDTH JOINER",
    "\uFEFF": "BYTE ORDER MARK"
}

def clean_text(text: str | None) -> str:
    """
    Clean text extracted from emails.
    
    - Handles None values
    - Decodes HTML entities
    - Removes zero-width Unicode characters
    - Normalizes whitespace
    """
    if not text:
        return ""
    
    text = html.unescape(text)
    for character in ZERO_WIDTH_CHARACTERS:
        text = text.replace(character, "")

    text = " ".join(text.split())  # Normalize whitespace

    return text