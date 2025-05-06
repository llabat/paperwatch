import sys
from tqdm import tqdm
from datetime import date
from collect_zotero import collect_urls
from scraping import fetch_all_abstracts, fetch_arxiv_cscl_new
from rank import compute_similarities, rank_all_abstracts
from utils import generate_ranking_pdf

if __name__ == "__main__":

    # Get path to the bib file from CLI
    collection_name = sys.argv[1]
    zotero_user_id = sys.argv[2]
    zotero_api_key = sys.argv[3]
    threshold = 0.75 if len(sys.argv) < 4 else sys.argv[4]

    # Get urls from bib file
    urls = collect_urls(collection_name, zotero_user_id, zotero_api_key)

    # Scrape abstracts
    seed_abstracts = fetch_all_abstracts(urls)
    
    # Collect all new arxiv papers
    new_papers = fetch_arxiv_cscl_new()
    new_abstracts = [paper["abstract"] for paper in new_papers]

    # Compute similarities
    similarities = compute_similarities(seed_abstracts, new_abstracts)

    # Rank abstracts by relevance
    ranking = rank_all_abstracts(new_papers, similarities)

    # Generate latex file
    filename = f"paperwatch_{collection_name}_{date.today()}"
    generate_ranking_pdf(ranking, collection_name, date.today(), filename)

