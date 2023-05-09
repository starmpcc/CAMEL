import argparse

import pandas as pd
from convert_deid_tag import replace_list_of_notes
from transformers import AutoTokenizer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mimic3_path", type=str, required=True)
    parser.add_argument("--mimic4_path", type=str, required=True)
    parser.add_argument("--i2b2_path", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    return parser.parse_args()


def merge(args):
    mimic3 = pd.read_csv(args.mimic3_path)
    mimic4 = pd.read_csv(args.mimic4_path)
    i2b2 = pd.read_json(args.i2b2_path)

    tokenizer = AutoTokenizer.from_pretrained(
        "decapoda-research/llama-7b-hf", revision="pr/7"
    )

    raw_notes = pd.DataFrame(columns=["category", "text", "token_len"])

    for text in mimic3[mimic3["CATEGORY"] == "Discharge summary"]["TEXT"]:
        text = replace_list_of_notes([text])[0]
        token_len = len(tokenizer(text)["input_ids"])
        raw_notes.loc[len(raw_notes)] = ["mimic3", text, token_len]

    for text in mimic4["text"]:
        token_len = len(tokenizer(text)["input_ids"])
        raw_notes.loc[len(raw_notes)] = ["mimic4", text, token_len]

    for data in i2b2["data"]:
        for index in len(data["paragraphs"]):
            text = "".join(data["paragraphs"][index]["context"])
            token_len = len(tokenizer(text)["input_ids"])
            raw_notes.loc[len(raw_notes)] = ["i2b2", text, token_len]

    raw_notes.to_csv(args.output)


def main():
    args = parse_args()

    merge(args)


if __name__ == "__main__":
    main()
