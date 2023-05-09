# Reference: Alpaca & Vicuna

import argparse
import io
import json

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

PROMPT_INPUT = (
    "Below is an instruction that describes a task, paired with an input that provides further context. "
    "Write a response that appropriately completes the request.\n\n"
    "### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:"
)
PROMPT_NO_INPUT = (
    "Below is an instruction that describes a task. "
    "Write a response that appropriately completes the request.\n\n"
    "### Instruction:\n{instruction}\n\n### Response:"
)
DEFAULT_PAD_TOKEN = "[PAD]"
DEFAULT_EOS_TOKEN = "</s>"
DEFAULT_BOS_TOKEN = "</s>"
DEFAULT_UNK_TOKEN = "</s>"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--output_path", type=str, default="result.jsonl")
    return parser.parse_args()


def jload(f, mode="r"):
    """Load a .json file into a dictionary."""
    if not isinstance(f, io.IOBase):
        f = open(f, mode=mode)
    jdict = json.load(f)
    f.close()
    return jdict


def main():
    args = parse_args()
    tokenizer = AutoTokenizer.from_pretrained(
        "decapoda-research/llama-7b-hf", revision="pr/7"
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name, torch_dtype=torch.bfloat16
    ).to("cuda")
    model.resize_token_embeddings(len(tokenizer))
    data = jload(args.data_path)

    tokenizer.add_special_tokens(
        {
            "pad_token": DEFAULT_PAD_TOKEN,
            "eos_token": DEFAULT_EOS_TOKEN,
            "bos_token": DEFAULT_BOS_TOKEN,
            "unk_token": DEFAULT_UNK_TOKEN,
        }
    )
    answers = []
    for sample in tqdm(data):
        for k, v in sample.items():
            sample[k] = v.strip("\n")
        text = (
            PROMPT_INPUT.format_map(sample)
            if sample.get("input", "") != ""
            else PROMPT_NO_INPUT.format_map(sample)
        )
        tokens = tokenizer.encode(text, return_tensors="pt").to("cuda")
        output = model.generate(
            tokens,
            max_length=args.max_length,
            num_beams=5,
            do_sample=True,
            temperature=1,
        )
        result = tokenizer.decode(output[0], skip_special_tokens=True)
        try:
            answer = result[
                len(text) : result.index("DEFAULT_EOS_TOKEN", len(text))
            ].strip()
        except:
            answer = result[len(text) :].strip()
        answers.append({"generated": answer})
    with open(args.output_path, "w") as f:
        json.dump(answers, f)


if __name__ == "__main__":
    main()
