from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import assemblyai as aai
import streamlit as st
import pandas as pd
from io import StringIO
import pyperclip
import os

def show_main_page():
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
    
    
    st.markdown("<h1 class='title'>Transcription Tool</h1>", unsafe_allow_html=True)

    st.write("""#### MP3 File Uploader""")
    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])
   

    def transcribe_mp3(file_path):
        aai.settings.api_key = "b002aa5439e74d0db7edb11dceee5250"
        config = aai.TranscriptionConfig(language_code="fr")  # Adjust language code as needed
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(file_path)
        return transcript
        
    def transcribe_speaker_mp3(file_path):
        aai.settings.api_key = "b002aa5439e74d0db7edb11dceee5250"
        config = aai.TranscriptionConfig(speaker_labels=True,language_code="fr") 
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(file_path)
        return transcript        
    
    def auto_chapters(file_path):
        aai.settings.api_key = "b002aa5439e74d0db7edb11dceee5250"
        config = aai.TranscriptionConfig(auto_chapters=True)
        transcript = aai.Transcriber().transcribe(file_path, config)
        return transcript
    
    def convertMillis(millis):
        seconds=int(millis/1000)%60
        minutes=int(millis/(1000*60))%60
        hours=int(millis/(1000*60*60))%24
        return seconds, minutes, hours
    
    if uploaded_file is not None:
        mp3_content = uploaded_file.read()
        st.audio(mp3_content,format='audio/mp3')

        save_path = "../uploads"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = os.path.join(save_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(mp3_content)
            
        transcribe_button = st.button("Transcribe")   
        speaker_button = st.button("Speaker Diarization") #speaker button
        chapter_button = st.button("Auto chapters")
        if transcribe_button:
            with st.spinner("Transcribing..."):
                transcript = transcribe_mp3(file_path)
                text_summarize = transcript.text
                paragraphs = transcript.get_paragraphs()
                
            if transcript:
                st.session_state['transcript_paragraphs'] = []
                for paragraph in paragraphs:
                    st.session_state['transcript_paragraphs'].append(paragraph.text)
        
        if speaker_button:
            with st.spinner("Performing Speaker Diarization..."):
                transcript = transcribe_speaker_mp3(file_path)  # Re-transcribe with speaker diarization
                for utterance in transcript.utterances:
                    con_sec, con_min, con_hour = convertMillis(int(utterance.start))
                    con_sec_end, con_min_end, con_hour_end = convertMillis(int(utterance.end))
                    st.write(f"SPEAKER {utterance.speaker}")
                    st.write(f":blue[{con_hour:02d}:{con_min:02d}:{con_sec:02d}] : {utterance.text}")  #- {con_hour_end:02d}:{con_min_end:02d}:{con_sec_end:02d}
        
        saved_transcript = st.session_state.get('transcript_paragraphs', [])
        if saved_transcript:
            st.markdown("<h2 class='title'>Transcript</h2>", unsafe_allow_html=True)
            for paragraph in saved_transcript:
                st.write(paragraph)

            full_transcript = '\n'.join(saved_transcript)
            copy_button = st.button("Copy Entire Transcript")
            if copy_button:
                pyperclip.copy(full_transcript)
                st.info("Transcript copied to clipboard!")
        
        if chapter_button:
            with st.spinner("Generating Auto Chapters..."):
                transcript = auto_chapters(file_path)
                for chapter in transcript.chapters:
                    con_sec, con_min, con_hour = convertMillis(int(chapter.start))
                    con_sec_end, con_min_end, con_hour_end = convertMillis(int(chapter.end))
                    st.write(f"{con_hour:02d}:{con_min:02d}:{con_sec:02d} - {con_hour_end:02d}:{con_min_end:02d}:{con_sec_end:02d}: {chapter.headline}")