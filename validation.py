"""Input validation so empty or junk text never reaches the LLM."""

MIN_CHARS = 40
MIN_WORDS = 8


def validate_job_description(text) -> tuple[bool, str]:
    """Return (is_valid, message)."""
    if text is None or not str(text).strip():
        return False, "Please paste a job description. The input is empty."

    text = str(text).strip()

    if len(text) < MIN_CHARS or len(text.split()) < MIN_WORDS:
        return False, "The text is too short to be a job description. Please paste the full posting."

    letters = sum(ch.isalpha() for ch in text)
    if letters / len(text) < 0.5:
        return False, "The text does not look like a job description (too many numbers or symbols)."

    return True, "OK"
