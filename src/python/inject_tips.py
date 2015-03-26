import fnmatch
import os
import re
import shutil
import subprocess
import urllib

from choose_reference import choose_reference
from find_terms import find_terms, remove_non_ascii_characters


def get_inject_css():
    return "    <link rel=\"stylesheet\" type=\"text/css\"" \
        + " href=\"inject_style.css\">\n"

#------------------------------------------------------------------------------
def get_inject_string(word, term, description = "Good news, everyone!"):
    result = "<a class=\"tooltip_inj\" href=\"#\">\n" + word + "\n"
    result += "<span class=\"custom help_inj\">\n"
    result += "<img src=\"clipboard.png\""
    result += "height=\"32\" width=\"32\" />"
    result += "<em> " + term + "</em>"
    result += description + " </span> </a>"
    return result
#------------------------------------------------------------------------------
def inject_tips_into_page(page, hints):
    # Step 1: inject css.
    pos = page.find("</head>")
    page = page[:pos] + get_inject_css() + page[pos:]
    
    # Step 2: inject tips.    
    index = page.find("<body")
    body = page[index:]
    for term in hints:
        body = re.sub(" (" + term + "[\a-zA-Z_]*[\ ,-;:])", r'zzz\1', 
                      body)
    body = body.replace("zzzzzz", "zzz"); 
    body = body.replace("zzzzzz", "zzz"); 
    body = body.replace("zzzzzz", "zzz"); 
    body = body.replace("zzzzzz", "zzz"); 
    for term in hints:
        body = body.replace("zzz" + term, " " + get_inject_string(term,
                            hints[term][0].encode("utf-8"), 
                            hints[term][1].encode("utf-8")))    
    return page[:index] + body

#------------------------------------------------------------------------------
def find_files(directory, pattern):
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename
                    
#------------------------------------------------------------------------------
if __name__ == "__main__":      
    url = "http://www.sciencedaily.com/releases/2014/04/140404140401.htm"
    
    with open("term_list.txt", "r") as f:
        lines = f.readlines()
        terms = []
        for line in lines:
            terms += line.split()
            
    subprocess.call(["wget", "-p", "--convert-links", url])
    
    dir = re.findall("www[.].*[.]com", url)[0]
    for filename in find_files(dir, '*.htm*'):
        break
    
    
    shutil.copyfile("inject_style.css", 
                    os.path.dirname(filename) + "/inject_style.css")
    shutil.copyfile("clipboard.png", 
                    os.path.dirname(filename) + "/clipboard.png")
    page = urllib.urlopen(filename).read()
        
    end_terms = []
    for term in terms:
        if page.find(term) > 0:
            end_terms += [term]
    print end_terms
    
    def sim_f(summaries):
        return choose_reference(remove_non_ascii_characters(page), 
                                [item for item in summaries],
                                "hamming")
     
    hints = find_terms(end_terms, 5, sim_f, show_time=True)
    
    page = inject_tips_into_page(page, hints)
    
    with open(filename, "w") as f:
        print >>f, page
    
    subprocess.Popen(['xdg-open', filename])
    