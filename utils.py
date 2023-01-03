import threading
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.olx.ua"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36",
    "Content-Type": "text/html; charset=utf-8",
}

CATEGORY_SLUG = "/d/uk/nedvizhimost/"

websites = []
for i in range(1, 3):
    websites.append(f"{BASE_URL}{CATEGORY_SLUG}?page={i}")


def get_image_src(href):
    single_page = requests.get(BASE_URL + href, headers=HEADERS)
    single_page_soup = BeautifulSoup(single_page.content, "html.parser")
    try:
        image_src = (
            single_page_soup.find("div", class_="swiper-zoom-container")
            .find("img")
            .get("src")
        )
    except Exception as e:
        image_src = None
    return image_src


class Scraper(threading.Thread):
    def __init__(self, thread_id, name, url):
        threading.Thread.__init__(self)
        self.name = name
        self.id = thread_id
        self.url = url

    def run(self):
        request = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(request.content, "html.parser")
        results = []

        for item in soup.select('div[data-cy="l-card"]'):
            href = item.find("a", class_="css-rc5s2u").get("href")
            image_src = get_image_src(href)

            results.append(
                {
                    "title": item.h6.get_text(strip=True),
                    "price": item.p.get_text(strip=True),
                    "image": image_src,
                }
            )
        return results


for url in websites:
    thread = Scraper(1, "thread" + str(i), url)
    result_dict = thread.run()
