"""A small Streamlit app with the Asyntai chat button.

Run it with:  streamlit run example/app.py
"""
import streamlit as st

from streamlit_ai_chatbot import chatbot

st.set_page_config(page_title="Asyntai chat example")

# Put your own ID here, or set ASYNTAI_WIDGET_ID in .streamlit/secrets.toml.
chatbot("asyntai_ab12cd34")

st.title("Asyntai chat example")
st.write("The chat button is in the bottom corner of the page.")

name = st.text_input("Your name")
if st.button("Say hello"):
    st.write(f"Hello, {name or 'visitor'}!")
