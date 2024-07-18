import google.generativeai as genai
import json
import streamlit as st


# Get the API key from the environment variables
genai.configure(api_key="AIzaSyBvDqRGZRkBfEXHzedjlCyBH5nx11ETRA8")



# Set up the model and load conversation history
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings
)

# template = f"If you know the answer then give it in proper way and i f you don't know the answer then please don't give any answer or don't make it by yourself. And always say thank you at the end of every answer. Also ask to Ask me more queries and feel free to interect. Don't give any excess information from your own if you don'st know. Also give their social media handles if you have it don't make it by your own."

# Loading Crops history for model

with open("soc.json", "r") as f:
    history = json.load(f)

# with open("crops.json", "r") as f:
#     Crop_history = json.load(f)

# Loading history for model
# with open("history.json", "r") as f:
#     history = json.load(f)

# Loading history for user
# with open("user_history.json", "r") as f:
#     uhistory = json.load(f)

# Loading history for model for students
# with open("students.json", "r") as f:
#     student_history = json.load(f)

# with open("output.json", "r") as f:
#     output = json.load(f)

# Set up the UI
st.title("GDSC BOT")
st.header("Come and chat with Thapar's first ever Society Bot!")



# Display a message indicating that the bot is in testing version
st.subheader("Testing Version")
st.write("<p style='color:red;'>This bot is currently in testing version on the website.</p>", unsafe_allow_html=True)



# Input and Generate Response Section
st.subheader("Ask me Anything about my GDSC family!")
input_prompt = st.text_area("Enter a prompt", key="input")
template = f"{input_prompt}. If you know the answer then give it in proper way and if you don't know the answer then please don't give any answer or don't make it by yourself. Give proper and short and straight to the point answer as a summer semester chatbot. Also ask to Ask me more queries and feel free to interect. Don't give any excess information from your own if you don'st know. also don't give any excess information from your own if you don't know. Just stick to the question and context"
# inputLLM = input_prompt + template
generate_response = st.button("Generate Response")

if generate_response:
    # convo = model.start_chat(history=output, context=template, safety_settings=safety_settings)
    convo = model.start_chat(history=history)
    response = convo.send_message(input_prompt)
    st.subheader("Response is:")
    st.write(response.text)

    #add user history to separate json file
    # uhistory.append({"role": "user", "parts": [input_prompt]})
    # uhistory.append({"role": "model", "parts": [response.text]})
    # with open("user_history.json", "w") as f:
    #     json.dump(uhistory, f)

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

# Save updated student history
with open("soc.json", "w") as f:
    json.dump(history, f)
