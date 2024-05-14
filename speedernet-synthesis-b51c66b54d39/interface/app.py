import streamlit as st
from main import show_main_page
from summary import show_summary_page

page = st.sidebar.selectbox("Transcribe or Summary",("Transcribe","Summary"))


if page == "Transcribe":
    show_main_page()
else:
    show_summary_page()




