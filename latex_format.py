
from pylatex import Document, Section, Command, Package
from pylatex.utils import NoEscape

def format_paper_info(doc, paper):
    with doc.create(Section(paper["title"])):
        doc.append(NoEscape(r'\large \textbf{' + paper["authors"] + r'}\\' + "\n"))
        doc.append(NoEscape(r'\url{' + paper["url"] + r'}\\' + "\n"))
        doc.append(paper["abstract"] + "\n\n")

def generate_latex_file(papers, theme, date, filename):
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

    # Add all papers
    for paper in papers:
        format_paper_info(doc, paper)

    # Export .pdf and keep .tex
    doc.generate_tex(filename)
    #doc.generate_pdf(filename, clean_tex=False, silent=True)
