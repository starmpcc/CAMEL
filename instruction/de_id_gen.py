import argparse
import os

import openai
import pandas as pd
from tqdm import trange

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = os.environ.get("OPENAI_API_BASE")
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

deployment_name = os.environ.get("OPENAI_DEPLOYMENT_NAME")


inst_prompt = """\"\"\"
{note}
\"\"\"

You are a healthcare professional.
Using above patient's discharge summary, you want to ask a well-trained model to help your clinical services.
Tell me 2 different instructions about deidentification that you will ask to the model.

Here are requirements:
1. The words used in the instructions should be diverse to maximize the diversity.
2. A GPT language model should be able to complete the instruction. For example, do not ask the model to create other than any textual output
3. The instructions should not contain questions asking any suggestion or recommendation.
"""


ans_prompt = """\"\"\"
{note}
\"\"\"

Given above discharge summary, answer to below instruction.

{question}

"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, default="instruction.csv")
    parser.add_argument("--mode", type=str, choices=["inst", "ans"])
    return parser.parse_args()


def generate_inst_prompt(note):
    return [
        {
            "role": "user",
            "content": inst_prompt.format(note=note),
        }
    ]


def generate_ans_prompt(note, question):
    return [
        {"role": "user", "content": ans_prompt.format(note=note, question=question)}
    ]


def make_answer_gpt(message):
    while True:
        try:
            response = openai.ChatCompletion.create(
                engine=deployment_name, messages=message, max_tokens=4096
            )
        except:
            continue
        break
    return response["choices"][0]["message"]["content"]


def inst_gen(args):
    df = pd.read_csv(args.input, index_col=0)
    df = df[(df["token_len"] < 1024) & (df["category"] == "i2b2")].reset_index(
        drop=True
    )
    df["questions"] = ""
    df["answers"] = ""
    df.iloc[:0].to_csv(args.output, index=False)

    for i in trange(len(df)):
        question_message = generate_inst_prompt(df.loc[i, "text"])
        questions = make_answer_gpt(question_message)
        df.loc[i, "questions"] = questions
        df.iloc[i : i + 1].to_csv(
            args.output,
            mode="a",
            header=False,
            index=False,
        )


def ans_gen(args):
    df = pd.read_csv(args.input)
    df.iloc[:0].to_csv(args.output, index=False)
    # Assume the file is pre-processed. i.e. split by questions.
    for i in trange(len(df)):
        question_message = generate_ans_prompt(
            df.loc[i, "text"],
            df.loc[i, "questions"],
        )
        answers = make_answer_gpt(question_message)
        df.loc[i, "answers"] = answers
        df.iloc[i : i + 1].to_csv(
            args.output,
            mode="a",
            header=False,
            index=False,
        )


def main():
    args = parse_args()

    if args.mode == "inst":
        inst_gen(args)
    elif args.mode == "ans":
        ans_gen(args)


if __name__ == "__main__":
    main()
