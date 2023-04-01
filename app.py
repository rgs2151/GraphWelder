import streamlit as st

st.title("Hello World")

# Add a sidebar

st.sidebar.title("About")

st.sidebar.info(
    "This is a demo of Streamlit's capabilities."
)

# Add a radio to the sidebar with multiple options

add_selectbox = st.sidebar.radio("How would you like to be contacted?", ("Email", "Home phone", "Mobile phone"))

# Add a text box to the sidebar

add_text = st.sidebar.text_input("What's your name?")

# continue the radio buttons from before

st.sidebar.radio("Model Piplelines", ())
