import argparse

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mimiciii_note_path", type=str, required=True)
    parser.add_argument(
        "--filter_index_path", type=str, default="mimiciii_filter_index.txt"
    )
    parser.add_argument("--output_path", type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    notes = pd.read_csv(args.note_path)

    with open(args.erase_index_path, "r") as f:
        erase_index = f.readlines()
    erase_index = [int(i) for i in erase_index]

    preprocessed_notes = notes[~notes["ROW_ID"].isin(erase_index)]

    # add category in front of each clinical notes
    preprocessed_notes["TEXT"] = preprocessed_notes.apply(
        lambda row: row["CATEGORY"] + "\n" + row["TEXT"], axis=1
    )

    preprocessed_notes.to_csv(args.output_path, index=False)


if __name__ == "__main__":
    main()
