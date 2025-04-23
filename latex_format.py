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
