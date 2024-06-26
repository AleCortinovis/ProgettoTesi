import boto3

def my_handler(event, context):
    #print(event)
    
    #riceve messaggi da coda test
    records = event['Records']
    
    for record in records:
        #per ogni messaggio ricevuto stampo il messaggio ricevuto
        body = record['body']
        print(body)
        
        client = boto3.client("sqs")
        response = client.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/760507411025/coda-link",
            MessageBody=body)