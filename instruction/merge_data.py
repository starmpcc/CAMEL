import argparse
import os

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    # Assume there are postprocessed instruction files in data path
    data = [pd.read_csv(args.data_path + i) for i in os.listdir(args.data_path)]
    data = [i[["text", "question", "answer"]] for i in data]
    merged = pd.concat(data)
    merged.rename(
        columns={"question": "instruction", "answer": "output", "text": "input"},
        inplace=True,
    )
    merged.sample(frac=1, random_state=42).to_json(
        args.output, orient="records", indent=4
    )
