import os
import re
import unicodedata

BASE_DIR = os.path.dirname(__file__) 
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data") 

female_file = os.path.join(DATA_DIR, "female.txt")
male_file = os.path.join(DATA_DIR, "male.txt")

allowed = set("abcdefghijklmnopqrstuvwxyz-'")

def clean_name(name, ascii_fold=False, min_len=2, max_len=30):
    """Clean and normalize a name string.

    Args:
        name (str): Raw input name.
        min_len (int, optional): Minimum length allowed for the name.
        max_len (int, optional): Maximum length allowed for the name.

    Returns:
        str | None: Cleaned name string, or None if invalid.
    """
    s = unicodedata.normalize("NFKC", name).strip()
    s = s.lower()
    s = s.replace("’", "'")
    s = re.sub(r"\s+", "-", s)
    s = "".join(ch for ch in s if ch in allowed)
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-'")

    if not s or not (min_len <= len(s) <= max_len):
        return None

    return s

def load_names(filename):
    """Load and clean all names from a file.

    Args:
        filename (str): Path to the file containing names.

    Returns:
        list[str]: List of cleaned names.
    """
    names = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            cleaned = clean_name(line)
            if cleaned: 
                names.append(cleaned)
    return names

female_names = load_names(female_file)
male_names = load_names(male_file)

