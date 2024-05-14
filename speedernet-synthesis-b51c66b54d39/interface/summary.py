import streamlit as st  
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import assemblyai as aai
import pandas as pd
from io import StringIO
import pyperclip
import os 

def show_summary_page():
  st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

  st.markdown("<h1 class='title'>Summary</h1>", unsafe_allow_html=True)
    
    
  def generate_response(txt):
       llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
       text_splitter = CharacterTextSplitter()
       texts = text_splitter.split_text(txt)
       docs = [Document(page_content=t) for t in texts]
       chain = load_summarize_chain(llm, chain_type='map_reduce')
       return chain.run(docs)
  
  
      
  txt_input = st.text_area('Enter your text', '', height=200)
      
      
  result = []
  with st.form('summarize_form', clear_on_submit=True):
      openai_api_key = st.text_input('OpenAI API Key', type = 'password', disabled=not txt_input)
      submitted = st.form_submit_button('Submit')
      if submitted and openai_api_key.startswith('sk-'):
          with st.spinner('Calculating...'):
              response = generate_response(txt_input)
              result.append(response)
              del openai_api_key
  if len(result):
      st.info(response)