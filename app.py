import streamlit as st
import pandas as pd 

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
  """
    <style>
      body {  
        background-color: #f0f2f6;
      }
    </style>
  """,
    unsafe_allow_html=True
)


st.markdown("""
         # How to navigate the app:
         ### Click on the sidebar to navigate to the different pages each with their own insights on the Enron Email Dataset""")

