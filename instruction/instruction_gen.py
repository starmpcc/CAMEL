import argparse
import os
import random

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
Using above patient's discharge summary, you want to ask a well-trained model to help your clinical decision making.
Below are high-level NLP categories that you might want to ask about.
Tell me {num_inst_per_note} different instructions that you will ask to the model.

Tasks :
{tasks}

Here are requirements:
1. The words used in the instructions should be diverse to maximize the diversity.
2. The question type should be diverse such as one-word answer question, open-ended question, multiple-choice question, and yes/no question.
3. A GPT language model should be able to complete the instruction. For example, do not ask the model to create other than any textual output.
4. Concat the used NLP categories on front such as Text Classification :
"""


ans_prompt = """\"\"\"
{note}
\"\"\"

You are a healthcare professional.
Using above patient's discharge summary, answer to the following questions.
The question is given with their own categoreis, with colon-concatenated form.

Questions:
{questions}

Here are requirements:
1. Note that each question is independent.
2. For every question, provide the answer in the following format: 'question category: answer'.
3. Number your responses.
4. Ensure that each answer is complete and does not raise another question.
5. Answers can span multiple lines if needed.
"""

tasks = [
    "Coreference Resolution",
    "Question Answering",
    "Natural Language Generation",
    "Text Summarization",
    "Text Classification",
    "Temporal Information Extraction",
    "Relation Extraction",
    "Named Entity Recognition",
    "Paraphrasing",
    "Clinical Concept Normalization",
    "Keyword Extraction",
    "Abbreviation expansion",
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, default="instruction.csv")
    parser.add_argument("--num_inst_per_note", default=12, type=int)
    parser.add_argument("--source", type=str, choices=["mimic3", "mimic4", "i2b2"])

    return parser.parse_args()


def generate_inst_prompt(note, num_inst_per_note):
    selected_tasks = random.sample(tasks, num_inst_per_note)
    return [
        {
            "role": "user",
            "content": inst_prompt.format(
                note=note,
                num_inst_per_note=num_inst_per_note,
                tasks="\n".join(selected_tasks),
            ),
        }
    ]


def generate_ans_prompt(note, questions):
    return [
        {"role": "user", "content": ans_prompt.format(note=note, questions=questions)}
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


def main():
    args = parse_args()
    notes = pd.read_csv(args.input, index_col=0)
    notes = notes[(notes["token_len"] < 1536) & (notes["token_len"] > 1024)]
    notes = notes[notes["category"] == args.source].reset_index(drop=True)
    notes["questions"] = ""
    notes["answers"] = ""
    notes.iloc[:0].to_csv(args.output, index=False)
    for i in trange(len(notes)):
        question_message = generate_inst_prompt(
            notes.loc[i, "text"], args.num_inst_per_note
        )
        questions = make_answer_gpt(question_message)
        notes.loc[i, "questions"] = questions
        answer_message = generate_ans_prompt(notes.loc[i, "text"], questions)
        answers = make_answer_gpt(answer_message)
        notes.loc[i, "answers"] = answers
        notes.iloc[i : i + 1].to_csv(
            args.output,
            mode="a",
            header=False,
            index=False,
        )


if __name__ == "__main__":
    main()
