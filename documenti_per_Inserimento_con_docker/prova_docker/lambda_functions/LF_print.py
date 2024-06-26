from urllib import request
import boto3
from urllib.parse import urlparse

def crea_nome_file(url):
    
    #url = "https://it.wikipedia.org/wiki/Web_scraping"
    #serve controllare che non ci sia un'altro file con lo stesso nome
    parsed_url = urlparse(url)
    base_url=parsed_url.netloc
    
    base_url = base_url.replace(".", "_")

    return base_url + ".txt"

def my_handler(event, context):
    
    #r = request.urlopen("https://it.wikipedia.org/wiki/Web_scraping")
    #print(r.read())
    
    s3 = boto3.resource('s3')
    bucket = "dati-scraping-test"
   
    #riceve messaggi da coda link
    records = event['Records']
    
    for record in records:
        #per ogni messaggio ricevuto stampo il messaggio ricevuto
        body = record['body']
        print(body)
        
        #estraggo html del url inviato
        r = request.urlopen(body)

        testo = r.read()
        testo = testo.decode("utf-8")
        
        nome_file = crea_nome_file(body)
        
        s3.Object(bucket, nome_file).put(
            Body = testo 
            )
        
        #manca la parte di invio in coda per LF_extract