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

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")









import streamlit as st

# --- 1. SEITENKONFIGURATION ---
# Konfiguriert die Seite mit Titel, Layout und Icon
st.set_page_config(
    page_title="Decision Navigator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ZUSTAND DER APP VERWALTEN (SESSION STATE) ---
# st.session_state ist entscheidend, um den Zustand der App zu speichern,
# wenn der Nutzer zwischen den Schritten navigiert.
# Wenn 'page' noch nicht existiert, setzen wir den Startwert auf 'start'.
if 'page' not in st.session_state:
    st.session_state.page = 'start'

# Initialisieren der Variablen für alle Schritte der Entscheidungsreise
# (damit sie später nicht mit Fehlern kollidieren)
if 'problem' not in st.session_state: st.session_state.problem = ""
if 'options' not in st.session_state: st.session_state.options = ["", ""]
if 'selected_values' not in st.session_state: st.session_state.selected_values = []
if 'values_rating' not in st.session_state: st.session_state.values_rating = {}
if 'emotions' not in st.session_state: st.session_state.emotions = ""
if 'future_1_year' not in st.session_state: st.session_state.future_1_year = ""
if 'future_3_years' not in st.session_state: st.session_state.future_3_years = ""
if 'future_5_years' not in st.session_state: st.session_state.future_5_years = ""
if 'first_step' not in st.session_state: st.session_state.first_step = ""

# Funktion, um die Seite zu wechseln
def next_page(page_name):
    st.session_state.page = page_name

# --- 3. DIE VERSCHIEDENEN SCHRITTE DER APP RENDERN ---

# Funktion für den Startbildschirm
def render_start_page():
    st.title("Willkommen beim Decision Navigator")
    st.markdown("---")
    st.markdown(
        """
        Hier startest du deine persönliche Entscheidungsreise.
        Lass uns gemeinsam deine Gedanken und Gefühle strukturieren,
        damit du die beste Entscheidung für dich treffen kannst.
        """
    )
    st.button("Starte deine Entscheidungsreise", on_click=next_page, args=['step_1'])

# Funktion für Schritt 1: Problem und Optionen definieren
def render_step_1():
    st.title("Schritt 1: Dein Problem & deine Optionen")
    st.markdown("---")

    st.markdown("### Was ist die Entscheidung, die dich beschäftigt?")
    st.session_state.problem = st.text_area(
        "Formuliere deine Frage so klar wie möglich.",
        value=st.session_state.problem
    )

    st.markdown("### Nenne deine Optionen")
    st.session_state.options[0] = st.text_input(
        "Option A:",
        value=st.session_state.options[0]
    )
    st.session_state.options[1] = st.text_input(
        "Option B:",
        value=st.session_state.options[1]
    )

    # Der Button für den nächsten Schritt
    if st.button("Weiter zur Werte-Analyse", disabled=not (st.session_state.problem and st.session_state.options[0] and st.session_state.options[1])):
        next_page('step_2')
    st.button("Zurück", on_click=next_page, args=['start'])

# Funktion für Schritt 2: Werte- und Motivationsanalyse
def render_step_2():
    st.title("Schritt 2: Deine Werte & Motivation")
    st.markdown("---")
    
    st.markdown("### Wähle deine wichtigsten Werte")
    st.markdown("Wähle aus der Liste, welche Werte für diese Entscheidung relevant sind.")
    
    # Beispiel-Werte
    all_values = ["Sicherheit", "Wachstum", "Kreativität", "Freiheit", "Stabilität", "Einfluss"]
    
    st.session_state.selected_values = st.multiselect(
        "Deine Top-Werte:",
        options=all_values,
        default=st.session_state.selected_values
    )
    
    # Hier werden die Schieberegler für jeden gewählten Wert erstellt
    if st.session_state.selected_values:
        st.markdown("### Bewerte deine Optionen nach diesen Werten")
        st.markdown("Bewerte, wie gut jede Option deine Werte erfüllt (1 = schlecht, 10 = sehr gut).")
        for value in st.session_state.selected_values:
            st.session_state.values_rating[f"{value}_A"] = st.slider(
                f"{st.session_state.options[0]} - {value}", 
                0, 10, st.session_state.values_rating.get(f"{value}_A", 5), key=f"slider_a_{value}"
            )
            st.session_state.values_rating[f"{value}_B"] = st.slider(
                f"{st.session_state.options[1]} - {value}", 
                0, 10, st.session_state.values_rating.get(f"{value}_B", 5), key=f"slider_b_{value}"
            )
            st.markdown("---")

    if st.button("Weiter zur Reflexion"):
        next_page('step_3')
    st.button("Zurück", on_click=next_page, args=['step_1'])

# Funktion für Schritt 3: Emotionen & Denkfehler
def render_step_3():
    st.title("Schritt 3: Emotionen & Denkfehler")
    st.markdown("---")
    
    st.markdown("### Was sagt dein Bauchgefühl?")
    st.markdown("Schreibe auf, welche Gefühle du zu den Optionen hast.")
    st.session_state.emotions = st.text_area(
        "Deine Gedanken und Gefühle:",
        value=st.session_state.emotions
    )
    
    st.markdown("### Reflektiere über Denkfehler")
    st.markdown("Oft beeinflussen uns kognitive Verzerrungen. Frage dich zum Beispiel: Konzentriere ich mich mehr auf das, was ich verlieren könnte (Verlustaversion)?")
    # Hier könntest du weitere Reflexionsfragen hinzufügen
    
    if st.button("Weiter zur Zukunftssimulation"):
        next_page('step_4')
    st.button("Zurück", on_click=next_page, args=['step_2'])

# Funktion für Schritt 4: Zukunftssimulation
def render_step_4():
    st.title("Schritt 4: Zukunftssimulation")
    st.markdown("---")
    
    st.markdown("### Stell dir vor, du hast die Entscheidung getroffen.")
    st.markdown("Wie würde dein Leben in 1, 3 und 5 Jahren aussehen?")
    
    st.markdown(f"#### Wenn du dich für {st.session_state.options[0]} entscheidest:")
    st.session_state.future_1_year = st.text_area("In 1 Jahr...", value=st.session_state.future_1_year, key="future_1_a")
    st.session_state.future_3_years = st.text_area("In 3 Jahren...", value=st.session_state.future_3_years, key="future_3_a")
    st.session_state.future_5_years = st.text_area("In 5 Jahren...", value=st.session_state.future_5_years, key="future_5_a")
    
    # Füge hier die Szenarien für die zweite Option hinzu
    
    if st.button("Weiter zur Zusammenfassung"):
        next_page('step_5')
    st.button("Zurück", on_click=next_page, args=['step_3'])

# Funktion für Schritt 5: Zusammenfassung & erster Handlungsschritt
def render_step_5():
    st.title("Schritt 5: Zusammenfassung & erster Handlungsschritt")
    st.markdown("---")
    
    st.markdown("### Deine Entscheidungsreise ist abgeschlossen.")
    st.markdown("Hier wäre der Ort, um eine visuelle Zusammenfassung deiner Eingaben zu zeigen (Diagramme, Highlights aus den Szenarien etc.).")
    
    st.markdown("### Was ist jetzt dein erster Schritt?")
    st.markdown("Formuliere einen kleinen, konkreten Schritt, den du sofort umsetzen kannst (SMART-Ziel).")
    st.session_state.first_step = st.text_input(
        "Dein erster konkreter Schritt:",
        value=st.session_state.first_step
    )
    
    if st.button("Entscheidung abschließen"):
        st.success("Deine Entscheidungsreise wurde gespeichert!")
        st.balloons()
        st.session_state.page = 'start' # Zurück zum Start
    st.button("Zurück", on_click=next_page, args=['step_4'])

# --- 4. DIE HAUPTLOGIK DER APP ---
# Streamlit rendert basierend auf dem aktuellen Wert von st.session_state.page
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

