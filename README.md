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
