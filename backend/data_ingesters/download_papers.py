import arxiv, json

def download_arxiv_papers(query, directory, max_results, metadata={}):

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
    