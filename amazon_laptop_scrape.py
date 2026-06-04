#Task 1:- Amazon Laptop Scraper

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from datetime import datetime

# fake browser

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.amazon.in/",
    "DNT": "1",
}

BASE_URL = "https://www.amazon.in/s?k=laptops&page={page}"

# scrape 3 pages (16 products per page)
PAGES_TO_SCRAPE = 3



def scrape_page(page_number):
    """
    Fetches one page of Amazon search results and
    extracts product details from it.
    Returns a list of dictionaries (one per product).
    """
    url = BASE_URL.format(page=page_number)
    print(f"Scraping page {page_number}: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Could not fetch page {page_number}: {e}")
        return []

    if response.status_code != 200:
        print(f"  [WARNING] Status code {response.status_code} on page {page_number}. Skipping.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    product_cards = soup.find_all("div", {"data-component-type": "s-search-result"})
    print(f"  Found {len(product_cards)} products on page {page_number}")

    products = []

    for card in product_cards:

        #Title
        title_tag = (
            card.find("span", {"class": "a-text-normal"}) or
            card.find("h2", {"class": "a-size-mini"}) or
            card.find("h2") or
            card.find("span", {"class": "a-size-medium"}) or
            card.find("span", {"class": "a-size-base-plus"})
                    )
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        #Price(splits the price into whole+fraction part)
        price_whole = card.find("span", {"class": "a-price-whole"})
        price_fraction = card.find("span", {"class": "a-price-fraction"})
        if price_whole:
            fraction = price_fraction.get_text(strip=True) if price_fraction else "00"
            whole = price_whole.get_text(strip=True).replace(",", "").strip()
            price = f"₹{whole[:-2]}"
        else:
            price = "N/A"

        #Rating
        rating_tag = card.find("span", {"class": "a-icon-alt"})
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        #Image URL
        img_tag = card.find("img", {"class": "s-image"})
        image_url = img_tag["src"] if img_tag else "N/A"

        #Ad or Organic
        sponsored_tag = card.find("span", string=lambda t: t and "Sponsored" in t)
        result_type = "Ad" if sponsored_tag else "Organic"

        products.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Image URL": image_url,
            "Result Type": result_type,
        })

    return products


#Save to CSV
def save_to_csv(all_products):
    """
    Saves the list of products to a CSV file.
    Filename includes a timestamp so each run creates a new file.
    Example: amazon_laptops_2025-06-03_14-30-22.csv
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"amazon_laptops_{timestamp}.csv"

    fieldnames = ["Title", "Price", "Rating", "Image URL", "Result Type"]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_products)

    print(f"\n Saved {len(all_products)} products to: {filename}")
    return filename


def main():
    print("=" * 55)
    print("  Amazon.in Laptop Scraper — Globussoft Task 1")
    print("=" * 55)

    all_products = []

    for page in range(1, PAGES_TO_SCRAPE + 1):
        products = scrape_page(page)
        all_products.extend(products)

        if page < PAGES_TO_SCRAPE:
            wait = random.uniform(2, 5)
            print(f"  Waiting {wait:.1f}s before next page...\n")
            time.sleep(wait)

    if all_products:
        save_to_csv(all_products)
    else:
        print("\n if No products found. Amazon blocked the request.")
        print("Try again.")

    print("\nDone!")


if __name__ == "__main__":
    main()
