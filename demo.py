import streamlit as st
import json
import pandas as pd

mtsamples = pd.read_json("mtsamples.json")

st.title("CAMEL : Clinically Adapted Model Enhanced from LLaMA demo")
st.write(
    "In order to prevent privacy leakage of the data we trained on, we fix the clinical notes and instructions that you can test. If you want to try with your own clinical notes and instructions, you need to download the model from PhysioNet. The notes were derived from MTSamples discharge summary that was used for our evaluation. Please choose each of the notes and instructions!"
)

st.markdown("""---""")

note_number = st.slider("Select the clinical note. There are total 105.", 1, 105, 1)


masked = mtsamples[mtsamples["note_number"] == note_number]

st.info(masked.input.values[0])


instruction = st.selectbox("Select your instruction", masked["instruction"].values)

masked_twice = masked[masked["instruction"] == instruction]

gpt_score = masked_twice["gpt-3.5-score"].values[0]
alpaca_score = masked_twice["alpaca-score"].values[0]
camel_score = masked_twice["clinical_alpaca(ft)-score"].values[0]

gpt = masked_twice["gpt-3.5"].values[0]
alpaca = masked_twice["alpaca"].values[0]
camel = masked_twice["clinical_alpaca(ft)"].values[0]

st.write("\n")
st.markdown("""---""")
st.write("\n")

st.write("**GPT-3.5**", f"({gpt_score}/10)")
st.success(gpt)

st.write("**CAMEL**", f"({camel_score}/10)")
st.warning(camel)

st.write("**Alpaca**", f"({alpaca_score}/10)")
st.error(alpaca)
