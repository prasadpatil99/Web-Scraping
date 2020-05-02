import urllib
import re
import bs4 

link = 'https://en.wikipedia.org/wiki/Quantum_machine_learning'

def req(link):
    raw = urllib.request.urlopen(link).read()
    soup = bs4.BeautifulSoup(raw, 'lxml')
    return soup

raw_data = req(link)

text = ""
for paragraph in raw_data.find_all('p'):    # extract from 'p' tag
    text += paragraph.text
    
def preprocess(data):
    text = re.sub(r'\[[0-9]*\]',' ',data)   # remove numbers
    text = re.sub(r'\s+',' ',text)          # eliminate duplicate whitespaces
    text = text.lower()                     # remove capital lettera
    return text

data = preprocess(text)