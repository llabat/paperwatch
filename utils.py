import os
import subprocess

def clean_up(texfile_name):
    name = texfile_name.replace(".tex", "")
    superfluous_files = [filename for filename in os.listdir(os.curdir) if name in filename and not filename.endswith(".pdf")]
    for filename in superfluous_files:
        os.remove(filename)
    
def generate_pdf(path_to_texfile):
    result = subprocess.run(["pdflatex", "-interaction=nonstopmode", path_to_texfile])