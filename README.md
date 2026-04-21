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

Dato che il pattern Proxy potrebbe creare problemi, specie se il proxy inserito “altera” il funzionamento (presente 
anche nella baseline, ma forse difficilmente riconoscibile). Come conseguenza di ciò è stato aggiunto un esempio di 
proxy logger, che fa solo task secondari.

Necessario anche tener conto della sperimentazione del lavoro, in particolare del fatto che per un dato codice sorgente 
potrebbero esserci più pattern “corretti” che potrebbero essere applicati (ad esempio, “strategy” al posto di “command”,
“abstract factory” invece di “factory method”, “proxy” sempre applicabile, ecc.).
- Annotato il dataset con tutti i pattern applicabili a un dato esempio (oltre a quello già previsto; senza 
  necessariamente andare a crearne la versione rifattorizzata); essere “aperti” a “active learning”, aka. successive 
  integrazioni valutando risposte dei modelli.
- Aggiunto supporto a una sperimentazione che misuri “accuracy” come “mi suggerisce uno dei pattern applicabili”, oltre 
  a prevedere la possibilità di “privilegiare” (lista in ordine di priorità, accuracy@top-k) i pattern che sarebbe 
  meglio applicare.

## Fase 1: partizionare il dataset in training set e test set 
Creati due nuovi file JSON, training_set.json e test_set.json, rispettivamente contenenti i dati di training e di 
test. Le partizioni sono state strutturate selezionando un esempio per pattern da inserire nel test set, lasciando al
training set i restanti esempi.

- Training set: [0,2,3,5,6,8,9,10,13,14,15,17,18,19,22,23,24,25,27,28,29]
- Test set: [1,4,7,11,12,16,20,21,26,30]

Gli esempi scelti sono tra i baseline più “challenging” e meno banali per il pattern di riferimento (responsabilità 
mescolate, alternative plausibili nella lista di priorità dei pattern applicabli). L'obiettivo non è penalizzare in fase 
di valutazione o semplificare il training del modello (che ha già a disposizione pattern interessanti), ma avere la  
sicurezza nella fase di test di sottoporlo a situazioni più "realistiche" evitando query composte da esempi "didattici"
o "troppo semplici".

## Fase 2: creazione del system prompt per l'LLM
Richiedere un insieme di predizioni su un dataset talmente strutturato, con 31 codici baseline, rende meno invitante
gestire "manualmente" il prompting ai modelli e il salvataggio dei risultati. Per questo motivo ho creato una procedura
automatizzata, nello script prompts_engineering.py, che, leggendo da un file json dove sono memorizzati le 
configurazioni prompt-modello ("prompts.json"), itera richiedendo predizioni sull'intero training set. Per implementarlo
ho consultato alcune sezioni della libreria offerta da OpenAI (in particolare
https://platform.openai.com/docs/api-reference/chat/create), che offre la possiiblità di interagire senza problemi con
modelli locali caricati sul programma "LM studio". Lo script, dopo aver interrogato il modello, salva la predizione 
calcolata e aggiunge una riga riassuntiva dell'esempio all'interno di un oggetto pandas.Dataframe, caratterizzato dagli 
attributi (id, name baseline, prompt, gold_truth, prediction, model, accuracy@top-1). 
Appena terminate le predizioni e creato il dataframe completo, il programma salva il dataframe in un file csv, il cui 
path è tracciato rigorosamente nel file "prompts.json".
CHIARISCI SEED E TEMPERATURA

## Fase 3: prompt engineering effettivo e considerazioni
Dalle varie esecuzioni è evidente come il modello, con alcuni prompt, non suggerisca mai alcuni dei 10 design pattern 
applicabili. È il caso del template method: essendo un path meno "popolare", viene spesso surclassato da strategy, più
flessibile al contesto e comune. Ad aggravare ulteriormente il problema è la natura stessa del pattern: mentre strategy
alterna algoritmi per composizione, template_method è penalizzato in quanto usa l'ereditarietà a tale scopo, ritenuta
meno flessibile.


Prossimi passi: Prompt engineering della richiesta da fare agli LLM, partendo da linee guida di OpenAI e 1-2 LLM 
(versione chat) di riferimento. 


Suggerimenti seguiti:
- tenere traccia di ogni prompt valutato;
- considerare alternative tramite ablation;
- valutare prompt “migliori” in termini di accuracy e accuracy@top-1 (su una porzione del dataset da usare come training
  set; il resto del dataset sarà usato come test set in fase di validazione).

Riferimento a un corso di HuggingFace: https://huggingface.co/learn/llm-course/chapter1/1

Creare infine:
delle descrizioni meccaniche, in inglese, nel campo description di ogni singola classe e dei metodi che contiene dei 
codici refactored aggiunti per espandere il dataset di partenza.
Creta infine una tabella con tutti i prompt fatti e i risultati ottenuti. Seguito foglio di carta come riferimento

Durante la fase di prompt engeneering evitare assolutamente di usare tutti i codici, tenere sempre un codice per pattern
per la fase di test finale. (?????)