'''
Sai Vemugunta

Thought Process: I first thought to call the transcriber api to take in an audio file from the front end.
I created the front end through streamlite frontend software. I also made a way for different audio files
each with their own language to be translated into their conversation.

Challenges: I faced a challenge in creating the frontend because this was my first time setting up a rather
complex frontend. To fix this I had to take the proccess slow and set up every step within my command line.

Tools/Libraries: Used the stream lit frontend software as it enabled me to code in python. Similarly, 
I used the assemblyai api in order to convert the audio file ito text. Furthermore, I used the fpdf and base64
libraries in order to download the transcript.



'''

import assemblyai as aai
import streamlit as st
import tempfile
from fpdf import FPDF
import base64

# Sets the API key

aai.settings.api_key = "ASSEMBLY AI  API KEY"

# Sets the title of your Streamlit app

st.title("Sai's Transcriptor!")

# File uploader for choosing an audio file

uploaded_file = st.file_uploader("Choose a file", type=("mp3", "wav", "aac", "m4a"))

# Displays supported languages for transcription

st.write("Languages that can be transcribed:")
st.write("Global English, Australian English, British English, US English, Spanish")
st.write("French, German, Italian, Portuguese, Hindi, Japanese, Chinese, Korean, Polish")
st.write("Russian, Turkish, Ukrainian, Vietnamese")
st.divider()

# Defines a variable to control PDF export (you can set it based on your logic)

export_as_pdf = True

if uploaded_file is not None:
    
    # Creates a temporary file to save the uploaded content
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Initializes the transcriber and configure language detection
    
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(language_detection=True)
    
    # Transcribes the uploaded audio file with language detection
    
    transcript = transcriber.transcribe(temp_path, config=config)
    
    # Gets the transcript ID
    
    transcript_id = transcript.id
    
    # Waits for the transcription to complete
    
    transcript.get_by_id(transcript_id)

    # Displays the transcript if the transcription is completed
    
    if transcript.status == "completed":
        st.write("Transcript:")
        st.write(transcript.text)
    else:
        st.write(f"Transcription status: {transcript.status}")

    # Removes the temporary file
    
    import os
    os.remove(temp_path)
    
    # Allows the user to edit the transcript
    
    textEdit = st.text_input("Edit transcript: ", value=transcript.text)
    
    # Defines a function to create a download link for the transcript in PDF
    
    def downloadTrans(bytes, filename):
        b64 = base64.b64encode(bytes)
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

    if export_as_pdf:
        
        # Creates a PDF and add the edited transcript
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Uses 'multi_cell' for text that wraps to the next line
        
        pdf.multi_cell(0, 10, textEdit)  
    
        # Generates a download link for the PDF
        
        html = downloadTrans(pdf.output(dest="S").encode("latin-1"), "transcript")
        st.markdown(html, unsafe_allow_html=True)
