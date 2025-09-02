# DSCI560

USC DSCI-560 Course Repository.

## Structure
- `lab1/` — Lab 1 (data/, scripts/, report/)
- `lab2/` — Lab 2 (future)
- `reading*/` — Reading summaries
- `final-project/` — Capstone work

## How to run Lab 1
```bash
cd lab1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 scripts/web_scraper.py
python3 scripts/data_filter.py