import streamlit as st
import pandas as pd
import spacy
import spacy_streamlit

# Set page configuration
st.set_page_config(page_title="Entities Visualiser", page_icon="📧", layout="centered", initial_sidebar_state="expanded")

st.markdown(
  """
    <style>
      background-color: #f0f2f6;
    </style>
  """,
    unsafe_allow_html=True
)

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Preprocessing function to extract header info and body
def extract_entities(text):
    entities = {"CARDINAL": [], "DATE": [], "EVENT": [], "FAC": [], "GPE": [], "LANGUAGE": [], "LAW": [], "LOC": [], "MONEY": [], "NORP": [], "ORDINAL": [], "ORG": [], "PERCENT": [], "PERSON": [], "PRODUCT": [], "QUANTITY": [], "TIME": [], "WORK_OF_ART": []}
    doc = nlp(text)
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
    return entities

def parse_email(message):
    headers, body = message.split('\n\n', 1)
    headers = dict([line.split(': ', 1) for line in headers.split('\n') if ': ' in line])
    return headers, body

# Load the dataset
emails = pd.read_csv('./emails_sample.csv')
emails['parsed'] = emails['message'].apply(parse_email)
emails['headers'] = emails['parsed'].apply(lambda x: x[0])
emails['body'] = emails['parsed'].apply(lambda x: x[1])
emails['entities'] = emails['body'].apply(extract_entities)

def email_visualiser():
  st.title('Email Visualiser')
  st.write("### This page allows you to visualize the Named Entities in the Enron Email Dataset for an email of your choice")
  email_indices = ["Select an email"] + list(emails.index)
  email_selection = st.selectbox("Select an email", email_indices)

  if email_selection != "Select an email":
    selected_email = emails.loc[email_selection]
    doc = nlp(selected_email['body'])
    with st.expander("See Header Information"):
      st.subheader("Email Header Information")
      st.markdown(f"**From**: {selected_email['headers'].get('From', 'N/A')}")
      st.markdown(f"**To**: {selected_email['headers'].get('To', 'N/A')}")
      st.markdown(f"**Subject**: {selected_email['headers'].get('Subject', 'N/A')}")
      st.markdown(f"**Date**: {selected_email['headers'].get('Date', 'N/A')}")
      st.markdown(f"**Cc**: {selected_email['headers'].get('Cc', 'N/A')}")
      st.markdown(f"**Bcc**: {selected_email['headers'].get('Bcc', 'N/A')}")

    ner = st.checkbox("Show NER Visualiser")
    if ner:
      spacy_streamlit.visualize_ner(doc, labels=nlp.get_pipe('ner').labels)

# Call the email_visualiser function
email_visualiser()
