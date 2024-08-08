import streamlit as st
import Task
import Suggestions
import EmailVisualiser 

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

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Email Visualizer", "Task", "Suggestions"])

if selection == "Home":
    st.markdown("""
         ### Click on the sidebar to navigate to the different pages each with their own insights on the Enron Email Dataset
         """)
elif selection == "Email Visualizer":
    EmailVisualiser.email_visualiser()
elif selection == "Task":
    Task.task()  
elif selection == "Suggestions":
    Suggestions.suggestions() 
