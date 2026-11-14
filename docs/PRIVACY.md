# Privacy e limiti

Questa distribuzione contiene soltanto codice, procedure neutrali e dati inventati.
Sono esclusi CV e lettere reali, profili, contatti, preferenze identificative,
esperienze, candidature, annunci reali, foto, firme, template remoti e identificativi,
chat, tracker, chiavi, credenziali, ambienti, cache, log, backup e cronologia privata.

`private/`, `sources/`, `operativo/`, `candidature/`, runtime e configurazioni locali
sono ignorati da Git. `.gitignore` non protegge dati salvati altrove né un `git add -f`.
Prima di pubblicare rivedi l'elenco esatto dei file, metadati e contenuti binari;
Gitleaks cerca segreti, non tutti i dati personali. Gli strumenti di audit non
devono caricare file privati né pubblicarne frammenti nei log CI.

Gli script PDF lavorano localmente. Quando usi un assistente, il materiale che gli
fornisci può essere inviato al servizio AI e agli strumenti attivati. Canva riceve
il testo impaginato. Verifica impostazioni e condizioni del tuo account e condividi
solo ciò che serve. Abbonamenti, eventuali consumi e costi sono a carico dell'utente;
nessuna chiamata a pagamento avviene nei test. Non è incluso un client API.
Se una credenziale è esposta, revocala o ruotala: rimuovere un file non basta.

I controlli automatici non certificano la verità: un numero già nel master può
essere associato alla frase sbagliata, una nuova affermazione senza numeri può
passare, una negazione può contenere un termine vietato. La prova CSV è un riferimento
da controllare a mano, non una verifica semantica della fonte. Mancanze documentali
non equivalgono a competenze assenti. Nessuna promessa ATS o di selezione.
Non vengono fornite conclusioni legali: condizioni contrattuali poco chiare sono
domande da rivolgere al selezionatore, non violazioni presunte.

PDF di terzi possono contenere autore, XMP, commenti, allegati e azioni. Il report
locale li aiuta a ispezionare ma non li bonifica automaticamente. La demo è generata
da zero e non contiene allegati, XMP, commenti o fotografie. Non c'è supporto DOCX,
OCR o garanzia di lettura universale dei PDF. Usa strumenti aggiornati per file non fidati.
