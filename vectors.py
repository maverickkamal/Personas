import os
import streamlit as st
from llama_index.indices import VectaraIndex
from llama_index.llms import Gemini

@st.cache_resource
def initialize_services():
    # Authenticate with Google Gemini and OpenAI

    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["OPENAI_API_KEY"] = st.secrets["OPEN_AI_API_KEY"]
    llm = Gemini(
        model="models/gemini-pro-vision"
    )
    

    # Load the vector index
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=5,
        summary_enabled=False,
        vectara_query_mode="mmr",
        mmr_k=50,
        mmr_diversity_bias=0.5,
    )
    return query_engine
