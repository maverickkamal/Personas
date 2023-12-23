import streamlit as st
import datetime 
from content import BirthDataCalculator
from vectors import initialize_services
from components.include import include
from eval import TrueLens



avatar = "https://media.roboflow.com/spaces/gemini-icon.png"
st.set_page_config(
    page_title="Personas - Personality Match", page_icon=avatar)

include(home=True)

#with open("app/style.css") as css:
   # st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
date = st.sidebar.date_input("Enter date of Birth", value="today", min_value=1900/1/1, max_value=2030/1/1)
time = st.sidebar.time_input("Enter time of birth", datetime.time(12, 00))
longitude = st.number_input("Insert your longitude", value=15, placeholder="Type your longitude...")
latitude = st.number_input("Insert your latitude", value=15, placeholder="Type your latitude...")

if st.sidebar.button('Load data'):
    birth_data = BirthDataCalculator(date, time, longitude, latitude)
    content = birth_data.calculate_birth_data()

query_engine = initialize_services()


# Define sudo
sudo = False  # Set this to False to disable dev_mode


def ask_and_respond(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=avatar):
        with st.spinner('Processing...'):
            response = query_engine.query(
                st.session_state.messages[-1]["content"])
        st.markdown(response)

    # TrueLens logic for dev_mode
    if sudo:
        developer = TrueLens(query_engine, prompt, response)
        dev_results = developer.return_rag_triad()
        with st.expander("Development Mode Evalution"):
            st.json(dev_results)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})


### Initial message ###
start_message = st.chat_message("assistant", avatar=avatar_img)
start_message.write(
    "Hello friend, I am your Personality assisstant. how may i help you?")
#start_message.write("Examples of questions I can answer:")
#examples = [
  #  "What is USCIS?",
  #  "How do I check my case status?",
   # "¿Puedo obtener una visa de opción STEM si voy a una universidad estadounidense?",
#]
#example_buttons = [start_message.button(example) for example in examples]
#######################

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=(avatar_img if message["role"] == "assistant" else None)):
        st.markdown(message["content"])

chat_input_box = st.chat_input("What would you like to ask about?")

for example, example_button in zip(examples, example_buttons):
    if example_button:
        ask_and_respond(example)

if chat_input_box:
    ask_and_respond(chat_input_box)
