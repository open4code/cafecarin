import streamlit as st
import altair as alt
import pandas as pd

# --- 1. SEITENKONFIGURATION ---
# Konfiguriert die Seite mit Titel, Layout und Icon
# Übernimmt das "wide" Layout aus deinem Beispiel
st.set_page_config(
    page_title="Decision Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ZUSTAND DER APP VERWALTEN (SESSION STATE) ---
# st.session_state ist entscheidend, um den Zustand der App zu speichern,
# wenn der Nutzer zwischen den Schritten navigiert.
# Wenn 'page' noch nicht existiert, setzen wir den Startwert auf 'start'.
if 'page' not in st.session_state:
    st.session_state.page = 'start'

# Initialisieren der Variablen für alle Schritte der Entscheidungsreise
# (damit sie später nicht mit Fehlern kollidieren und leere Werte haben)
if 'problem' not in st.session_state: st.session_state.problem = ""
if 'options' not in st.session_state: st.session_state.options = ["", ""]
if 'selected_values' not in st.session_state: st.session_state.selected_values = []
if 'values_rating' not in st.session_state: st.session_state.values_rating = {}
if 'emotions' not in st.session_state: st.session_state.emotions = ""
if 'pro_contra_a' not in st.session_state: st.session_state.pro_contra_a = ""
if 'pro_contra_b' not in st.session_state: st.session_state.pro_contra_b = ""
if 'future_scenario_a' not in st.session_state: st.session_state.future_scenario_a = ""
if 'future_scenario_b' not in st.session_state: st.session_state.future_scenario_b = ""
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
    all_values = ["Sicherheit", "Finanzielle Absicherung", "Wachstum und Selbstverwirklichung", "Kreativität", "Freiheit", "Stabilität", "Einfluss"]
    
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
                f"Wie gut erfüllt '{st.session_state.options[0]}' den Wert '{value}'?", 
                0, 10, st.session_state.values_rating.get(f"{value}_A", 5), key=f"slider_a_{value}"
            )
            st.session_state.values_rating[f"{value}_B"] = st.slider(
                f"Wie gut erfüllt '{st.session_state.options[1]}' den Wert '{value}'?", 
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
    
    if st.button("Weiter zur Pro & Contra Simulation"):
        next_page('step_4')
    st.button("Zurück", on_click=next_page, args=['step_2'])

# Funktion für Schritt 4: Pro & Contra und Zukunftssimulation
def render_step_4():
    st.title("Schritt 4: Pro & Contra und Zukunftsszenario")
    st.markdown("---")
    
    st.markdown(f"### Pro- & Contra-Liste für '{st.session_state.options[0]}'")
    st.session_state.pro_contra_a = st.text_area(
        "Liste deine Gedanken auf:",
        value=st.session_state.pro_contra_a,
        key="pro_contra_a_area"
    )

    st.markdown(f"### Pro- & Contra-Liste für '{st.session_state.options[1]}'")
    st.session_state.pro_contra_b = st.text_area(
        "Liste deine Gedanken auf:",
        value=st.session_state.pro_contra_b,
        key="pro_contra_b_area"
    )
    
    st.markdown("### Die 1, 3, 5-Jahres-Simulation")
    st.markdown(f"Stell dir vor, du hast die Entscheidung für **{st.session_state.options[0]}** getroffen.")
    st.session_state.future_scenario_a = st.text_area(
        "Beschreibe, wie dein Leben in 1, 3 und 5 Jahren aussieht:",
        value=st.session_state.future_scenario_a,
        key="scenario_a"
    )
    
    st.markdown(f"Stell dir nun vor, du hast dich für **{st.session_state.options[1]}** entschieden.")
    st.session_state.future_scenario_b = st.text_area(
        "Beschreibe, wie dein Leben in 1, 3 und 5 Jahren aussieht:",
        value=st.session_state.future_scenario_b,
        key="scenario_b"
    )

    if st.button("Weiter zur Zusammenfassung"):
        next_page('step_5')
    st.button("Zurück", on_click=next_page, args=['step_3'])


# Funktion für Schritt 5: Zusammenfassung & erster Handlungsschritt
def render_step_5():
    # Dein originaler Code-Abschnitt
    st.title("Interaktives Tool mit CafeCarin, um die Welt zu verbessern")
    st.write("""
    Lasst uns gemeinsam die Welt verbessern.
    """)

    st.markdown("---")
    st.markdown(
    """
    **Anleitung:**
    1. Teste die Streamlit Features im Playground https://streamlit.io/playground
    2. Check die Docs mit mache dich mit den Streamlit Möglichkeiten vertraut https://docs.streamlit.io
    3. Erweitere diesen Code auf Github, und teste die Änderungen auf https://cafecarin-0815.streamlit.app
    """
    )
    
    if st.button("Send balloons!"):
        st.balloons()

    # --- Die Zusammenfassung unserer App ---
    st.markdown("---")
    st.markdown("## Deine Entscheidungs-Zusammenfassung")
    st.markdown("### 📝 Übersicht deiner Entscheidungsreise")
    st.subheader("Deine Entscheidung:")
    st.info(st.session_state.problem)

    st.subheader("Deine Optionen:")
    st.write(f"**Option A:** {st.session_state.options[0]}")
    st.write(f"**Option B:** {st.session_state.options[1]}")

    if st.session_state.selected_values:
        st.subheader("Deine Werte-Bewertung:")
        data = []
        for value in st.session_state.selected_values:
            data.append({
                "value": value,
                "option": st.session_state.options[0],
                "rating": st.session_state.values_rating.get(f"{value}_A", 0)
            })
            data.append({
                "value": value,
                "option": st.session_state.options[1],
                "rating": st.session_state.values_rating.get(f"{value}_B", 0)
            })
        
        df = pd.DataFrame(data)

        if not df.empty:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('value', title='Werte'),
                y=alt.Y('rating', title='Bewertung (1-10)'),
                color='option',
                column='option'
            ).properties(
                title="Werte-Bewertung im Vergleich"
            )
            st.altair_chart(chart, use_container_width=True)

    st.subheader("Deine Gedanken & Szenarien:")
    st.markdown(f"**Pro & Contra für {st.session_state.options[0]}:**")
    st.write(st.session_state.pro_contra_a)
    st.markdown(f"**Pro & Contra für {st.session_state.options[1]}:**")
    st.write(st.session_state.pro_contra_b)
    st.markdown(f"**Zukunftsszenario {st.session_state.options[0]}:**")
    st.write(st.session_state.future_scenario_a)
    st.markdown(f"**Zukunftsszenario {st.session_state.options[1]}:**")
    st.write(st.session_state.future_scenario_b)


    st.markdown("### Was ist jetzt dein erster Schritt?")
    st.markdown("Formuliere einen kleinen, konkreten Schritt, den du sofort umsetzen kannst (SMART-Ziel).")
    st.session_state.first_step = st.text_input(
        "Dein erster konkreter Schritt:",
        value=st.session_state.first_step
    )
    
    if st.button("Entscheidung abschließen"):
        st.success("🎉 Deine Entscheidungsreise wurde abgeschlossen!")
        st.balloons()

    st.write("Ihre Carolin")
    
    # Dein originaler Feedback-Abschnitt
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
    
    if st.button("Neue Entscheidungsreise starten", on_click=next_page, args=['start']):
        # Zurück zum Start und alle Variablen zurücksetzen
        st.session_state.clear()
        st.session_state.page = 'start'


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
