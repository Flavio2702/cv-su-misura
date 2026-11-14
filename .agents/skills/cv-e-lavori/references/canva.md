# Procedura Canva configurabile

Serve un connettore Canva dell'assistente e un template che l'utente possa usare.
Non è incluso un asset Canva. Leggi `private/canva.json`: template_id, eventuale
mappa dei blocchi e limiti di layout devono riferirsi al template dell'utente.
Se vuoti, chiedi il template o usa la versione PDF locale. Non recuperare template
da precedenti candidature o altri account.

1. Scopri gli strumenti disponibili per copia, lettura/modifica e export. I nomi
   e contratti cambiano: usa lo schema effettivamente esposto, non comandi presunti.
   Se manca una capacità, dichiarala e conserva il Markdown per il fallback locale.
2. Copia il template e registra ID e link della copia solo nella cartella privata.
   Verifica che l'ID sia diverso dall'originale prima di modificare.
3. Leggi contenuto e anteprime della copia. Ricava i locator attuali dal documento,
   riconosci nome, titolo, profilo, contatti, esperienze, formazione e lingue.
   La mappa locale aiuta, ma non sostituisce la lettura. Mai mantenere contatti,
   foto, link o testi preesistenti non confermati per questo candidato.
4. Sostituisci testo e titolo della copia. Conserva stili, marcatori elenco e ordine
   di lettura. Non aggiungere blocchi in fondo ai livelli se altera la lettura del
   PDF; preferisci blocchi esistenti. Se serve ristrutturare, controlla nuovamente
   ordine e secondo lettore. Non modificare il template originale.
5. Rileggi altezze e coordinate restituite dopo ogni modifica. Per ogni colonna:
   corpo sotto il titolo, blocco successivo sotto il precedente più spaziatura;
   controlla top + altezza entro altezza pagina meno margine basso. Nessun ID,
   coordinata o font dell'autore è un'impostazione universale.
6. Se il testo sfora, elimina ridondanze e accorcia prima di ridurre il font;
   rispetta il minimo leggibile concordato. Se resta molto spazio, aumenta
   uniformemente interlinea e spaziatura entro i limiti locali, rileggendo le
   altezze dopo ogni passo. Titolo non sovrapposto al profilo, colonne coerenti.
7. Mostra l'anteprima per l'approvazione prevista dal connettore. In una transazione
   aperta, salva solo dopo approvazione; annulla se l'utente rinuncia. Nei test
   non salvare né esportare dati reali. Se lo schema non supporta transazioni,
   segui il relativo flusso di revisione e lavora sempre sulla copia.
8. Esporta PDF con il formato consentito, salva come nuova versione locale, apri
   con i due verificatori e guarda tutte le pagine. Su errore correggi la copia
   Canva e ripeti anteprima/approvazione, non soltanto il PDF scaricato.
9. Consegna il link della copia e il PDF verificato. Nessuna candidatura viene inviata.

Errori: autorizzazione scaduta → chiedi riconnessione o fallback; timeout/esito
incerto di copia o salvataggio → leggi lo stato prima di ritentare, evita duplicati;
export fallito → non dichiarare PDF pronto; locator obsoleto → rileggi il documento;
modello AI assente → non fingere l'adattamento, restano strumenti PDF locali.
La procedura è revisionata, ma non collaudata live in questa distribuzione.
