import os, hashlib, json
from dotenv import load_dotenv
from data_ingesters.download_papers import download_arxiv_papers
from data_ingesters.scrape import scrape_data
from ddgs import DDGS

load_dotenv()

scraped_dir = os.getenv("SCRAPE_DIR")
pdf_dir = os.getenv("PDF_DIR")

def make_filename(identifier, length=12):
    return hashlib.md5(identifier.encode()).hexdigest()[:length]

def collect_web_data(query, directory, max_results, metadata={}):
    results = DDGS().text(query, max_results=max_results)
    for result in results:
        title = result["title"]
        url = result["href"]
        filename = make_filename(url)

        text_name = filename+".txt"
        scrape_data(url=url,directory=directory ,filename=text_name)
        
        meta_name = filename+".json"
        metadata["title"] = title
        metadata["url"] = url
        
        f = open(str(directory)+meta_name,"w", encoding="utf-8")
        json.dump(metadata, f, ensure_ascii=False, indent=2)
        f.close()

def collect_pdf_data(query, directory, max_results):
    download_arxiv_papers(query,directory=directory, max_results=max_results)

if __name__ == "__main__":
    collect_web_data("what is web scraping", directory=scraped_dir, max_results=5)