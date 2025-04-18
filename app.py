from s3 import ingest_to_s3
from io import StringIO
from rds import get_all
import boto3
import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob
from wordcloud import WordCloud

def move_next(): 
    print("WORKS")

st.header("Survey Analytics")

f = st.file_uploader("Upload your survey results in a CSV below", on_change=move_next)

try: 
    st.session_state['df'] = pd.read_csv(f)
except: 
    pass

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# put actual conds later
if f:
    # ingest to s3
    ingest_to_s3(f.name, f, "ds4300-raw-bucket-test")
    # get from rds 
    res = get_all()

    df = st.session_state['df']


    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    df["sentiment"] = df["blurb"].apply(get_sentiment)

    # viz 1: word cloud
    st.subheader("Word Cloud")
    text = " ".join(df["blurb"].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig1, ax1 = plt.subplots()
    ax1.imshow(wordcloud, interpolation="bilinear")
    ax1.axis("off")
    st.pyplot(fig1)
    
    # viz 2: customizable bar chart
    st.subheader("Customizable Bar Chart")

    # dropdown menus
    group_by = st.selectbox("Group by", ["class", "professor_name", "class + professor"])
    metric = st.selectbox("Metric", ["rating", "sentiment"])
    sort = st.selectbox("Sort by", ["Ascending", "Descending", "Alphabetical"])

    # grouping
    if group_by == "class + professor":
        group_cols = ["class", "professor_name"]
        df["class_prof"] = df["class"] + " - " + df["professor_name"]
        group_label = "class_prof"
        grouped = df.groupby(group_cols)[metric].mean().reset_index()
        grouped["label"] = grouped["class"] + " - " + grouped["professor_name"]
    else:
        group_label = group_by
        grouped = df.groupby(group_label)[metric].mean().reset_index()
        grouped["label"] = grouped[group_label]

    if sort == "Alphabetical":
        grouped = grouped.sort_values(by="label", ascending=False)
    elif sort == "Ascending":
        grouped = grouped.sort_values(by=metric)
    else:
        grouped = grouped.sort_values(by=metric, ascending=False)

    fig, ax = plt.subplots(figsize=(10, max(4, len(grouped) * 0.4)))
    bars = ax.barh(grouped["label"], grouped[metric])

    for bar in bars:
        width = bar.get_width()
        padding = (grouped[metric].max() - grouped[metric].min()) * 0.02
        height = bar.get_y() + bar.get_height() / 2

        # positive values: value printed to the right of the bar
        if width >= 0:
            ax.text(width + padding, height, f"{width:.2f}", va="center", ha="left")
        # negative values: value printed to the left of the bar
        else:
            ax.text(width - padding, height, f"{width:.2f}", va="center", ha="right")

    ax.set_title(f"Average {metric.capitalize()} by {group_by.replace('_', ' ').title()}")
    ax.set_xlabel(metric.capitalize())
    ax.set_ylabel(group_by.replace("_", " ").title())

    # ratings 0-5
    if metric == "rating":
        ax.set_xlim(0, grouped[metric].max() + 0.5)

    # sentiment can have positive/negative
    else:
        min_val = min(0, grouped[metric].min())
        max_val = grouped[metric].max()
        ax.set_xlim(min_val - 0.1, max_val + 0.1)

    st.pyplot(fig)