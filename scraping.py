import requests
from bs4 import BeautifulSoup

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
