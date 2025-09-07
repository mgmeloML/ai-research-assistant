from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "NewToWebScraping/1.0 (https://example.com/contact)"
}

def scrape_data(url, directory, filename):
    source = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(source, "lxml")

    for data in soup.find_all("p"):
        text = data.text
        f = open(str(directory)+filename, "a", encoding="utf-8")
        f.write(text)
        f.close()

if __name__ == "__main__":
    pass
