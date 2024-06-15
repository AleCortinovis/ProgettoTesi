import boto3

client = boto3.client("sqs")

def my_handler(event, context):
    
    #riceve messaggi da coda test
    records = event['Records']
    
    for record in records:
        #per ogni messaggio ricevuto stampo il messaggio ricevuto
        body = record['body']
        print(body)
        
        response = client.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/760507411025/coda-link",
            MessageBody=body)
