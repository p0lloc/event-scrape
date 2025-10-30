import requests
from bs4 import BeautifulSoup
import re

base = "https://www.goteborg.com"
params_template = {
    "start": "2025-10-29",
    "end": "2025-10-29",
    "page": 1
}

def scrape_page(page):
    params = params_template.copy()
    params["page"] = page
    response = requests.get(base + "/evenemang", params=params, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# First page to detect total pages
first_soup = scrape_page(1)

# Find total number of pages: "Visar sida 1 av 3"
info_text = first_soup.select_one(".wrap-container")
print(info_text)
match = re.search(r"av\s+(\d+)", info_text.get_text() if info_text else "")
total_pages = int(match.group(1)) if match else 1

print("Total pages:", total_pages)

results = []

for page in range(1, total_pages + 1):
    print(f"Scraping page {page}/{total_pages}")
    soup = scrape_page(page)

    cards = soup.select("div.image-card-alt")

    for card in cards:
        title_tag = card.select_one(".image-card-alt__title")
        title = title_tag.get_text(strip=True) if title_tag else None

        link_tag = card.select_one("a.stretched-link")
        link = base + link_tag.get("href") if link_tag else None

        img = card.select_one("figure.image-tag img")
        image = img.get("src") if img else None

        results.append({
            "title": title,
            "link": link,
            "image": image
        })

print("Done! Found", len(results), "events.")
for r in results:
    print(r)
