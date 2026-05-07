# WEEKS 1-2 (11-03-2026 - 25-03-2026)
Espansione del dataset del repo "LLMDesignPatternRefactoring" con l'implementazione di tre esempi distinti per ognuno 
dei seguenti design patterns:

- **Abstract factory pattern**
- **Builder pattern** 
- **Proxy pattern**
- **Command pattern** 
- **Template method pattern**

Gli esempi sono implementati in Python, sono commentati per facilitare la comprensione e cercano di esibire al meglio
le caratteristiche principali di ogni pattern.

Il dataset è stato organizzato nel seguente modo:

```
.
├── README.md
└── data
    ├── createjson.py
    ├── dataset.json
    └── pattern_examples
        ├── behavioural
        │   ├── command
        │   │   ├── baseline
        │   │   └── refactored
        │   │       ├── bankaccount.py
        │   │       ├── restaurant.py
        │   │       └── rover.py
        │   ├── state
        │   │   ├── baseline
        │   │   └── refactored
        │   │       ├── Stall.py
        │   │       ├── elevator.py
        │   │       └── traffic_light.py
        │   ├── strategy
        │   │   ├── baseline
        │   │   └── refactored
        │   │       ├── Vector.py
        │   │       ├── graphtraversal.py
        │   │       └── validator.py
        │   └── template_method
        │       ├── baseline
        │       └── refactored
        │           ├── departure.py
        │           ├── formfilling.py
        │           └── rescuelogic.py
        ├── creational
        │   ├── abstract_factory
        │   │   ├── baseline
        │   │   └── refactored
        │   │       ├── battle.py
        │   │       ├── house.py
        │   │       └── tv.py
        │   ├── builder
        │   │   ├── baseline
        │   │   └── refactored
        │   │       ├── computer.py
        │   │       ├── datastructurebuilder.py
        │   │       └── gamengine.py
        │   └── factory_method
        │       ├── baseline
        │       └── refactored
        │           ├── car.py
        │           ├── monster.py
        │           └── wand.py
        └── structural
            ├── adapter
            │   ├── baseline
            │   └── refactored
            │       ├── calculator.py
            │       ├── gridmovement.py
            │       └── roundhole.py
            ├── decorator
            │   ├── baseline
            │   └── refactored
            │       ├── cafecito.py
            │       ├── icecream.py
            │       └── sword.py
            └── proxy
                ├── baseline
                └── refactored
                    ├── blockchain.py
                    ├── deliveryvehicles.py
                    └── tenantproxy.py
```

I pattern sono stati organizzati in cartelle per tipologia; inoltre per ciascun pattern è presente una divisione
nelle sottocartelle "refactored", che contiene i tre esempi che implementano correttamente il pattern, e "baseline",
che contiene i tre rispettivi esempi equivalenti che non implementano il pattern o lo fanno parzialmente.
Si è cercato di espandere il dataset coinvolgendo esempi non facilmente riconducibili alla letteratura, al fine di 
facilitare la comprensione della reale capacità di generalizzazione dei modelli a domini nuovi.

È stato creato un file JSON per organizzare i file, utilizzando un script Python. L'obiettivo è strutturare
un dataset "accoppiato", in modo che per ogni esempio refactored sia presente anche l'esempio baseline. Per ogni esempio 
sono stati memorizzati diversi attributi, quali l'identificatore univoco della coppia, il nome del pattern, la categoria 
del pattern, percorso relativo del file refactored, il percorso relativo del file baseline e una descrizione di cosa 
tratta l'esempio.

Le versioni baseline degli esempi e le descrizioni nel JSON sono ancora da implementare.

# WEEKS 3-4-5 (25-03-2026 - 14-04-2026)
Riorganizzazione del file json come segue:
- Rappresentazione del campo “pattern” come una lista di possibili pattern applicabili (se singolo pattern, una sola 
  etichetta nella lista, se più pattern tutte le etichette possibili nella lista);
- Rappresentazione del campo “path_refactored” come una lista di path alle versioni refactored (una sola se singolo 
  pattern, più versioni se più pattern applicabili) 
- Aggiunta di un campo “tests_refactored” contenente una lista di path dei test per le diverse versioni refactored 
- Aggiunta di un campo “tests_baseline” che contiene il path del test per la versione baseline

**Scelta di implementazione delle batterie di test:**
L'obiettivo è sviluppare un sistema di classificazione per rilevare i Design Pattern mediante LLM. Manipolando frammenti
per un dataset di ricerca mirato all'analisi architetturale e non codice destinato a un sistema in produzione, 
implementare una gestione approfondita degli errori di input o dei casi limite sarebbe potutto risultare
controproducente. Dato che i modelli linguistici e i sistemi di classificazione si basano sull'analisi della struttura, 
delle interfacce e delle dipendenze, saturare il codice con validazioni difensive avrebbe aumentato il rischio di 
mascherare la logica del pattern, aggiungendo "rumore" che peggiorerebbe le performance del classificatore 
nell'individuare la struttura d'interesse. 

Riorganizzato il dataset come segue:
- Creazione di un'unica cartella “baseline” contenente tutti i file Python non rifattorizzati 
- Creazione di un'unica artella “refactored” contenente tutte le versioni rifattorizzate (refactoring diversi di stessi 
  file distinti tramite naming convention) 

Nuova struttura del dataset:
```
.
├── baseline
│   ├── Stall_baseline.py
│   ├── Vector_baseline.py
│   ├── bankaccount_baseline.py
│   ├── battle_baseline.py
│   ├── cafecito_baseline.py
│   ├── calculator_baseline.py
│   ├── car_baseline.py
│   ├── computer_baseline.py
│   ├── datastructure_baseline.py
│   ├── deliveryvehicles_baseline.py
│   ├── departure_baseline.py
│   ├── elevator_baseline.py
│   ├── formfilling_baseline.py
│   ├── gamengine_baseline.py
│   ├── graphtraversal_baseline.py
│   ├── gridmovement_baseline.py
│   ├── house_baseline.py
│   ├── icecream_baseline.py
│   ├── ledger_baseline.py
│   ├── monster_baseline.py
│   ├── rescuelogic_baseline.py
│   ├── restaurant_baseline.py
│   ├── roundhole_baseline.py
│   ├── rover_baseline.py
│   ├── sword_baseline.py
│   ├── tenant_baseline.py
│   ├── traffic_light_baseline.py
│   ├── tv_baseline.py
│   ├── validator_baseline.py
│   └── wand_baseline.py
├── refactored
│   ├── Stall_refactored.py
│   ├── Vector_refactored.py
│   ├── bankaccount_refactored.py
│   ├── battle_refactored_af.py
│   ├── battle_refactored_fm.py
│   ├── cafecito_refactored.py
│   ├── calculator_refactored.py
│   ├── car_refactored_af.py
│   ├── car_refactored_fm.py
│   ├── computer_refactored.py
│   ├── datastructure_refactored.py
│   ├── deliveryvehicles_refactored.py
│   ├── departure_refactored.py
│   ├── elevator_refactored.py
│   ├── formfilling_refactored.py
│   ├── gamengine_refactored.py
│   ├── graphtraversal_refactored.py
│   ├── gridmovement_refactored.py
│   ├── house_refactored_af.py
│   ├── house_refactored_fm.py
│   ├── icecream_refactored.py
│   ├── ledger_refactored.py
│   ├── monster_refactored_af.py
│   ├── monster_refactored_fm.py
│   ├── rescuelogic_refactored.py
│   ├── restaurant_refactored.py
│   ├── roundhole_refactored.py
│   ├── rover_refactored.py
│   ├── sword_refactored.py
│   ├── tenant_refactored.py
│   ├── traffic_light_refactored.py
│   ├── tv_refactored_af.py
│   ├── tv_refactored_fm.py
│   ├── validator_refactored.py
│   ├── wand_refactored_af.py
│   └── wand_refactored_fm.py
├── tests_baseline
│   ├── Stall_baseline_test.py
│   ├── Vector_baseline_test.py
│   ├── bankaccount_baseline_test.py
│   ├── battle_baseline_test.py
│   ├── cafecito_baseline_test.py
│   ├── calculator_baseline_test.py
│   ├── car_baseline_test.py
│   ├── computer_baseline_test.py
│   ├── datastructure_baseline_test.py
│   ├── deliveryvehicles_baseline_test.py
│   ├── departure_baseline_test.py
│   ├── elevator_baseline_test.py
│   ├── formfilling_baseline_test.py
│   ├── gamengine_baseline_test.py
│   ├── graphtraversal_baseline_test.py
│   ├── gridmovement_baseline_test.py
│   ├── house_baseline_test.py
│   ├── icecream_baseline_test.py
│   ├── ledger_baseline_test.py
│   ├── monster_baseline_test.py
│   ├── rescuelogic_baseline_test.py
│   ├── restaurant_baseline_test.py
│   ├── roundhole_baseline_test.py
│   ├── rover_baseline_test.py
│   ├── sword_baseline_test.py
│   ├── tenant_baseline_test.py
│   ├── traffic_light_baseline_test.py
│   ├── tv_baseline_test.py
│   ├── validator_baseline_test.py
│   └── wand_baseline_test.py
└── tests_refactored
    ├── Stall_refactored_test.py
    ├── Vector_refactored_test.py
    ├── bankaccount_refactored_test.py
    ├── battle_refactored_af_test.py
    ├── battle_refactored_fm_test.py
    ├── cafecito_refactored_test.py
    ├── calculator_refactored_test.py
    ├── car_refactored_af_test.py
    ├── car_refactored_fm_test.py
    ├── computer_refactored_test.py
    ├── datastructure_refactored_test.py
    ├── deliveryvehicles_refactored_test.py
    ├── departure_refactored_test.py
    ├── elevator_refactored_test.py
    ├── formfilling_refactored_test.py
    ├── gamengine_refactored_test.py
    ├── graphtraversal_refactored_test.py
    ├── gridmovement_refactored_test.py
    ├── house_refactored_af_test.py
    ├── house_refactored_fm_test.py
    ├── icecream_refactored_test.py
    ├── ledger_refactored_test.py
    ├── monster_refactored_af_test.py
    ├── monster_refactored_fm_test.py
    ├── rescuelogic_refactored_test.py
    ├── restaurant_refactored_test.py
    ├── roundhole_refactored_test.py
    ├── rover_refactored_test.py
    ├── sword_refactored_test.py
    ├── tenant_refactored_test.py
    ├── traffic_light_refactored_test.py
    ├── tv_refactored_af_test.py
    ├── tv_refactored_fm_test.py
    ├── validator_refactored_test.py
    ├── wand_refactored_af_test.py
    └── wand_refactored_fm_test.py
```

## Introduzione naming convention per pattern rifattorizzati più volte
L'introduzione di più versioni rifattorizzate (come per esempio il dualisimo abstract_factory - factory_method) porta
alla necessità di introdurre una naming convention specializzata per gestire questi tipi di esempi refactored:
- Abstract Factory → af
- Factory Method → fm
- Builder → bld
- Command → cmd
- Strategy → str
- Template Method → tm
- State → state
- Proxy → proxy
- Decorator → dec
- Adapter → adp


# WEEKS 6-7 (17-04-2026 - 27-04-2026)

Aggiunto il suffisso con il nome del pattern nei refactored.

Il pattern Proxy potrebbe creare problemi, specie se il proxy inserito “altera” il funzionamento (feature presente 
anche nella baseline, ma forse difficilmente riconoscibile). Come conseguenza di ciò è stato aggiunto un esempio di 
proxy logger, che fa solo task secondari in modo trasparente.

Necessario anche tener conto della sperimentazione del lavoro, in particolare del fatto che per un dato codice sorgente 
potrebbero esserci più pattern “corretti” che potrebbero essere applicati (ad esempio, “strategy” al posto di “command”,
“abstract factory” invece di “factory method”, “proxy” sempre applicabile, ecc.).

Modifiche rilevanti effettuate:
- Annotato il dataset con tutti i pattern applicabili a un dato esempio (oltre a quello già previsto; senza 
  necessariamente andare a crearne la versione rifattorizzata). L'idea è essere “aperti” a “active learning”, aka. 
  successive integrazioni valutando risposte dei modelli.
- Aggiunto supporto a una sperimentazione che misuri “accuracy” come “mi suggerisce uno dei pattern applicabili”, oltre 
  a prevedere la possibilità di “privilegiare” (lista in ordine di priorità, accuracy@top-k) i pattern che sarebbe 
  meglio applicare.

## Fase 1: partizionare il dataset in training set e test set 
Creati due nuovi file JSON, training_set.json e test_set.json, rispettivamente contenenti i dati di training e di 
test. Le partizioni sono state strutturate selezionando un esempio per pattern da inserire nel test set, lasciando al
training set i restanti esempi.

- Training set: [0,2,3,5,6,8,9,10,13,14,15,17,18,19,22,23,24,25,27,28,29]
- Test set: [1,4,7,11,12,16,20,21,26,30]

Gli esempi scelti per il test sono, a mio avviso, tra i baseline più “challenging” e meno banali per il pattern di 
riferimento(responsabilità mescolate, alternative plausibili nella lista di priorità dei pattern applicabli). 
L'obiettivo non è penalizzare in fase di valutazione o semplificare il training del modello (che ha già a disposizione 
esempi interessanti), ma avere la sicurezza nella fase di test di sottoporlo a situazioni più "realistiche" evitando 
query composte da esempi "didattici" o "troppo semplici".

## Fase 2: creazione del system prompt per l'LLM
Richiedere un insieme di predizioni su un dataset talmente strutturato, con 21 codici baseline, rende meno invitante
gestire "manualmente" il prompting ai modelli e il salvataggio dei risultati. Per questo motivo ho creato una procedura
automatizzata, nello script prompts_engineering.py, che, leggendo da un file json dove sono memorizzati le 
configurazioni prompt-modello ("prompts.json"), itera richiedendo predizioni sull'intero training set. Per implementarlo
ho consultato alcune sezioni della libreria offerta da OpenAI (in particolare
https://platform.openai.com/docs/api-reference/chat/create), che offre la possibilità di interagire senza problemi con
modelli locali caricati sul programma "LM studio". Lo script, dopo aver interrogato LLM, salva la predizione calcolata e 
aggiunge una riga riassuntiva dell'esempio all'interno di un oggetto pandas.Dataframe, caratterizzato dagli attributi 
["id", "prompt_label", "model", "name_baseline", "gold_truth", "prediction", "acc-top1", "ndcg", "false-positive-rate"]. 
Appena terminate le predizioni e creato il dataframe completo, il programma lo salva in un file csv con nome 
prompt_model_promptID, all'interno di una cartella one_shot/zero_shot. La cartella di destinazione del salvataggio è 
scelta in base al fatto che il modello sia stato interrogando fornendo insieme al prompt, nel json schema, un esempio di
coppia baseline-risposta attesa(tratto da un esempio su refactoring.guru che verrà rifattorizzat con un template method). 
Al fine di permettere al modello di esplorare soluzioni più "creative", il parametro "temperature" è stato impostato a 
0.3, con l'obiettivo di permettere una migliore generalizzazione. Il seed è stato impostato a un valore fisso per 
aumentare le probabilità di ottenere output simili in Epoch differenti. Dopo aver ottenuto la predizione lo script salva 
alcune metriche di accuracy "totali", relative ai risultati ottenuti, in corrispondenza del prompt usato dentro 
promots.json. In caso di interazione di lm studio, viene sfruttata un'interazione via cli (usando Python subprocess): 
sfruttando le permette API rest di Lm studio si riesce ad avviare il server locale e stopparlo invocando l'unload dei 
modelli attivi. Le risposte effettivamente restituite dal modello e le azioni del server, con i log inclusi, è 
monitorabile dalla UI di LM Studio.

## Fase 3: scelta dei modelli
Al fine di obbligare il modello a fornire risposte secondo un preciso formato ho sfruttato l'API "structured outputs",
nativamente supportata da LM-studio (https://lmstudio.ai/docs/developer/openai-compat/structured-output). L'idea è
obbligare il modello a rispondere con un array di elementi scelti tra i 10 possibili design patterns, rispettando un
formato definito con json schema. Ciò semplifica notevolmente la fase di parsing e analisi delle predizioni, in quanto 
la generazione di token è vincolata matematicamente a produrre token validi per lo schema scelto. Purtroppo però il
supporto a "structured outputs" non è garantito da tutti i modelli locali (in particolare quelli con meno di 7B di 
parametri) presenti sul programma LM studio, è possibile comunque verificarne la compatibilità leggendo le varie model
cards. Senza il supporto a tale API, il modello probabilmente ignorerebbe il json schema e la risposta divenderebbe 
imprevedibile: per supportare tale categoria di modelli sarebbe opportuno "appesantire" i prompt anche con delle 
istruzioni di formattazione della risposta in JSON, con il rischio di degradare l'accuracy e aumentare l'incertezza che
il modello rispetti davvero la convenzione proposta.
Al netto di queste considerazioni, la fase di sperimentazione ha coinvolto i seguenti modelli: 
- gpt-oss-20b (KV cache quantization: 8 bits)
- qwen3.5-9b
- gemma-4-e4b


## Fase 4: prompt engineering effettivo e considerazioni
Dalle varie esecuzioni è evidente alcuni modelli (come gpt-oss 20B), con alcuni prompt, non suggeriscano mai alcuni dei 
design pattern applicabili. È il caso del template method: essendo un path meno "popolare", viene spesso "eclissato" da 
strategy, più comune e flessibile al contesto. Ad aggravare ulteriormente il problema è la natura stessa del pattern: 
mentre strategy alterna algoritmi per composizione, template_method è penalizzato in quanto usa l'ereditarietà a tale 
scopo, ritenuta meno pratica.
Il vantaggio principale di aver adottato una strategia automatizzata è quello di poter valutare facilmente ogni 
predizione, oltre alle peformance totali dell'intera epoch. Per "farsi un'idea" di come ha performato LLM sul training 
set, ho definito più metriche di valutazione:
- accuracy@top-1: il primo design pattern suggerito è nella ground truth? Ideale: 1.0
- NDCG (Normalized Discounted Cumulative Gain): i design pattern corretti sono in cima alla predizione? Ideale: 1.0
- false_positive_rate: quanti pattern sbagliati sono stati suggeriti? Ideale: 0.0 (1.0 se il mdoello ha "spammato")

Accuracy@1 svolge il ruolo di capire se il design pattern indicato come "più applicabile" del modello è effettivamente
presente tra quelli considerati corretti. 
NDGC è stata proposta (https://it.wikipedia.org/wiki/Apprendimento_di_ranking) in quanto adibita esattamente 
alla misurazione della qualità del ranking del modello, misurando quindi la similarità tra la lista ground_truth e
la prediction. 
False_positive_rate è una metrica il cui obiettivo è suggerire possibili situazioni dove il modello, sebbene possa aver
azzeccato l'ordine corretto di applicabilità dei pattern producendo score elevati nei casi precedenti, abbia 
semplicemente inserito tutti i 10 design pattern nella lista, suggerendone di cosneguenza molti sbagliati.
Per ciascuna coppia prompt-modello sono state calcolate anche le medie di queste 3 misure di performance, al fine di
avere una stima più generale delle performance.


Riferimento a un corso di HuggingFace: https://huggingface.co/learn/llm-course/chapter1/1

Da creare infine delle descrizioni meccaniche, in inglese, nel campo description di ogni singola classe e dei metodi che 
contiene dei codici refactored aggiunti per espandere il dataset di partenza.

# # WEEKS 8-9 (27-04-2026 - 13-05-2026)

- aggiungere accuracy top 1 effettiva, introdurre ndcg a parametri invertiti, similarità posizionale e media di queste
  ultime 3 (BNPS aka Bidirectional Ndcg & Positional Score)—> 7 metriche in totale.
- introdurre iperparametro della temperatura (valori: 0.0, 0.3, 0.5, 0.7)
- correggere prompt (return lista ordinata deve essere sostituita con descrizione output atteso)
- introdurre varianti di prompt dove scambio l’ordine dei moduli base, role e rules 
- introdurre un prompt dove chiedo un miglioramento a chat gpt 
- eseguire grid search, selezionare iperparametri migliori
- fissati gli iperparametri (shot type incluso), tracciare grafici sulle tre categorie di design patterns considerando 
  le metriche fake accuracy top 1 e BNPS per esibire la performance sulle varie categorie
- (opzionale) considerate di modificare l’esempio dato in input e ripetere passo precedente. Aggiungere descrizioni in 
  inglese ai codici di tutto il dataset 

Sono stati inseriti nuovi prompt riordianando "id 2" con due varianti significative: anticipare la descrizione 
dell'output e invertendo l'assegnamento del task con le regole. "Role" non è stato cambiato di posizione in quanto 
sempre in testa per convenzione, è stato ritenuto che permutare anche esso non avrebbe quindi prodotto alternative
interessanti.

Le metriche utilizzate per valutare le performance in totale sono 7:
[precision@1, BNPS, false_positive_rate, acc_top1, positional_similarity, ndcg_standard, ndcg_inverted].
Le prime due della lista, di cui la seconda ottenuta come una media aritmetica delle ultime 3, sono state prese come
riferimento nella scelta delle migliori configurazioni (a livello di shot type, temperatura e prompt sottomesso) per i
tre modelli. Lo studio è stato condotto eseguendo iterativamente tutte 144 possiibli configurazioni sul training set
(3 modelli * 2 shot_type * 4 temperature * 6 prompt_label) su una macchina Windows, considerando quindi per necessità
architetturali solo le versioni GGUF. Gpt-oss-20b ha richiesto di essere eseguito in versione quantizzata (Q8) per 
causa di limiti hardware.

Al fine di contratstare l'aleatoreità dei risultati, l'esperimento è stato ripetuto in 5 run differenti. È emerso un 
problema con gpt-oss 20b e qwen i quali, a causa di un probabile bug nel motore locale di LM studio, non rispettano 
il vincolo di fornire in output items unici: ne consegue che in alcune predizioni il modello "spamma" più volte lo 
stesso pattern (https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1105).
Ciò degrada probabilmente la qualità dell'intera predizione, il problema dovrebbe essere comunque limitato a pochi csv,
Per risolvere è stato applicato del post processing sui file csv al fine di eliminare i duplicati dalle liste di
predizione, eliminando i duplicati.
È emersa inoltre una seconda caratteristica: su Windows, col seed fissato, l'esperimento è riproducibile in qualsiasi
conigurazione, indipendentemente quindi dalla scelta del modello, della temperatura, dello shot type o del prompt. 
Tale aspetto invece non emerge su macos, che per sua natura non garantisce riproducibilità col seed fissato
(https://adityakarnam.com/mlx-non-determinism-apple-silicon/). 
Per misurare più accuratamente le performance delle varie configurazioni, tutte le run sono state eseguite senza seed 
fissato. 