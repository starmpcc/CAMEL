# Adapted From: https://raw.githubusercontent.com/zphang/minimal-llama/main/tokenize_dataset.py

import argparse
import re

import datasets
import numpy as np
import pandas as pd
import tqdm.auto as tqdm
from pandarallel import pandarallel
from transformers import AutoTokenizer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument(
        "--model_name", type=str, default="decapoda-research/llama-7b-hf"
    )
    parser.add_argument("--save_path", type=str, required=True)
    return parser.parse_args()


def main():
    pandarallel.initialize(nb_workers=32, progress_bar=True)
    args = parse_args()
    revision = "pr/7" if "decapoda-research/llama" in args.model_name else "main"
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, revision=revision)
    # No unused tokens in llama tokenizers, so just use pad_token (unused) as anon
    tokenizer.add_special_tokens({"pad_token": "[ANON]"})
    all_tokenized = []
    df = pd.read_csv(args.data_path)
    text_name = "TEXT" if "TEXT" in df.columns else "text"
    all_tokenized = (
        df[text_name]
        .sample(frac=1)
        .parallel_map(lambda x: tokenizer.encode(re.sub(r"___", "[ANON]", x)))
    )
    print(f"Total number of tokens if {all_tokenized.str.len().sum()}")
    all_tokens = [1] + [
        tok
        for row in all_tokenized
        for tok in row + [tokenizer.eos_token_id, tokenizer.bos_token_id]
    ]

    truncated_tokens = all_tokens[: (len(all_tokens) // 2048) * 2048]
    arr = np.array(truncated_tokens).reshape(-1, 2048)
    ds = datasets.Dataset.from_dict({"input_ids": arr})
    ds.save_to_disk(args.save_path)
    print(f"Generated {arr.shape[0]} samples.")


if __name__ == "__main__":
    main()
