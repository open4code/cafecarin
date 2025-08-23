import streamlit as st
import altair as alt
import pandas as pd
import time
import uuid

# Initialisiert den Streamlit-Session-Zustand, um Daten über die Seiten hinweg zu speichern.
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'step_1'
if 'page' not in st.session_state:
    st.session_state.page = 'start'
if 'problem' not in st.session_state:
    st.session_state.problem = ""
if 'problem_category' not in st.session_state:
    st.session_state.problem_category = "Wähle eine Kategorie"
if 'options' not in st.session_state:
    st.session_state.options = ["", ""]
if 'selected_values' not in st.session_state:
    st.session_state.selected_values = []
if 'values_rating' not in st.session_state:
    st.session_state.values_rating = {}
if 'emotions' not in st.session_state:
    st.session_state.emotions = ""
if 'pro_a' not in st.session_state:
    st.session_state.pro_a = ""
if 'contra_a' not in st.session_state:
    st.session_state.contra_a = ""
if 'pro_b' not in st.session_state:
    st.session_state.pro_b = ""
if 'contra_b' not in st.session_state:
    st.session_state.contra_b = ""
if 'creative_options' not in st.session_state:
    st.session_state.creative_options = ""
if 'future_scenario_a' not in st.session_state:
    st.session_state.future_scenario_a = ""
if 'future_scenario_b' not in st.session_state:
    st.session_state.future_scenario_b = ""
if 'first_step' not in st.session_state:
    st.session_state.first_step = ""
if 'resilience_answers' not in st.session_state:
    st.session_state.resilience_answers = {}
if 'resilience_score' not in st.session_state:
    st.session_state.resilience_score = None
if 'resilience_analysis' not in st.session_state:
    st.session_state.resilience_analysis = ""
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'current_path' not in st.session_state:
    st.session_state.current_path = None
if 'health_challenges' not in st.session_state:
    st.session_state.health_challenges = {
        'Stressabbau': 0, 'Selbstbild stärken': 0,
        'Selbstwirksamkeitserwartung': 0, 'Verbundenheit': 0, 'Konfliktlösung': 0
    }
if 'unlocked_trophies' not in st.session_state:
    st.session_state.unlocked_trophies = []
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'show_special_thing' not in st.session_state:
    st.session_state.show_special_thing = False

# Annahme: Diese Daten existieren bereits in Ihrer App.
# Hier werden sie zur Demonstration hart kodiert.
category_content = {
    "Beruf & Karriere": {
        "values": ["Karrierewachstum", "Einkommen", "Work-Life-Balance"],
        "cognitive_biases": {
            "biases": [
                ("Bestätigungsfehler", "Suchen Sie nur nach Informationen, die Ihre bevorzugte Option bestätigen?"),
                ("Verlust-Aversion", "Wie stark beeinflusst die Angst, etwas zu verlieren, Ihre Entscheidung?")
            ]
        }
    },
    "Beziehungen": {
        "values": ["Vertrauen", "Kommunikation", "Unabhängigkeit"],
        "cognitive_biases": {
            "biases": [
                ("Ankereffekt", "Lassen Sie sich von einer ursprünglichen Idee oder einem Gefühl beeinflussen, das Sie haben?")
            ]
        }
    },
    "Finanzen": {
        "values": ["Sicherheit", "Wachstum", "Flexibilität"],
        "cognitive_biases": {
            "biases": [
                ("Status-quo-Bias", "Ziehen Sie es vor, beim Alten zu bleiben, auch wenn es bessere Optionen gibt?"),
                ("Herding-Effekt", "Folgen Sie dem, was andere tun, anstatt selbst zu denken?")
            ]
        }
    },
    "Gesundheit": {
        "values": ["Vitalität", "Entspannung", "Ausdauer"],
        "cognitive_biases": {
            "biases": [
                ("Overconfidence-Bias", "Sind Sie zu sicher, dass Ihre Entscheidung die besten Ergebnisse liefert?")
            ]
        }
    }
}

resilience_questions = [
    "Ich bin überzeugt, dass ich mein Leben selbst gestalten kann.",
    "Ich kann mich schnell von Rückschlägen erholen.",
    "Ich sehe Schwierigkeiten als Herausforderungen an, die ich meistern kann.",
    "Ich kann gut mit Unsicherheit umgehen.",
    "Ich finde in schwierigen Zeiten Trost und Unterstützung bei anderen."
]

health_challenges_content = {
    "Stressabbau": [
        "Challenge 1: Atmen Sie tief durch. Expertentipp: Üben Sie 3-4-5 Atmung.",
        "Challenge 2: Machen Sie einen 10-minütigen Spaziergang. Expertentipp: Konzentrieren Sie sich auf Ihre Umgebung.",
        "Challenge 3: Hören Sie entspannende Musik. Expertentipp: Nutzen Sie binaurale Beats.",
        "Challenge 4: Schreiben Sie Ihre Gedanken auf. Expertentipp: Führen Sie ein Dankbarkeitstagebuch.",
        "Challenge 5: Gönnen Sie sich eine Pause. Expertentipp: Machen Sie eine 'digitale Entgiftung'.",
        "Challenge 6: Sagen Sie 'Nein' zu einer unnötigen Verpflichtung. Expertentipp: Priorisieren Sie Ihre Bedürfnisse.",
        "Challenge 7: Machen Sie eine kurze Meditation. Expertentipp: Fokussieren Sie sich auf das Hier und Jetzt.",
        "Challenge 8: Trinken Sie ein warmes, beruhigendes Getränk. Expertentipp: Probieren Sie Kamillentee oder Goldene Milch.",
        "Challenge 9: Strecken Sie Ihren Körper sanft. Expertentipp: Lösen Sie Verspannungen im Nacken und Schultern.",
        "Challenge 10: Planen Sie eine entspannende Aktivität für das Wochenende. Expertentipp: Machen Sie einen Ausflug in die Natur."
    ],
    "Selbstbild stärken": [
        "Challenge 1: Schreiben Sie 3 positive Eigenschaften über sich auf. Expertentipp: Seien Sie ehrlich und wertfrei.",
        "Challenge 2: Sagen Sie sich eine positive Affirmation. Expertentipp: Ich bin stark und fähig.",
        "Challenge 3: Kleiden Sie sich heute so, dass Sie sich wohlfühlen. Expertentipp: Komfort steigert das Selbstvertrauen.",
        "Challenge 4: Machen Sie ein Foto von etwas, das Sie schön finden. Expertentipp: Wertschätzen Sie die Schönheit um Sie herum.",
        "Challenge 5: Akzeptieren Sie ein Kompliment ohne Widerrede. Expertentipp: Sagen Sie einfach 'Danke'.",
        "Challenge 6: Setzen Sie sich ein kleines, erreichbares Ziel. Expertentipp: Das Gefühl des Erfolgs stärkt Ihr Selbstbild.",
        "Challenge 7: Sprechen Sie heute mit einer fremden Person. Expertentipp: Ein kurzes 'Hallo' genügt.",
        "Challenge 8: Vergeben Sie sich einen kleinen Fehler. Expertentipp: Selbstmitgefühl ist der Schlüssel.",
        "Challenge 9: Machen Sie etwas, das Sie gut können. Expertentipp: Fokussieren Sie sich auf Ihre Stärken.",
        "Challenge 10: Reflektieren Sie über Ihre Erfolge in dieser Woche. Expertentipp: Führen Sie ein Erfolgstagebuch."
    ],
    "Selbstwirksamkeitserwartung": [
        "Challenge 1: Identifizieren Sie ein Problem, das Sie lösen können. Expertentipp: Wählen Sie ein kleines Problem.",
        "Challenge 2: Erstellen Sie einen einfachen Plan zur Lösung. Expertentipp: Teilen Sie das Problem in kleine Schritte auf.",
        "Challenge 3: Beginnen Sie mit dem ersten Schritt. Expertentipp: Machen Sie den Anfang, egal wie klein.",
        "Challenge 4: Holen Sie sich Feedback zu Ihrem Plan. Expertentipp: Fragen Sie eine vertrauenswürdige Person.",
        "Challenge 5: Erledigen Sie eine Aufgabe, die Sie aufgeschoben haben. Expertentipp: Das Gefühl der Erleichterung ist eine Belohnung.",
        "Challenge 6: Üben Sie, eine neue Fähigkeit zu erlernen. Expertentipp: Nehmen Sie sich täglich 15 Minuten Zeit dafür.",
        "Challenge 7: Visualisieren Sie den Erfolg. Expertentipp: Stellen Sie sich vor, wie Sie Ihr Ziel erreichen.",
        "Challenge 8: Teilen Sie Ihre Fortschritte mit jemandem. Expertentipp: So bleiben Sie motiviert.",
        "Challenge 9: Reflektieren Sie, welche Hindernisse Sie überwunden haben. Expertentipp: Erkennen Sie Ihre Resilienz.",
        "Challenge 10: Überwinden Sie eine kleine Angst. Expertentipp: Beginnen Sie mit kleinen Expositionen."
    ],
    "Verbundenheit": [
        "Challenge 1: Schicken Sie einer Person, die Ihnen wichtig ist, eine Nachricht. Expertentipp: Eine einfache Geste genügt.",
        "Challenge 2: Fragen Sie jemanden, wie sein Tag war. Expertentipp: Zeigen Sie aufrichtiges Interesse.",
        "Challenge 3: Geben Sie heute ein echtes Kompliment. Expertentipp: Fokussieren Sie sich auf eine spezifische positive Eigenschaft.",
        "Challenge 4: Verbringen Sie Zeit mit einem Freund oder Familienmitglied. Expertentipp: Planen Sie eine Aktivität, die beiden Spaß macht.",
        "Challenge 5: Nehmen Sie sich Zeit für ein Gespräch ohne Ablenkungen. Expertentipp: Legen Sie Ihr Handy beiseite.",
        "Challenge 6: Schreiben Sie eine Dankeskarte. Expertentipp: Drücken Sie Ihre Wertschätzung schriftlich aus.",
        "Challenge 7: Helfen Sie jemandem. Expertentipp: Bieten Sie ungefragt Ihre Hilfe an.",
        "Challenge 8: Nehmen Sie Kontakt zu einer alten Bekanntschaft auf. Expertentipp: Erinnern Sie sich an eine gemeinsame positive Erfahrung.",
        "Challenge 9: Zeigen Sie jemandem, dass Sie ihn hören. Expertentipp: Wiederholen Sie in eigenen Worten, was die Person gesagt hat.",
        "Challenge 10: Machen Sie sich bewusst, wie Sie mit anderen verbunden sind. Expertentipp: Visualisieren Sie Ihr persönliches Netzwerk."
    ],
    "Konfliktlösung": [
        "Challenge 1: Hören Sie jemandem aktiv zu, ohne zu unterbrechen. Expertentipp: Fokus auf die Perspektive des anderen.",
        "Challenge 2: Suchen Sie nach Gemeinsamkeiten in einem Konflikt. Expertentipp: Finden Sie gemeinsame Ziele.",
        "Challenge 3: Formulieren Sie eine 'Ich-Botschaft'. Expertentipp: Sagen Sie 'Ich fühle mich...' statt 'Du hast...'.",
        "Challenge 4: Machen Sie eine Pause, bevor Sie reagieren. Expertentipp: Geben Sie sich 5 Sekunden Bedenkzeit.",
        "Challenge 5: Üben Sie, die Gefühle anderer zu benennen. Expertentipp: Sagen Sie 'Ich merke, dass du wütend bist'.",
        "Challenge 6: Bieten Sie eine Kompromisslösung an. Expertentipp: Finden Sie eine Lösung, die für beide Seiten akzeptabel ist.",
        "Challenge 7: Entschuldigen Sie sich aufrichtig, wenn Sie im Unrecht sind. Expertentipp: Eine echte Entschuldigung zeigt Stärke.",
        "Challenge 8: Sprechen Sie ein Problem an, das Sie schon länger beschäftigt. Expertentipp: Wählen Sie den richtigen Zeitpunkt und Ort.",
        "Challenge 9: Versuchen Sie, die Situation aus der Sicht der anderen Person zu sehen. Expertentipp: Perspektivenwechsel fördert Empathie.",
        "Challenge 10: Finden Sie ein Muster in Ihren Konflikten. Expertentipp: Reflektieren Sie, ob sich Probleme wiederholen."
    ]
}


def get_canned_analysis(score, max_score):
    """Bietet eine vorab definierte Analyse basierend auf dem Resilienz-Score."""
    if score >= max_score * 0.8:
        return "<p>Sie haben eine hohe Punktzahl erreicht, was auf eine starke Resilienz hindeutet. Sie können wahrscheinlich gut mit Stress und Rückschlägen umgehen und betrachten Herausforderungen als Wachstumschancen. Halten Sie an Ihren Strategien fest und nutzen Sie Ihre Stärken, um schwierige Entscheidungen zu treffen.</p>"
    elif score >= max_score * 0.5:
        return "<p>Ihre Punktzahl deutet auf eine solide Resilienz hin. Sie haben Stärken im Umgang mit Schwierigkeiten, aber es gibt möglicherweise Bereiche, in denen Sie noch wachsen können. Üben Sie sich in Achtsamkeit und reflektieren Sie, wie Sie mit Stress umgehen. Das kann Ihnen helfen, Ihre innere Stärke weiter auszubauen.</p>"
    else:
        return "<p>Ihre Punktzahl deutet darauf hin, dass Sie möglicherweise anfälliger für Stress sind und sich von Rückschlägen leichter entmutigen lassen. Nehmen Sie sich Zeit, um zu reflektieren, was Ihre Resilienz beeinträchtigt. Suchen Sie bei Bedarf professionelle Hilfe, denn Resilienz kann gelernt und gestärkt werden.</p>"

def set_theme(theme_name):
    st.session_state.theme = theme_name

# Dynamisches CSS für Hell- und Dunkelmodus und Handy-Optik
st.markdown(f"""
<style>
    :root {{
        --primary-color: #4CAF50;
        --background-color: #f0f2f6;
        --secondary-background-color: #ffffff;
        --text-color: #333333;
        --card-border-radius: 12px;
        --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stApp {{
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .main .block-container {{
        padding: 1rem;
        max-width: 600px;
        width: 100%;
    }}
    .stButton > button {{
        background-color: var(--primary-color);
        color: white;
        padding: 12px 24px;
        border-radius: var(--card-border-radius);
        border: none;
        width: 100%;
        margin-top: 10px;
        font-weight: bold;
        box-shadow: var(--card-shadow);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }}
    .card-button {{
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: var(--card-border-radius);
        text-align: center;
        margin-bottom: 15px;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: var(--card-shadow);
        border: 2px solid transparent;
        transition: all 0.2s ease;
        cursor: pointer;
    }}
    .card-button:hover {{
        border: 2px solid var(--primary-color);
    }}
    .bottom-nav {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: var(--secondary-background-color);
        padding: 10px 0;
        display: flex;
        justify-content: space-around;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        z-index: 1000;
    }}
    .nav-item {{
        text-align: center;
        text-decoration: none;
        color: #333;
        font-weight: bold;
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        transition: color 0.2s ease;
    }}
    .nav-item .icon {{
        font-size: 24px;
        margin-bottom: 5px;
    }}
    .nav-item.active {{
        color: var(--primary-color);
    }}
    .badge {{
        background-color: var(--primary-color);
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-top: 10px;
    }}
    .stProgress > div > div {{
        background-color: var(--primary-color) !important;
    }}
    .st-emotion-cache-1j0z1l1 {{
        color: var(--primary-color);
    }}
    .st-emotion-cache-1f1l65j {{
        background-color: var(--background-color);
    }}
</style>
""", unsafe_allow_html=True)

# CSS für den Dunkelmodus, falls aktiviert
if st.session_state.theme == 'dark':
    st.markdown("""
    <style>
        :root {{
            --primary-color: #4CAF50;
            --background-color: #121212;
            --secondary-background-color: #1e1e1e;
            --text-color: #e0e0e0;
        }}
    </style>
    """, unsafe_allow_html=True)


# Hilfsfunktionen zur Navigation und zum Zurücksetzen
def next_page(page_name):
    st.session_state.page = page_name

def reset_app():
    st.session_state.problem = ""
    st.session_state.problem_category = "Wähle eine Kategorie"
    st.session_state.options = ["", ""]
    st.session_state.selected_values = []
    st.session_state.values_rating = {}
    st.session_state.emotions = ""
    st.session_state.pro_a = ""
    st.session_state.contra_a = ""
    st.session_state.pro_b = ""
    st.session_state.contra_b = ""
    st.session_state.creative_options = ""
    st.session_state.future_scenario_a = ""
    st.session_state.future_scenario_b = ""
    st.session_state.first_step = ""
    st.session_state.resilience_answers = {}
    st.session_state.resilience_score = None
    st.session_state.health_challenges = {
        'Stressabbau': 0, 'Selbstbild stärken': 0,
        'Selbstwirksamkeitserwartung': 0, 'Verbundenheit': 0, 'Konfliktlösung': 0
    }
    st.session_state.unlocked_trophies = []
    st.session_state.total_points = 0
    st.session_state.show_special_thing = False
    st.session_state.page = 'start'

def render_start_page():
    st.title("Willkommen! 🚀")
    
    # Theme-Umschalter
    st.markdown("---")
    st.subheader("Einstellungen")
    if st.session_state.theme == 'light':
        if st.button("Dunkelmodus aktivieren"):
            set_theme('dark')
            st.rerun()
    else:
        if st.button("Lichtmodus aktivieren"):
            set_theme('light')
            st.rerun()

    st.markdown("---")
    st.subheader("Wähle dein Ziel")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Entscheidungsreise", key="start_decide_btn"):
            next_page('step_1')
    with col2:
        if st.button("Resilienz-Fragebogen", key="start_resilience_btn"):
            next_page('wert_reflexion')
    with col3:
        if st.button("Gesundheitspfade", key="start_health_btn"):
            next_page('health_paths')

def render_step_1():
    """Rendert die Benutzeroberfläche für Schritt 1: Problem und Optionen."""
    st.title("Step 1: Dein Problem & deine Optionen")
    with st.container():
        st.markdown("#### Problem und Kategorie")
        st.session_state.problem = st.text_area(
            "Was ist die Entscheidung, die dich beschäftigt?",
            value=st.session_state.problem, key="problem_input", height=100
        )
        options = ["Wähle eine Kategorie"] + list(category_content.keys())
        try:
            current_index = options.index(st.session_state.problem_category)
        except ValueError:
            current_index = 0
        st.session_state.problem_category = st.selectbox(
            "Kategorie:", options=options, index=current_index
        )
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
    """Rendert die Benutzeroberfläche für Schritt 2: Werte & Motivation."""
    st.title("Step 2: Werte & Motivation")
    selected_category = st.session_state.problem_category
    all_values = category_content.get(selected_category, {}).get("values", [])
    
    with st.container():
        st.markdown(f"#### Psychologische Werte")
        st.markdown(f"Wähle alle Werte aus, die für deine Entscheidung in der Kategorie **{selected_category}** relevant sind.")
        st.session_state.selected_values = []
        cols = st.columns(3)
        for i, value in enumerate(all_values):
            col = cols[i % 3]
            if col.checkbox(value, key=f"checkbox_{value}"):
                st.session_state.selected_values.append(value)

    if st.session_state.selected_values:
        with st.container():
            st.markdown("#### Werte-Bewertung (Deine Entscheidungsmatrix)")
            st.markdown("Bewerte auf einer Skala von 1 bis 10, wie gut jede Option deine gewählten Werte erfüllt.")
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
        if not st.session_state.selected_values:
            st.warning("Bitte wähle mindestens einen Wert aus, bevor du fortfährst.")
        else:
            next_page('step_3')
    
def render_step_3():
    """Rendert die Benutzeroberfläche für Schritt 3: Emotionen & Denkfehler."""
    st.title("Step 3: Emotionen & Denkfehler")
    with st.container():
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

    if st.button("Weiter"):
        next_page('step_4')

def render_step_4():
    """Rendert die Benutzeroberfläche für Schritt 4: Pro/Contra & Zukunft."""
    st.title("Step 4: Pro/Contra & Zukunft")
    
    with st.container():
        st.markdown(f"#### Vorteile (Der 'Gelbe Hut')")
        st.session_state.pro_a = st.text_area(
            f"Was spricht für Option A: '{st.session_state.options[0]}'?",
            value=st.session_state.pro_a, key="pro_a_area", height=150
        )
        st.session_state.pro_b = st.text_area(
            f"Was spricht für Option B: '{st.session_state.options[1]}'?",
            value=st.session_state.pro_b, key="pro_b_area", height=150
        )
    with st.container():
        st.markdown(f"#### Nachteile (Der 'Schwarze Hut')")
        st.session_state.contra_a = st.text_area(
            f"Was spricht gegen Option A: '{st.session_state.options[0]}'?",
            value=st.session_state.contra_a, key="contra_a_area", height=150
        )
        st.session_state.contra_b = st.text_area(
            f"Was spricht gegen Option B: '{st.session_state.options[1]}'?",
            value=st.session_state.contra_b, key="contra_b_area", height=150
        )
        
    with st.container():
        st.markdown("#### Kreative Optionen (Der 'Grüne Hut')")
        st.markdown("Gibt es noch andere, unkonventionelle Optionen, die du bisher nicht in Betracht gezogen hast?")
        st.session_state.creative_options = st.text_area(
            "Andere Ideen:", value=st.session_state.creative_options, key="creative_options_area", height=150
        )

    with st.container():
        st.markdown(f"#### Zukunftsszenario (nach Jeff Bezos)")
        st.markdown("Stelle dir vor, du bist 80 Jahre alt. Welche Entscheidung würdest du am meisten bereuen? Das Regret Minimization Framework hilft dir, aus einer langfristigen Perspektive zu entscheiden.")
        st.session_state.future_scenario_a = st.text_area(
            f"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option A entscheidest?",
            value=st.session_state.future_scenario_a, key="scenario_a", height=200
        )
        st.session_state.future_scenario_b = st.text_area(
            f"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option B entscheidest?",
            value=st.session_state.future_scenario_b, key="scenario_b", height=200
        )

    if st.button("Weiter"):
        next_page('step_5')

def render_step_5():
    """Rendert die Benutzeroberfläche für Schritt 5: Zusammenfassung."""
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
                
                st.altair_chart(chart, use_container_width=True)
                
                # Anzeige der Gesamtpunktzahl
                st.write(f"**Gesamtpunktzahl Option A:** {score_a}")
                st.write(f"**Gesamtpunktzahl Option B:** {score_b}")
    
    with st.container():
        st.markdown("---")
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
        st.markdown("---")
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

def render_resilience_questions_page():
    st.title("Resilienz-Fragebogen")
    st.markdown("Bewerte auf einer Skala von **1 (stimme gar nicht zu)** bis **5 (stimme voll und ganz zu)**, wie sehr die folgenden Aussagen auf dich zutreffen.")

    # Fragen rendern und Antworten speichern
    for i, question in enumerate(resilience_questions):
        st.session_state.resilience_answers[i] = st.slider(
            question,
            1, 5, st.session_state.resilience_answers.get(i, 3), key=f"resilience_q_{i}"
        )

    # Weiter-Button zum Anzeigen der Ergebnisse
    if st.button("Fragebogen abschließen"):
        with st.spinner("Deine Punktzahl wird berechnet... bitte habe einen kleinen Moment Geduld."):
            time.sleep(1)
            st.session_state.resilience_score = sum(st.session_state.resilience_answers.values())
        next_page('resilience_results')

def render_resilience_results_page():
    st.title("Deine Resilienz-Analyse")
    st.warning("Disclaimer: Dieser Fragebogen ist ein nicht-klinisches Werkzeug zur Selbsterkenntnis und ersetzt keine professionelle psychologische Beratung.")
    
    if st.session_state.resilience_score is None:
        st.warning("Bitte fülle zuerst den Fragebogen aus.")
        if st.button("Zum Fragebogen zurückkehren"):
            next_page('wert_reflexion')
        return

    total_score = st.session_state.resilience_score
    max_score = len(resilience_questions) * 5
    st.markdown(f"**Deine Gesamtpunktzahl:** **{total_score}** von **{max_score}**")
    
    st.session_state.resilience_analysis = get_canned_analysis(total_score, max_score)
    
    if st.session_state.resilience_analysis:
        st.markdown(st.session_state.resilience_analysis, unsafe_allow_html=True)

    if st.button("Neue Reflexion starten"):
        reset_app()

def render_health_paths_page():
    st.title("Gesundheitspfade 🧘")
    st.markdown("Wähle einen Pfad, um deine mentalen Fähigkeiten zu stärken. Jeder Pfad besteht aus 10 täglichen Challenges.")

    path_names = ["Stressabbau", "Selbstbild stärken", "Selbstwirksamkeitserwartung", "Verbundenheit", "Konfliktlösung"]
    
    for path in path_names:
        completed = st.session_state.health_challenges.get(path, 0)
        max_challenges = 10
        trophy_unlocked = path in st.session_state.unlocked_trophies

        if trophy_unlocked:
            st.markdown(f"<div class='card-button' style='background-color: var(--primary-color); color: white;'>"
                        f"✨ {path} ✨ "
                        f"</div>", unsafe_allow_html=True)
        else:
            if st.button(f"{path}", key=f"path_btn_{path}"):
                st.session_state.current_path = path
                next_page('health_challenge_page')
            st.progress(completed / max_challenges)

    st.markdown("---")
    st.subheader("Deine Trophäen-Galerie")
    if st.button("Trophäen anzeigen", key="trophy_gallery_btn"):
        next_page('trophy_gallery')

def render_health_challenge_page():
    path = st.session_state.current_path
    if not path:
        next_page('health_paths')
        return
    
    challenges = health_challenges_content.get(path, [])
    current_challenge_index = st.session_state.health_challenges.get(path, 0)
    
    st.title(f"{path}")
    st.subheader("Deine tägliche Challenge")

    if current_challenge_index >= len(challenges):
        st.success(f"🎉 Du hast den Pfad **'{path}'** abgeschlossen!")
        if path not in st.session_state.unlocked_trophies:
            st.session_state.unlocked_trophies.append(path)
            st.session_state.total_points += 50
            if len(st.session_state.unlocked_trophies) == 5:
                st.session_state.show_special_thing = True
            st.balloons()
        st.markdown("Du kannst nun zur Trophäen-Galerie gehen, um deine Trophäe zu sehen.")
        if st.button("Zurück zu den Pfaden"):
            next_page('health_paths')
        return

    challenge_text = challenges[current_challenge_index]
    st.info(challenge_text)

    if st.button("Challenge abgeschlossen", key=f"complete_challenge_{uuid.uuid4()}"):
        st.session_state.health_challenges[path] += 1
        st.session_state.total_points += 10
        st.success("Challenge abgeschlossen! 💪")
        st.info(f"Deine Gesamtpunkte: {st.session_state.total_points}")
        st.rerun()

    st.markdown("---")
    st.markdown(f"**Fortschritt:** Challenge {current_challenge_index + 1} von {len(challenges)}")
    st.progress((current_challenge_index + 1) / len(challenges))

def render_trophy_gallery_page():
    st.title("Deine Trophäen-Galerie 🏆")
    st.markdown(f"Gesamtpunkte: **{st.session_state.total_points}**")

    if not st.session_state.unlocked_trophies:
        st.info("Du hast noch keine Trophäen gesammelt. Starte eine Challenge, um deine erste Trophäe freizuschalten!")
    else:
        st.subheader("Freigeschaltete Trophäen:")
        cols = st.columns(len(st.session_state.unlocked_trophies))
        for i, path in enumerate(st.session_state.unlocked_trophies):
            with cols[i]:
                st.markdown(f"<div style='text-align: center;'><h2>🏆</h2><p>{path}</p></div>", unsafe_allow_html=True)
    
    if st.session_state.show_special_thing:
        st.markdown("---")
        st.success("🎉 **Herzlichen Glückwunsch!** Du hast alle 5 Pfade abgeschlossen und damit die besondere Belohnung freigeschaltet! Du hast gezeigt, dass du entschlossen bist, dich kontinuierlich weiterzuentwickeln und an dir zu arbeiten. Deine mentale Stärke und dein Durchhaltevermögen sind bewundernswert. Dies ist erst der Anfang deiner Reise!")

    if st.button("Zurück zu den Pfaden"):
        next_page('health_paths')

def render_bottom_nav():
    # Render a fixed bottom navigation bar using HTML and CSS
    nav_html = f"""
    <div class="bottom-nav">
        <a href="?page=start" class="nav-item {'active' if st.session_state.page == 'start' else ''}">
            <span class="icon">🏠</span> Home
        </a>
        <a href="?page=step_1" class="nav-item {'active' if st.session_state.page in ['step_1', 'step_2', 'step_3', 'step_4', 'step_5'] else ''}">
            <span class="icon">🧠</span> Decide
        </a>
        <a href="?page=wert_reflexion" class="nav-item {'active' if st.session_state.page in ['wert_reflexion', 'resilience_results'] else ''}">
            <span class="icon">🧘</span> Reflect
        </a>
        <a href="?page=health_paths" class="nav-item {'active' if st.session_state.page in ['health_paths', 'health_challenge_page', 'trophy_gallery'] else ''}">
            <span class="icon">🏆</span> Grow
        </a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

def main():
    query_params = st.query_params
    if 'page' in query_params:
        st.session_state.page = query_params['page'][0]

    # Zentraler Router für alle Seiten
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
        render_resilience_questions_page()
    elif st.session_state.page == 'resilience_results':
        render_resilience_results_page()
    elif st.session_state.page == 'health_paths':
        render_health_paths_page()
    elif st.session_state.page == 'health_challenge_page':
        render_health_challenge_page()
    elif st.session_state.page == 'trophy_gallery':
        render_trophy_gallery_page()
    
    # Die untere Navigationsleiste wird auf allen Seiten außer der Startseite angezeigt
    if st.session_state.page not in ['start']:
        render_bottom_nav()

main()
