from s3 import ingest_to_s3
from io import StringIO
import boto3
import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob
from wordcloud import WordCloud

def move_next(): 
    print(st.session_state)
    print("PEEEEEE")

st.header("Survey Analytics")

f = st.file_uploader("Upload your survey results in a CSV below", on_change=move_next)

# if f: # only if f is real :3
    # ingest_to_s3(f.name, f, "ds4300-edited-slicedbread")

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# put actual conds later
if f:
    # upload to s3
    # read back from s3
    # check if csv file has the right columns?

    df = pd.read_csv(f)

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

    # viz 2: sentiment by class (bar chart)
    st.subheader("Average Sentiment by Class")
    avg_sent = df.groupby("class")["sentiment"].mean().reset_index()

    fig2, ax2 = plt.subplots()
    ax2.bar(avg_sent["class"], avg_sent["sentiment"])
    ax2.set_title("Average Sentiment by Class")
    ax2.set_ylabel("Sentiment")
    ax2.set_xlabel("Class")
    plt.xticks()
    st.pyplot(fig2)

    # viz 3: prof ratings (horiz bar chart)
    st.subheader("Professor Average Ratings")
    avg_rating = df.groupby("professor_name")["rating"].mean().reset_index()
    avg_rating = avg_rating.sort_values(by="rating")

    fig3, ax3 = plt.subplots()
    bars = ax3.barh(avg_rating["professor_name"], avg_rating["rating"])

    for bar in bars:
        width = bar.get_width()
        ax3.text(width + 0.05, bar.get_y() + bar.get_height()/2, f"{width:.2f}", va="center")

    ax3.set_title("Average Rating by Professor")
    ax3.set_xlabel("Rating")
    ax3.set_ylabel("Professor")
    ax3.set_xlim(0, df["rating"].max() + 0.5)
    st.pyplot(fig3)