import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw_data"
PROCESSED_DIR = BASE_DIR / "data" / "processed_data"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://www.cnbc.com/world/?region=world"
OUT_FILE = RAW_DIR / "web_data.html"

headers = {
    # Pretend to be a real browser
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

print(f"Fetching: {URL}")
with requests.Session() as s:
    s.headers.update(headers)
    # follow redirects; some sites require a first GET to set cookies
    r = s.get(URL, timeout=30, allow_redirects=True)
    r.raise_for_status()
    html = r.text

OUT_FILE.write_text(html, encoding="utf-8")
print(f" Saved HTML to {OUT_FILE.relative_to(BASE_DIR)}")

# Print first 10 lines
lines = html.splitlines()[:10]
print("—— First 10 lines —————————————")
for i, line in enumerate(lines, 1):
    print(f"{i:02d}| {line}")
