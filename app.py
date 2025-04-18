import streamlit as st
import pandas as pd
from s3 import ingest_to_s3
from io import StringIO
from rds import give_status


def move_next(): 
    print(st.session_state)
    print('PEEEEEE')

st.header("Survey Analytics")

f = st.file_uploader("Upload your survey results in a CSV below", on_change=move_next)

if f: # only if f is real :3
    ingest_to_s3(f.name, f, "ds4300-raw-bucket-test")
    give_status()
    # ingest_to_s3(f.name, f)
    


