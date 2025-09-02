from data_ingesters.download_papers import download_arxiv_papers
from data_ingesters.scrape import scrape_data
from ddgs import DDGS
import hashlib, json

def make_filename(identifier):
    return str(hashlib.md5(identifier.encode()).hexdigest())

metadata = {"title":None,"url":None}
def collect_data(query:str, search_mode:str, max_results:int):
    if search_mode == "web":
        results = DDGS().text(query, max_results=max_results)
        for result in results:
            title = result["title"]
            url = result["href"]
            filename = make_filename(url)

            text_name = filename+".txt"
            scrape_data(url=url, filename=text_name)
            
            meta_name = filename+".json"
            metadata["title"] = title
            metadata["url"] = url
            f = open("data/raw/scraped/"+meta_name,"w", encoding="utf-8")
            json.dump(metadata, f, ensure_ascii=False, indent=2)
            f.close()
            
    elif search_mode == "research":
        download_arxiv_papers(query, max_results=max_results)

if __name__ == "__main__":
    collect_data("what is web scraping", search_mode="web",max_results=5)