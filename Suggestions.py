#suggestions.py
import streamlit as st

SUGGESTIONS_FILE = 'suggestions.txt'

def save_suggestion(name, suggestion):
    with open(SUGGESTIONS_FILE, 'a') as f:
        f.write(f"Name: {name}\nSuggestion: {suggestion}\n\n")

def suggestions():
    st.title("Suggestions for Improvements or Enhancements")
    
    st.write("Please use the form below to submit your suggestions or feedback on the app")
    
    #form for suggestions
    with st.form(key='suggestion_form'):
        name = st.text_input("Your Name (Optional)")
        suggestion = st.text_area("Your Suggestion or Feedback", height=150)
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            if suggestion:
                st.success("Thank you for your suggestion! We appreciate your feedback.")
            else:
                st.error("Please enter a suggestion before submitting.")

suggestions()
