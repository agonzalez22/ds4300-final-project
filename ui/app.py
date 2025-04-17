import streamlit as st
import pandas as pd

st.header("Survey Analytics")

f = st.file_uploader("Upload your survey results in a CSV below")

if f: 
    df = pd.read_csv(f)
    print(df)