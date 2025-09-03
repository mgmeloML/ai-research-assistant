import os, json
from dotenv import load_dotenv
import arxiv

load_dotenv()

directory = os.getenv("PDF_DIR")
metadata = {
    "title" :None,
    "url":None
}

def download_arxiv_papers(query, max_results):

    client = arxiv.Client()

    search = arxiv.Search(
    query = query,
    max_results = max_results,
    sort_by = arxiv.SortCriterion.Relevance
    )

    results = client.results(search)   

    for paper in results:
        filename = f"{paper.entry_id.split('/')[-1]}.pdf"
        paper.download_pdf(dirpath=directory, filename=filename)

        filename = f"{paper.entry_id.split('/')[-1]}.json"
        metadata["title"] = paper.title
        metadata["url"] = paper.pdf_url

        with open(str(directory)+"/"+str(filename), "w") as f:
            json.dump(metadata, f)

if __name__ == "__main__":
    download_arxiv_papers("machine learning", 5)
    