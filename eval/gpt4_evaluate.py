import argparse
import json
import os

import openai
import pandas as pd
from tqdm import trange

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORGANIZATION")

prompt = """You are a helpful and precise assistant for checking the quality of the answer.
[The start of Clinical note]
{clinical_note}
[The end of Clinical note]
[The start of Question] 
{question}
[The end of Question]
[The Start of Assistant 1's Answer]
{answer_1}
[The End of Assistant 1's Answer]
[The Start of Assistant 2's Answer]
{answer_2}
[The End of Assistant 2's Answer]
[The Start of Assistant 3's Answer]
{answer_3}
[The End of Assistant 3's Answer]
[The Start of Assistant 4's Answer]
{answer_4}
[The End of Assistant 4's Answer]
We would like to request your feedback on the performance of four AI assistants in response to the user question on the clinical note displayed above.
Please rate the relevance, accuracy of their responses. Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance.
Please first output a single line containing only two values indicating the scores for each assistants respectively. The scores are separated by a space. In the subsequent line, please provide a short explanation of your evaluation, avoiding any potential bias and ensuring that the order in which the responses were presented does not affect your judgment.
"""

def generate_inst_prompt(row):
    return [
        {
            "role": "user",
            "content": prompt.format(
                clinical_note = row["input"],
                question = row["instruction"],
                answer_1 = row["gpt-3.5"],
                answer_2 = row["alpaca"],
                answer_3 = row["clinical-alpaca"],
                answer_4 = row["clinical_alpaca(ft)"]
            ),
        }
    ]

def make_answer_gpt(message):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-4", messages=message, max_tokens=4096, temperature = 0
            )
        except:
            continue
        break

    return response["choices"][0]["message"]["content"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--gpt4_output", type=str, help = "if passed, save only gpt-4 generated file. Json format")

    return parser.parse_args()


def main():
    args = parse_args()
    mtsamples = pd.read_json(args.input)
    save_answers = list()

    for i in trange(len(mtsamples)):
        question_message = generate_inst_prompt(mtsamples.iloc[i])
        answers = make_answer_gpt(question_message)
        

        answers = answers.strip("\"")
        answers = answers.strip("\'")
        splitted_answer = answers.split()

        if splitted_answer[0].isdigit() and splitted_answer[1].isdigit() and splitted_answer[2].isdigit() and splitted_answer[3].isdigit():
            mtsamples.loc[i,"gpt-3.5-score"] = int(splitted_answer[0])
            mtsamples.loc[i,"alpaca-score"] = int(splitted_answer[1])
            mtsamples.loc[i,"clinical-alpaca-score"] = int(splitted_answer[2])
            mtsamples.loc[i,"clinical_alpaca(ft)-score"] = int(splitted_answer[3])
        else:
            mtsamples.loc[i,"gpt-3.5-score"] = 0
            mtsamples.loc[i,"alpaca-score"] = 0
            mtsamples.loc[i,"clinical-alpaca-score"] = 0
            mtsamples.loc[i,"clinical_alpaca(ft)-score"] = 0

        save_answers.append(answers)

    # gpt4_output.json
    if args.gpt4_output:
        with open(args.gpt4_output,"w") as f:
            json.dump(save_answers,f)
    
    mtsamples.to_json(args.output)

if __name__ == "__main__":
    main()