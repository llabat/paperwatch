import re
import sys
import requests
import numpy as np
import bibtexparser
from tqdm import tqdm
from datetime import date
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

def format_paper_info(paper_dict):
    title_str = "\\section{" + paper_dict["title"] + "} \\\\\n"
    author_str = "\\large \\textbf{" + paper_dict["authors"] + "} \\\\\\\\\n"
    url_str = '\\url{' + paper_dict["url"] + "} \\\\\\\\\n"
    abstract_str = paper_dict["abstract"] + "\\\\\n\n"
    return title_str + author_str + url_str + abstract_str

def generate_latex_file(papers, theme, date):
    entete = "\\documentclass{article}\n"
    packages = ["\\usepackage[english]{babel}", "\\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}",
                "\\usepackage{hyperref}", "\\usepackage{amsmath}", "\\usepackage{graphicx}", "\\usepackage[colorlinks=true, allcolors=blue]{hyperref}"] 
    title_str = "\\title{Paper Watch (arXiv)\\\\ \\Large " + theme + "}\n\\author{Leo Labat}\n\\date{" + str(date) + "}\n\n"
    beginner = "\\begin{document}\n\\maketitle\n"
    ender = "\\end{document}"

    return entete + "\n".join(packages) + title_str + beginner + "\n".join(format_paper_info(paper) for paper in papers) + ender

def fetch_arxiv_cscl_new():
    print("Scraping new arXiv papers...")
    url = 'https://arxiv.org/list/cs.CL/new'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    papers = []
    for dt, dd in zip(soup.find_all('dt'), soup.find_all('dd')):
        arxiv_id = dt.find('a', title='Abstract').text.strip()
        title = dd.find('div', class_='list-title').text.replace('Title:', '').strip()
        authors = dd.find('div', class_='list-authors').text.replace('Authors:', '').strip()
        abstract = dd.find('p', class_='mathjax').text.strip()
        papers.append({
            'id': arxiv_id,
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'url': f"https://arxiv.org/abs/{arxiv_id}"
        })
    return papers

def fetch_arxiv_abstract(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    if "aclanthology" in url:
        css_selector = ".acl-abstract span"
    elif "arxiv" in url:
        css_selector = ".abstract"
    else:
        raise ValueError(f"Unsupported website referenced in {url}")
    
    abstract_element = soup.select_one(css_selector)
    return abstract_element.text.strip().replace("Abstract:", "") if abstract_element else None

if __name__ == "__main__":

    # Get path to the bib file from CLI
    path2bib = sys.argv[1]
    seed_name = sys.argv[2]

    # Read bib file
    with open("mcq-seed.bib", 'r') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    # Get urls from bib file
    urls = [ref.get("url") for ref in bib_database.entries]

    # Scrape abstracts
    seed_abstracts = [fetch_arxiv_abstract(url) for url in tqdm(urls, desc="Scraping abstract seeds...")]
    
    # Collect all new arxiv papers
    new_papers = fetch_arxiv_cscl_new()
    new_abstracts = [paper["abstract"] for paper in new_papers]

    # Load sentence encoder model
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    # Project abstracts onto the model space
    seed_embeddings = model.encode(seed_abstracts)
    new_abstract_embeddings = model.encode(new_abstracts)

    # Compute cosine similarity
    similarities = model.similarity(new_abstract_embeddings, seed_embeddings)

    # Average the scores
    scores = similarities.mean(axis=1)

    # Rank new abstract average cosine similarity with seeds (from highest to lowest)
    ranking = np.argsort(scores).flip(0)

    # Write the ranking to a file
    with open(f"paper_watch_{seed_name.replace(' ', '-')}_{date.today()}.txt", "w") as f:
        reordered = [new_papers[i] for i in ranking]
        f.write(generate_latex_file(reordered, seed_name, date.today()))

