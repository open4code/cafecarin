import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Interaktives Tool mit CafeCarin, um die Welt zu verbessern")

st.write("""
Lasst uns gemeinsam die Welt verbessern.
""")

st.markdown(
    """
    ---
    **Anleitung:**
    1. Teste die Streamlit Features im Playground https://streamlit.io/playground
    2. Check die Docs mit mache dich mit den Streamlit Möglichkeiten vertraut https://docs.streamlit.io
    3. Erweitere diesen Code auf Github, und teste die Änderungen auf https://cafecarin-0815.streamlit.app
    """
)

if st.button("Send balloons!"):
    st.balloons()

st.write("""
Ihre Carolin
""")
