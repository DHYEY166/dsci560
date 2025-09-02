# DSCI560

USC DSCI-560: Data Science Professional Practicum Repository

## Repository Structure

- `lab1/` — Lab 1: System setup, web scraping, and data processing  
  - `data/`  
     - `raw_data/` — Contains original, scraped HTML files  
     - `processed_data/` — Contains generated CSV files with filtered data  
  - `scripts/` — Python scripts for scraping and processing  
  - `report/` — Screenshots and documentation for Lab 1
- `lab2/` — Lab 2 (to be added)
- `reading*/` — Reading summaries (if any)
- `final-project/` — Capstone project work

## Lab 1 Instructions

### Environment Setup

cd lab1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

text

### Running the Scripts

**Step 1: Web Scraping**  
Fetch raw HTML from CNBC World and save to the raw data directory.

python3 scripts/web_scraper.py

text
- Output: `data/raw_data/web_data.html`

**Step 2: Data Filtering**  
Parse HTML and extract market banner and latest news, exporting to CSV.

python3 scripts/data_filter.py

text
- Output:
  - `data/processed_data/market_data.csv`
  - `data/processed_data/news_data.csv`

### Additional Notes

- Screenshots and the assignment report are located in the `report/` folder.
- All terminal, script, and output evidence are included for grading and reproducibility.
- Remember to activate your virtual environment before running scripts.
- Modify file paths if your environment is structured differently.

---