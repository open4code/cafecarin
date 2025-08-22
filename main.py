# -*- coding: utf-8 -*-
# Python script for a Streamlit application with three distinct modules.
# Module 1: A "Decision Journey" tool that helps analyze pros and cons.
# Module 2: A "Resilience Reflection" guide based on user input.
# Module 3: A set of interactive "Health Paths".

import streamlit as st
import altair as alt
import pandas as pd
import json
import requests
import time
import base64
import random

# --- 1. SEITENKONFIGURATION & STYLING ---
st.set_page_config(
    page_title="VitaBoost",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# The CSS has been completely rewritten to replicate the layout from the image.
custom_css = """
<style>
    /* General color palette and font */
    :root {
        --primary-color: #E2B060;
        --secondary-color: #F8D8C9;
        --background-color: #FFF8E1;
        --text-color: #4A4A4A;
        --container-bg: #FFFFFF;
        --border-radius: 16px;
    }

    body {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: var(--background-color);
    }

    /* Styling for all containers and expanders (the "cards") */
    div[data-testid="stVerticalBlock"] > div.st-emotion-cache-1r6y9j9,
    div[data-testid="stVerticalBlock"] > div.st-emotion-cache-1n1p067,
    .stTabs [role="tablist"] button[aria-selected="true"] {
        background-color: var(--container-bg);
        border-radius: var(--border-radius);
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .st-emotion-cache-1jm692n, .st-emotion-cache-1j0r921 {
        background-color: transparent;
        padding: 0;
    }

    /* Styling for headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
        font-weight: 600;
    }
    h1 {
        color: var(--primary-color);
        font-size: 2.5rem;
    }
    
    .st-emotion-cache-12m32bb {
        background-color: #FFF;
        border-radius: 16px;
        padding: 10px;
    }

    /* Styling for buttons */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #D4A35B;
    }
    
    .st-emotion-cache-79elbk {
      gap: 20px;
    }

    /* Specific styling for text areas and input fields (colored background) */
    .st-emotion-cache-13gs647, .st-emotion-cache-1cpx9g8, .st-emotion-cache-13v2p5x, .st-emotion-cache-1l006n6 {
        background-color: var(--secondary-color) !important;
        color: var(--text-color);
        border-radius: 12px;
        border: none;
        padding: 10px;
    }

    /* Styling for sliders */
    .st-emotion-cache-14u43s4 {
        background-color: var(--secondary-color);
        border-radius: 10px;
        height: 10px;
    }
    .st-emotion-cache-14u43s4 > div {
        background-color: var(--primary-color);
    }
    .stSlider > div > div > div:nth-child(2) {
        background-color: var(--secondary-color); /* Slider track */
    }
    .stSlider > div > div > div:nth-child(2) > div:nth-child(1) {
        background-color: var(--primary-color); /* Slider fill */
    }

    /* Styling for the bottom navigation bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: var(--container-bg);
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 10px 0;
        z-index: 1000;
        border-top-left-radius: var(--border-radius);
        border-top-right-radius: var(--border-radius);
    }
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        color: var(--text-color);
        cursor: pointer;
        font-size: 14px;
        opacity: 0.7;
        transition: opacity 0.3s;
    }
    .nav-item:hover, .nav-item.active {
        opacity: 1;
        color: var(--primary-color);
    }
    .nav-item .icon {
        font-size: 24px;
        margin-bottom: 4px;
    }

    /* Card styling for path selection */
    .path-card-container {
        background-color: #f0f0f0; 
        border-radius: 12px; 
        padding: 20px; 
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid #ddd;
    }

    .path-card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    
    .path-card-container h4 {
        color: var(--primary-color);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- Configuration for LLM API (DO NOT CHANGE) ---
# The API key is provided by the runtime environment.
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

# --- 2. MANAGING APP STATE (SESSION STATE) ---
def init_session_state():
    if 'page' not in st.session_state: st.session_state.page = 'start'
    if 'problem' not in st.session_state: st.session_state.problem = ""
    if 'problem_category' not in st.session_state: st.session_state.problem_category = "Wähle eine Kategorie"
    if 'options' not in st.session_state: st.session_state.options = ["", ""]
    if 'selected_values' not in st.session_state: st.session_state.selected_values = []
    if 'values_rating' not in st.session_state: st.session_state.values_rating = {}
    if 'emotions' not in st.session_state: st.session_state.emotions = ""
    if 'pro_a' not in st.session_state: st.session_state.pro_a = ""
    if 'contra_a' not in st.session_state: st.session_state.contra_a = ""
    if 'pro_b' not in st.session_state: st.session_state.pro_b = ""
    if 'contra_b' not in st.session_state: st.session_state.contra_b = ""
    if 'creative_options' not in st.session_state: st.session_state.creative_options = ""
    if 'future_scenario_a' not in st.session_state: st.session_state.future_scenario_a = ""
    if 'future_scenario_b' not in st.session_state: st.session_state.future_scenario_b = ""
    if 'first_step' not in st.session_state: st.session_state.first_step = ""
    
    # State for the resilience questionnaire
    if 'resilience_answers' not in st.session_state: st.session_state.resilience_answers = {}
    if 'resilience_score' not in st.session_state: st.session_state.resilience_score = None
    if 'resilience_analysis' not in st.session_state: st.session_state.resilience_analysis = None
    if 'processing_analysis' not in st.session_state: st.session_state.processing_analysis = False
    
    # State for resilience paths
    if 'current_path' not in st.session_state: st.session_state.current_path = None
    if 'current_stage_index' not in st.session_state: st.session_state.current_stage_index = 0
    if 'show_path_screen' not in st.session_state: st.session_state.show_path_screen = False

init_session_state()

def next_page(page_name):
    st.session_state.page = page_name

def reset_app():
    st.session_state.clear()
    init_session_state()
    st.experimental_rerun()

# --- 3. DYNAMIC CONTENT FOR EACH CATEGORY ---
category_content = {
    "Karriere & Beruf": {
        "values": ["Finanzielle Sicherheit", "Wachstum", "Autonomie", "Einfluss", "Anerkennung", "Work-Life-Balance"],
        "cognitive_biases": {
            "title": "Common Career Thinking Errors",
            "biases": [
                ("Loss Aversion", "Am I focusing more on what I could lose in my current job than on what I could gain in the new one?"),
                ("Anchoring Effect", "Am I too fixated on the first salary offer or promotion I received, which is preventing me from seeing a better opportunity?"),
                ("Confirmation Bias", "Am I only looking for information that confirms my decision for or against a job, and ignoring contrary information?")
            ]
        },
    },
    "Persönliches Wachstum": {
        "values": ["Selbstverwirklichung", "Kreativität", "Lernen", "Soziale Bindungen", "Entwicklung", "Freiheit"],
        "cognitive_biases": {
            "title": "Common Thinking Errors in Personal Growth",
            "biases": [
                ("Status Quo Bias", "Do I prefer the easy option because I'm afraid of change, even if the new option would help me grow?"),
                ("Confirmation Bias", "Am I only looking for information that confirms my belief that a new skill is too hard to learn?"),
                ("Availability Heuristic", "Am I basing my decision only on easily available, spectacular stories, rather than on more realistic facts?")
            ]
        },
    },
    "Beziehungen & Familie": {
        "values": ["Soziale Bindungen", "Harmonie", "Vertrauen", "Empathie", "Stabilität", "Zugehörigkeit"],
        "cognitive_biases": {
            "title": "Common Thinking Errors in Relationships",
            "biases": [
                ("Cherry Picking", "Am I ignoring all the negative aspects and only focusing on the good ones to avoid a difficult situation?"),
                ("Sunk Cost Fallacy", "Am I staying in a relationship or situation just because I've already invested so much time and energy, instead of looking ahead?"),
                ("Confirmation Bias", "Do I only listen to friends who share my opinion and avoid conversations that challenge me?")
            ]
        },
    }
}


# Data for the different resilience paths
paths = {
    'stress': {
        'title': 'Stressabbau',
        'description': 'Find inner peace through guided meditations and breathing exercises.',
        'stages': [
            {'title': 'Atemübungen', 'description': 'Beginnen Sie mit einer einfachen Atemübung, um zur Ruhe zu kommen.'},
            {'title': 'Geführte Meditation', 'description': 'Hören Sie sich eine kurze geführte Meditation an, um Ihren Geist zu klären.'},
            {'title': 'Körperliche Aktivität', 'description': 'Bauen Sie Stress durch eine kurze körperliche Aktivität ab, z.B. einen Spaziergang.'}
        ],
        'tips': [
            'Achten Sie auf Ihre Atmung.',
            'Lassen Sie Gedanken los, ohne sie zu bewerten.',
            'Regelmäßigkeit ist der Schlüssel.'
        ]
    },
    'self-image': {
        'title': 'Selbstbild stärken',
        'description': 'Stärken Sie Ihr Selbstwertgefühl und Ihre Selbstwirksamkeit.',
        'stages': [
            {'title': 'Positive Affirmationen', 'description': 'Beginnen Sie jeden Tag mit einer positiven Affirmation.'},
            {'title': 'Dankbarkeits-Journal', 'description': 'Schreiben Sie täglich drei Dinge auf, für die Sie dankbar sind.'},
            {'title': 'Erfolge feiern', 'description': 'Erinnern Sie sich an einen Erfolg aus Ihrer Vergangenheit und feiern Sie ihn.'}
        ],
        'tips': [
            'Wiederholen Sie die Affirmationen laut.',
            'Fokussieren Sie sich auf kleine, tägliche Erfolge.',
            'Seien Sie geduldig und freundlich zu sich selbst.'
        ]
    },
    'self-efficacy': {
        'title': 'Selbstwirksamkeitserwartung',
        'description': 'Develop the confidence to successfully master your goals.',
        'stages': [
            {'title': 'Kleine Ziele setzen', 'description': 'Wählen Sie ein kleines, leicht erreichbares Ziel und erreichen Sie es.'},
            {'title': 'Lernkurve erkennen', 'description': 'Betrachten Sie Misserfolge als Lernchancen, nicht als Rückschläge.'},
            {'title': 'Mentoren finden', 'description': 'Lernen Sie von Menschen, die Ihre Ziele bereits erreicht haben.'}
        ],
        'tips': [
            'Feiern Sie jeden noch so kleinen Fortschritt.',
            'Seien Sie realistisch mit Ihren Zielen.',
            'Umgeben Sie sich mit positiven Vorbildern.'
        ]
    },
    'connectedness': {
        'title': 'Verbundenheit',
        'description': 'Strengthen your relationships and your connection to others.',
        'stages': [
            {'title': 'Kontakt aufnehmen', 'description': 'Schreiben Sie einer Person, die Ihnen wichtig ist, eine kurze Nachricht.'},
            {'title': 'Zuhören', 'description': 'Üben Sie aktives Zuhören in einem Gespräch.'},
            {'title': 'Empathie zeigen', 'description': 'Versuchen Sie, die Perspektive einer anderen Person zu verstehen.'}
        ],
        'tips': [
            'Seien Sie präsent im Moment.',
            'Ein Lächeln kann Wunder wirken.',
            'Qualität geht vor Quantität.'
        ]
    }
}


def render_start_page():
    # Main container for the start page
    with st.container():
        st.title("VitaBoost")
        st.image("https://placehold.co/1200x400/FFF8E1/E2B060?text=Stärke+deine+Entscheidungen%2C+stärke+dein+Leben")
        st.markdown("Stärke deine Entscheidungen, stärke dein Leben. Wähle den passenden Pfad für deine Situation.")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### Entscheidungsreise")
            st.markdown("Strukturiere deine Gedanken und Gefühle, um eine fundierte Entscheidung zu treffen.")
            st.button("Starte die Entscheidungsreise", on_click=next_page, args=['step_1'])

        with col2:
            st.markdown("### Resilienz-Test")
            st.markdown("Teste deine Widerstandsfähigkeit und stärke die Faktoren, die dich widerstandsfähig machen.")
            if st.button("Starte den Resilienz-Test"):
                st.query_params['page'] = 'wert_reflexion'
                st.query_params['tab'] = 'questionnaire'
                st.experimental_rerun()

        with col3:
            st.markdown("### Gesundheitspfade")
            st.markdown("Du steckst gerade in einer Krise? Stärke deine Resilienzfaktoren, um zukünftige Krisen gut zu bewältigen.")
            if st.button("Starte die Pfade"):
                st.query_params['page'] = 'wert_reflexion'
                st.query_params['tab'] = 'paths'
                st.experimental_rerun()


def render_wert_reflexion_page():
    st.title("Werte-Reflexion & Resilienz")
    
    # Get the active tab from query parameters, default to "questionnaire"
    active_tab = st.query_params.get('tab', ['questionnaire'])[0]
    
    # Create the tabs
    tab1, tab2 = st.tabs(["Resilienz-Fragebogen", "Interaktive Pfade"])

    with tab1:
        st.header("Wie steht es um deine Resilienz?")
        st.markdown("Beantworte die folgenden Fragen, um eine erste Einschätzung deiner Widerstandsfähigkeit zu erhalten.")
        
        # Questions for the questionnaire
        questions = [
            "Ich kann mich gut von Rückschlägen erholen.",
            "Ich habe ein starkes soziales Netzwerk, auf das ich mich verlassen kann.",
            "Ich betrachte Herausforderungen als Chancen zu wachsen.",
            "Ich bin optimistisch, was meine Zukunft angeht.",
            "Ich kann meine Emotionen gut regulieren, auch in stressigen Situationen."
        ]
        
        answers = {}
        for i, question in enumerate(questions):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(question)
            with col2:
                answers[i] = st.selectbox(
                    "Rating",
                    options=[1, 2, 3, 4, 5],
                    index=st.session_state.resilience_answers.get(i, 2),
                    key=f"q_{i}",
                    format_func=lambda x: f"{x} / 5"
                )
        
        st.session_state.resilience_answers = answers
        
        if st.button("Ergebnis analysieren"):
            st.session_state.resilience_score = sum(answers.values())
            
            # Show a spinner while analysis is running
            with st.spinner('Analysiere dein Ergebnis...'):
                prompt = (
                    f"Based on a resilience questionnaire with 5 questions (1=strongly disagree, 5=strongly agree), a user achieved a total score of {st.session_state.resilience_score}. "
                    f"The maximum score is 25. Generate a personalized, encouraging analysis that explains what the score means. "
                    f"Also provide concrete suggestions on how to further strengthen resilience. Use friendly, motivating language. "
                    f"Begin directly with the analysis, without an introduction."
                )
                
                # Call the LLM API
                llm_response = call_llm_api_with_backoff(prompt)
                
                if llm_response:
                    try:
                        analysis_text = llm_response['candidates'][0]['content']['parts'][0]['text']
                        st.session_state.resilience_analysis = analysis_text
                    except (KeyError, IndexError):
                        st.session_state.resilience_analysis = "There was a problem with the analysis. Please try again later."
            
            st.experimental_rerun()
            
        if st.session_state.resilience_analysis:
            st.subheader("Deine persönliche Analyse")
            st.info(st.session_state.resilience_analysis)
            st.markdown(f"**Dein Gesamtscore:** {st.session_state.resilience_score} von 25 Punkten.")
            st.markdown("---")
            st.button("Fragebogen zurücksetzen", on_click=reset_app)

    with tab2:
        st.header("Interaktive Resilienz-Pfade")
        if st.session_state.show_path_screen:
            render_path_screen()
        else:
            # Path selection view
            st.markdown("### Wähle deinen Pfad")
            
            def start_path(path_key):
                st.session_state.current_path = paths[path_key]
                st.session_state.current_stage_index = 0
                st.session_state.show_path_screen = True
                st.experimental_rerun()

            col_stress, col_self_image = st.columns(2)
            with col_stress:
                st.markdown(
                    f"""
                    <div class="path-card-container">
                        <h4>{paths['stress']['title']}</h4>
                        <p>{paths['stress']['description']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                if st.button("Starten", key="start_stress"):
                    start_path('stress')
            
            with col_self_image:
                st.markdown(
                    f"""
                    <div class="path-card-container">
                        <h4>{paths['self-image']['title']}</h4>
                        <p>{paths['self-image']['description']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                if st.button("Starten", key="start_self_image"):
                    start_path('self-image')

            col_efficacy, col_connectedness = st.columns(2)
            with col_efficacy:
                st.markdown(
                    f"""
                    <div class="path-card-container">
                        <h4>{paths['self-efficacy']['title']}</h4>
                        <p>{paths['self-efficacy']['description']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                if st.button("Starten", key="start_self_efficacy"):
                    start_path('self-efficacy')

            with col_connectedness:
                st.markdown(
                    f"""
                    <div class="path-card-container">
                        <h4>{paths['connectedness']['title']}</h4>
                        <p>{paths['connectedness']['description']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                if st.button("Starten", key="start_connectedness"):
                    start_path('connectedness')
            
def render_path_screen():
    path_data = st.session_state.current_path
    
    st.markdown(f"### {path_data['title']}")
    st.markdown(f"_{path_data['description']}_")
    
    # Progress bar
    progress = (st.session_state.current_stage_index + 1) / len(path_data['stages'])
    st.progress(progress)
    
    # Current stage
    current_stage = path_data['stages'][st.session_state.current_stage_index]
    
    st.subheader(f"Schritt {st.session_state.current_stage_index + 1}: {current_stage['title']}")
    st.markdown(current_stage['description'])
    
    # Expert tip
    st.info(f"**Expertentipp:** {random.choice(path_data['tips'])}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zur Pfad-Auswahl"):
            st.session_state.show_path_screen = False
            st.experimental_rerun()
    with col2:
        if st.button("Nächster Schritt"):
            if st.session_state.current_stage_index < len(path_data['stages']) - 1:
                st.session_state.current_stage_index += 1
                st.experimental_rerun()
            else:
                st.success("Herzlichen Glückwunsch! Sie haben diesen Pfad abgeschlossen.")
                st.session_state.show_path_screen = False
                st.session_state.current_path = None
                st.experimental_rerun()


def render_step_1():
    st.title("Step 1: Dein Problem & deine Optionen")
    
    # 1. Container for problem and category (now in the first place)
    with st.container():
        st.markdown("#### Problem und Kategorie")
        st.session_state.problem = st.text_area(
            "Was ist die Entscheidung, die dich beschäftigt?",
            value=st.session_state.problem,
            key="problem_input",
            height=100
        )
        
        options = ["Wähle eine Kategorie"] + list(category_content.keys())
        try:
            current_index = options.index(st.session_state.problem_category)
        except ValueError:
            current_index = 0
        st.session_state.problem_category = st.selectbox(
            "Kategorie:",
            options=options,
            index=current_index
        )
    
    # 2. Container for the options
    with st.container():
        st.markdown("#### Optionen")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.options[0] = st.text_area("Option A:", value=st.session_state.options[0], height=100, key="option_a_input")
        with col2:
            st.session_state.options[1] = st.text_area("Option B:", value=st.session_state.options[1], height=100, key="option_b_input")
    
    is_valid = all([st.session_state.problem, st.session_state.options[0], st.session_state.options[1], st.session_state.problem_category != "Wähle eine Kategorie"])
    if st.button("Weiter", disabled=not is_valid):
        next_page('step_2')

def render_step_2():
    st.title("Step 2: Werte & Motivation")
    selected_category = st.session_state.problem_category
    all_values = category_content.get(selected_category, {}).get("values", ["Sicherheit", "Freiheit", "Entwicklung"])
    
    with st.container():
        st.markdown(f"#### Psychologische Werte")
        # Corrected line to display the category name correctly
        st.markdown(f"Wähle alle Werte aus, die für deine Entscheidung in der Kategorie **{selected_category}** relevant sind.")
        
        # Clear the list of selected values before the checkboxes are rendered to update the state correctly
        st.session_state.selected_values = []
        cols = st.columns(3) # Creates 3 columns for the checkboxes
        for i, value in enumerate(all_values):
            col = cols[i % 3] # Distributes the checkboxes across the columns
            if col.checkbox(value, key=f"checkbox_{value}"):
                st.session_state.selected_values.append(value)

    # Sliders are only displayed if values have been selected
    if st.session_state.selected_values:
        with st.container():
            st.markdown("#### Werte-Bewertung (Deine Entscheidungsmatrix)")
            st.markdown("Bewerte auf einer Skala von 1 bis 10, wie gut jede Option deine gewählten Werte erfüllt.")
            st.markdown("Die Punktzahl, die du hier vergibst, **gewichtet** automatisch die Wichtigkeit der Werte für deine endgültige Entscheidung.")
            for value in st.session_state.selected_values:
                st.subheader(f"Wert: {value}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.session_state.values_rating[f"{value}_A"] = st.slider(
                        f"Option A: {st.session_state.options[0]}",
                        0, 10, st.session_state.values_rating.get(f"{value}_A", 5), key=f"slider_a_{value}"
                    )
                with col_b:
                    st.session_state.values_rating[f"{value}_B"] = st.slider(
                        f"Option B: {st.session_state.options[1]}",
                        0, 10, st.session_state.values_rating.get(f"{value}_B", 5), key=f"slider_b_{value}"
                    )

    if st.button("Weiter"):
        # Perform a final check
        if not st.session_state.selected_values:
            st.warning("Bitte wähle mindestens einen Wert aus, bevor du fortfährst.")
        else:
            next_page('step_3')
    
def render_step_3():
    st.title("Step 3: Emotionen & Denkfehler")
    with st.container():
        # The Red Hat
        st.markdown("#### Dein Bauchgefühl (Der 'Rote Hut' von Edward de Bono)")
        st.markdown("Schreibe auf, welche Gefühle und intuitive Gedanken du zu den Optionen hast. Es geht nicht um Logik, sondern um Emotionen.")
        st.session_state.emotions = st.text_area("Deine Gedanken:", value=st.session_state.emotions, height=150)
    
    selected_content = category_content.get(st.session_state.problem_category, {})
    biases = selected_content.get("cognitive_biases", {}).get("biases", [])
    
    if biases:
        with st.container():
            st.markdown("#### Reflektiere über Denkfehler")
            for bias_title, bias_question in biases:
                with st.expander(f"**{bias_title}**"):
                    st.markdown(bias_question)

    # The "Continue" button has been moved here to appear after the expanders.
    if st.button("Weiter"):
        next_page('step_4')

def render_step_4():
    st.title("Step 4: Pro/Contra & Zukunft")
    
    # The Yellow and Black Hat
    with st.container():
        st.markdown(f"#### Vorteile (Der 'Gelbe Hut' von Edward de Bono)")
        st.session_state.pro_a = st.text_area(
            f"Was spricht für Option A: '{st.session_state.options[0]}'?",
            value=st.session_state.pro_a,
            key="pro_a_area", height=150
        )
        st.session_state.pro_b = st.text_area(
            f"Was spricht für Option B: '{st.session_state.options[1]}'?",
            value=st.session_state.pro_b,
            key="pro_b_area", height=150
        )
    
    with st.container():
        st.markdown(f"#### Nachteile (Der 'Schwarze Hut' von Edward de Bono)")
        st.session_state.contra_a = st.text_area(
            f"Was spricht gegen Option A: '{st.session_state.options[0]}'?",
            value=st.session_state.contra_a,
            key="contra_a_area", height=150
        )
        st.session_state.contra_b = st.text_area(
            f"Was spricht gegen Option B: '{st.session_state.options[1]}'?",
            value=st.session_state.contra_b,
            key="contra_b_area", height=150
        )
        
    # The Green Hat
    with st.container():
        st.markdown("#### Kreative Optionen (Der 'Grüne Hut' von Edward de Bono)")
        st.markdown("Gibt es noch andere, unkonventionelle Optionen, die du bisher nicht in Betracht gezogen hast? Schreibe sie hier auf.")
        st.session_state.creative_options = st.text_area(
            "Andere Ideen:",
            value=st.session_state.creative_options,
            key="creative_options_area", height=150
        )

    # Regret Minimization Framework
    with st.container():
        st.markdown(f"#### Zukunftsszenario (nach Jeff Bezos)")
        st.markdown("Stelle dir vor, du bist 80 Jahre alt. Welche Entscheidung würdest du am meisten bereuen? Das Regret Minimization Framework hilft dir, aus einer langfristigen Perspektive zu entscheiden.")
        st.session_state.future_scenario_a = st.text_area(
            f"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option A entscheidest?",
            value=st.session_state.future_scenario_a,
            key="scenario_a", height=200
        )
        st.session_state.future_scenario_b = st.text_area(
            f"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option B entscheidest?",
            value=st.session_state.future_scenario_b,
            key="scenario_b", height=200
        )

    if st.button("Weiter"):
        next_page('step_5')

def render_step_5():
    st.title("Step 5: Zusammenfassung")
    
    with st.container():
        st.markdown("#### Übersicht")
        st.subheader("Deine Entscheidung:")
        st.info(st.session_state.problem)
        st.subheader("Deine Optionen:")
        st.write(f"**Option A:** {st.session_state.options[0]}")
        st.write(f"**Option B:** {st.session_state.options[1]}")

    if st.session_state.selected_values:
        with st.container():
            st.markdown("#### Quantitative Auswertung (nach Werten):")
            data = []
            score_a = 0
            score_b = 0
            for value in st.session_state.selected_values:
                rating_a = st.session_state.values_rating.get(f"{value}_A", 0)
                rating_b = st.session_state.values_rating.get(f"{value}_B", 0)
                score_a += rating_a
                score_b += rating_b
                data.append({
                    "value": value,
                    "option": st.session_state.options[0],
                    "rating": rating_a
                })
                data.append({
                    "value": value,
                    "option": st.session_state.options[1],
                    "rating": rating_b
                })
            
            df = pd.DataFrame(data)
            if not df.empty:
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('value', title='Werte'),
                    y=alt.Y('rating', title='Bewertung (1-10)'),
                    color=alt.Color('option', legend=alt.Legend(title="Option")),
                    column=alt.Column('option', header=alt.Header(titleOrient="bottom"))
                ).properties(
                    title="Werte-Bewertung im Vergleich"
                )
                
                cols = st.columns([4, 4, 4, 4, 4, 4, 4],width=4000)
                with cols[0]:
                    st.altair_chart(chart, use_container_width=True)         
                
                # Display the total score
                st.write(f"**Gesamtpunktzahl Option A:** {score_a}")
                st.write(f"**Gesamtpunktzahl Option B:** {score_b}")


    with st.container():
        st.markdown("#### Deine Gedanken & Szenarien:")
        st.write(f"**Vorteile für {st.session_state.options[0]}:**")
        st.write(st.session_state.pro_a)
        st.write(f"**Nachteile für {st.session_state.options[0]}:**")
        st.write(st.session_state.contra_a)
        st.write(f"**Vorteile für {st.session_state.options[1]}:**")
        st.write(st.session_state.pro_b)
        st.write(f"**Nachteile für {st.session_state.options[1]}:**")
        st.write(st.session_state.contra_b)
        st.write(f"**Zukunftsszenario {st.session_state.options[0]}:**")
        st.write(st.session_state.future_scenario_a)
        st.write(f"**Zukunftsszenario {st.session_state.options[1]}:**")
        st.write(st.session_state.future_scenario_b)

        if st.session_state.creative_options:
            st.markdown("#### Weitere Ideen (Der 'Grüne Hut')")
            st.write(st.session_state.creative_options)
    
    with st.container():
        st.markdown("#### Dein erster konkreter Schritt (Der 'Blaue Hut' & SMART-Ziele)")
        st.markdown("""
        Dieser Hut hilft dir, den Prozess zu planen. Um deinen ersten Schritt umsetzbar zu machen, nutze die **SMART-Methode**:
        - **S**pezifisch: Was genau willst du tun?
        - **M**essbar: Woran erkennst du, dass du dein Ziel erreicht hast?
        - **A**ttraktiv: Warum ist dir das Ziel wichtig?
        - **R**ealistisch: Ist das Ziel erreichbar?
        - **T**erminiert: Bis wann willst du es umsetzen?
        """)
        st.session_state.first_step = st.text_input(
            "Dein erster konkreter SMART-Schritt:",
            value=st.session_state.first_step
        )
        if st.button("Entscheidung abschließen"):
            st.success("🎉 Deine Entscheidungsreise wurde abgeschlossen!")

    st.button("Neue Entscheidungsreise starten", on_click=reset_app)


def render_bottom_nav():
    # Render a fixed bottom navigation bar using HTML and CSS
    # Check if a tab is active in the query parameters
    current_tab = st.query_params.get('tab', ['questionnaire'])[0]
    
    # Check if a page is active in the query parameters
    current_page = st.query_params.get('page', ['start'])[0]

    nav_html = f"""
    <div class="bottom-nav">
        <a href="?page=start" class="nav-item {'active' if current_page == 'start' else ''}">
            <span class="icon">🏠</span> Home
        </a>
        <a href="?page=step_1" class="nav-item {'active' if current_page in ['step_1', 'step_2', 'step_3', 'step_4', 'step_5'] else ''}">
            <span class="icon">🧠</span> Entscheiden
        </a>
        <a href="?page=wert_reflexion&tab=questionnaire" class="nav-item {'active' if current_page == 'wert_reflexion' and current_tab == 'questionnaire' else ''}">
            <span class="icon">💡</span> Resilienz
        </a>
        <a href="?page=wert_reflexion&tab=paths" class="nav-item {'active' if current_page == 'wert_reflexion' and current_tab == 'paths' else ''}">
            <span class="icon">🧘</span> Pfade
        </a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

def main():
    query_params = st.query_params
    
    # Determine the current page from query parameters, default to 'start'
    page = query_params.get('page', ['start'])[0]
    st.session_state.page = page

    if st.session_state.page == 'start':
        render_start_page()
    elif st.session_state.page == 'step_1':
        render_step_1()
    elif st.session_state.page == 'step_2':
        render_step_2()
    elif st.session_state.page == 'step_3':
        render_step_3()
    elif st.session_state.page == 'step_4':
        render_step_4()
    elif st.session_state.page == 'step_5':
        render_step_5()
    elif st.session_state.page == 'wert_reflexion':
        render_wert_reflexion_page()
    
    # The bottom navigation bar is displayed on all pages except the start page
    if st.session_state.page not in ['start']:
        render_bottom_nav()

main()
