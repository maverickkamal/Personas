import streamlit as st
from st_pages import add_page_title, show_pages_from_config

def include(home=False):
    if home:
        show_pages_from_config()
    # else:
    add_page_title()

    with open( "app/style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    with st.sidebar:
        st.expander("ℹ️ Disclaimer").caption(
                "We do not take account of any data you give to the AI, We don't store or have access to any information you shared with the AI."
            )
        st.link_button("View on GitHub", "https://github.com/maverickkamal/Personas")
