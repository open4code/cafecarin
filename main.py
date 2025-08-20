import streamlit as st
import altair as alt
import pandas as pd
import json

# --- 1. SEITENKONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Decision Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Das CSS wurde komplett neu geschrieben, um das Layout aus dem Bild zu replizieren
custom_css = """
<style>
    /* Allgemeine Farbpalette und Schriftart */
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

    /* Styling für alle Container und Expander (die "Karten") */
    div[data-testid="stVerticalBlock"] > div.st-emotion-cache-1r6y9j9,
    div[data-testid="stVerticalBlock"] > div.st-emotion-cache-1n1p067 {
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

    /* Styling für Überschriften */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
        font-weight: 600;
    }
    h1 {
        color: var(--primary-color);
        font-size: 2.5rem;
    }

    /* Styling für Buttons */
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

    /* Spezielles Styling für Textbereiche und Eingabefelder (Farbhintergrund) */
    .st-emotion-cache-13gs647, .st-emotion-cache-1cpx9g8, .st-emotion-cache-13v2p5x, .st-emotion-cache-1l006n6 {
        background-color: var(--secondary-color) !important;
        color: var(--text-color);
        border-radius: 12px;
        border: none;
        padding: 10px;
    }

    /* Styling für Schieberegler (Slider) */
    .st-emotion-cache-14u43s4 {
        background-color: var(--secondary-color);
        border-radius: 10px;
        height: 10px;
    }
    .st-emotion-cache-14u43s4 > div {
        background-color: var(--primary-color);
    }

    /* Styling für die untere Navigationsleiste */
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 2. ZUSTAND DER APP VERWALTEN (SESSION STATE) ---
def init_session_state():
    if 'page' not in st.session_state: st.session_state.page = 'start'
    if 'problem' not in st.session_state: st.session_state.problem = ""
    if 'problem_category' not in st.session_state: st.session_state.problem_category = "Wähle eine Kategorie"
    if 'options' not in st.session_state: st.session_state.options = ["", ""]
    # Die Liste der ausgewählten Werte muss beim initialen Laden leer sein
    if 'selected_values' not in st.session_state: st.session_state.selected_values = []
    if 'values_rating' not in st.session_state: st.session_state.values_rating = {}
    if 'emotions' not in st.session_state: st.session_state.emotions = ""
    if 'pro_a' not in st.session_state: st.session_state.pro_a = ""
    if 'contra_a' not in st.session_state: st.session_state.contra_a = ""
    if 'pro_b' not in st.session_state: st.session_state.pro_b = ""
    if 'contra_b' not in st.session_state: st.session_state.contra_b = ""
    # Neues Feld für kreative Optionen
    if 'creative_options' not in st.session_state: st.session_state.creative_options = ""
    if 'future_scenario_a' not in st.session_state: st.session_state.future_scenario_a = ""
    if 'future_scenario_b' not in st.session_state: st.session_state.future_scenario_b = ""
    if 'first_step' not in st.session_state: st.session_state.first_step = ""

init_session_state()

def next_page(page_name):
    st.session_state.page = page_name

def reset_app():
    st.session_state.clear()
    init_session_state()

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
    },
    "Persönliches Wachstum": {
        "values": ["Selbstverwirklichung", "Kreativität", "Lernen", "Soziale Bindungen", "Entwicklung", "Freiheit"],
        "cognitive_biases": {
            "title": "Häufige Denkfehler bei persönlichem Wachstum",
            "biases": [
                ("Status-quo-Verzerrung", "Ziehe ich die einfache Option vor, weil ich Angst vor Veränderungen habe, auch wenn die neue Option mich wachsen lässt?"),
                ("Bestätigungsfehler", "Suche ich nur nach Informationen, die meine Überzeugung bestätigen, dass eine neue Fähigkeit zu schwer zu erlernen ist?"),
                ("Verfügbarkeitsheuristik", "Stütze ich meine Entscheidung nur auf leicht verfügbare, spektakuläre Geschichten, statt auf realistischere Fakten?")
            ]
        },
    },
    "Beziehungen & Familie": {
        "values": ["Soziale Bindungen", "Harmonie", "Vertrauen", "Empathie", "Stabilität", "Zugehörigkeit"],
        "cognitive_biases": {
            "title": "Häufige Denkfehler in Beziehungen",
            "biases": [
                ("Rosinenpicken (Cherry Picking)", "Ignoriere ich alle negativen Aspekte und konzentriere ich mich nur auf die guten, um eine schwierige Situation zu vermeiden?"),
                ("Irrglaube an versunkene Kosten (Sunk Cost Fallacy)", "Bleibe ich in einer Beziehung oder Situation, nur weil ich schon so viel Zeit und Energie investiert habe, anstatt nach vorne zu schauen?"),
                ("Bestätigungsfehler", "Höre ich nur auf Freunde, die meine Meinung teilen, und vermeide ich Gespräche, die mich herausfordern?")
            ]
        },
    }
}

# --- 4. SEITEN-INHALT RENDERN ---

def render_start_page():
    # Haupt-Container für die Startseite
    with st.container():
        st.title("Decision Navigator")
        st.image("https://placehold.co/1200x400/FFF8E1/E2B060?text=Deine+Entscheidungsreise")
        st.markdown("Starte deine persönliche Entscheidungsreise. Lass uns deine Gedanken und Gefühle strukturieren, damit du die beste Entscheidung für dich treffen kannst.")
        st.button("Starten", on_click=next_page, args=['step_1'])

def render_step_1():
    st.title("Step 1: Dein Problem & deine Optionen")
    
    # 1. Container für Problem und Kategorie (jetzt an erster Stelle)
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
    
    # 2. Container für die Optionen
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
        st.markdown("Wähle alle Werte aus, die für deine Entscheidung in der Kategorie **'{selected_category}'** relevant sind.")
        
        # Leere die Liste der ausgewählten Werte, bevor die Checkboxen gerendert werden, um den Zustand korrekt zu aktualisieren
        st.session_state.selected_values = []
        cols = st.columns(3) # Erstellt 3 Spalten für die Kontrollkästchen
        for i, value in enumerate(all_values):
            col = cols[i % 3] # Verteilt die Checkboxen auf die Spalten
            if col.checkbox(value, key=f"checkbox_{value}"):
                st.session_state.selected_values.append(value)

    # Die Schieberegler werden nur angezeigt, wenn Werte ausgewählt wurden
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
        # Führe eine abschließende Überprüfung durch
        if not st.session_state.selected_values:
            st.warning("Bitte wähle mindestens einen Wert aus, bevor du fortfährst.")
        else:
            next_page('step_3')
    
def render_step_3():
    st.title("Step 3: Emotionen & Denkfehler")
    with st.container():
        # Der Rote Hut
        st.markdown("#### Dein Bauchgefühl (Der 'Rote Hut' von Edward de Bono)")
        st.markdown("Schreibe auf, welche Gefühle und intuitiven Gedanken du zu den Optionen hast. Es geht nicht um Logik, sondern um Emotionen.")
        st.session_state.emotions = st.text_area("Deine Gedanken:", value=st.session_state.emotions, height=150)
    
    selected_content = category_content.get(st.session_state.problem_category, {})
    biases = selected_content.get("cognitive_biases", {}).get("biases", [])
    
    if biases:
        with st.container():
            st.markdown("#### Reflektiere über Denkfehler")
            for bias_title, bias_question in biases:
                with st.expander(f"**{bias_title}**"):
                    st.markdown(bias_question)

    # Die "Weiter" Schaltfläche wurde hierher verschoben, um erst nach den Expandern zu erscheinen.
    if st.button("Weiter"):
        next_page('step_4')

def render_step_4():
    st.title("Step 4: Pro/Contra & Zukunft")
    
    # Der Gelbe und Schwarze Hut
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
        
    # Der Grüne Hut
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
                #st.altair_chart(chart, use_container_width=True)
                #trying to make chart narrower
                #cols = st.columns([1, 1, 1, 1, 1, 1, 1])
                cols = st.columns([2, 2, 2, 2, 2, 2, 2],width=800)
                with cols[0]:
                    st.altair_chart(chart, use_container_width=True)                
                
                # Anzeige der Gesamtpunktzahl
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
    nav_html = f"""
    <div class="bottom-nav">
        <a href="?page=start" class="nav-item {'active' if st.session_state.page == 'start' else ''}">
            <span class="icon">🏠</span> Home
        </a>
        <a href="?page=step_1" class="nav-item {'active' if st.session_state.page == 'step_1' else ''}">
            <span class="icon">🧠</span> Decide
        </a>
        <a href="?page=step_5" class="nav-item {'active' if st.session_state.page == 'step_5' else ''}">
            <span class="icon">📊</span> Summary
        </a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

def main():
    query_params = st.query_params
    if 'page' in query_params:
        st.session_state.page = query_params['page'][0]

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
    
    if st.session_state.page != 'start':
        render_bottom_nav()

main()
