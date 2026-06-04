# Amazon_Product_scrapper
Web scraper to extract laptop listings from Amazon.in using Python and BeautifulSoup.

# Amazon Product Scraper

A Python web scraper that extracts laptop listings from Amazon.in and saves them to a CSV file.

## What it scrapes
- Product Title
- Price
- Rating
- Image URL
- Result Type (Ad or Organic)

## How to run

**Install dependencies:**
```bash
pip install requests beautifulsoup4
```

**Run the scraper:**
```bash
python amazon_scraper.py
```

## Output
Saves a CSV file with timestamp in the filename.
Example: `amazon_laptops_2026-06-04_01-43-22.csv`

## Sample Output
See `amazon_laptops_2026-06-04_01-43-22.csv` in this repo.

## Tech Stack
- Python
- requests
- BeautifulSoup4
- csv
