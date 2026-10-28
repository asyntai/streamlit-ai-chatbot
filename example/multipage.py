"""A multipage Streamlit app with the Asyntai chat button on every page.

Run it with:  streamlit run example/multipage.py
"""
import streamlit as st

from streamlit_ai_chatbot import chatbot


def home():
    st.title("Home")
    st.write("Open the chat, then go to the Pricing page. The chat stays open.")


def pricing():
    st.title("Pricing")
    st.write("This is the second page.")


pg = st.navigation([st.Page(home, title="Home"), st.Page(pricing, title="Pricing")])

# Call it in the main file, before pg.run(), so every page gets the chat.
chatbot("asyntai_ab12cd34")

pg.run()
