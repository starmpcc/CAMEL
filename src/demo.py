# Reference: Alpaca & Vicuna

import argparse
import re

import torch
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--prompting", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    tokenizer = AutoTokenizer.from_pretrained(
        "decapoda-research/llama-7b-hf", revision="pr/7"
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name, torch_dtype=torch.bfloat16
    ).to("cuda")

    tokenizer.add_special_tokens({"pad_token": "[ANON]"})
    model.resize_token_embeddings(len(tokenizer))
    while True:
        if args.prompting:
            example = {
                "instruction": input("Enter instruction: "),
                "input": input("Enter input: "),
            }
            text = (
                PROMPT_INPUT.format_map(example)
                if example.get("input", "") != ""
                else PROMPT_NO_INPUT.format_map(example)
            )
        else:
            text = input("Enter text: ")
        text = re.sub(r"___", "[ANON]", text)
        tokens = tokenizer.encode(text, return_tensors="pt").to("cuda")
        output = model.generate(
            tokens, max_length=2048, do_sample=True, temperature=1, num_beams=5
        )
        result = tokenizer.decode(output[0], skip_special_tokens=True)
        try:
            answer = result[len(text) : result.index("###", len(text))].strip()
        except:
            answer = result[len(text) :].strip()
        print(answer)


if __name__ == "__main__":
    main()
