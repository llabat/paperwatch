import os
import subprocess
from latex_format import generate_latex_file

def clean_up(texfile_name):
    name = texfile_name.replace(".tex", "")
    superfluous_files = [filename for filename in os.listdir(os.curdir) if name in filename and not filename.endswith(".pdf")]
    for filename in superfluous_files:
        os.remove(filename)
    
def generate_pdf(path_to_texfile):
    result = subprocess.run(["pdflatex", "-interaction=nonstopmode", path_to_texfile])

def generate_ranking_pdf(papers, theme, date, standouts, filename):
    generate_latex_file(papers, theme, date.today(), standouts, filename)
    texfile = filename + ".tex"
    generate_pdf(texfile)
    clean_up(texfile)