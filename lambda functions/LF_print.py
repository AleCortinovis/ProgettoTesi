from urllib import request
import json
import boto3
from urllib.parse import urlparse

def esiste_file(file_name):
    s3_client = boto3.client('s3')
    s3_bucket = "dati-scraping-test"
    controllo = 0
    ris = s3_client.list_objects(Bucket = s3_bucket)
    
    for obj in ris.get('Contents'):
        key = obj.get('Key')
        if key == file_name:
            controllo = 1
    
    return controllo

def crea_nome_file(url):
    
    #url = "https://it.wikipedia.org/wiki/Web_scraping"
    parsed_url = urlparse(url)
    base_url=parsed_url.netloc
    
    base_url = base_url.replace(".", "_")
    nome_file = base_url + ".txt"
    
    controllo = esiste_file(nome_file)
    counter = 0
    
    while controllo == 1:
        counter += 1
        print(counter)
        num = str(counter)
        nome_file = base_url + "_" + num + ".txt"
        controllo = esiste_file(nome_file)
        
    return nome_file

def my_handler(event, context):
    
    client = boto3.client("sqs")  
    
    s3 = boto3.resource('s3')
    bucket = "dati-scraping-test"
    
    
    #riceve messaggi da coda link
    records = event['Records']
    
    for record in records:
        #per ogni messaggio ricevuto stampo il messaggio ricevuto
        body = record['body']
        #print(body)
        
        #estraggo html del url inviato
        r = request.urlopen(body)
        
        testo = r.read()
        testo = testo.decode("utf-8")
        
        nome_file = crea_nome_file(body)
        
        s3.Object(bucket, nome_file).put(
            Body = testo 
            )
        
        print(nome_file)
        
        client = boto3.client("sqs") 
        
        #manda a coda print-extract 
        #il nome del file da analizzare e il link per poter eseguire la funzione extruct.extract
        
        msg_to_extract_json = {
            "nome": nome_file,
            "link": body
        }
        print(nome_file)
        msg_to_extract = json.dumps(msg_to_extract_json)
        
        print(msg_to_extract)
        
        response = client.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/760507411025/coda-print-extract",
            MessageBody=msg_to_extract)
