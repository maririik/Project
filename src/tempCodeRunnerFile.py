
        (see app.py). This script is included only as a quick, minimal example
        for testing or experimenting without the UI.
        """
    from pathlib import Path

    PROJECT_DIR = Path(__file__).parent.parent
    DATA_FILE = PROJECT_DIR / "data" / "female.txt"

    if not DATA_FILE.exists():
        print(f"Dataset not found: {DATA_FILE}")
        exit(1)

    txt = DATA_FILE.read_text(encoding="utf-8", errors="ignore")
    names = [line.strip().lower() for line in txt.splitlines() if line.strip()]
    print(f"Loaded {len(names)} names from {DATA_FILE}")

    try:
        order = int(input("Enter desired n-gram order (e.g. 2, 3, 4): "))