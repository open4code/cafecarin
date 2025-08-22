# -*- coding: utf-8 -*-
# Python script for a Streamlit application with two distinct modules.
# Module 1: A "Decision Journey" tool that helps analyze pros and cons.
# Module 2: A "Value Reflection" guide based on user input.

import streamlit as st
import requests
import json
import time

# --- Configuration for LLM API (DO NOT MODIFY) ---
# API key will be provided by the runtime environment.
API_KEY = ""
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=" + API_KEY
API_HEADERS = {'Content-Type': 'application/json'}

# --- Helper function for making API calls with exponential backoff ---
def call_llm_api_with_backoff(prompt, max_retries=5, initial_delay=1):
    """
    Calls the LLM API with exponential backoff to handle rate limiting.
    
    Args:
        prompt (str): The text prompt for the LLM.
        max_retries (int): The maximum number of retries.
        initial_delay (int): The initial delay in seconds.
        
    Returns:
        dict: The JSON response from the API or None on failure.
    """
    retries = 0
    while retries < max_retries:
        try:
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            }
            response = requests.post(API_URL, headers=API_HEADERS, data=json.dumps(payload))
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
            
            result = response.json()
            if result.get('candidates') and result['candidates'][0].get('content'):
                return result
            else:
                st.error("Error: The LLM response was empty or malformed. Please try again.")
                return None

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                delay = initial_delay * (2 ** retries)
                st.warning(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                retries += 1
            else:
                st.error(f"HTTP Error: {err}")
                return None
        except requests.exceptions.RequestException as err:
            st.error(f"Request Error: {err}")
            return None
    st.error("Maximum retries reached. The API call failed.")
    return None

# --- Main App Structure ---
st.set_page_config(page_title="Entscheidungs-App", layout="centered")

# Use a selectbox to switch between the two app sections
selected_section = st.sidebar.selectbox(
    "Wähle einen Bereich:",
    ("Entscheidungsreise", "Werte-Reflexion & Großes Bild")
)

# --- Module 1: Decision Journey (Entscheidungsreise) ---
if selected_section == "Entscheidungsreise":
    st.title("Deine Entscheidungsreise 🚀")
    st.markdown("Finde Klarheit, indem du die Vor- und Nachteile deiner Entscheidung durchdenkst.")

    # Initialize session state for analysis results if not already present
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = ""
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False

    # Create a form for user input
    with st.form("decision_form"):
        st.subheader("Deine Entscheidung")
        decision = st.text_input("Worüber musst du dich entscheiden?")
        
        st.subheader("Pro-Argumente")
        pros_text = st.text_area("Was spricht dafür? (Ein Argument pro Zeile)", height=150)
        
        st.subheader("Kontra-Argumente")
        cons_text = st.text_area("Was spricht dagegen? (Ein Argument pro Zeile)", height=150)
        
        submit_button = st.form_submit_button("Starte die Entscheidungsreise")

    # Handle form submission
    if submit_button:
        if not decision:
            st.warning("Bitte gib deine Entscheidung ein.")
        elif not pros_text and not cons_text:
            st.warning("Bitte gib mindestens ein Pro- oder Kontra-Argument an.")
        else:
            # Set loading state
            st.session_state.is_loading = True
            
            with st.spinner("Deine Gedanken werden analysiert..."):
                pros_list = [p.strip() for p in pros_text.split("\n") if p.strip()]
                cons_list = [c.strip() for c in cons_text.split("\n") if c.strip()]
                
                # Construct the prompt for the LLM
                prompt = (
                    "Analysiere die folgende Entscheidung. Gib eine ausgewogene, "
                    "zusammenfassende Einschätzung, die sowohl die Vor- als auch die Nachteile berücksichtigt. "
                    "Gib keine Ratschläge, sondern nur eine objektive Bewertung.\n\n"
                    f"Entscheidung: {decision}\n\n"
                    f"Pro-Argumente:\n{'- ' + '\n- '.join(pros_list) if pros_list else 'Keine'}\n\n"
                    f"Kontra-Argumente:\n{'- ' + '\n- '.join(cons_list) if cons_list else 'Keine'}"
                )
                
                # Make the LLM API call
                llm_response = call_llm_api_with_backoff(prompt)
                
                if llm_response:
                    try:
                        analysis_text = llm_response['candidates'][0]['content']['parts'][0]['text']
                        st.session_state.analysis_result = analysis_text
                    except (KeyError, IndexError):
                        st.session_state.analysis_result = "Fehler bei der Analyse. Konnte die Antwort nicht verarbeiten."
            
            # Reset loading state
            st.session_state.is_loading = False
            
    # Display the analysis results
    if st.session_state.analysis_result:
        st.subheader("Deine Analyse")
        st.markdown(st.session_state.analysis_result)

# --- Module 2: Value Reflection & Big Picture (Werte-Reflexion & Großes Bild) ---
elif selected_section == "Werte-Reflexion & Großes Bild":
    st.title("Werte-Reflexion & Das große Bild")
    st.markdown("""
    Dies ist ein Bereich mit Potenzial, um **deine täglichen Handlungen mit deinen tiefsten Werten und deinem Lebenssinn in Einklang zu bringen**.
    """)

    st.subheader("Strategien zur Verbesserung:")
    
    st.markdown("""
    **1. Werte identifizieren:**
    Nehmen Sie sich Zeit, um zu identifizieren, was Ihnen wirklich wichtig ist. Schreiben Sie Ihre zentralen Werte auf, wie z.B. Familie, Ehrlichkeit, Kreativität oder Erfolg.
    """)
    
    st.markdown("""
    **2. Zusammenhänge verstehen:**
    Wenn Sie mit einem kleinen Problem konfrontiert sind, versuchen Sie, es in einen größeren Kontext zu stellen. Versuchen Sie, Verhaltensweisen von Menschen oder Ereignisse aus einem anderen Blickwinkel zu betrachten.
    """)
    
    st.markdown("""
    **3. Sinn finden:**
    Suchen Sie nach Wegen, wie Sie Ihren Alltag als sinnvoller empfinden können, z.B. indem Sie Ihre Arbeit mit Ihren persönlichen Werten verknüpfen.
    """)

