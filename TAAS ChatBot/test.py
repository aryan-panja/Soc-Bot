import google.generativeai as genai
import json
import streamlit as st
import os
import os
from dotenv import load_dotenv

from gtts import gTTS
from io import BytesIO
import IPython.display as ipd
import tempfile
import base64



# Configure the API key (replace with your actual API key)
# Load the environment variables from the .env file
load_dotenv()



# Get the API key from the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



# Set up the model and load conversation history
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings
)

# Loading Crops history for model
with open("crops.json", "r") as f:
    Crop_history = json.load(f)

# Loading history for model
with open("history.json", "r") as f:
    history = json.load(f)



# Loading history for user
with open("user_history.json", "r") as f:
    uhistory = json.load(f)



# Set up the UI
st.title("TAAS BOT")
st.header("Come and chat with Thapar's first ever Society Bot!")



# Display a message indicating that the bot is in testing version
st.subheader("Testing Version")
st.write("<p style='color:red;'>This bot is currently in testing version on the website.</p>", unsafe_allow_html=True)



# Input and Generate Response Section
st.subheader("Ask me Anything about my TAAS family!")
input_prompt = st.text_area("Enter a prompt", key="input")
generate_response = st.button("Generate Response")

if generate_response:
    convo = model.start_chat(history=history)
    response = convo.send_message(input_prompt)
    st.subheader("Response is:")
    st.write(response.text)

    # Convert text to voice using gTTS
    tts = gTTS(text=response.text, lang='en')

    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tts.save(tmp_audio.name)

    # Play the audio automatically using HTML audio element
    st.markdown(f'<audio src="data:audio/mp3;base64,{base64.b64encode(open(tmp_audio.name, "rb").read()).decode()}" autoplay controls>', unsafe_allow_html=True)

    #add user history to separate json file
    uhistory.append({"role": "user", "parts": [input_prompt]})
    uhistory.append({"role": "model", "parts": [response.text]})
    with open("user_history.json", "w") as f:
        json.dump(uhistory, f)

# Add to History Section
st.subheader("Add to History")
new_prompt = st.text_area("Enter a prompt", key="input2")
new_response = st.text_area("Enter a response", key="input3", height=300)
add_to_history = st.button("Add to History")

if add_to_history:
    history.append({"role": "user", "parts": [new_prompt]})
    history.append({"role": "model", "parts": [new_response]})

    
    # Show success message
    st.success("Successfully added to history!")

# Save updated history
with open("history.json", "w") as f:
    json.dump(history, f)
