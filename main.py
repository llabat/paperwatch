import sys
from tqdm import tqdm
from datetime import date
from collect_zotero import collect_urls
from latex_format import generate_latex_file
from scraping import fetch_arxiv_abstract, fetch_arxiv_cscl_new
from rank import rank_abstracts_by_relevance

if __name__ == "__main__":

    # Get path to the bib file from CLI
    collection_name = sys.argv[1]
    zotero_user_id = sys.argv[2]
    zotero_api_key = sys.argv[3]

    # Get urls from bib file
    urls = collect_urls(collection_name, zotero_user_id, zotero_api_key)

    # Scrape abstracts
    seed_abstracts = [fetch_arxiv_abstract(url) for url in tqdm(urls, desc="Scraping abstract seeds...")]
    
    # Collect all new arxiv papers
    new_papers = fetch_arxiv_cscl_new()
    new_abstracts = [paper["abstract"] for paper in new_papers]

    # Rank abstracts by relevance
    ranking = rank_abstracts_by_relevance(seed_abstracts, new_abstracts)

    # Write the ranking to a file
    with open(f"paperwatch_{collection_name}_{date.today()}.txt", "w") as f:
        reordered = [new_papers[i] for i in ranking]
        f.write(generate_latex_file(reordered, collection_name, date.today()))

