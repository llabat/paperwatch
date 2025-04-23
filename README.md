# 📰 PaperWatch

**PaperWatch** is a script-based tool to monitor and rank new papers in arXiv's Computational Linguistics category (`cs.CL`) based on their relevance to a Zotero collection. It uses semantic similarity to filter and format relevant papers into a LaTeX report.

---

## 🚀 Features

- Extracts seed paper abstracts from a Zotero collection
- Scrapes new `cs.CL` papers from arXiv
- Ranks new papers by semantic similarity to seed papers using Sentence Transformers
- Automatically generates a LaTeX report with formatted abstracts and metadata
- Outputs a final PDF for easy reading

---

## 📦 Requirements

- Python 3.7+
- Working `pdflatex` command in your system (e.g., via TeX Live or MikTeX)
- The `lastpage` LaTeX package must be installed (*tlmgr install lastpage*)
- Dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

You can install a lightweight version of pdflatex :
- on MacOS:
```bash
curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
```
- on Linux:
```bash
wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh
```

---

## 🛠 Usage
```bash
python main.py <collection_name> <zotero_user_id> <zotero_api_key>
```


This will:
1. Fetch the paper links from your Zotero collection  
2. Scrape abstracts from these papers  
3. Get the latest `cs.CL` papers from arXiv  
4. Rank them by similarity to your Zotero collection  
5. Generate a LaTeX document and convert it to a PDF  

---

## 📝 Output

You’ll find a PDF file named like:
```bash
paperwatch_<collection_name>_<today's date>.pdf
```

This file contains the most relevant new `cs.CL` arXiv papers formatted for review.

---

## 📄 License

MIT License

---

## 🤝 Contributions

Feel free to open issues or submit PRs to improve PaperWatch!