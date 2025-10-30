import requests
from bs4 import BeautifulSoup

base_url = "https://goteborg.se"
url = "https://goteborg.se/wps/portal/enhetssida/stadsbiblioteket/bibliotekets-program?fromDate=2025-10-29&toDate=2025-10-29"  # example page URL

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

events = []

for card in soup.select('[data-testid="kalendarium-activity"] .c-card'):
    title_tag = card.select_one('.c-card__title-link')
    place_tag = card.select_one('.c-card__byline')
    date_tag = card.select_one('dt:contains("Datum") + dd')
    time_tag = card.select_one('dt:contains("Tid") + dd')
    status_tag = card.select_one('dt:contains("Status") + dd')
    img_tag = card.select_one('.c-image__image')

    event = {
        "title": title_tag.get_text(strip=True) if title_tag else None,
        "link": title_tag['href'] if title_tag else None,
        "place": place_tag.get_text(strip=True) if place_tag else None,
        "date": date_tag.get_text(strip=True) if date_tag else None,
        "time": time_tag.get_text(strip=True) if time_tag else None,
        "status": status_tag.get_text(strip=True) if status_tag else None,
        "image": img_tag['src'] if img_tag else None
    }

    event_url = requests.compat.urljoin(base_url, title_tag['href'])
    detail_res = requests.get(event_url)
    detail_res.raise_for_status()
    detail_soup = BeautifulSoup(detail_res.text, "html.parser")

    # Step 4: Extract inner text from `.c-text`
    text_block = detail_soup.select_one('.c-text')
    description = text_block.get_text("\n", strip=True) if text_block else None
    event["content"] = description

    events.append(event)

for e in events:
    print(e)
