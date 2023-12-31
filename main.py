import streamlit as st
import datetime 
from context import BirthDataCalculator
from vectors import initialize_services
import google.generativeai as genai
from eval import TruLens
from image_processing import gemini
from util.word_check import WordChecker
from util.word_list import wordlist
#from util.schema import run_conversation
from util.scheme import run_conversation


avatar = "https://media.roboflow.com/spaces/gemini-icon.png"
avatar2 = "https://i.ibb.co/8BKfNPx/avatar.png"
st.set_page_config(
    page_title="ZENTiDE - Personality Match", page_icon=avatar)

st.markdown('''# **ZENTiDE** - *Personality and Gene Keys*
Zentide uniquely guides your path to self-growth and purpose by revealing AI-powered insights personalized to your DNA, 
chronorhythm, and higher consciousness through an integrated framework of neural networks, ancient wisdoms and bio-algorithms.
''')

#include(home=True)

#with open("app/style.css") as css:
   # st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
image = st.file_uploader(f"File uploader ", accept_multiple_files=False, type = ['jpg', 'png'])
with open("button.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

minDate = datetime.date(1900, 1, 1)
maxDate = datetime.date(2030, 1, 1)
global content
content = None  # Global variable

def load_data():
    global content
    content = birth_data
    if "error" in content:
        st.write(f"Error: {content['error']}")
#global content
with st.sidebar:
    st.markdown('''# **Description**
    Zentide offers a gateway to self-actualization through harmonizing your inner consciousness with the cosmic dynamics that influence us all.

Combining a foundation of mindful zen practices for presence with an overlay of your unique bio-rhythms and external cycles, Zentide provides tailored daily guidance to help you achieve inner peace and outward purpose.

At Zentide's core sits an integrative framework powering personalized recommendations and insights generated from our proprietary fusion of neural networks, genetic algorithms, chronobiology research and ancient philosophies.

The result? A pioneering path to discover your highest self – designed just for you each day by bridging cutting-edge AI capabilities with timeless intuitive wisdom.

Zentide invites you on a beautiful journey of understanding your consciousness through the interplay of modern and ancient knowledge streams. Our intelligent platform nurtures self-growth and actualization within the greater context of natural rhythms all around and within us.
    # **Note**: It's still in development as the Personality Schema is still underway 

    ''')
    st.write("# Provide your Personas")
    stdate = st.date_input("Enter date of Birth", value="today", min_value=minDate, max_value=maxDate, format="DD/MM/YYYY")
    sttime = st.sidebar.time_input("Enter time of birth", datetime.time(12, 00))
    longitude = st.number_input("Insert your longitude", value=15, placeholder="Type your longitude...")
    latitude = st.number_input("Insert your latitude", value=15, placeholder="Type your latitude...")
    sdate = datetime.datetime.strptime(str(stdate), "%Y-%m-%d")
    date = sdate.strftime("%d/%m/%Y")
    stime = datetime.datetime.strptime(str(sttime), "%H:%M:%S")
    time = stime.strftime("%H:%M")
    birth_data = (date, time, longitude, latitude)
    st.write(date, time)
    if st.button('Load data'):
        content = birth_data
        #content = birth_data.calculate_birth_data()  # Call the method
        #if "error" in content:
           # st.write(f"Error: {content['error']}")
        #else:
           # st.write(content)

    st.divider()
    st.markdown("""<span ><font size=1>Connect With Me</font></span>""",unsafe_allow_html=True)
    "[Linkedin](www.linkedin.com/in/musa-kamaludeen-814009218/)"
    "[GitHub](https://github.com/maverickkamal)"

#st.write(content)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')
    
query_engine = initialize_services()


# Define sudo
sudo = False # Set this to False to disable dev_mode
wordz = wordlist()
checker = WordChecker(wordz)



def ask_and_respond(prompt):
    #global content
    #content = content
    #st.write(content)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=avatar2):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=avatar):
        with st.spinner('Generating...'):
            #content = load_data()
            res = st.session_state.messages[-1]["content"]
            templ = f"Convert the provided JSON {content} into a tabular form, representing the person's personality information with relevant details excluding gate number or any numeric value. using this query: {res} as a secondary guide"
            wordcheck = checker.check_word_in_statement(res)
            
            system_message = "You are an AI bot that can do everything using function calls. When you are asked to do something, use the function call you have available and then respond with a message shortly confirming what you have done. When writing Personality, Summarize the key aspects of the persons character in a table while keping it personal. When writing the Personality, Make it motivational by telling the person about their inner self."
            if image is not None:
                bytes_data = image.getvalue()
                response = gemini(res, bytes_data)
            elif wordcheck == True:
                message = {
                     "role": "user",
                     "parts": [{"text": system_message + "\n\n" + prompt}]
                }
                response = run_conversation(message, messages1)
                #resps = model.generate_content(templ)
                #response = resps.text
            else:
                response = query_engine.query(res)
                #print("Not Found")
            #res = model.generate_content(f"{content} - {response}")
        st.markdown(response)

    # TrueLens logic for dev_mode
    if sudo:
        developer = TruLens(query_engine, prompt, response)
        dev_results = developer.return_rag_triad()
        with st.expander("Development Mode Evalution"):
            st.json(dev_results)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})


### Initial message ###
start_message = st.chat_message("assistant", avatar=avatar)
start_message.write(
    "Hello friend, I am your Personality assisstant. how may i help you?")
start_message.write("Examples of questions I can answer:")
examples = [
    "What is Gene Keys?",
    "What is the Concept personality?",
    "How to Leverage my Potential",
]
example_buttons = [start_message.button(example) for example in examples]
#######################
messages1 = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=(avatar if message["role"] == "assistant" else (avatar2 if message["role"] == "user" else None))):
        st.markdown(message["content"])

chat_input_box = st.chat_input("what's on your mind??")

for example, example_button in zip(examples, example_buttons):
    if example_button:
        ask_and_respond(example)

if chat_input_box:
    ask_and_respond(chat_input_box)
