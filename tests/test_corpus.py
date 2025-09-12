import os
from pathlib import Path
from namegen.corpus import clean_name, load_names, DATA_DIR

def test_clean_name_basic():
    assert clean_name("  Anna \n") == "anna"

def test_clean_name_apostrophe_and_dash():
    assert clean_name("O’Connor") == "o'connor" 
    assert clean_name("Mary  Anne") == "mary-anne" 

def test_clean_name_filters_chars_and_length_bounds():
    assert clean_name("Anna!!!") == "anna"
    assert clean_name("A", min_len=2) is None
    assert clean_name("avery"*10, max_len=10) is None 

def test_load_names_reads_and_cleans(tmp_path):

    p = tmp_path / "sample.txt"
    p.write_text(
        "  Anna  \n"
        "O’Connor\n"
        "Mary   Anne\n"
        "!!!\n", 
        encoding="utf-8",
    )

    names = load_names(os.fspath(p))

    # Expect cleaned, non-empty names in order
    assert names == ["anna", "o'connor", "mary-anne"]


def test_real_data_loads_without_errors():
    data_dir = Path(DATA_DIR)
    male = load_names(data_dir / "male.txt")
    female = load_names(data_dir / "female.txt")

    assert len(male) > 0
    assert len(female) > 0
    assert all(isinstance(n, str) and len(n) >= 2 for n in male + female)
    
    print("\nFirst 10 male names:", male[:10])
    print("First 10 female names:", female[:10])