import openai
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
from pyngrok import ngrok

# Set OpenAI API Key (Use an environment variable for security)
openai.api_key = 'your api key here '




def speak(text):
    """Convert the text to speech and play it."""
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # macOS (Use 'mpg321 response.mp3' on Linux)

def listen():
    """Listen for voice input and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for your question...")
        audio = recognizer.listen(source)
    
    try:
        st.info("Recognizing...")
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand your speech. Please try again.")
        return None
    except sr.RequestError:
        st.error("Speech recognition service is unavailable.")
        return None

def get_gpt_response(query):
    """Get a response from OpenAI's GPT model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("Voice-Enabled Chat with GPT")
st.write("Ask a question using text or voice!")

user_input = st.text_input("Enter your question:")
if st.button("Submit"):
    if user_input:
        response = get_gpt_response(user_input)
        st.success(response)
        speak(response)

if st.button("Use Voice Input"):
    query = listen()
    if query:
        st.text(f"You said: {query}")
        response = get_gpt_response(query)
        st.success(response)
        speak(response)

# Ngrok setup
public_url = ngrok.connect(8501)
st.write(f"Public URL: {public_url}")
