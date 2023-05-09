import argparse

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--discharge_note_path", type=str, required=True)
    parser.add_argument("--radiology_note_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    discharge_notes = pd.read_csv(args.discharge_note_path, usecols=["text"])
    radiology_notes = pd.read_csv(args.radiology_note_path, usecols=["text"])

    discharge_notes["text"] = discharge_notes["text"].map(
        lambda x: "Discharge summary\n" + x
    )
    radiology_notes["text"] = radiology_notes["text"].map(lambda x: "Radiology\n" + x)

    preprocessed_notes = pd.concat([discharge_notes, radiology_notes])
    preprocessed_notes.to_csv(args.output_path, index=False)


if __name__ == "__main__":
    main()
