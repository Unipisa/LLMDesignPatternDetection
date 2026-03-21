import os, json


root = "pattern_examples"
examples = []
count=0

for category in os.listdir(root):
    if not os.path.isdir(os.path.join(root, category)):
        continue
    for pattern in os.listdir(os.path.join(root, category)):
        if not os.path.isdir(os.path.join(root, category, pattern)):
            continue
        p = os.path.join(root, category, pattern)
        for file in os.listdir(os.path.join(p, "refactored")):
            if file.endswith(".py"):
                examples.append({
                    "id": count,
                    "category": category,
                    "pattern": pattern,
                    "path_refactored": f"{p}/refactored/{file}",
                    "path_baseline": f"{p}/baseline/{file}",
                    "description": ""
                })
                count+=1

with open("dataset.json", "w") as f:
    json.dump(examples, f, indent=4)