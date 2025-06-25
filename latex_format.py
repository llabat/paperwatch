from pylatex import Document, Section, Command, Package
from pylatex.utils import NoEscape

def escape_latex(text):
    return (text.replace("&", "\\&")
                .replace("%", "\\%")
                .replace("_", "\\_")
                .replace("#", "\\#")
                .replace("{", "\\{")
                .replace("}", "\\}")
                .replace("$", "\\$")
                .replace("^", "\\^{}")
                .replace("~", "\\~{}")
                .replace("\\", "\\textbackslash{}"))

def generate_latex_table(specials, seeds, id2paper, max_rows=None):
    rows = []
    for i, (paper_id, pairs) in enumerate(specials.items()):
        if max_rows and i >= max_rows:
            break

        paper = id2paper[paper_id]
        title = escape_latex(paper["title"])
        authors = "\\scriptsize " + escape_latex(paper["authors"])
        abstract = f"\\scriptsize {escape_latex(paper['abstract'])[:300]}..."
            
        if len(pairs) == 1:
            seed_id, sim = pairs[0]
            seed_title = escape_latex(seeds[seed_id]["title"])
            seed_info = f"\\scriptsize {seed_title} ({sim:.2f})"
        else:
            seed_items = []
            for seed_id, sim in pairs:
                seed_title = escape_latex(seeds[seed_id]["title"])
                seed_items.append(f"\\item {seed_title[:int(len(seed_title)/1.3)]}... ({sim:.2f})")
            seed_info = "\\scriptsize " + "\n".join(seed_items)

        rows.append(f"{title} & {authors} & {abstract} & {seed_info} \\\\")

    latex = "\\begin{center}\n\\Large\\textbf{Standouts}\n\\end{center}\n\\vspace{0.5em}"
    latex += "\\begin{tabular}{|p{4cm}|p{2cm}|p{4cm}|p{4cm}|}\n"
    latex += "\\hline\n"
    latex += "Title & Authors & Abstract & Seeds \\\\\n"
    latex += "\\hline\n"
    latex += "\n\\hline\n".join(rows)
    latex += "\n\\hline\n\\end{tabular}"
    return latex

def format_paper_info(doc, paper):
    with doc.create(Section(paper["title"])):
        doc.append(NoEscape(r'\large \textbf{' + paper["authors"] + r'}\\' + "\n"))
        doc.append(NoEscape(r'\url{' + paper["url"] + r'}\\' + "\n"))
        doc.append(paper["abstract"] + "\n\n")

def generate_latex_file(papers, theme, date, standouts, filename):
    # Setup document with custom geometry
    doc = Document(documentclass='article')
    
    # Add packages
    doc.packages.append(Package('babel', options='english'))
    doc.packages.append(Package('geometry', options='letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm'))
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('hyperref', options='colorlinks=true, allcolors=blue'))

    # Add title and metadata
    doc.preamble.append(Command('title', NoEscape(f'Paper Watch (arXiv)\\\\ \\Large {theme}')))
    doc.preamble.append(Command('author', 'Leo Labat'))
    doc.preamble.append(Command('date', date))
    doc.append(NoEscape(r'\maketitle'))

    doc.append(NoEscape(standouts))

    # Add all papers
    for paper in papers:
        format_paper_info(doc, paper)

    # Export .pdf and keep .tex
    doc.generate_tex(filename)
    #doc.generate_pdf(filename, clean_tex=False, silent=True)
