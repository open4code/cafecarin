import streamlit as st
import altair as alt
import pandas as pd
import json

# --- 1. SEITENKONFIGURATION & STYLING ---
# Konfiguriert die Seite und lädt das benutzerdefinierte Design
st.set_page_config(
    page_title="Decision Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Benutzerdefiniertes CSS für die Farbpalette und das Design
custom_css = """
<style>
    :root {
        --primary-color: #E2B060;   /* Ein helles Orange/Beige für Buttons */
        --secondary-color: #F8D8C9; /* Ein leichtes Rosé als Akzent */
        --background-color: #FFF8E1; /* Ein helles Beige für den Hintergrund */
        --text-color: #4A4A4A;
        --container-bg: #FFFFFF;
    }

    body {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .stApp {
        background-color: var(--background-color);
    }

    /* Styling für Überschriften */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color);
    }
    
    /* Styling für Haupt-Container und Expander */
    .css-1jc7r36, .css-1yjc820 {
        background-color: var(--container-bg) !important;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .st-emotion-cache-1r6y9j9, .st-emotion-cache-1n1p067 {
        background-color: var(--container-bg) !important;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .st-emotion-cache-1jm692n {
        background-color: transparent;
        padding: 0;
    }
    .st-emotion-cache-1j0r921 {
        background-color: transparent;
        padding: 0;
    }

    /* Styling für Buttons */
    .st-emotion-cache-1g8w4t4 {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Styling für Textbereiche und Eingabefelder */
    .st-emotion-cache-13gs647, .st-emotion-cache-1cpx9g8 {
        background-color: var(--secondary-color) !important;
        color: var(--text-color);
        border-radius: 10px;
        border: 1px solid var(--primary-color);
    }

    /* Styling für Schieberegler (Slider) */
    .stSlider > div > div > div:first-child {
        background-color: var(--primary-color);
    }
    .stSlider > div > div > div > div {
        background-color: var(--primary-color);
    }
    .stSlider > div > div > div {
        background-color: var(--secondary-color);
        border-radius: 5px;
    }
    .stSlider > div > div > div:first-child {
        background-color: var(--primary-color);
    }

    /* Styling für Checkboxen/Multiselect */
    .st-emotion-cache-1b4z83b {
        color: var(--primary-color);
    }
    .st-emotion-cache-79elbk {
        color: var(--primary-color);
    }

    /* Feedback-Sterne */
    .st-emotion-cache-t221l2 {
        color: var(--primary-color);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 2. ZUSTAND DER APP VERWALTEN (SESSION STATE) ---
if 'page' not in st.session_state:
    st.session_state.page = 'start'

# Initialisieren aller Variablen
if 'problem' not in st.session_state: st.session_state.problem = ""
if 'problem_category' not in st.session_state: st.session_state.problem_category = ""
if 'options' not in st.session_state: st.session_state.options = ["", ""]
if 'selected_values' not in st.session_state: st.session_state.selected_values = []
if 'values_rating' not in st.session_state: st.session_state.values_rating = {}
if 'emotions' not in st.session_state: st.session_state.emotions = ""
if 'pro_contra_a' not in st.session_state: st.session_state.pro_contra_a = ""
if 'pro_contra_b' not in st.session_state: st.session_state.pro_contra_b = ""
if 'future_scenario_a' not in st.session_state: st.session_state.future_scenario_a = ""
if 'future_scenario_b' not in st.session_state: st.session_state.future_scenario_b = ""
if 'first_step' not in st.session_state: st.session_state.first_step = ""
if 'eisenhower_a' not in st.session_state: st.session_state.eisenhower_a = {}
if 'eisenhower_b' not in st.session_state: st.session_state.eisenhower_b = {}


# Funktion, um die Seite zu wechseln
def next_page(page_name):
    st.session_state.page = page_name

# --- 3. DYNAMISCHE INHALTE FÜR JEDE KATEGORIE ---
category_content = {
    "Karriere & Beruf": {
        "values": ["Finanzielle Sicherheit", "Wachstum", "Autonomie", "Einfluss", "Anerkennung", "Work-Life-Balance"],
        "cognitive_biases": {
            "title": "Häufige Denkfehler in der Karriere",
            "biases": [
                ("Verlustaversion", "Konzentriere ich mich mehr auf das, was ich im aktuellen Job verlieren könnte, als auf das, was ich im neuen gewinnen könnte?"),
                ("Ankereffekt", "Hänge ich zu sehr am ersten Gehaltsangebot oder einer ersten Beförderung fest, die ich erhalten habe, und hindert mich das daran, eine bessere Gelegenheit zu erkennen?"),
                ("Bestätigungsfehler", "Suche ich nur nach Informationen, die meine Entscheidung für oder gegen einen Job bestätigen, und ignoriere ich gegenteilige Informationen?")
            ]
        },
        "step_title": "Pro & Contra für Karriere-Entscheidungen",
    },
    "Persönliches Wachstum": {
        "values": ["Selbstverwirklichung", "Finanzielle Stabilität", "Sicherheit", "Kreativität", "Autonomie", "Soziale Bindungen", "Entwicklung", "Anerkennung", "Freiheit"],
        "cognitive_biases": {
            "title": "Häufige Denkfehler bei persönlichem Wachstum",
            "biases": [
                ("Status-quo-Verzerrung", "Ziehe ich die einfache Option vor, weil ich Angst vor Veränderungen habe, auch wenn die neue Option mich wachsen lässt?"),
                ("Bestätigungsfehler", "Suche ich nur nach Informationen, die meine Überzeugung bestätigen, dass eine neue Fähigkeit zu schwer zu erlernen ist?"),
                ("Verfügbarkeitsheuristik", "Stütze ich meine Entscheidung nur auf leicht verfügbare, spektakuläre Geschichten, statt auf realistischere Fakten?")
            ]
        },
        "step_title": "Pro & Contra für Persönliches Wachstum",
    },
    "Beziehungen & Familie": {
        "values": ["Soziale Bindungen", "Harmonie", "Vertrauen", "Empathie", "Stabilität", "Zugehörigkeit"],
        "cognitive_biases": {
            "title": "Häufige Denkfehler in Beziehungen",
            "biases": [
                ("Rosinenpicken (Cherry Picking)", "Ignoriere ich alle negativen Aspekte und konzentriere mich nur auf die guten, um eine schwierige Situation zu vermeiden?"),
                ("Irrglaube an versunkene Kosten (Sunk Cost Fallacy)", "Bleibe ich in einer Beziehung oder Situation, nur weil ich schon so viel Zeit und Energie investiert habe, anstatt nach vorne zu schauen?"),
                ("Bestätigungsfehler", "Höre ich nur auf Freunde, die meine Meinung teilen, und vermeide ich Gespräche, die mich herausfordern?")
            ]
        },
        "step_title": "Pro & Contra für Beziehungs-Entscheidungen",
    }
}

# --- 4. DIE VERSCHIEDENEN SCHRITTE DER APP RENDERN ---

# Startseite
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
    st.image("https://placehold.co/1200x400/FFF8E1/E2B060?text=Ein+interaktives+Tool+von+CafeCarin")

# Schritt 1: Problem und Optionen definieren
def render_step_1():
    st.title("Schritt 1: Dein Problem & deine Optionen")
    st.markdown("---")
    
    st.markdown("### Was ist die Entscheidung, die dich beschäftigt?")
    st.session_state.problem = st.text_area(
        "Formuliere deine Frage so klar wie möglich.",
        value=st.session_state.problem,
        key="problem_input"
    )
    
    st.markdown("### Wähle eine Problemkategorie")
    st.markdown("Die Kategorie hilft uns, die passenden psychologischen Modelle für deine Situation auszuwählen.")
    st.session_state.problem_category = st.selectbox(
        "Kategorie:",
        options=["Wähle eine Kategorie"] + list(category_content.keys()),
        index=0 if st.session_state.problem_category == "" else list(category_content.keys()).index(st.session_state.problem_category) + 1
    )

    st.markdown("### ➡️ Nenne deine Optionen")
    st.session_state.options[0] = st.text_input(
        "Option A:",
        value=st.session_state.options[0],
        key="option_a_input"
    )
    st.session_state.options[1] = st.text_input(
        "Option B:",
        value=st.session_state.options[1],
        key="option_b_input"
    )

    is_valid = st.session_state.problem and st.session_state.options[0] and st.session_state.options[1] and st.session_state.problem_category != "Wähle eine Kategorie"
    if st.button("Weiter zur Werte-Analyse", disabled=not is_valid):
        next_page('step_2')
    st.button("Zurück zur Startseite", on_click=next_page, args=['start'])

# Schritt 2: Werte- und Motivationsanalyse
def render_step_2():
    st.title("Schritt 2: Werte & Motivation")
    st.markdown("---")
    
    selected_category = st.session_state.problem_category
    all_values = category_content.get(selected_category, {}).get("values", ["Sicherheit", "Freiheit", "Entwicklung"])
    
    st.markdown("### Wähle deine wichtigsten Werte")
    st.markdown(f"""
    Wähle die Werte, die für deine Entscheidung in der Kategorie **"{selected_category}"** relevant sind.
    """)
    
    st.session_state.selected_values = st.multiselect(
        "Deine Top-Werte:",
        options=all_values,
        default=st.session_state.selected_values
    )
    
    if st.session_state.selected_values:
        st.markdown("### Bewerte deine Optionen nach diesen Werten")
        st.markdown("Bewerte auf einer Skala von 1 bis 10, wie gut jede Option deine gewählten Werte erfüllt.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Option A: {st.session_state.options[0]}")
            for value in st.session_state.selected_values:
                st.session_state.values_rating[f"{value}_A"] = st.slider(
                    f"**{value}**", 
                    0, 10, st.session_state.values_rating.get(f"{value}_A", 5), key=f"slider_a_{value}"
                )
        with col2:
            st.subheader(f"Option B: {st.session_state.options[1]}")
            for value in st.session_state.selected_values:
                st.session_state.values_rating[f"{value}_B"] = st.slider(
                    f"**{value}**", 
                    0, 10, st.session_state.values_rating.get(f"{value}_B", 5), key=f"slider_b_{value}"
                )
        
    if st.button("Weiter zur Reflexion"):
        next_page('step_3')
    st.button("Zurück", on_click=next_page, args=['step_1'])

# Schritt 3: Emotionen & Denkfehler
def render_step_3():
    st.title("Schritt 3: Emotionen & Denkfehler")
    st.markdown("---")
    
    st.markdown("### Was sagt dein Bauchgefühl?")
    st.markdown("Schreibe auf, welche Gefühle und intuitiven Gedanken du zu den Optionen hast.")
    st.session_state.emotions = st.text_area(
        "Deine Gedanken und Gefühle:",
        value=st.session_state.emotions
    )
    
    st.markdown("---")
    st.markdown("### Reflektiere über deine Denkfehler")
    st.markdown("""
    Sogenannte **kognitive Verzerrungen** sind systematische Fehler im Denken, die uns von einer rationalen Entscheidung abhalten können.
    
    **Frage dich, ob folgende Denkfehler deine Entscheidung beeinflussen könnten:**
    """)
    
    selected_content = category_content.get(st.session_state.problem_category, {})
    biases = selected_content.get("cognitive_biases", {}).get("biases", [])
    
    for bias_title, bias_question in biases:
        with st.expander(f"**{bias_title}**"):
            st.markdown(bias_question)

    if st.button("Weiter zur Eisenhower-Matrix"):
        next_page('step_4')
    st.button("Zurück", on_click=next_page, args=['step_2'])

# Schritt 4: Eisenhower-Matrix
def render_step_4():
    st.title("Schritt 4: Die Eisenhower-Matrix")
    st.markdown("---")
    st.markdown("### ⏰ Bewerte Dringlichkeit & Wichtigkeit")
    st.markdown("""
    Die **Eisenhower-Matrix** hilft dir, die Prioritäten deiner Optionen zu klären. 
    Bewerte jede Option nach ihrer **Wichtigkeit** (Wie sehr trägt sie zu deinen langfristigen Zielen bei?) und **Dringlichkeit** (Wie schnell muss eine Entscheidung getroffen werden?).
    """)
    
    # Sicherstellen, dass die Session-Zustände initialisiert sind
    if 'eisenhower_a_wichtig' not in st.session_state.eisenhower_a: st.session_state.eisenhower_a['wichtig'] = False
    if 'eisenhower_a_dringend' not in st.session_state.eisenhower_a: st.session_state.eisenhower_a['dringend'] = False
    if 'eisenhower_b_wichtig' not in st.session_state.eisenhower_b: st.session_state.eisenhower_b['wichtig'] = False
    if 'eisenhower_b_dringend' not in st.session_state.eisenhower_b: st.session_state.eisenhower_b['dringend'] = False

    st.subheader(f"Option A: {st.session_state.options[0]}")
    st.session_state.eisenhower_a['wichtig'] = st.checkbox("Wichtig", value=st.session_state.eisenhower_a['wichtig'], key="eisenhower_a_wichtig")
    st.session_state.eisenhower_a['dringend'] = st.checkbox("Dringend", value=st.session_state.eisenhower_a['dringend'], key="eisenhower_a_dringend")
    
    st.subheader(f"Option B: {st.session_state.options[1]}")
    st.session_state.eisenhower_b['wichtig'] = st.checkbox("Wichtig", value=st.session_state.eisenhower_b['wichtig'], key="eisenhower_b_wichtig")
    st.session_state.eisenhower_b['dringend'] = st.checkbox("Dringend", value=st.session_state.eisenhower_b['dringend'], key="eisenhower_b_dringend")

    if st.button("Weiter zur Pro & Contra Simulation"):
        next_page('step_5')
    st.button("Zurück", on_click=next_page, args=['step_3'])

# Schritt 5: Pro & Contra und Zukunftssimulation
def render_step_5():
    st.title("Schritt 5: Pro & Contra und Zukunftsszenario")
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
        next_page('step_6')
    st.button("Zurück", on_click=next_page, args=['step_4'])


    

    # --- Die Zusammenfassung unserer App ---
    st.markdown("---")
    st.markdown("## Übersicht deiner Entscheidungsreise")
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
                color=alt.Color('option', legend=alt.Legend(title="Option")),
                column=alt.Column('option', header=alt.Header(titleOrient="bottom"))
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
    
    st.markdown("---")

    st.markdown("### Dein erster konkreter Schritt")
    st.markdown("""
    Formuliere einen kleinen, konkreten Schritt, den du sofort umsetzen kannst. Ein guter Ansatz hierfür ist die **SMART-Methode**:
    * **S - Spezifisch:** Was genau möchtest du tun? Wer ist beteiligt? Wo findet es statt?
    * **M - Messbar:** Woran erkennst du, dass du dein Ziel erreicht hast? (Z. B. "Ich habe 3 Angebote eingeholt.")
    * **A - Attraktiv:** Ist der Schritt für dich motivierend und lohnenswert?
    * **R - Realistisch:** Ist der Schritt machbar und passt er zu deinen Ressourcen (Zeit, Geld, Fähigkeiten)?
    * **T - Terminiert:** Bis wann möchtest du diesen Schritt abgeschlossen haben?
    """)
    st.session_state.first_step = st.text_input(
        "Dein erster konkreter SMART-Schritt:",
        value=st.session_state.first_step
    )
    
    if st.button("Entscheidung abschließen"):
        st.success("Deine Entscheidungsreise ist abgeschlossen!")
       
        
    
    if st.button("Neue Entscheidungsreise starten", on_click=next_page, args=['start']):
        # Zurück zum Start und alle Variablen zurücksetzen
        st.session_state.clear()
        st.session_state.page = 'start'


# --- 5. DIE HAUPTLOGIK DER APP ---
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
elif st.session_state.page == 'step_6':
    render_step_6()
