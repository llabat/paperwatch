import sys
from tqdm import tqdm
from datetime import date
from collect_zotero import collect_urls
from scraping import fetch_all_abstracts, fetch_arxiv_cscl_new, fetch_arxiv_details
from rank import compute_similarities, rank_all_abstracts, single_out_specials
from latex_format import generate_latex_table
from utils import generate_ranking_pdf

if __name__ == "__main__":

    # Get path to the bib file from CLI
    collection_name = sys.argv[1]
    zotero_user_id = sys.argv[2]
    zotero_api_key = sys.argv[3]
    threshold = 0.75 if len(sys.argv) < 4 else float(sys.argv[4])

    # Get urls from bib file
    urls = collect_urls(collection_name, zotero_user_id, zotero_api_key)

    # Scrape abstracts
    seeds = [fetch_arxiv_details(url) for url in urls]
    seed_abstracts = [seed["abstract"] for seed in seeds]
    
    # Collect all new arxiv papers
    new_papers = fetch_arxiv_cscl_new()
    new_abstracts = [paper["abstract"] for paper in new_papers]

    # Compute similarities
    similarities = compute_similarities(seed_abstracts, new_abstracts)

    # Rank abstracts by relevance
    ranking = rank_all_abstracts(new_papers, similarities)

    # Single out special papers
    specials = single_out_specials(similarities, threshold)

    # Build latex table for special papers
    standout_table = generate_latex_table(specials, seeds, new_papers, max_rows=None) if specials else f"No Standouts Today (with threshold = {threshold})"

    # Generate latex file
    filename = f"paperwatch_{collection_name}_{date.today()}"
    generate_ranking_pdf(ranking, collection_name, date.today(), standout_table, filename)

