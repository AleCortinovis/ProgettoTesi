import extruct
import json
import boto3
from w3lib.html import get_base_url
from urllib.parse import urlparse

def extract_metadata(url, nome_file):
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


    #estraggo il contenuto dal file
    s3_client = boto3.client('s3')
    nome_bucket = 'dati-scraping-test'
    #bucket = s3.BUcket('dati-scraping-test')
    obj = s3_client.get_object(Bucket=nome_bucket, Key=nome_file)
    data = obj['Body'].read().decode('utf-8')
    #print(data)
    #print("____--fine estrazione dati--_____")
    
    #r = requests.get(url)
    #base_url = get_base_url(r.text, r.url)
    """metadata = extruct.extract(data, 
                               base_url=url,
                               uniform=True,
                               syntaxes=['json-ld',
                                         'microdata',
                                         'opengraph'])
    """
    metadata = extruct.extract(data, 
                               base_url=url)
                               
    return metadata

def my_handler(event, context):
    
    #riceve messaggi da coda link
    records = event['Records']
    #intanto non riceve messaggi in coda perché è in fase di test.
    #ipotesi di avere come messaggio in coda un item json con link e nome file da leggere
    
    for record in records:
        #per ogni messaggio ricevuto stampo il messaggio ricevuto
        body = record['body']
        print(body)
        
        body_json = json.loads(body)
        nome_file = body_json["nome"]
        #print("nome_file = " +  nome_file)
        link = body_json["link"]
        #print("link = " +  link)
        #print("____----_____")
                
        #link = "https://it.wikipedia.org/wiki/Web_scraping"
        #link = "http://olympus.realpython.org/profiles/aphrodite"
        
        ris = extract_metadata(link, nome_file)
        
        print(ris)

        #salvo i dati estratti in bucket
        s3 = boto3.resource('s3')
        bucket = "dati-scraping-estratti"

        nome_file_estratto = nome_file.replace(".txt", "")
        nome_file_estratto = nome_file_estratto + "_estratto.txt"
        
        s3.Object(bucket, nome_file_estratto).put(
            Body = json.dumps(ris) 
            )

