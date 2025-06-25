import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def fetch_arxiv_details(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    if "aclanthology" in url:
        css_selector = ".acl-abstract span"
        title_element = soup.select_one("#title")
    elif "arxiv" in url:
        css_selector = ".abstract"
        title_element = soup.select_one(".title")
    else:
        raise ValueError(f"Unsupported website referenced in {url}")
    
    abstract_element = soup.select_one(css_selector)
    abstract = abstract_element.text.strip().replace("Abstract:", "") if abstract_element else None
    title = title_element.text.strip().replace("Title:", "") if title_element else None

    return {"title" : title, "abstract" : abstract, "url" : url}

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

def fetch_all_abstracts(urls, max_workers=10):
    results = [None] * len(urls)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {executor.submit(fetch_arxiv_abstract, url): idx for idx, url in enumerate(urls)}
        for future in tqdm(as_completed(future_to_idx), total=len(urls), desc="Scraping abstract seeds..."):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"Error fetching URL at index {idx}: {e}")
    return results