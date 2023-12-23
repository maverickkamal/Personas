import streamlit as st
import datetime 
from content import BirthDataCalculator
from vectors import initialize_services
import google.generativeai as genai
from eval import TruLens
#from datetime import datetime



avatar = "https://media.roboflow.com/spaces/gemini-icon.png"
st.set_page_config(
    page_title="ZENTiDE - Personality Match", page_icon=avatar)

#include(home=True)

#with open("app/style.css") as css:
   # st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
minDate = datetime.date(1900, 1, 1)
maxDate = datetime.date(2030, 1, 1)
with st.sidebar:
    st.write("Provide your Personas")
    stdate = st.date_input("Enter date of Birth", value="today", min_value=minDate, max_value=maxDate, format="DD/MM/YYYY")
    sttime = st.sidebar.time_input("Enter time of birth", datetime.time(12, 00))
    longitude = st.number_input("Insert your longitude", value=15, placeholder="Type your longitude...")
    latitude = st.number_input("Insert your latitude", value=15, placeholder="Type your latitude...")
    sdate = datetime.datetime.strptime(str(stdate), "%Y-%m-%d")
    date = sdate.strftime("%d/%m/%Y")
    stime = datetime.datetime.strptime(str(sttime), "%H:%M:%S")
    time = stime.strftime("%H:%M")
    st.write(date, time)
    if st.button('Load data'):
        birth_data = BirthDataCalculator(date, time, longitude, latitude)
        content = birth_data.calculate_birth_data
        st.write(content)

    st.divider()
    st.markdown("""<span ><font size=1>Connect With Me</font></span>""",unsafe_allow_html=True)
    "[Linkedin](www.linkedin.com/in/musa-kamaludeen-814009218/)"
    "[GitHub](https://github.com/maverickkamal)"


genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')
    
query_engine = initialize_services()


# Define sudo
sudo = False  # Set this to False to disable dev_mode


def ask_and_respond(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=avatar):
        with st.spinner('Generating...'):
            response = query_engine.query(
                st.session_state.messages[-1]["content"])
            #res = model.generate_content(f"{content} - {response}")
        #st.markdown(res.text)

    # TrueLens logic for dev_mode
    if sudo:
        developer = TrueLens(query_engine, prompt, response)
        dev_results = developer.return_rag_triad()
        with st.expander("Development Mode Evalution"):
            st.json(dev_results)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})


### Initial message ###
start_message = st.chat_message("assistant", avatar=avatar)
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
    with st.chat_message(message["role"], avatar=(avatar if message["role"] == "assistant" else None)):
        st.markdown(message["content"])

chat_input_box = st.chat_input("what's on your mind??")

#for example, example_button in zip(examples, example_buttons):
    #if example_button:
     #   ask_and_respond(example)

if chat_input_box:
    ask_and_respond(chat_input_box)
