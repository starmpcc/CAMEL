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
        text = row[1]["text"]
        questions = row[1]["questions"]

        if "Instruction1: " in questions:
            ins1 = questions[
                questions.find("Instruction1: ")
                + len("Instruction1: ") : questions.find("Instruction2: ")
            ].strip()
            ins2 = questions[
                questions.find("Instruction2: ") + len("Instruction2: ") :
            ].strip()
        elif "Instruction1 : " in questions:
            ins1 = questions[
                questions.find("Instruction1 : ")
                + len("Instruction1 : ") : questions.find("Instruction2 : ")
            ].strip()
            ins2 = questions[
                questions.find("Instruction2 : ") + len("Instruction2 : ") :
            ].strip()
        elif "Instruction 1: " in questions:
            ins1 = questions[
                questions.find("Instruction 1: ")
                + len("Instruction 1: ") : questions.find("Instruction 2: ")
            ].strip()
            ins2 = questions[
                questions.find("Instruction 2: ") + len("Instruction 2: ") :
            ].strip()
        elif "Instruction 1 : " in questions:
            ins1 = questions[
                questions.find("Instruction 1 : ")
                + len("Instruction 1 : ") : questions.find("Instruction 2 : ")
            ].strip()
            ins2 = questions[
                questions.find("Instruction 2 : ") + len("Instruction 2 : ") :
            ].strip()

        ins1 = ins1.strip("'")
        ins2 = ins2.strip("'")
        ins1 = ins1.strip('"')
        ins2 = ins2.strip('"')

        df.loc[len(df)] = ["i2b2", text, "Deidentification", ins1, ""]
        df.loc[len(df)] = ["i2b2", text, "Deidentification", ins2, ""]

    df.to_csv(args.output)


def main():
    args = parse_args()

    postprocess(args)


if __name__ == "__main__":
    main()
