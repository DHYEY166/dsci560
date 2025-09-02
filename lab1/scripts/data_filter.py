from bs4 import BeautifulSoup
from pathlib import Path
import csv

BASE_DIR  = Path(__file__).resolve().parent.parent
RAW_HTML  = BASE_DIR / "data" / "raw_data" / "web_data.html"
PROC_DIR  = BASE_DIR / "data" / "processed_data"
MARKET_CSV = PROC_DIR / "market_data.csv"
NEWS_CSV   = PROC_DIR / "news_data.csv"

print("Reading raw HTML…")
if not RAW_HTML.exists():
    raise FileNotFoundError(f"Missing file: {RAW_HTML} (run web_scraper.py first)")

html = RAW_HTML.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# Ensure output dir
PROC_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Market banner extraction
# ---------------------------
print(" Filtering fields for Market banner (symbol, stockPosition/price, changePct)…")
market_rows = []

# Heuristic 1: elements carrying data attributes
for el in soup.find_all(attrs={"data-symbol": True}):
    symbol = (el.get("data-symbol") or "").strip()
    pos    = (el.get("data-stockposition") or el.get("data-price") or "").strip()
    chg    = (el.get("data-changepct") or el.get("data-change-pct") or "").strip()
    if symbol:
        market_rows.append((symbol, pos, chg))

# Heuristic 2: cards with class similar to "MarketCard"
if not market_rows:
    def has_mc_class(tag):
        return tag.has_attr("class") and any("marketcard" in c.lower() for c in tag["class"])
    for card in soup.find_all(has_mc_class):
        symbol = (card.get("data-symbol") or "").strip()
        # try to pick text for price/change inside card
        stock_el = card.find(attrs={"data-field": "Last"}) or card.find(attrs={"data-field": "last"})
        chg_el   = card.find(attrs={"data-field": "ChangePct"}) or card.find(attrs={"data-field": "changePct"})
        stock = stock_el.get_text(strip=True) if stock_el else ""
        chg   = chg_el.get_text(strip=True) if chg_el else ""
        if symbol:
            market_rows.append((symbol, stock, chg))

print(f"Market rows found: {len(market_rows)}")

# ---------------------------
# Latest News extraction
# ---------------------------
print("Filtering fields for Latest News (timestamp, title, link)…")
news_rows = []

# Strategy 1: find a heading that is exactly 'Latest News'
latest_heading = None
for h in soup.find_all(["h2", "h3", "h4"]):
    if h.get_text(strip=True).lower() == "latest news":
        latest_heading = h
        break

def pick_time_around(node):
    t = node.find_previous("time") or node.find_next("time")
    return t.get_text(strip=True) if t else ""

if latest_heading:
    container = latest_heading.find_parent() or latest_heading
    for a in container.find_all("a", href=True):
        title = a.get_text(strip=True)
        href  = a["href"]
        ts    = pick_time_around(a)
        if title and href:
            news_rows.append((ts, title, href))

# Strategy 2: classes mentioning LatestNews
if not news_rows:
    def has_ln_class(tag):
        return tag.has_attr("class") and any("latestnews" in c.lower() for c in tag["class"])
    for item in soup.find_all(has_ln_class):
        a = item.find("a", href=True)
        if a:
            title = a.get_text(strip=True)
            href  = a["href"]
            ts_el = item.find("time") or item.find("span")
            ts    = ts_el.get_text(strip=True) if ts_el else ""
            news_rows.append((ts, title, href))

print(f"Latest News rows found: {len(news_rows)}")

# ---------------------------
# Write CSVs
# ---------------------------
print("Storing Market data → CSV…")
with MARKET_CSV.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["marketCard_symbol", "marketCard_stockPosition", "marketCard-changePct"])
    for row in market_rows:
        w.writerow(row)

print("Storing Latest News → CSV…")
with NEWS_CSV.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["LatestNews-timestamp", "title", "link"])
    for row in news_rows:
        w.writerow(row)

print("CSV created:")
print(f"   - {MARKET_CSV.relative_to(BASE_DIR)}  (rows: {len(market_rows)})")
print(f"   - {NEWS_CSV.relative_to(BASE_DIR)}    (rows: {len(news_rows)})")

# Friendly hint if nothing found
if not market_rows:
    print("No market rows detected. Open data/raw_data/web_data.html and adjust selectors if CNBC markup changed.")
if not news_rows:
    print("No news rows detected. Inspect the 'Latest News' section in the saved HTML and tweak selectors.")
