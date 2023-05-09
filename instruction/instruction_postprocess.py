import argparse

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, default="instruction_processed.csv")
    return parser.parse_args()


def postprocess(args):
    notes = pd.read_csv(args.input)

    df = pd.DataFrame(columns=["category", "text", "type", "question", "answer"])

    for row in notes.iterrows():
        category = row[1]["category"]
        text = row[1]["text"]
        questions = row[1]["questions"]
        answers = row[1]["answers"]

        for i in range(1, 13):
            if i >= 10 and i < 12:
                question = questions[
                    questions.find(str(i) + ". ")
                    + 4 : questions.find(str(i + 1) + ". ")
                ]
                answer = answers[
                    answers.find(str(i) + ". ") + 4 : answers.find(str(i + 1) + ". ")
                ]
            elif i == 12:
                question = questions[questions.find(str(i) + ". ") + 4 :]
                answer = answers[answers.find(str(i) + ". ") + 4 :]
            else:
                question = questions[
                    questions.find(str(i) + ". ")
                    + 3 : questions.find(str(i + 1) + ". ")
                ]
                answer = answers[
                    answers.find(str(i) + ". ") + 3 : answers.find(str(i + 1) + ". ")
                ]

            question = question.strip()
            answer = answer.strip()

            questions = questions[questions.find(question) + len(question) :]
            answers = answers[answers.find(answer) + len(answer) :]

            tag_question = question[: question.find(":")].strip()
            question = question[question.find(":") + 1 :].strip()

            tag_answer = answer[: answer.find(":")].strip()
            answer = answer[answer.find(":") + 1 :].strip()

            try:
                if (
                    question[0].isupper()
                    and answer[0].isupper()
                    and tag_question == tag_answer
                ):
                    df.loc[len(df)] = [category, text, tag_question, question, answer]
            except:
                continue

    df.to_csv(args.output)


def main():
    args = parse_args()

    postprocess(args)


if __name__ == "__main__":
    main()
