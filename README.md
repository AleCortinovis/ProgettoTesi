# ProgettoTesi - soluzione scalabile e in cloud per web scraping

Il progetto consiste nel creare una semplice applicazione che ricebuto in ingresso uno o più siti, li analizzi e restituisca il codice html e estrai i dati contenuti al loro interno, ovviamente se fosse possibile estrarre i dati.

la cartella Lambda functions contiene le lambda functions create in AWS e in Visual Studio Code.
- lambda_read_queue ha lo scopo di leggere i messaggi ricevuti in coda e di inviarli uno alla volta alla funzione successiva tramite una seconda coda, facendo da buffer per l’invio dell’elenco dei siti da analizzare.
- lambda_print una volta ricevuto il messaggio inizia ad analizzare il sito effettuando una richiesta GET per ottenere lo script HTML della pagina. Successivamente salva lo script all’interno di un file di testo nel bucket S3 apposito, ma non prima di aver controllato l’esistenza del file: infatti se si salvasse un file con lo stesso nome di un altro file presente nel bucket, l’ultimo sovrascriverebbe il documento precedente. Infine, la funzione, tramite una terza e ultima coda SQS, invia un messaggio contenente il link del sito appena analizzato e il nome del file appena salvato alla terza funzione.
- lambda_extract ha il compito di estrarre i contenuti della pagina ricevuta in ingresso. I dati estratti sono a loro volta salvati in un nuovo file nello spazio di storage apposito.

*più nel dettaglio:*

La funzione lambda_read_queue, come descritto nella sezione precedente, serve solo da buffer per l’invio dell’elenco dei siti alla funzione lambda_print. È attivata dai messaggi ricevuti in ingresso e a sua volta invia messaggi in una seconda coda. Lo sviluppo della funzione è stato fatto direttamente in AWS, dal pannello della sezione codice della Lambda Function.

Anche la funzione lambda_print è stata realizzata in AWS, e il suo funzionamento è triggerato dalla seconda coda di messaggi popolata dalla prima lambda function. Ricevuto il messaggio con l’URL del sito da analizzare, la funzione estrae il codice HTML con codifica utf-8 ed è pronto per salvarlo in un file di testo per la successiva analisi ed estrazione. 
Il file di testo viene denominato automaticamente grazie a una funzione che, dato l’URL in ingresso, restituisce il nome del sito senza i componenti del percorso o query. Ovviamente prima di restituire il nome del file creato, serve verificare la presenza o meno di altri file con lo stesso nome per evitare la sovrascrittura e perdita dei dati precedentemente raccolti. Questo viene fatto tramite una seconda funzione che controlla l’esistenza dei file nel bucket S3 e restituisce 1 se esiste il file. Il controllo viene effettuato in una prima istanza con il nome del sito e se esiste il controllo viene fatto sul vecchio nome con accodato “_” e un numero che viene incrementato finché non si trova un nome che non esiste già.
Quando il nome del file è stato scelto, il codice estratto viene salvato nel bucket prescelto. 
Come ultimo passo la funzione invia un messaggio in formato JSON grazie a una coda SQS alla funzione per estrarre i dati, contenente il link del sito che è stato analizzato e il nome del file in cui è stato salvato.

{“nome”: nome_del_file_appena_salvato,
  “link”: link_del_file_ricevuto_in_ingresso}


La funzione lambda_extract dopo aver ricevuto in ingresso il messaggio, salva i dati ricevuti in variabili singole e procede con l’esecuzione dell’estrazione.
L’estrazione dei dati viene effettuata tramite la funzione extract del pacchetto extruct presente in Python. La funzione extruct.extract ricevuti in ingresso il codice html e il link del sito restituisce valori di microdata, json-Id, opengraph, microformat, rdfa e dublincore. Per il progetto non si è fatto distinzione, ma si può specificare il tipo di dato che deve essere restituito nel campo syntaxes della funzione. 
I valori estratti sono salvati in maniera simile a come effettuato nella funzione precedente: viene aggiunto in coda al nome del file del codice “_estratto” (facendo diventare nell’esempio di it_wikipedia_org_1.txt in it_wikipedia_org_1_estratto.txt) e viene salvato nel bucket predefinito per i file estratti.



