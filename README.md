# ProgettoTesi

Lambda functions contiene le lambda functions create in AWS.
  LF_read_queue riceve in entrata messaggio da coda1 e manda messaggio a coda2
  LF_print riceve messaggio da coda2 e salva file txt nel bucket prescelto. Dovrebbe inviare in coda3 il link scaricato e il nome del file txt appena creato a LF_extract
  LF_extract contiene il codice per estrarre i metadata dal sito. Non ho ancora separato il download e l'estrazione perché volevo testare il codice in maniera isolata dal resto.

  In VScode segna come errore import boto3 (per mandare e ricevere mesaggi dalle code) ma in AWS non da problemi.

Test_docker contiene il docker file e il codice python usati per creare la docker image.
    (la docker image l'ho creata con comandi in shell AWS e Docker desktop)
