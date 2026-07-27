import textwrap

def wrap_text(
        text: str,
        width: int,
) -> str:
    """
    Wrap text without breaking words.
    """
    if not text:
        return ""
    
    return textwrap.fill(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )