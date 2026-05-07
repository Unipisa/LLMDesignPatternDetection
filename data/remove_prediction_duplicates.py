import os
import sys
import pandas as pd
import ast

"""
Rimuove items duplicati all'interno delle predizioni memorizzate nei csv (se presenti)
"""


if __name__ == "__main__":
    dir_to_process = "results/original"
    if not os.path.exists(dir_to_process):
        print("Directory doesn't exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(dir_to_process):
        print("This is not a directory", dir_to_process, file=sys.stderr)
        sys.exit(1)
    for run in os.listdir(dir_to_process):
        if not os.path.isdir(os.path.join(dir_to_process, run)):
            print("Directory doesn't exist", os.path.join(dir_to_process, run), file=sys.stderr)
            continue
        for result_file in os.listdir(os.path.join(dir_to_process, run)):
            if not result_file.endswith(".csv"):
                print("This is not a csv file", os.path.join(dir_to_process, run, result_file), file=sys.stderr)
                continue
            df = pd.read_csv(os.path.join(dir_to_process, run, result_file))
            temp = df["prediction"].apply(lambda prediction: list(dict.fromkeys(ast.literal_eval(prediction))))
            if not df["prediction"].equals(temp.apply(str)):
                print("Duplicates in", os.path.join(dir_to_process, run, result_file), file=sys.stderr)
            df["prediction"] = temp
            df.to_csv(os.path.join(dir_to_process, run, result_file), index=False)