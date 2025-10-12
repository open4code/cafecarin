 Ich erstelle jetzt die erweiterte Streamlit-App mit dem kompletten Resilienz-Pfad als neue Datei. Die App wird alle bestehenden Funktionen behalten und die neuen Resilienz-Pfade hinzufügen.
Action: file_editor create /app/streamlit_app.py --file-text "# -*- coding: utf-8 -*-
# Python script for a Streamlit application with three distinct modules.
# Module 1: A \"Decision Journey\" tool that helps analyze pros and cons.
# Module 2: A \"Resilience Reflection\" guide based on user input.
# Module 3: A \"Resilience Path\" with 10-day challenges for different resilience factors.

import streamlit as st
import altair as alt
import pandas as pd
import json
import requests
import time
import base64

# --- 1. SEITENKONFIGURATION & STYLING ---
st.set_page_config(
    page_title=\"VitaBoost\",
    layout=\"wide\",
    initial_sidebar_state=\"collapsed\"
)

# Das CSS wurde komplett neu geschrieben, um das Layout aus dem Bild zu replizieren
custom_css = \"\"\"
<style>
    /* Allgemeine Farbpalette und Schriftart */
    :root {
        --primary-color: #E2B060;
        --secondary-color: #F8D8C9;
        --background-color: #FFF8E1;
        --text-color: #4A4A4A;
        --container-bg: #FFFFFF;
        --border-radius: 16px;
        --success-color: #4CAF50;
        --trophy-gold: #FFD700;
    }

    body {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: var(--background-color);
    }

    /* Styling für alle Container und Expander (die \"Karten\") */
    div[data-testid=\"stVerticalBlock\"] > div.st-emotion-cache-1r6y9j9,
    div[data-testid=\"stVerticalBlock\"] > div.st-emotion-cache-1n1p067 {
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
    
    .st-emotion-cache-79elbk {
      gap: 20px;
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
    .stSlider > div > div > div:nth-child(2) {
        background-color: var(--secondary-color); /* Slider track */
    }
    .stSlider > div > div > div:nth-child(2) > div:nth-child(1) {
        background-color: var(--primary-color); /* Slider fill */
    }

    /* Trophy Card Styling */
    .trophy-card {
        background: linear-gradient(135deg, var(--trophy-gold) 0%, #FFA500 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 10px;
    }
    
    .trophy-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }

    /* Progress Bar Styling */
    .progress-container {
        background-color: var(--secondary-color);
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--success-color) 100%);
        height: 100%;
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 12px;
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
    
    /* Expert Tip Box */
    .expert-tip {
        background-color: #E8F5E9;
        border-left: 4px solid var(--success-color);
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
</style>
\"\"\"
st.markdown(custom_css, unsafe_allow_html=True)


# --- Konfiguration für LLM API (NICHT ÄNDERN) ---
# Der API-Schlüssel wird von der Laufzeitumgebung bereitgestellt.
API_KEY = \"\"
API_URL = \"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=\" + API_KEY
API_HEADERS = {'Content-Type': 'application/json'}

# --- Helper function for making API calls with exponential backoff ---
def call_llm_api_with_backoff(prompt, max_retries=5, initial_delay=1):
    \"\"\"
    Calls the LLM API with exponential backoff to handle rate limiting.
    
    Args:
        prompt (str): The text prompt for the LLM.
        max_retries (int): The maximum number of retries.
        initial_delay (int): The initial delay in seconds.
        
    Returns:
        dict: The JSON response from the API or None on failure.
    \"\"\"
    retries = 0
    while retries < max_retries:
        try:
            payload = {
                \"contents\": [
                    {
                        \"role\": \"user\",
                        \"parts\": [{\"text\": prompt}]
                    }
                ]
            }
            response = requests.post(API_URL, headers=API_HEADERS, data=json.dumps(payload))
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
            
            result = response.json()
            if result.get('candidates') and result['candidates'][0].get('content'):
                return result
            else:
                st.error(\"Error: The LLM response was empty or malformed. Please try again.\")
                return None

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                delay = initial_delay * (2 ** retries)
                st.warning(f\"Rate limit exceeded. Retrying in {delay} seconds...\")
                time.sleep(delay)
                retries += 1
            else:
                st.error(f\"HTTP Error: {err}\")
                return None
        except requests.exceptions.RequestException as err:
            st.error(f\"Request Error: {err}\")
            return None
    st.error(\"Maximum retries reached. The API call failed.\")
    return None

# --- 2. RESILIENZ-PFAD DATENSTRUKTUR ---
RESILIENCE_PATHS = {
    \"Stressabbau\": {
        \"icon\": \"🧘\",
        \"description\": \"Lerne effektive Techniken zur Stressbewältigung und inneren Ruhe\",
        \"color\": \"#4CAF50\",
        \"expert_tip\": \"Ein schneller Weg zur Ruhe: Atmen Sie 4 Sekunden lang durch die Nase ein, halten Sie den Atem 7 Sekunden lang an und atmen Sie 8 Sekunden lang durch den Mund aus. Das senkt den Herzschlag und beruhigt sofort.\",
        \"days\": {
            1: {
                \"title\": \"Die 4-7-8 Atemtechnik\",
                \"exercise\": \"Übe die 4-7-8 Atemtechnik für 5 Minuten. Atme 4 Sekunden ein, halte 7 Sekunden, atme 8 Sekunden aus. Wiederhole dies 5 Mal.\",
                \"reflection\": \"Wie fühlst du dich nach der Übung? Welche Veränderungen bemerkst du in deinem Körper?\",
                \"motivation\": \"Du hast den ersten Schritt zu mehr Ruhe gemacht! Jeder Atemzug bringt dich näher zu deiner inneren Balance.\",
                \"points\": 10
            },
            2: {
                \"title\": \"Körperwahrnehmung\",
                \"exercise\": \"Body Scan: Lege dich hin und scanne deinen Körper von Kopf bis Fuß. Wo sitzt die Anspannung? Atme bewusst in diese Bereiche.\",
                \"reflection\": \"Welche Körperregionen waren besonders angespannt? Was könnte der Grund dafür sein?\",
                \"motivation\": \"Großartig! Du lernst, die Signale deines Körpers zu verstehen. Das ist der Schlüssel zur Stressbewältigung.\",
                \"points\": 10
            },
            3: {
                \"title\": \"Stressauslöser identifizieren\",
                \"exercise\": \"Erstelle eine Liste deiner Top 5 Stressauslöser. Was triggert dich am meisten im Alltag?\",
                \"reflection\": \"Welcher dieser Auslöser ist am häufigsten? Was könntest du ändern, um ihn zu vermeiden oder besser damit umzugehen?\",
                \"motivation\": \"Bewusstsein ist der erste Schritt zur Veränderung. Du bist auf dem richtigen Weg!\",
                \"points\": 10
            },
            4: {
                \"title\": \"Progressive Muskelentspannung\",
                \"exercise\": \"Spanne nacheinander verschiedene Muskelgruppen für 5 Sekunden an und entspanne sie dann für 10 Sekunden. Beginne mit den Füßen und arbeite dich nach oben.\",
                \"reflection\": \"Welche Muskelgruppe fiel dir am schwersten zu entspannen? Warum könnte das so sein?\",
                \"motivation\": \"Dein Körper lernt, zwischen Anspannung und Entspannung zu unterscheiden. Das ist eine wertvolle Fähigkeit!\",
                \"points\": 10
            },
            5: {
                \"title\": \"Natur als Stressabbau\",
                \"exercise\": \"Verbringe mindestens 20 Minuten in der Natur. Gehe spazieren oder setze dich einfach nach draußen. Nimm bewusst die Umgebung wahr.\",
                \"reflection\": \"Wie hat die Natur dein Stresslevel beeinflusst? Was hast du bemerkt?\",
                \"motivation\": \"Die Natur ist ein kraftvoller Verbündeter im Kampf gegen Stress. Du hast heute gut für dich gesorgt!\",
                \"points\": 10
            },
            6: {
                \"title\": \"Stresstagebuch\",
                \"exercise\": \"Führe heute ein Stresstagebuch. Notiere jeden stressigen Moment: Was passierte? Wie hast du reagiert? Was hättest du anders machen können?\",
                \"reflection\": \"Welche Muster erkennst du in deinen Stressreaktionen?\",
                \"motivation\": \"Selbstreflexion ist Gold wert! Du entwickelst ein tiefes Verständnis für deine Stressmuster.\",
                \"points\": 10
            },
            7: {
                \"title\": \"Genussmomente schaffen\",
                \"exercise\": \"Plane heute bewusst 3 Genussmomente ein. Das kann eine Tasse Tee, ein Lieblingslied oder ein Sonnenuntergang sein. Genieße sie vollkommen.\",
                \"reflection\": \"Wie schwer oder leicht war es, dir diese Momente zu erlauben? Was hat dich daran gehindert oder unterstützt?\",
                \"motivation\": \"Du lernst, Freude aktiv in deinen Tag zu integrieren. Das ist aktive Stressprävention!\",
                \"points\": 10
            },
            8: {
                \"title\": \"Grenzen setzen\",
                \"exercise\": \"Sage heute zu einer Sache 'Nein', die dich überlasten würde. Übe, deine Grenzen zu kommunizieren.\",
                \"reflection\": \"Wie hat es sich angefühlt, Nein zu sagen? Was hat dich daran gehindert oder bestärkt?\",
                \"motivation\": \"Grenzen zu setzen ist Selbstfürsorge, keine Schwäche. Du schützt deine Energie!\",
                \"points\": 10
            },
            9: {
                \"title\": \"Bewegung als Ventil\",
                \"exercise\": \"Bewege dich heute für mindestens 30 Minuten. Joggen, Tanzen, Yoga – finde, was dir guttut und Stress abbaut.\",
                \"reflection\": \"Wie hat sich die Bewegung auf deine Stimmung ausgewirkt? Welche Form der Bewegung hat dir am meisten Freude bereitet?\",
                \"motivation\": \"Bewegung ist Medizin für Körper und Geist! Du investierst in deine Gesundheit.\",
                \"points\": 10
            },
            10: {
                \"title\": \"Dein persönlicher Anti-Stress-Plan\",
                \"exercise\": \"Erstelle einen persönlichen Anti-Stress-Notfallplan. Welche 5 Techniken helfen dir am besten? Schreibe sie auf und hänge sie sichtbar auf.\",
                \"reflection\": \"Was sind deine effektivsten Stress-Tools? Wie kannst du sicherstellen, dass du sie regelmäßig anwendest?\",
                \"motivation\": \"🎉 Du hast den Stressabbau-Pfad gemeistert! Du besitzt jetzt ein Arsenal an Werkzeugen für mehr Gelassenheit.\",
                \"points\": 10
            }
        }
    },
    \"Selbstwirksamkeit\": {
        \"icon\": \"💪\",
        \"description\": \"Stärke dein Vertrauen in deine eigenen Fähigkeiten\",
        \"color\": \"#FF9800\",
        \"expert_tip\": \"Das Gehirn lernt durch kleine Siege. Jedes Mal, wenn Sie ein kleines Ziel erreichen – sei es nur, ein Glas Wasser zu trinken – stärken Sie Ihr Vertrauen in Ihre Fähigkeit, Dinge zu bewirken. Nutzen Sie diese kleinen Momente der Bestätigung.\",
        \"days\": {
            1: {
                \"title\": \"Mikro-Erfolge sammeln\",
                \"exercise\": \"Setze dir heute 3 winzige, erreichbare Ziele (z.B. Bett machen, 1 Glas Wasser trinken, 5 Minuten lesen). Hake sie ab!\",
                \"reflection\": \"Wie fühlte es sich an, diese kleinen Ziele zu erreichen? Welche Emotion begleitete das Abhaken?\",
                \"motivation\": \"Jeder kleine Sieg zählt! Du beweist dir selbst, dass du Dinge bewegen kannst.\",
                \"points\": 10
            },
            2: {
                \"title\": \"Erfolge dokumentieren\",
                \"exercise\": \"Erstelle eine 'Erfolgs-Liste'. Schreibe 10 Dinge auf, die du in deinem Leben bereits gemeistert hast – groß oder klein.\",
                \"reflection\": \"Welcher Erfolg macht dich am meisten stolz? Welche Stärken hast du dabei gezeigt?\",
                \"motivation\": \"Du hast bereits so viel erreicht! Diese Liste ist der Beweis deiner Fähigkeiten.\",
                \"points\": 10
            },
            3: {
                \"title\": \"Komfortzone erweitern\",
                \"exercise\": \"Tue heute eine Sache, die dich leicht herausfordert, aber machbar ist. Etwas, das du normalerweise vermeidest.\",
                \"reflection\": \"Was hast du gewählt? Wie hast du dich vorher und nachher gefühlt?\",
                \"motivation\": \"Du wächst außerhalb deiner Komfortzone! Jeder Schritt macht dich stärker.\",
                \"points\": 10
            },
            4: {
                \"title\": \"Fähigkeiten-Inventur\",
                \"exercise\": \"Liste 20 Fähigkeiten auf, die du besitzt. Von praktischen (kochen, tippen) bis zu sozialen (zuhören, empathisch sein).\",
                \"reflection\": \"Welche Fähigkeit überrascht dich? Welche möchtest du weiter ausbauen?\",
                \"motivation\": \"Du bist voller Talente! Erkenne an, was du alles kannst.\",
                \"points\": 10
            },
            5: {
                \"title\": \"Ein Problem lösen\",
                \"exercise\": \"Identifiziere ein kleines Problem in deinem Alltag und löse es heute. Repariere etwas, organisiere etwas oder finde eine Lösung.\",
                \"reflection\": \"Welches Problem hast du gelöst? Wie bist du vorgegangen? Was hast du über deine Problemlösungsfähigkeiten gelernt?\",
                \"motivation\": \"Du bist ein Problemlöser! Jede Lösung stärkt dein Vertrauen in deine Fähigkeiten.\",
                \"points\": 10
            },
            6: {
                \"title\": \"Feedback einholen\",
                \"exercise\": \"Frage 3 Menschen, die dich gut kennen: 'Was ist eine Stärke, die du an mir siehst?' Notiere ihre Antworten.\",
                \"reflection\": \"Welche Stärken wurden genannt? Waren sie dir bewusst? Welche hat dich überrascht?\",
                \"motivation\": \"Andere sehen Stärken in dir, die du vielleicht übersiehst. Du bist wertvoller, als du denkst!\",
                \"points\": 10
            },
            7: {
                \"title\": \"Eine neue Fähigkeit beginnen\",
                \"exercise\": \"Beginne heute, eine neue kleine Fähigkeit zu lernen. 15 Minuten reichen – ein paar Worte einer Sprache, ein Akkord auf der Gitarre, ein neues Rezept.\",
                \"reflection\": \"Was hast du gewählt? Wie fühlte es sich an, Anfänger zu sein?\",
                \"motivation\": \"Du beweist dir, dass du wachsen und lernen kannst. Das ist pure Selbstwirksamkeit!\",
                \"points\": 10
            },
            8: {
                \"title\": \"Rückschläge umdeuten\",
                \"exercise\": \"Denke an einen vergangenen 'Misserfolg'. Was hast du daraus gelernt? Wie hat er dich stärker gemacht?\",
                \"reflection\": \"Wie verändert sich deine Sicht auf den Rückschlag, wenn du ihn als Lernchance siehst?\",
                \"motivation\": \"Rückschläge sind keine Endstation, sondern Umwege zum Erfolg. Du lernst und wächst!\",
                \"points\": 10
            },
            9: {
                \"title\": \"Selbstgespräch überprüfen\",
                \"exercise\": \"Achte heute auf deine innere Stimme. Jedes Mal, wenn du denkst 'Das kann ich nicht', ersetze es durch 'Ich lerne, wie ich das kann'.\",
                \"reflection\": \"Wie oft hast du dich selbst sabotiert? Wie fühlte sich die neue Formulierung an?\",
                \"motivation\": \"Deine Worte formen deine Realität. Du trainierst dein Gehirn auf Erfolg!\",
                \"points\": 10
            },
            10: {
                \"title\": \"Dein Selbstwirksamkeits-Manifest\",
                \"exercise\": \"Schreibe ein persönliches Manifest: 'Ich bin fähig, weil...' Liste alle Beweise deiner Selbstwirksamkeit auf. Lies es laut vor.\",
                \"reflection\": \"Wie fühlt es sich an, deine Fähigkeiten laut zu bestätigen? Was glaubst du jetzt über dich selbst?\",
                \"motivation\": \"🎉 Du hast deine Selbstwirksamkeit gestärkt! Du weißt jetzt: Du kannst mehr, als du denkst.\",
                \"points\": 10
            }
        }
    },
    \"Selbstbild stärken\": {
        \"icon\": \"🌟\",
        \"description\": \"Entwickle ein positives und realistisches Selbstbild\",
        \"color\": \"#9C27B0\",
        \"expert_tip\": \"Negative Gedanken wie 'Das kann ich nicht' sind nur Gewohnheiten. Fragen Sie sich: 'Was ist das Gegenteil dieses Gedankens?' Ersetzen Sie ihn durch eine neutrale oder positive Alternative, wie 'Ich lerne und werde besser.'\",
        \"days\": {
            1: {
                \"title\": \"Selbstbild-Check\",
                \"exercise\": \"Schreibe 10 Adjektive auf, die beschreiben, wie du dich selbst siehst. Sei ehrlich, sowohl positiv als auch negativ.\",
                \"reflection\": \"Überwiegen positive oder negative Begriffe? Was sagt das über dein Selbstbild aus?\",
                \"motivation\": \"Bewusstsein ist der erste Schritt zur Veränderung. Du schaust mutig hin!\",
                \"points\": 10
            },
            2: {
                \"title\": \"Innerer Kritiker vs. innerer Unterstützer\",
                \"exercise\": \"Identifiziere eine Situation, in der dein innerer Kritiker laut war. Was hat er gesagt? Schreibe eine Antwort von deinem inneren Unterstützer.\",
                \"reflection\": \"Wie unterscheidet sich die Perspektive? Welche Stimme fühlte sich wahrer an?\",
                \"motivation\": \"Du lernst, deinem inneren Kritiker Paroli zu bieten. Das ist Selbstliebe in Aktion!\",
                \"points\": 10
            },
            3: {
                \"title\": \"Stärken-Fokus\",
                \"exercise\": \"Erstelle eine Liste mit 15 deiner Stärken. Wenn es schwerfällt, frage: 'Was würden meine Freunde sagen?'\",
                \"reflection\": \"Welche Stärke nutzt du zu wenig? Wie könntest du sie mehr einsetzen?\",
                \"motivation\": \"Du bist voller Stärken! Sie zu erkennen ist der Grundstein für ein positives Selbstbild.\",
                \"points\": 10
            },
            4: {
                \"title\": \"Vergleichsfalle vermeiden\",
                \"exercise\": \"Beobachte heute, wann du dich mit anderen vergleichst. Halte an und frage: 'Was ist mein eigener Maßstab?'\",
                \"reflection\": \"Wie oft hast du verglichen? Was löst das in dir aus? Wie fühlte es sich an, eigene Maßstäbe zu setzen?\",
                \"motivation\": \"Dein einziger Vergleich solltest du gestern sein. Du definierst deinen eigenen Erfolg!\",
                \"points\": 10
            },
            5: {
                \"title\": \"Komplimente annehmen\",
                \"exercise\": \"Wenn dir heute jemand ein Kompliment macht, nimm es einfach an mit 'Danke'. Keine Abschwächung, keine Rechtfertigung.\",
                \"reflection\": \"Wie schwer war es, ein Kompliment anzunehmen? Was hindert dich normalerweise daran?\",
                \"motivation\": \"Du verdienst Anerkennung! Komplimente anzunehmen stärkt dein Selbstbild.\",
                \"points\": 10
            },
            6: {
                \"title\": \"Selbstmitgefühl üben\",
                \"exercise\": \"Schreibe einen Brief an dich selbst, so wie du ihn an deinen besten Freund schreiben würdest, der gerade kämpft. Mit Mitgefühl und Verständnis.\",
                \"reflection\": \"Wie hat es sich angefühlt, freundlich zu dir selbst zu sein? Was macht es so schwer oder leicht?\",
                \"motivation\": \"Selbstmitgefühl ist keine Schwäche, sondern die Basis für echte Stärke. Du lernst, dein eigener Freund zu sein!\",
                \"points\": 10
            },
            7: {
                \"title\": \"Perfektionismus hinterfragen\",
                \"exercise\": \"Identifiziere einen Bereich, in dem du perfekt sein willst. Frage dich: Warum? Was würde passieren, wenn ich 'gut genug' akzeptiere?\",
                \"reflection\": \"Woher kommt dieser Perfektionsdruck? Was könntest du gewinnen, wenn du ihn loslässt?\",
                \"motivation\": \"Perfektion ist eine Illusion. Du bist 'gut genug' – und das ist mehr als genug!\",
                \"points\": 10
            },
            8: {
                \"title\": \"Deine Werte leben\",
                \"exercise\": \"Liste deine Top 5 Werte auf. Reflektiere: Lebe ich nach diesen Werten? Wo stimmen meine Handlungen mit meinen Werten überein?\",
                \"reflection\": \"Wo gibt es Diskrepanzen? Was könntest du ändern, um authentischer zu leben?\",
                \"motivation\": \"Authentizität stärkt dein Selbstbild. Du lernst, dir selbst treu zu sein!\",
                \"points\": 10
            },
            9: {
                \"title\": \"Körperliche Selbstakzeptanz\",
                \"exercise\": \"Stelle dich vor den Spiegel. Finde 5 Dinge an deinem Körper, für die du dankbar bist (z.B. 'Meine Beine tragen mich', 'Meine Hände erschaffen').\",
                \"reflection\": \"Wie hat diese Übung deine Beziehung zu deinem Körper verändert?\",
                \"motivation\": \"Dein Körper ist dein Zuhause. Dankbarkeit dafür ist ein Akt der Selbstliebe!\",
                \"points\": 10
            },
            10: {
                \"title\": \"Dein neues Selbstbild\",
                \"exercise\": \"Schreibe ein neues, realistisches und liebevolles Selbstbild. Wer bist du wirklich? Nicht zu hart, nicht zu idealisiert – einfach wahr.\",
                \"reflection\": \"Wie unterscheidet sich dieses Selbstbild von dem zu Beginn? Was hat sich verändert?\",
                \"motivation\": \"🎉 Du hast ein stärkeres Selbstbild entwickelt! Du siehst dich jetzt mit freundlicheren Augen.\",
                \"points\": 10
            }
        }
    },
    \"Verbundenheit\": {
        \"icon\": \"🤝\",
        \"description\": \"Baue tiefere und bedeutungsvollere Beziehungen auf\",
        \"color\": \"#2196F3\",
        \"expert_tip\": \"Wahre Nähe entsteht oft erst, wenn wir uns verletzlich zeigen. Das Teilen einer ehrlichen Sorge oder eines kleinen Moments der Unsicherheit ist keine Schwäche, sondern ein Akt des Vertrauens, der Ihre Beziehungen vertiefen kann.\",
        \"days\": {
            1: {
                \"title\": \"Beziehungs-Inventur\",
                \"exercise\": \"Liste alle wichtigen Menschen in deinem Leben auf. Bewerte auf einer Skala von 1-10, wie nah du dich ihnen fühlst.\",
                \"reflection\": \"Welche Beziehungen sind erfüllend? Welche möchtest du vertiefen? Welche kosten dich mehr Energie, als sie geben?\",
                \"motivation\": \"Du schaust bewusst auf deine Beziehungen. Das ist der erste Schritt zu mehr Verbundenheit!\",
                \"points\": 10
            },
            2: {
                \"title\": \"Aktives Zuhören\",
                \"exercise\": \"Führe heute ein Gespräch, in dem du nur zuhörst. Keine Ratschläge, keine Unterbrechungen – nur volle Aufmerksamkeit.\",
                \"reflection\": \"Wie schwer war es, nur zuzuhören? Was hast du über die Person gelernt?\",
                \"motivation\": \"Zuhören ist ein Geschenk. Du schenkst heute jemandem deine volle Präsenz!\",
                \"points\": 10
            },
            3: {
                \"title\": \"Verletzlichkeit zeigen\",
                \"exercise\": \"Teile heute mit einer Person, der du vertraust, eine kleine Sorge oder Unsicherheit. Nichts Dramatisches, nur ehrlich.\",
                \"reflection\": \"Wie fühlte es sich an, dich verletzlich zu zeigen? Wie hat die Person reagiert?\",
                \"motivation\": \"Verletzlichkeit ist Mut, nicht Schwäche. Du baust echte Nähe auf!\",
                \"points\": 10
            },
            4: {
                \"title\": \"Dankbarkeit ausdrücken\",
                \"exercise\": \"Schreibe oder sage 3 Menschen, wofür du ihnen dankbar bist. Sei spezifisch: 'Danke, dass du...'\",
                \"reflection\": \"Wie haben die Menschen reagiert? Wie hat es sich für dich angefühlt, Dankbarkeit auszudrücken?\",
                \"motivation\": \"Dankbarkeit vertieft Beziehungen. Du investierst in deine Verbindungen!\",
                \"points\": 10
            },
            5: {
                \"title\": \"Quality Time planen\",
                \"exercise\": \"Plane ein bewusstes Treffen mit einer Person, die dir wichtig ist. Keine Ablenkung, keine Smartphones – nur ihr beide.\",
                \"reflection\": \"Wie unterschied sich dieses Treffen von euren üblichen Interaktionen? Was hat es mit eurer Verbindung gemacht?\",
                \"motivation\": \"Qualität schlägt Quantität. Du nährst eine wichtige Beziehung!\",
                \"points\": 10
            },
            6: {
                \"title\": \"Grenzen kommunizieren\",
                \"exercise\": \"Identifiziere eine Grenze in einer Beziehung, die du setzen möchtest. Kommuniziere sie klar und liebevoll.\",
                \"reflection\": \"Wie hat die Person reagiert? Wie fühlst du dich nach dem Setzen der Grenze?\",
                \"motivation\": \"Grenzen sind gesund und notwendig. Du schützt deine Beziehungen, indem du sie setzt!\",
                \"points\": 10
            },
            7: {
                \"title\": \"Empathie üben\",
                \"exercise\": \"Wenn heute jemand etwas sagt oder tut, das dich irritiert, pausiere. Frage dich: 'Was könnte diese Person gerade durchmachen?'\",
                \"reflection\": \"Hat diese Perspektive deine Reaktion verändert? Wie hat sich Empathie angefühlt?\",
                \"motivation\": \"Empathie ist die Brücke zu echter Verbundenheit. Du übst, die Welt durch andere Augen zu sehen!\",
                \"points\": 10
            },
            8: {
                \"title\": \"Alte Verbindungen wiederbeleben\",
                \"exercise\": \"Kontaktiere heute eine Person, mit der du den Kontakt verloren hast, aber die dir wichtig war. Ein einfaches 'Hey, ich habe an dich gedacht'.\",
                \"reflection\": \"Wie hat es sich angefühlt, den Kontakt wiederherzustellen? Wie hat die Person reagiert?\",
                \"motivation\": \"Verbindungen können wiederbelebt werden. Du zeigst, dass dir Menschen wichtig sind!\",
                \"points\": 10
            },
            9: {
                \"title\": \"Konflikt konstruktiv angehen\",
                \"exercise\": \"Gibt es einen ungelösten Konflikt in deinem Leben? Überlege, wie du ihn ansprechen könntest – mit Ich-Botschaften und dem Wunsch nach Lösung.\",
                \"reflection\": \"Was hält dich davon ab, den Konflikt anzusprechen? Was wäre das Beste, das passieren könnte?\",
                \"motivation\": \"Konflikte anzugehen ist ein Zeichen von Reife. Du investierst in gesunde Beziehungen!\",
                \"points\": 10
            },
            10: {
                \"title\": \"Dein Beziehungs-Manifest\",
                \"exercise\": \"Schreibe auf, was dir in Beziehungen wichtig ist. Was brauchst du? Was kannst du geben? Wie willst du in Beziehungen sein?\",
                \"reflection\": \"Wie klar sind dir deine Beziehungswerte jetzt? Was wirst du anders machen?\",
                \"motivation\": \"🎉 Du hast Verbundenheit vertieft! Du weißt jetzt, wie du echte Nähe aufbaust.\",
                \"points\": 10
            }
        }
    },
    \"Optimismus\": {
        \"icon\": \"☀️\",
        \"description\": \"Kultiviere eine positive Lebenseinstellung ohne Realitätsverlust\",
        \"color\": \"#FFEB3B\",
        \"expert_tip\": \"Optimismus bedeutet nicht, Probleme zu ignorieren, sondern zu glauben, dass Lösungen gefunden werden können. Es ist die Überzeugung, dass Schwierigkeiten vorübergehend sind und dass Sie die Ressourcen haben, sie zu meistern.\",
        \"days\": {
            1: {
                \"title\": \"Dankbarkeits-Ritual\",
                \"exercise\": \"Schreibe jeden Abend diese Woche 3 Dinge auf, für die du heute dankbar bist. Auch winzige Dinge zählen.\",
                \"reflection\": \"Wie verändert diese Praxis deinen Blick auf den Tag? Was fällt dir auf?\",
                \"motivation\": \"Dankbarkeit trainiert dein Gehirn auf Positives. Du legst das Fundament für Optimismus!\",
                \"points\": 10
            },
            2: {
                \"title\": \"Positive Umdeutung\",
                \"exercise\": \"Denke an eine aktuelle Herausforderung. Finde 3 mögliche positive Aspekte oder Lernchancen darin.\",
                \"reflection\": \"Wie verändert sich deine Emotion zur Herausforderung durch diese Perspektive?\",
                \"motivation\": \"Du lernst, in Problemen Chancen zu sehen. Das ist die Essenz von Optimismus!\",
                \"points\": 10
            },
            3: {
                \"title\": \"Best-Case-Szenario\",
                \"exercise\": \"Für eine Situation, vor der du Angst hast, male dir das best-mögliche Szenario aus. Was wäre, wenn alles gut geht?\",
                \"reflection\": \"Wie realistisch ist dieses positive Szenario? Wie fühlt es sich an, es dir vorzustellen?\",
                \"motivation\": \"Du gibst deinem Gehirn Erlaubnis, positive Ausgänge zu erwarten. Das ist nicht naiv, sondern heilsam!\",
                \"points\": 10
            },
            4: {
                \"title\": \"Pessimismus-Detektor\",
                \"exercise\": \"Achte heute auf pessimistische Gedanken. Jedes Mal, wenn du einen bemerkst, notiere ihn und formuliere eine optimistische Alternative.\",
                \"reflection\": \"Wie oft warst du pessimistisch? Was sind deine typischen pessimistischen Muster?\",
                \"motivation\": \"Bewusstsein ist Macht. Du durchbrichst negative Denkmuster!\",
                \"points\": 10
            },
            5: {
                \"title\": \"Inspirierende Geschichten\",
                \"exercise\": \"Lies, höre oder schau dir heute eine inspirierende Geschichte von jemandem an, der Schwierigkeiten überwunden hat.\",
                \"reflection\": \"Was hat dich an dieser Geschichte berührt? Welche Lektion nimmst du mit?\",
                \"motivation\": \"Geschichten der Hoffnung nähren deinen Optimismus. Du tankst Inspiration!\",
                \"points\": 10
            },
            6: {
                \"title\": \"Zukunfts-Vision\",
                \"exercise\": \"Schreibe einen Brief aus der Zukunft (1 Jahr von jetzt). Beschreibe, wie gut es dir geht und was du alles erreicht hast.\",
                \"reflection\": \"Wie fühlte es sich an, diese positive Zukunft zu visualisieren? Was brauchst du, um dahin zu kommen?\",
                \"motivation\": \"Du erschaffst eine positive Vision. Dein Gehirn arbeitet jetzt darauf hin!\",
                \"points\": 10
            },
            7: {
                \"title\": \"Positives Selbstgespräch\",
                \"exercise\": \"Heute nur positive Selbstgespräche. Ertappst du dich bei Selbstkritik, korrigiere es sofort zu etwas Aufbauendem.\",
                \"reflection\": \"Wie oft musstest du korrigieren? Wie hat sich deine Stimmung im Laufe des Tages entwickelt?\",
                \"motivation\": \"Deine innere Stimme formt deine Realität. Du wählst jetzt bewusst Optimismus!\",
                \"points\": 10
            },
            8: {
                \"title\": \"Lächeln als Werkzeug\",
                \"exercise\": \"Lächle heute bewusst – auch ohne Grund. Schau, was es mit dir und deiner Umgebung macht.\",
                \"reflection\": \"Wie hat das Lächeln deine Stimmung beeinflusst? Wie haben andere reagiert?\",
                \"motivation\": \"Ein Lächeln verändert deine Chemie und die Welt um dich herum. Du verbreitest Positivität!\",
                \"points\": 10
            },
            9: {
                \"title\": \"Ressourcen-Check\",
                \"exercise\": \"Liste alle inneren und äußeren Ressourcen auf, die du hast, um mit Schwierigkeiten umzugehen (Fähigkeiten, Menschen, Erfahrungen).\",
                \"reflection\": \"Wie gut ausgestattet bist du wirklich? Verändert diese Liste dein Selbstvertrauen?\",
                \"motivation\": \"Du bist nicht hilflos – du hast so viele Ressourcen! Das ist der Grund für realistischen Optimismus.\",
                \"points\": 10
            },
            10: {
                \"title\": \"Dein Optimismus-Anker\",
                \"exercise\": \"Erstelle einen 'Optimismus-Anker': ein Objekt, Bild oder Zitat, das dich an deine optimistische Grundhaltung erinnert. Platziere es sichtbar.\",
                \"reflection\": \"Was hast du gewählt? Warum? Wie wirst du es nutzen, wenn es schwierig wird?\",
                \"motivation\": \"🎉 Du hast gelernt, Optimismus zu kultivieren! Du siehst jetzt Möglichkeiten, wo andere Hindernisse sehen.\",
                \"points\": 10
            }
        }
    },
    \"Konfliktlösung\": {
        \"icon\": \"🕊️\",
        \"description\": \"Entwickle Fähigkeiten für konstruktive Konfliktbewältigung\",
        \"color\": \"#E91E63\",
        \"expert_tip\": \"Konflikte sind nicht das Problem – wie wir mit ihnen umgehen, entscheidet. Gute Konfliktlösung bedeutet, die Bedürfnisse aller Beteiligten zu hören und nach Lösungen zu suchen, bei denen niemand sein Gesicht verliert.\",
        \"days\": {
            1: {
                \"title\": \"Konflikt-Muster erkennen\",
                \"exercise\": \"Reflektiere über vergangene Konflikte. Wie reagierst du typischerweise? Vermeidung, Angriff, Rückzug, Kompromiss?\",
                \"reflection\": \"Was ist dein Konflikt-Standard-Modus? Wie gut funktioniert er? Was möchtest du ändern?\",
                \"motivation\": \"Selbsterkenntnis ist der erste Schritt zu besserer Konfliktlösung. Du schaust mutig hin!\",
                \"points\": 10
            },
            2: {
                \"title\": \"Ich-Botschaften üben\",
                \"exercise\": \"Übe, Ich-Botschaften zu formulieren: 'Ich fühle X, wenn Y passiert, weil Z.' Schreibe 5 Beispiele aus deinem Leben.\",
                \"reflection\": \"Wie unterscheiden sich Ich-Botschaften von 'Du'-Vorwürfen? Wie würde das Konflikte verändern?\",
                \"motivation\": \"Du lernst, deine Bedürfnisse auszudrücken, ohne anzugreifen. Das ist Kommunikations-Gold!\",
                \"points\": 10
            },
            3: {
                \"title\": \"Perspektivwechsel\",
                \"exercise\": \"Denke an einen aktuellen oder vergangenen Konflikt. Schreibe die Situation aus der Perspektive der anderen Person.\",
                \"reflection\": \"Was siehst du jetzt, das du vorher nicht gesehen hast? Verändert das deine Emotion?\",
                \"motivation\": \"Empathie ist der Schlüssel zur Konfliktlösung. Du öffnest dein Herz für andere Sichtweisen!\",
                \"points\": 10
            },
            4: {
                \"title\": \"Pausieren lernen\",
                \"exercise\": \"Wenn du heute in eine Konfliktsituation gerätst (oder eine simulierst), übe zu pausieren, bevor du reagierst. Tief atmen, zählen, dann antworten.\",
                \"reflection\": \"Wie schwer war es zu pausieren? Was veränderte sich durch die Pause?\",
                \"motivation\": \"Zwischen Reiz und Reaktion liegt deine Macht. Du lernst, bewusst zu reagieren!\",
                \"points\": 10
            },
            5: {
                \"title\": \"Aktives Zuhören im Konflikt\",
                \"exercise\": \"Übe die Technik des 'Spiegelns': 'Wenn ich dich richtig verstehe, sagst du...' Probiere es in einem Gespräch.\",
                \"reflection\": \"Wie hat die andere Person reagiert, als du wirklich zugehört hast? Was hat es mit dem Konflikt gemacht?\",
                \"motivation\": \"Verstanden zu werden ist ein Grundbedürfnis. Du schenkst das heute jemandem!\",
                \"points\": 10
            },
            6: {
                \"title\": \"Bedürfnisse identifizieren\",
                \"exercise\": \"Bei einem Konflikt: Grabe tiefer als die Positionen. Was ist das zugrunde liegende Bedürfnis – bei dir und beim anderen?\",
                \"reflection\": \"Welches Bedürfnis steht hinter dem Konflikt? Wie könnte man beide Bedürfnisse erfüllen?\",
                \"motivation\": \"Hinter jedem Konflikt stehen Bedürfnisse. Du lernst, die Wurzel zu finden!\",
                \"points\": 10
            },
            7: {
                \"title\": \"Win-Win denken\",
                \"exercise\": \"Nimm einen Konflikt und brainstorme 5 mögliche Win-Win-Lösungen. Kreativität ist erlaubt!\",
                \"reflection\": \"Wie viele Lösungen hast du gefunden? Welche ist die beste für alle Beteiligten?\",
                \"motivation\": \"Es gibt fast immer eine Lösung, bei der alle gewinnen. Du denkst in Möglichkeiten!\",
                \"points\": 10
            },
            8: {
                \"title\": \"Entschuldigung üben\",
                \"exercise\": \"Eine echte Entschuldigung hat 3 Teile: 'Es tut mir leid für X. Ich verstehe, dass es Y verursacht hat. Ich werde Z tun.' Schreibe eine.\",
                \"reflection\": \"Wie fühlt es sich an, Verantwortung zu übernehmen? Für was in deinem Leben möchtest du dich entschuldigen?\",
                \"motivation\": \"Sich zu entschuldigen ist Stärke, nicht Schwäche. Du baust Brücken!\",
                \"points\": 10
            },
            9: {
                \"title\": \"Grenzen im Konflikt\",
                \"exercise\": \"Identifiziere, wann ein Konflikt nicht konstruktiv ist (Respektlosigkeit, Gewalt). Übe zu sagen: 'Ich möchte das klären, aber nicht so. Lass uns pausieren.'\",
                \"reflection\": \"Wo sind deine Grenzen in Konflikten? Wie kannst du sie schützen?\",
                \"motivation\": \"Nicht jeder Konflikt kann sofort gelöst werden. Du lernst, dich zu schützen!\",
                \"points\": 10
            },
            10: {
                \"title\": \"Dein Konfliktlösungs-Toolkit\",
                \"exercise\": \"Erstelle ein persönliches Toolkit: Welche 5 Strategien helfen dir in Konflikten? Schreibe sie als Notfallplan auf.\",
                \"reflection\": \"Was sind deine effektivsten Konfliktlösungs-Tools? Wie wirst du sie nutzen?\",
                \"motivation\": \"🎉 Du bist jetzt ein Friedensstifter! Du hast gelernt, Konflikte als Chance für Wachstum zu sehen.\",
                \"points\": 10
            }
        }
    }
}

# --- 3. ZUSTAND DER APP VERWALTEN (SESSION STATE) ---
def init_session_state():
    # Existing states
    if 'page' not in st.session_state: st.session_state.page = 'start'
    if 'problem' not in st.session_state: st.session_state.problem = \"\"
    if 'problem_category' not in st.session_state: st.session_state.problem_category = \"Wähle eine Kategorie\"
    if 'options' not in st.session_state: st.session_state.options = [\"\", \"\"]
    if 'selected_values' not in st.session_state: st.session_state.selected_values = []
    if 'values_rating' not in st.session_state: st.session_state.values_rating = {}
    if 'emotions' not in st.session_state: st.session_state.emotions = \"\"
    if 'pro_a' not in st.session_state: st.session_state.pro_a = \"\"
    if 'contra_a' not in st.session_state: st.session_state.contra_a = \"\"
    if 'pro_b' not in st.session_state: st.session_state.pro_b = \"\"
    if 'contra_b' not in st.session_state: st.session_state.contra_b = \"\"
    if 'creative_options' not in st.session_state: st.session_state.creative_options = \"\"
    if 'future_scenario_a' not in st.session_state: st.session_state.future_scenario_a = \"\"
    if 'future_scenario_b' not in st.session_state: st.session_state.future_scenario_b = \"\"
    if 'first_step' not in st.session_state: st.session_state.first_step = \"\"
    if 'resilience_answers' not in st.session_state: st.session_state.resilience_answers = {}
    if 'resilience_score' not in st.session_state: st.session_state.resilience_score = None
    if 'resilience_analysis' not in st.session_state: st.session_state.resilience_analysis = None
    if 'processing_analysis' not in st.session_state: st.session_state.processing_analysis = False
    
    # New states for Resilience Paths
    if 'total_points' not in st.session_state: st.session_state.total_points = 0
    if 'current_path' not in st.session_state: st.session_state.current_path = None
    if 'current_day' not in st.session_state: st.session_state.current_day = 1
    if 'path_progress' not in st.session_state: st.session_state.path_progress = {}
    if 'completed_paths' not in st.session_state: st.session_state.completed_paths = []
    if 'trophies' not in st.session_state: st.session_state.trophies = []
    if 'day_completed' not in st.session_state: st.session_state.day_completed = False


init_session_state()

def next_page(page_name):
    st.session_state.page = page_name

def reset_app():
    st.session_state.clear()
    init_session_state()

# --- 4. DYNAMISCHE INHALTE FÜR JEDE KATEGORIE (DECISION JOURNEY) ---
category_content = {
    \"Karriere & Beruf\": {
        \"values\": [\"Finanzielle Sicherheit\", \"Wachstum\", \"Autonomie\", \"Einfluss\", \"Anerkennung\", \"Work-Life-Balance\"],
        \"cognitive_biases\": {
            \"title\": \"Häufige Denkfehler in der Karriere\",
            \"biases\": [
                (\"Verlustaversion\", \"Konzentriere ich mich mehr auf das, was ich im aktuellen Job verlieren könnte, als auf das, was ich im neuen gewinnen könnte?\"),
                (\"Ankereffekt\", \"Hänge ich zu sehr am ersten Gehaltsangebot oder einer ersten Beförderung fest, die ich erhalten habe, und hindert mich das daran, eine bessere Gelegenheit zu erkennen?\"),
                (\"Bestätigungsfehler\", \"Suche ich nur nach Informationen, die meine Entscheidung für oder gegen einen Job bestätigen, und ignoriere ich gegenteilige Informationen?\")
            ]
        },
    },
    \"Persönliches Wachstum\": {
        \"values\": [\"Selbstverwirklichung\", \"Kreativität\", \"Lernen\", \"Soziale Bindungen\", \"Entwicklung\", \"Freiheit\"],
        \"cognitive_biases\": {
            \"title\": \"Häufige Denkfehler bei persönlichem Wachstum\",
            \"biases\": [
                (\"Status-quo-Verzerrung\", \"Ziehe ich die einfache Option vor, weil ich Angst vor Veränderungen habe, auch wenn die neue Option mich wachsen lässt?\"),
                (\"Bestätigungsfehler\", \"Suche ich nur nach Informationen, die meine Überzeugung bestätigen, dass eine neue Fähigkeit zu schwer zu erlernen ist?\"),
                (\"Verfügbarkeitsheuristik\", \"Stütze ich meine Entscheidung nur auf leicht verfügbare, spektakuläre Geschichten, statt auf realistischere Fakten?\")
            ]
        },
    },
    \"Beziehungen & Familie\": {
        \"values\": [\"Soziale Bindungen\", \"Harmonie\", \"Vertrauen\", \"Empathie\", \"Stabilität\", \"Zugehörigkeit\"],
        \"cognitive_biases\": {
            \"title\": \"Häufige Denkfehler in Beziehungen\",
            \"biases\": [
                (\"Rosinenpicken (Cherry Picking)\", \"Ignoriere ich alle negativen Aspekte und konzentriere ich mich nur auf die guten, um eine schwierige Situation zu vermeiden?\"),
                (\"Irrglaube an versunkene Kosten (Sunk Cost Fallacy)\", \"Bleibe ich in einer Beziehung oder Situation, nur weil ich schon so viel Zeit und Energie investiert habe, anstatt nach vorne zu schauen?\"),
                (\"Bestätigungsfehler\", \"Höre ich nur auf Freunde, die meine Meinung teilen, und vermeide ich Gespräche, die mich herausfordern?\")
            ]
        },
    }
}

# Fragen für den Resilienz-Fragebogen (jetzt alle 33 Fragen)
resilience_questions = [
    \"Ich bin mir meiner Stärken und Schwächen bewusst.\",
    \"Ich kenne meine Emotionen und kann sie benennen.\",
    \"Ich erkenne, wie meine Gedanken mein Verhalten beeinflussen.\",
    \"Ich bin überzeugt, dass ich schwierige Situationen meistern kann.\",
    \"Ich glaube an meine Fähigkeit, Probleme zu lösen.\",
    \"Ich fühle mich kompetent, um meine Ziele zu erreichen.\",
    \"Ich habe Menschen, auf die ich mich in Krisen verlassen kann.\",
    \"Ich suche aktiv den Kontakt zu Freunden und Familie, wenn ich Unterstützung brauche.\",
    \"Ich fühle mich in meinen Beziehungen geborgen und angenommen.\",
    \"Ich kann mit starken Gefühlen wie Wut oder Trauer umgehen, ohne dass sie mich überfordern.\",
    \"Ich finde gesunde Wege, um mich nach einem stressigen Tag zu entspannen.\",
    \"Ich erlaube mir, alle meine Gefühle zu spüren, ohne sie zu bewerten.\",
    \"Ich habe Techniken, um mich in stressigen Momenten zu beruhigen.\",
    \"Ich kann Prioritäten setzen, um Stress zu reduzieren.\",
    \"Ich weiß, wie ich meine Energiereserven wieder aufladen kann.\",
    \"Ich gehe Problemen aktiv und systematisch an, anstatt sie zu ignorieren.\",
    \"Ich kann eine Situation aus verschiedenen Perspektiven betrachten, um eine Lösung zu finden.\",
    \"Ich bin kreativ in der Suche nach neuen Lösungen.\",
    \"Ich bin optimistisch, was meine Zukunft angeht.\",
    \"Ich kann mir positive Entwicklungen für mein Leben vorstellen.\",
    \"Ich habe klare Ziele, die mir Orientierung geben.\",
    \"Ich kann Dinge akzeptieren, die ich nicht ändern kann.\",
    \"Ich vergebe mir selbst für Fehler, die ich gemacht habe.\",
    \"Ich nehme Herausforderungen als Teil des Lebens an.\",
    \"Ich finde meine Handlungen auch in schwierigen Zeiten sinnvoll.\",
    \"Ich spüre eine Verbindung zu etwas Größerem als mir selbst.\",
    \"Meine Werte leiten mich durchs Leben.\",
    \"Ich bin offen für neue Ideen und unkonventionelle Lösungen.\",
    \"Ich nutze meine Vorstellungskraft, um aus einer schwierigen Situation herauszukommen.\",
    \"Ich kann mich von starren Denkmustern lösen.\",
    \"Ich kann auch in schwierigen Situationen noch lachen.\",
    \"Ich nutze Humor als Ventil, um Anspannung zu lösen.\",
    \"Ich kann über mich selbst lachen, ohne mich zu verurteilen.\"
]

# Vorab definierte Analysen basierend auf dem Score (als Ersatz für die API)
def get_canned_analysis(score, max_score):
    if score <= max_score * 0.4:
        return \"\"\"
**Deine Resilienz: Fundament aufbauen**

Deine aktuelle Punktzahl deutet darauf hin, dass du dich in einigen Bereichen deiner Resilienz noch im Aufbau befindest. Das ist eine wichtige Erkenntnis! Es zeigt, dass du das Potenzial hast, deine Widerstandsfähigkeit gezielt zu stärken und dich besser auf künftige Herausforderungen vorzubereiten. Die Arbeit an diesen Faktoren kann einen großen Unterschied in deinem Wohlbefinden machen.

**Tipps zur Stärkung deiner Resilienz:**

1.  **Selbstwahrnehmung & Selbstfürsorge**: Beginne damit, dich selbst besser kennenzulernen. Frage dich, wie du dich fühlst und was du wirklich brauchst. Integriere kleine Rituale in deinen Alltag, die nur dir gewidmet sind, sei es ein 10-minütiger Spaziergang, eine Tasse Tee in Ruhe oder ein heißes Bad.
2.  **Soziale Beziehungen aktiv pflegen**: Suche den Kontakt zu Menschen, die dir guttun und denen du vertraust. Ein offenes Gespräch über deine Gefühle kann eine enorme Last von deinen Schultern nehmen.
3.  **Realistische Ziele setzen**: Große Probleme können überwältigend wirken. Zerlege sie in kleine, überschaubare Schritte. Wenn du zum Beispiel eine neue Fähigkeit lernen willst, fange mit einem 15-minütigen Online-Tutorial an, anstatt direkt einen ganzen Kurs zu planen.
4.  **Umgang mit Gefühlen lernen**: Gefühle sind Wegweiser. Versuche, sie ohne Urteil zu beobachten, anstatt sie zu unterdrücken. Ein Emotionstagebuch kann dir helfen, Muster zu erkennen.
5.  **Perspektivwechsel üben**: Wenn eine Situation aussichtslos erscheint, versuche sie aus einem anderen Blickwinkel zu betrachten. Wie würde ein Freund die Situation sehen? Welche Lektion kannst du daraus lernen?
\"\"\"
    elif score <= max_score * 0.7:
        return \"\"\"
**Deine Resilienz: Solides Fundament**

Deine Punktzahl zeigt, dass du bereits über ein solides Fundament an Resilienz verfügst. Du bist in der Lage, mit Herausforderungen umzugehen und hast bereits einige der wichtigsten Resilienzfaktoren in deinem Leben integriert. Das ist eine großartige Ausgangslage, um deine Fähigkeiten gezielt weiter auszubauen.

**Tipps zur Stärkung deiner Resilienz:**

1.  **Soziales Netz bewusst stärken**: Pflege deine Beziehungen aktiv. Organisiere regelmäßige Treffen, sei ein guter Zuhörer und biete deine Hilfe an. Ein starkes soziales Netz ist dein wichtigster Puffer in schwierigen Zeiten.
2.  **Kreative Problemlösung**: Wenn du vor einem Problem stehst, gehe es nicht nur auf dem naheliegendsten Weg an. Brainstorme unkonventionelle Lösungen, denke \"out of the box\". Manchmal liegt die Lösung in einer völlig unerwarteten Idee.
3.  **Sinn und Werte vertiefen**: Reflektiere regelmäßig darüber, was dir im Leben wirklich wichtig ist. Wenn du deine Handlungen an deinen Werten ausrichtest, gewinnst du an innerer Stärke und Orientierung. Überlege, wie du dein Handeln noch besser mit deinen tiefsten Überzeugungen in Einklang bringen kannst.
4.  **Optimismus kultivieren**: Übe dich darin, auch in schwierigen Situationen nach den positiven Aspekten zu suchen, ohne die Realität zu leugnen. Welche Lektion kannst du aus dieser Erfahrung lernen? Betrachte Krisen als Wachstumschancen.
5.  **Humor einsetzen**: Nimm das Leben nicht immer zu ernst. Humor ist ein mächtiges Werkzeug, um Anspannung zu lösen und eine positive Perspektive zu bewahren. Suche bewusst nach Gelegenheiten zum Lachen, sei es durch Filme, Witze oder einfach das Teilen lustiger Anekdoten.
\"\"\"
    else:
        return \"\"\"
**Deine Resilienz: Hohe Widerstandsfähigkeit**

Herzlichen Glückwunsch! Deine hohe Punktzahl zeigt, dass du über eine starke Resilienz verfügst. Du bist gut gerüstet, um mit Rückschlägen und Krisen umzugehen und kannst diese sogar als Chance für Wachstum nutzen. Deine Fähigkeiten in Bereichen wie Selbstwahrnehmung, Problemlösung und sozialen Beziehungen sind gut ausgeprägt.

**Tipps zur Aufrechterhaltung und Weiterentwicklung:**

1.  **Mentoring und Wissensaustausch**: Nutze deine Stärke, um auch anderen zu helfen. Indem du deine Erfahrungen teilst, stärkst du nicht nur dein eigenes Fundament, sondern unterstützt auch dein Umfeld und schaffst ein Netzwerk der gegenseitigen Unterstützung.
2.  **Aktivität in den Lebensbereichen**: Setze dir bewusst Ziele in Bereichen, die du vielleicht bisher vernachlässigt hast. Ob es darum geht, ein neues Hobby zu beginnen, eine neue Sprache zu lernen oder dich ehrenamtlich zu engagieren – du hast die Fähigkeit, dich anzupassen und zu wachsen.
3.  **Lebenssinn vertiefen**: Reflektiere, wie deine täglichen Handlungen zu deinem größeren Lebenssinn beitragen. Wenn du eine starke Sinnorientierung hast, kannst du auch die größten Stürme überstehen, ohne dein Ziel aus den Augen zu verlieren.
4.  **Kreativität als Lebenshaltung**: Nutze deine Kreativität nicht nur zur Problemlösung, sondern auch als Ausdruck deiner Persönlichkeit. Malen, schreiben, Musik machen oder einfach nur das Finden unkonventioneller Wege im Alltag können deine innere Stärke weiter festigen.
5.  **Humor als Resilienzanker**: Integriere Humor bewusst in deinen Alltag. Lache über dich selbst, teile lustige Momente mit anderen und nutze Humor, um Anspannung zu reduzieren. Humor ist eine der stärksten Waffen gegen Widrigkeiten.
\"\"\"

# --- 5. SEITEN-INHALT RENDERN ---

def render_start_page():
    with st.container():
        st.title(\"VitaBoost\")
        st.image(\"https://placehold.co/1200x400/FFF8E1/E2B060?text=Stärke+deine+Entscheidungen%2C+stärke+dein+Leben\")
        st.markdown(\"Stärke deine Entscheidungen, stärke dein Leben. Wähle den passenden Pfad für deine Situation.\")
        
        # Punktestand anzeigen
        if st.session_state.total_points > 0:
            st.markdown(f\"### 🏆 Deine Gesamtpunkte: **{st.session_state.total_points}**\")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(\"### Entscheidungsreise\")
            st.markdown(\"Strukturiere deine Gedanken und Gefühle, um eine fundierte Entscheidung zu treffen.\")
            st.button(\"Starte die Entscheidungsreise\", on_click=next_page, args=['step_1'], key=\"start_decision\")

        with col2:
            st.markdown(\"### Werte-Reflexion\")
            st.markdown(\"Du steckst gerade in einer Krise? Finden wir heraus was deine Resilienzfaktoren sein könnten.\")
            st.button(\"Starte die Werte-Reflexion\", on_click=next_page, args=['wert_reflexion'], key=\"start_reflection\")
        
        with col3:
            st.markdown(\"### Resilienz-Pfad\")
            st.markdown(\"Stärke deine Resilienz mit 10-Tages-Challenges zu verschiedenen Lebensthemen.\")
            st.button(\"Starte den Resilienz-Pfad\", on_click=next_page, args=['resilience_path_selection'], key=\"start_path\")
        
        # Trophäen-Galerie Button
        if st.session_state.trophies:
            st.markdown(\"---\")
            st.button(\"🏆 Meine Trophäen ansehen\", on_click=next_page, args=['trophy_gallery'], key=\"view_trophies\")

# --- RESILIENCE PATH PAGES ---

def render_resilience_path_selection():
    st.title(\"🌱 Wähle deinen Resilienz-Pfad\")
    st.markdown(\"Jeder Pfad enthält eine 10-Tages-Challenge mit täglichen Übungen, Reflexionen und Expertentipps.\")
    
    # Punktestand
    st.markdown(f\"### 🏆 Deine Gesamtpunkte: **{st.session_state.total_points}**\")
    
    # Pfade in 2 Spalten anzeigen
    paths = list(RESILIENCE_PATHS.keys())
    for i in range(0, len(paths), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(paths):
                path_name = paths[i + j]
                path_data = RESILIENCE_PATHS[path_name]
                
                with col:
                    with st.container():
                        # Icon und Titel
                        st.markdown(f\"## {path_data['icon']} {path_name}\")
                        st.markdown(path_data['description'])
                        
                        # Fortschritt anzeigen
                        progress = st.session_state.path_progress.get(path_name, 0)
                        if progress > 0:
                            st.progress(progress / 10)
                            st.markdown(f\"**Fortschritt: {progress}/10 Tage**\")
                        
                        # Status
                        if path_name in st.session_state.completed_paths:
                            st.success(\"✅ Abgeschlossen!\")
                        elif progress > 0:
                            st.info(f\"📍 In Bearbeitung (Tag {progress})\")
                        
                        # Button zum Starten/Fortsetzen
                        button_text = \"Fortsetzen\" if progress > 0 else \"Starten\"
                        if st.button(button_text, key=f\"path_{path_name}\"):
                            st.session_state.current_path = path_name
                            st.session_state.current_day = progress + 1 if progress < 10 else 1
                            st.session_state.day_completed = False
                            next_page('resilience_path_day')
    
    st.markdown(\"---\")
    st.button(\"🏠 Zurück zur Startseite\", on_click=next_page, args=['start'])

def render_resilience_path_day():
    if not st.session_state.current_path:
        next_page('resilience_path_selection')
        return
    
    path_name = st.session_state.current_path
    path_data = RESILIENCE_PATHS[path_name]
    current_day = st.session_state.current_day
    day_data = path_data['days'][current_day]
    
    # Header
    st.title(f\"{path_data['icon']} {path_name}\")
    st.markdown(f\"### Tag {current_day}/10: {day_data['title']}\")
    
    # Fortschrittsbalken
    progress_percent = (current_day - 1) / 10 * 100
    st.markdown(f\"\"\"
    <div class=\"progress-container\">
        <div class=\"progress-bar\" style=\"width: {progress_percent}%\">
            {int(progress_percent)}%
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    # Expertentipp am Anfang (Tag 1) oder bei besonderen Tagen
    if current_day == 1:
        st.markdown(f\"\"\"
        <div class=\"expert-tip\">
            <strong>💡 Expertentipp für diesen Pfad:</strong><br>
            {path_data['expert_tip']}
        </div>
        \"\"\", unsafe_allow_html=True)
    
    # Tagesübung
    with st.container():
        st.markdown(\"#### 📋 Deine heutige Übung\")
        st.markdown(day_data['exercise'])
    
    # Reflexionsfragen
    with st.container():
        st.markdown(\"#### 🤔 Reflexion\")
        st.markdown(day_data['reflection'])
        
        reflection_text = st.text_area(
            \"Deine Gedanken und Erkenntnisse:\",
            height=150,
            key=f\"reflection_{path_name}_{current_day}\"
        )
    
    # Tag abschließen
    if not st.session_state.day_completed:
        if st.button(\"✅ Tag abschließen\", key=\"complete_day\"):
            # Punkte vergeben
            st.session_state.total_points += day_data['points']
            
            # Fortschritt aktualisieren
            st.session_state.path_progress[path_name] = current_day
            
            # Wenn letzter Tag, Pfad als abgeschlossen markieren
            if current_day == 10:
                if path_name not in st.session_state.completed_paths:
                    st.session_state.completed_paths.append(path_name)
                    # Trophäe hinzufügen
                    st.session_state.trophies.append({
                        'path': path_name,
                        'icon': path_data['icon'],
                        'completed_date': time.strftime(\"%d.%m.%Y\")
                    })
            
            st.session_state.day_completed = True
            st.rerun()
    
    # Motivierender Spruch nach Abschluss
    if st.session_state.day_completed:
        st.success(\"🎉 Tag abgeschlossen!\")
        st.markdown(f\"\"\"
        <div style=\"background: linear-gradient(135deg, #E2B060 0%, #FFD700 100%); 
                    border-radius: 12px; padding: 20px; text-align: center; color: white; margin: 20px 0;\">
            <h3 style=\"color: white; margin: 0;\">💫 {day_data['motivation']}</h3>
            <p style=\"margin-top: 10px; font-size: 18px;\"><strong>+{day_data['points']} Punkte!</strong></p>
            <p>Gesamtpunkte: {st.session_state.total_points}</p>
        </div>
        \"\"\", unsafe_allow_html=True)
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if current_day < 10:
                if st.button(\"➡️ Nächster Tag\", key=\"next_day\"):
                    st.session_state.current_day += 1
                    st.session_state.day_completed = False
                    st.rerun()
            else:
                if st.button(\"🏆 Pfad abgeschlossen!\", key=\"path_completed\"):
                    next_page('resilience_path_selection')
        
        with col2:
            st.button(\"🏠 Zurück zur Übersicht\", on_click=next_page, args=['resilience_path_selection'], key=\"back_to_paths\")

def render_trophy_gallery():
    st.title(\"🏆 Deine Trophäen-Galerie\")
    st.markdown(f\"### Gesamtpunkte: **{st.session_state.total_points}**\")
    
    if not st.session_state.trophies:
        st.info(\"Du hast noch keine Trophäen gesammelt. Schließe einen Resilienz-Pfad ab, um deine erste Trophäe zu erhalten!\")
    else:
        st.markdown(\"---\")
        st.markdown(\"### 🎖️ Abgeschlossene Pfade\")
        
        # Trophäen in Grid anzeigen
        cols = st.columns(3)
        for idx, trophy in enumerate(st.session_state.trophies):
            with cols[idx % 3]:
                st.markdown(f\"\"\"
                <div class=\"trophy-card\">
                    <div class=\"trophy-icon\">{trophy['icon']}</div>
                    <h3 style=\"color: white; margin: 10px 0;\">{trophy['path']}</h3>
                    <p style=\"color: white; margin: 0;\">Abgeschlossen am<br>{trophy['completed_date']}</p>
                </div>
                \"\"\", unsafe_allow_html=True)
        
        # Statistiken
        st.markdown(\"---\")
        st.markdown(\"### 📊 Deine Statistiken\")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(\"Abgeschlossene Pfade\", len(st.session_state.completed_paths))
        with col2:
            total_days = sum([st.session_state.path_progress.get(p, 0) for p in RESILIENCE_PATHS.keys()])
            st.metric(\"Absolvierte Tage\", total_days)
        with col3:
            st.metric(\"Gesammelte Punkte\", st.session_state.total_points)
    
    st.markdown(\"---\")
    st.button(\"🏠 Zurück zur Startseite\", on_click=next_page, args=['start'])

# --- EXISTING PAGES (DECISION JOURNEY & REFLECTION) ---

def render_wert_reflexion_page():
    st.title(\"Werte-Reflexion & Das große Bild\")
    st.markdown(\"\"\"
    Dies ist ein Bereich mit Potenzial, um **deine täglichen Handlungen mit deinen tiefsten Werten und deinem Lebenssinn in Einklang zu bringen**.
    \"\"\")

    st.subheader(\"Strategien zur Verbesserung:\")
    
    st.markdown(\"\"\"
    **1. Werte identifizieren:**
    Nehmen Sie sich Zeit, um zu identifizieren, was Ihnen wirklich wichtig ist. Schreiben Sie Ihre zentralen Werte auf, wie z.B. Familie, Ehrlichkeit, Kreativität oder Erfolg.
    \"\"\")
    
    st.markdown(\"\"\"
    **2. Zusammenhänge verstehen:**
    Wenn Sie mit einem kleinen Problem konfrontiert sind, versuchen Sie, es in einen größeren Kontext zu stellen. Versuchen Sie, Verhaltensweisen von Menschen oder Ereignisse aus einem anderen Blickwinkel zu betrachten.
    \"\"\")
    
    st.markdown(\"\"\"
    **3. Sinn finden:**
    Suchen Sie nach Wegen, wie Sie Ihren Alltag als sinnvoller empfinden können, z.B. indem Sie Ihre Arbeit mit Ihren persönlichen Werten verknüpfen.
    \"\"\")
    if st.button(\"Zurück zur Startseite\"):
      next_page('start')

def render_step_1():
    st.title(\"Step 1: Dein Problem & deine Optionen\")
    
    with st.container():
        st.markdown(\"#### Problem und Kategorie\")
        st.session_state.problem = st.text_area(
            \"Was ist die Entscheidung, die dich beschäftigt?\",
            value=st.session_state.problem,
            key=\"problem_input\",
            height=100
        )
        
        options = [\"Wähle eine Kategorie\"] + list(category_content.keys())
        try:
            current_index = options.index(st.session_state.problem_category)
        except ValueError:
            current_index = 0
        st.session_state.problem_category = st.selectbox(
            \"Kategorie:\",
            options=options,
            index=current_index
        )
    
    with st.container():
        st.markdown(\"#### Optionen\")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.options[0] = st.text_area(\"Option A:\", value=st.session_state.options[0], height=100, key=\"option_a_input\")
        with col2:
            st.session_state.options[1] = st.text_area(\"Option B:\", value=st.session_state.options[1], height=100, key=\"option_b_input\")
    
    is_valid = all([st.session_state.problem, st.session_state.options[0], st.session_state.options[1], st.session_state.problem_category != \"Wähle eine Kategorie\"])
    if st.button(\"Weiter\", disabled=not is_valid):
        next_page('step_2')

def render_step_2():
    st.title(\"Step 2: Werte & Motivation\")
    selected_category = st.session_state.problem_category
    all_values = category_content.get(selected_category, {}).get(\"values\", [\"Sicherheit\", \"Freiheit\", \"Entwicklung\"])
    
    with st.container():
        st.markdown(f\"#### Psychologische Werte\")
        st.markdown(f\"Wähle alle Werte aus, die für deine Entscheidung in der Kategorie **{selected_category}** relevant sind.\")
        
        st.session_state.selected_values = []
        cols = st.columns(3)
        for i, value in enumerate(all_values):
            col = cols[i % 3]
            if col.checkbox(value, key=f\"checkbox_{value}\"):
                st.session_state.selected_values.append(value)

    if st.session_state.selected_values:
        with st.container():
            st.markdown(\"#### Werte-Bewertung (Deine Entscheidungsmatrix)\")
            st.markdown(\"Bewerte auf einer Skala von 1 bis 10, wie gut jede Option deine gewählten Werte erfüllt.\")
            st.markdown(\"Die Punktzahl, die du hier vergibst, **gewichtet** automatisch die Wichtigkeit der Werte für deine endgültige Entscheidung.\")
            for value in st.session_state.selected_values:
                st.subheader(f\"Wert: {value}\")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.session_state.values_rating[f\"{value}_A\"] = st.slider(
                        f\"Option A: {st.session_state.options[0]}\",
                        0, 10, st.session_state.values_rating.get(f\"{value}_A\", 5), key=f\"slider_a_{value}\"
                    )
                with col_b:
                    st.session_state.values_rating[f\"{value}_B\"] = st.slider(
                        f\"Option B: {st.session_state.options[1]}\",
                        0, 10, st.session_state.values_rating.get(f\"{value}_B\", 5), key=f\"slider_b_{value}\"
                    )

    if st.button(\"Weiter\"):
        if not st.session_state.selected_values:
            st.warning(\"Bitte wähle mindestens einen Wert aus, bevor du fortfährst.\")
        else:
            next_page('step_3')
    
def render_step_3():
    st.title(\"Step 3: Emotionen & Denkfehler\")
    with st.container():
        st.markdown(\"#### Dein Bauchgefühl (Der 'Rote Hut' von Edward de Bono)\")
        st.markdown(\"Schreibe auf, welche Gefühle und intuitiven Gedanken du zu den Optionen hast. Es geht nicht um Logik, sondern um Emotionen.\")
        st.session_state.emotions = st.text_area(\"Deine Gedanken:\", value=st.session_state.emotions, height=150)
    
    selected_content = category_content.get(st.session_state.problem_category, {})
    biases = selected_content.get(\"cognitive_biases\", {}).get(\"biases\", [])
    
    if biases:
        with st.container():
            st.markdown(\"#### Reflektiere über Denkfehler\")
            for bias_title, bias_question in biases:
                with st.expander(f\"**{bias_title}**\"):
                    st.markdown(bias_question)

    if st.button(\"Weiter\"):
        next_page('step_4')

def render_step_4():
    st.title(\"Step 4: Pro/Contra & Zukunft\")
    
    with st.container():
        st.markdown(f\"#### Vorteile (Der 'Gelbe Hut' von Edward de Bono)\")
        st.session_state.pro_a = st.text_area(
            f\"Was spricht für Option A: '{st.session_state.options[0]}'?\",
            value=st.session_state.pro_a,
            key=\"pro_a_area\", height=150
        )
        st.session_state.pro_b = st.text_area(
            f\"Was spricht für Option B: '{st.session_state.options[1]}'?\",
            value=st.session_state.pro_b,
            key=\"pro_b_area\", height=150
        )
    
    with st.container():
        st.markdown(f\"#### Nachteile (Der 'Schwarze Hut' von Edward de Bono)\")
        st.session_state.contra_a = st.text_area(
            f\"Was spricht gegen Option A: '{st.session_state.options[0]}'?\",
            value=st.session_state.contra_a,
            key=\"contra_a_area\", height=150
        )
        st.session_state.contra_b = st.text_area(
            f\"Was spricht gegen Option B: '{st.session_state.options[1]}'?\",
            value=st.session_state.contra_b,
            key=\"contra_b_area\", height=150
        )
        
    with st.container():
        st.markdown(\"#### Kreative Optionen (Der 'Grüne Hut' von Edward de Bono)\")
        st.markdown(\"Gibt es noch andere, unkonventionelle Optionen, die du bisher nicht in Betracht gezogen hast? Schreibe sie hier auf.\")
        st.session_state.creative_options = st.text_area(
            \"Andere Ideen:\",
            value=st.session_state.creative_options,
            key=\"creative_options_area\", height=150
        )

    with st.container():
        st.markdown(f\"#### Zukunftsszenario (nach Jeff Bezos)\")
        st.markdown(\"Stelle dir vor, du bist 80 Jahre alt. Welche Entscheidung würdest du am meisten bereuen? Das Regret Minimization Framework hilft dir, aus einer langfristigen Perspektive zu entscheiden.\")
        st.session_state.future_scenario_a = st.text_area(
            f\"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option A entscheidest?\",
            value=st.session_state.future_scenario_a,
            key=\"scenario_a\", height=200
        )
        st.session_state.future_scenario_b = st.text_area(
            f\"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option B entscheidest?\",
            value=st.session_state.future_scenario_b,
            key=\"scenario_b\", height=200
        )

    if st.button(\"Weiter\"):
        next_page('step_5')

def render_step_5():
    st.title(\"Step 5: Zusammenfassung\")
    
    with st.container():
        st.markdown(\"#### Übersicht\")
        st.subheader(\"Deine Entscheidung:\")
        st.info(st.session_state.problem)
        st.subheader(\"Deine Optionen:\")
        st.write(f\"**Option A:** {st.session_state.options[0]}\")
        st.write(f\"**Option B:** {st.session_state.options[1]}\")

    if st.session_state.selected_values:
        with st.container():
            st.markdown(\"#### Quantitative Auswertung (nach Werten):\")
            data = []
            score_a = 0
            score_b = 0
            for value in st.session_state.selected_values:
                rating_a = st.session_state.values_rating.get(f\"{value}_A\", 0)
                rating_b = st.session_state.values_rating.get(f\"{value}_B\", 0)
                score_a += rating_a
                score_b += rating_b
                data.append({
                    \"value\": value,
                    \"option\": st.session_state.options[0],
                    \"rating\": rating_a
                })
                data.append({
                    \"value\": value,
                    \"option\": st.session_state.options[1],
                    \"rating\": rating_b
                })
            
            df = pd.DataFrame(data)
            if not df.empty:
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('value', title='Werte'),
                    y=alt.Y('rating', title='Bewertung (1-10)'),
                    color=alt.Color('option', legend=alt.Legend(title=\"Option\")),
                    column=alt.Column('option', header=alt.Header(titleOrient=\"bottom\"))
                ).properties(
                    title=\"Werte-Bewertung im Vergleich\"
                )
                
                st.altair_chart(chart, use_container_width=True)
                
                st.write(f\"**Gesamtpunktzahl Option A:** {score_a}\")
                st.write(f\"**Gesamtpunktzahl Option B:** {score_b}\")

    with st.container():
        st.markdown(\"#### Deine Gedanken & Szenarien:\")
        st.write(f\"**Vorteile für {st.session_state.options[0]}:**\")
        st.write(st.session_state.pro_a)
        st.write(f\"**Nachteile für {st.session_state.options[0]}:**\")
        st.write(st.session_state.contra_a)
        st.write(f\"**Vorteile für {st.session_state.options[1]}:**\")
        st.write(st.session_state.pro_b)
        st.write(f\"**Nachteile für {st.session_state.options[1]}:**\")
        st.write(st.session_state.contra_b)
        st.write(f\"**Zukunftsszenario {st.session_state.options[0]}:**\")
        st.write(st.session_state.future_scenario_a)
        st.write(f\"**Zukunftsszenario {st.session_state.options[1]}:**\")
        st.write(st.session_state.future_scenario_b)

        if st.session_state.creative_options:
            st.markdown(\"#### Weitere Ideen (Der 'Grüne Hut')\")
            st.write(st.session_state.creative_options)
    
    with st.container():
        st.markdown(\"#### Dein erster konkreter Schritt (Der 'Blaue Hut' & SMART-Ziele)\")
        st.markdown(\"\"\"
        Dieser Hut hilft dir, den Prozess zu planen. Um deinen ersten Schritt umsetzbar zu machen, nutze die **SMART-Methode**:
        - **S**pezifisch: Was genau willst du tun?
        - **M**essbar: Woran erkennst du, dass du dein Ziel erreicht hast?
        - **A**ttraktiv: Warum ist dir das Ziel wichtig?
        - **R**ealistisch: Ist das Ziel erreichbar?
        - **T**erminiert: Bis wann willst du es umsetzen?
        \"\"\")
        st.session_state.first_step = st.text_input(
            \"Dein erster konkreter SMART-Schritt:\",
            value=st.session_state.first_step
        )
        if st.button(\"Entscheidung abschließen\"):
            st.success(\"🎉 Deine Entscheidungsreise wurde abgeschlossen!\")

    st.button(\"Neue Entscheidungsreise starten\", on_click=reset_app)

def render_resilience_questions_page():
    st.title(\"Resilienz-Fragebogen\")
    st.markdown(\"Bewerte auf einer Skala von **1 (stimme gar nicht zu)** bis **5 (stimme voll und ganz zu)**, wie sehr die folgenden Aussagen auf dich zutreffen.\")

    for i, question in enumerate(resilience_questions):
        st.session_state.resilience_answers[i] = st.slider(
            question,
            1, 5, st.session_state.resilience_answers.get(i, 3), key=f\"resilience_q_{i}\"
        )

    if st.button(\"Fragebogen abschließen\"):
        with st.spinner(\"Deine Punktzahl wird berechnet... bitte habe einen kleinen Moment Geduld.\"):
            time.sleep(1)
            st.session_state.resilience_score = sum(st.session_state.resilience_answers.values())
        
        next_page('resilience_results')

def render_resilience_results_page():
    st.title(\"Deine Resilienz-Analyse\")
    st.warning(\"Disclaimer: Dieser Fragebogen ist ein nicht-klinisches Werkzeug zur Selbsterkenntnis und ersetzt keine professionelle psychologische Beratung.\")
    
    if st.session_state.resilience_score is None:
        st.warning(\"Bitte fülle zuerst den Fragebogen aus.\")
        if st.button(\"Zum Fragebogen zurückkehren\"):
            next_page('wert_reflexion')
        return

    total_score = st.session_state.resilience_score
    max_score = len(resilience_questions) * 5
    st.markdown(f\"**Deine Gesamtpunktzahl:** **{total_score}** von **{max_score}**\")
    
    st.session_state.resilience_analysis = get_canned_analysis(total_score, max_score)
    
    if st.session_state.resilience_analysis:
        st.markdown(st.session_state.resilience_analysis, unsafe_allow_html=True)

    if st.button(\"Neue Reflexion starten\"):
        reset_app()

def render_bottom_nav():
    nav_html = f\"\"\"
    <div class=\"bottom-nav\">
        <a href=\"?page=start\" class=\"nav-item {'active' if st.session_state.page == 'start' else ''}\">
            <span class=\"icon\">🏠</span> Home
        </a>
        <a href=\"?page=step_1\" class=\"nav-item {'active' if st.session_state.page in ['step_1', 'step_2', 'step_3', 'step_4', 'step_5'] else ''}\">
            <span class=\"icon\">🧠</span> Decide
        </a>
        <a href=\"?page=wert_reflexion\" class=\"nav-item {'active' if st.session_state.page in ['wert_reflexion', 'resilience_results'] else ''}\">
            <span class=\"icon\">🧘</span> Reflect
        </a>
        <a href=\"?page=resilience_path_selection\" class=\"nav-item {'active' if st.session_state.page in ['resilience_path_selection', 'resilience_path_day', 'trophy_gallery'] else ''}\">
            <span class=\"icon\">🌱</span> Grow
        </a>
    </div>
    \"\"\"
    st.markdown(nav_html, unsafe_allow_html=True)

# --- MAIN APP LOGIC ---

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
    elif st.session_state.page == 'wert_reflexion':
        render_resilience_questions_page()
    elif st.session_state.page == 'resilience_results':
        render_resilience_results_page()
    elif st.session_state.page == 'resilience_path_selection':
        render_resilience_path_selection()
    elif st.session_state.page == 'resilience_path_day':
        render_resilience_path_day()
    elif st.session_state.page == 'trophy_gallery':
        render_trophy_gallery()
    
    if st.session_state.page not in ['start']:
        render_bottom_nav()

if __name__ == \"__main__\":
    main()
"
Observation: Create successful: /app/streamlit_app.py
