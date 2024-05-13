import extruct
import requests
from w3lib.html import get_base_url
from urllib.parse import urlparse

def extract_metadata(url):
    """Extract all metadata present in the page and return a dictionary of metadata lists. 
    
    Args:
        url (string): URL of page from which to extract metadata. 
    
    Returns: 
        metadata (dict): Dictionary of json-ld, microdata, and opengraph lists. 
        Each of the lists present within the dictionary contains multiple dictionaries.
    """
    #url = "http://olympus.realpython.org/profiles/aphrodite"

    #La funzione è stata lasciata come originale per effettuare test
    #quando funzionerà r.text verrà sostituito dal testo scaricato precedentemente.

    r = requests.get(url)
    base_url = get_base_url(r.text, r.url)
    metadata = extruct.extract(r.text, 
                               base_url=base_url,
                               uniform=True,
                               syntaxes=['json-ld',
                                         'microdata',
                                         'opengraph'])
    
    return metadata
    #return r.text

def my_handler(event, context):
    #riceve messaggi da coda link
    records = event['Records']
    #intanto non riceve messaggi in coda perché è in fase di test.
    #ipotesi di avere come messaggio in coda un item json con link e nome file da leggere
    
        
    #link = "https://it.wikipedia.org/wiki/Web_scraping"
    link = "http://olympus.realpython.org/profiles/aphrodite"
    ris = extract_metadata(link)
    print(ris)