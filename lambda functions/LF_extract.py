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

    #estraggo il contenuto dal file
    s3_client = boto3.client('s3')
    nome_bucket = 'dati-scraping-test'
    obj = s3_client.get_object(Bucket=nome_bucket, Key=nome_file)
    data = obj['Body'].read().decode('utf-8')

    
    #r = requests.get(url)
    #base_url = get_base_url(r.text, r.url)
    """metadata = extruct.extract(data, 
                                   base_url=url,
                                   uniform=True,
                                   syntaxes=['json-ld',
                                             'microdata',
                                             'opengraph'])
    """
    #opzione alternativa con più parametri
    
    parsed_url = urlparse(url)
    base_url = parsed_url.netloc
    
    metadata = extruct.extract( data, 
                                base_url=base_url,
                                uniform=True)
                               
    return metadata

def my_handler(event, context):
    
    #riceve messaggi da coda link
    records = event['Records']
    #messaggio in coda è un item json con link e nome file da leggere
    
    for record in records:
        #per ogni messaggio ricevuto stampo il messaggio ricevuto
        body = record['body']
        print(body)
        
        body_json = json.loads(body)
        nome_file = body_json["nome"]
        link = body_json["link"]
        
        ris = extract_metadata(link, nome_file)

        #salvo i dati estratti in bucket
        s3 = boto3.resource('s3')
        bucket = "dati-scraping-estratti"

        nome_file_estratto = nome_file.replace(".txt", "")
        nome_file_estratto = nome_file_estratto + "_estratto.txt"
        
        s3.Object(bucket, nome_file_estratto).put(
            Body = json.dumps(ris) 
            )
