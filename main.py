# Python script for a Streamlit application with three distinct modules.
# Module 1: A \"Decision Journey\" tool that helps analyze pros and cons.
# Module 2: A \"Resilience Reflection\" guide based on user input.
# Module 3: A \"Resilience Path\" with 10-day challenges for different resilience factors.

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import json
import requests
import time
import base64
from datetime import datetime, timedelta

# --- 1. SEITENKONFIGURATION & STYLING ---
st.set_page_config(
    page_title="VitaBoost",
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
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- Konfiguration für LLM API (NICHT ÄNDERN) ---
# Der API-Schlüssel wird von der Laufzeitumgebung bereitgestellt.
API_KEY = ""
# Korrektur der fehlerhaften URL: / vor API_KEY entfernt
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

# --- 2. RESILIENZ-PFAD DATENSTRUKTUR ---
RESILIENCE_PATHS = {
    "Stressabbau": {
        "icon": "🧘",
        "description": "Lerne effektive Techniken zur Stressbewältigung und inneren Ruhe",
        "color": "#4CAF50",
        "expert_tip": "Ein schneller Weg zur Ruhe: Atmen Sie 4 Sekunden lang durch die Nase ein, halten Sie den Atem 7 Sekunden lang an und atmen Sie 8 Sekunden lang durch den Mund aus. Das senkt den Herzschlag und beruhigt sofort.",
        "days": {
            1: {
                "title": "Die 4-7-8 Atemtechnik",
                "exercise": "Übe die 4-7-8 Atemtechnik für 5 Minuten. Atme 4 Sekunden ein, halte 7 Sekunden, atme 8 Sekunden aus. Wiederhole dies 5 Mal.",
                "reflection": "Wie fühlst du dich nach der Übung? Welche Veränderungen bemerkst du in deinem Körper?",
                "motivation": "Du hast den ersten Schritt zu mehr Ruhe gemacht! Jeder Atemzug bringt dich näher zu deiner inneren Balance.",
                "points": 10
            },
            2: {
                "title": "Körperwahrnehmung",
                "exercise": "Body Scan: Lege dich hin und scanne deinen Körper von Kopf bis Fuß. Wo sitzt die Anspannung? Atme bewusst in diese Bereiche.",
                "reflection": "Welche Körperregionen waren besonders angespannt? Was könnte der Grund dafür sein?",
                "motivation": "Großartig! Du lernst, die Signale deines Körpers zu verstehen. Das ist der Schlüssel zur Stressbewältigung.",
                "points": 10
            },
            3: {
                "title": "Stressauslöser identifizieren",
                "exercise": "Erstelle eine Liste deiner Top 5 Stressauslöser. Was triggert dich am meisten im Alltag?",
                "reflection": "Welcher dieser Auslöser ist am häufigsten? Was könntest du ändern, um ihn zu vermeiden oder besser damit umzugehen?",
                "motivation": "Bewusstsein ist der erste Schritt zur Veränderung. Du bist auf dem richtigen Weg!",
                "points": 10
            },
            4: {
                "title": "Progressive Muskelentspannung",
                "exercise": "Spanne nacheinander verschiedene Muskelgruppen für 5 Sekunden an und entspanne sie dann für 10 Sekunden. Beginne mit den Füßen und arbeite dich nach oben.",
                "reflection": "Welche Muskelgruppe fiel dir am schwersten zu entspannen? Warum könnte das so sein?",
                "motivation": "Dein Körper lernt, zwischen Anspannung und Entspannung zu unterscheiden. Das ist eine wertvolle Fähigkeit!",
                "points": 10
            },
            5: {
                "title": "Natur als Stressabbau",
                "exercise": "Verbringe mindestens 20 Minuten in der Natur. Gehe spazieren oder setze dich einfach nach draußen. Nimm bewusst die Umgebung wahr.",
                "reflection": "Wie hat die Natur dein Stresslevel beeinflusst? Was hast du bemerkt?",
                "motivation": "Die Natur ist ein kraftvoller Verbündeter im Kampf gegen Stress. Du hast heute gut für dich gesorgt!",
                "points": 10
            },
            6: {
                "title": "Stresstagebuch",
                "exercise": "Führe heute ein Stresstagebuch. Notiere jeden stressigen Moment: Was passierte? Wie hast du reagiert? Was hättest du anders machen können?",
                "reflection": "Welche Muster erkennst du in deinen Stressreaktionen?",
                "motivation": "Selbstreflexion ist Gold wert! Du entwickelst ein tiefes Verständnis für deine Stressmuster.",
                "points": 10
            },
            7: {
                "title": "Genussmomente schaffen",
                "exercise": "Plane heute bewusst 3 Genussmomente ein. Das kann eine Tasse Tee, ein Lieblingslied oder ein Sonnenuntergang sein. Genieße sie vollkommen.",
                "reflection": "Wie schwer oder leicht war es, dir diese Momente zu erlauben? Was hat dich daran gehindert oder unterstützt?",
                "motivation": "Du lernst, Freude aktiv in deinen Tag zu integrieren. Das ist aktive Stressprävention!",
                "points": 10
            },
            8: {
                "title": "Grenzen setzen",
                "exercise": "Sage heute zu einer Sache 'Nein', die dich überlasten würde. Übe, deine Grenzen zu kommunizieren.",
                "reflection": "Wie hat es sich angefühlt, Nein zu sagen? Was hat dich daran gehindert oder bestärkt? Ratschläge von deinem zukünftigen Ich an dein heutiges Ich: Was würdest du dir raten, um deine Grenzen besser zu schützen?",
                "motivation": "Grenzen zu setzen ist Selbstfürsorge, keine Schwäche. Du schützt deine Energie!",
                "points": 10
            },
            9: {
                "title": "Bewegung als Ventil",
                "exercise": "Bewege dich heute für mindestens 30 Minuten. Joggen, Tanzen, Yoga – finde, was dir guttut und Stress abbaut.",
                "reflection": "Wie hat sich die Bewegung auf deine Stimmung ausgewirkt? Welche Form der Bewegung hat dir am meisten Freude bereitet? Welche Alternativen gibt es, wenn das Wetter schlecht ist?",
                "motivation": "Bewegung ist Medizin für Körper und Geist! Du investierst in deine Gesundheit.",
                "points": 10
            },
            10: {
                "title": "Dein persönlicher Anti-Stress-Plan",
                "exercise": "Erstelle einen persönlichen Anti-Stress-Notfallplan. Welche 5 Techniken helfen dir am besten? Schreibe sie auf und hänge sie sichtbar auf.",
                "reflection": "Was sind deine effektivsten Stress-Tools? Wie kannst du sicherstellen, dass du sie regelmäßig anwendest?",
                "motivation": "🎉 Du hast den Stressabbau-Pfad gemeistert! Du besitzt jetzt ein Arsenal an Werkzeugen für mehr Gelassenheit.",
                "points": 10
            }
        }
    },
    "Selbstwirksamkeit": {
        "icon": "💪",
        "description": "Stärke dein Vertrauen in deine eigenen Fähigkeiten",
        "color": "#FF9800",
        "expert_tip": "Das Gehirn lernt durch kleine Siege. Jedes Mal, wenn Sie ein kleines Ziel erreichen – sei es nur, ein Glas Wasser zu trinken – stärken Sie Ihr Vertrauen in Ihre Fähigkeit, Dinge zu bewirken. Nutzen Sie diese kleinen Momente der Bestätigung.",
        "days": {
            1: {
                "title": "Mikro-Erfolge sammeln",
                "exercise": "Setze dir heute 3 winzige, erreichbare Ziele (z.B. Bett machen, 1 Glas Wasser trinken, 5 Minuten lesen). Hake sie ab!",
                "reflection": "Wie fühlte es sich an, diese kleinen Ziele zu erreichen? Welche Emotion begleitete das Abhaken? Schreibe dir auf, warum du diese Ziele erreichen konntest.",
                "motivation": "Jeder kleine Sieg zählt! Du beweist dir selbst, dass du Dinge bewegen kannst.",
                "points": 10
            },
            2: {
                "title": "Erfolge dokumentieren",
                "exercise": "Erstelle eine 'Erfolgs-Liste'. Schreibe 10 Dinge auf, die du in deinem Leben bereits gemeistert hast – groß oder klein. Füge hinzu, welche Hindernisse du dabei überwunden hast.",
                "reflection": "Welcher Erfolg macht dich am meisten stolz? Welche Stärken hast du dabei gezeigt?",
                "motivation": "Du hast bereits so viel erreicht! Diese Liste ist der Beweis deiner Fähigkeiten.",
                "points": 10
            },
            3: {
                "title": "Komfortzone erweitern",
                "exercise": "Tue heute eine Sache, die dich leicht herausfordert, aber machbar ist. Etwas, das du normalerweise vermeidest (z.B. eine Frage in einer Besprechung stellen).",
                "reflection": "Was hast du gewählt? Wie hast du dich vorher und nachher gefühlt?",
                "motivation": "Du wächst außerhalb deiner Komfortzone! Jeder Schritt macht dich stärker.",
                "points": 10
            },
            4: {
                "title": "Fähigkeiten-Inventur",
                "exercise": "Liste 20 Fähigkeiten auf, die du besitzt. Von praktischen (kochen, tippen) bis zu sozialen (zuhören, empathisch sein). Frage dich: Wie kann ich diese Fähigkeiten nutzen, um ein aktuelles Problem zu lösen?",
                "reflection": "Welche Fähigkeit überrascht dich? Welche möchtest du weiter ausbauen?",
                "motivation": "Du bist voller Talente! Erkenne an, was du alles kannst.",
                "points": 10
            },
            5: {
                "title": "Ein Problem lösen",
                "exercise": "Identifiziere ein kleines Problem in deinem Alltag und löse es heute. Repariere etwas, organisiere etwas oder finde eine Lösung.",
                "reflection": "Welches Problem hast du gelöst? Wie bist du vorgegangen? Was hast du über deine Problemlösungsfähigkeiten gelernt?",
                "motivation": "Du bist ein Problemlöser! Jede Lösung stärkt dein Vertrauen in deine Fähigkeiten.",
                "points": 10
            },
            6: {
                "title": "Feedback einholen",
                "exercise": "Frage 3 Menschen, die dich gut kennen: 'Was ist eine Stärke, die du an mir siehst?' Notiere ihre Antworten. Überlege, in welchen Situationen diese Stärke besonders hilfreich ist.",
                "reflection": "Welche Stärken wurden genannt? Waren sie dir bewusst? Welche hat dich überrascht? Wie kannst du diese Stärken bewusster einsetzen?",
                "motivation": "Andere sehen Stärken in dir, die du vielleicht übersiehst. Du bist wertvoller, als du denkst!",
                "points": 10
            },
            7: {
                "title": "Eine neue Fähigkeit beginnen",
                "exercise": "Beginne heute, eine neue kleine Fähigkeit zu lernen. 15 Minuten reichen – ein paar Worte einer Sprache, ein Akkord auf der Gitarre, ein neues Rezept.",
                "reflection": "Was hast du gewählt? Wie fühlte es sich an, Anfänger zu sein? Was ist dein nächster kleiner Lernschritt für morgen?",
                "motivation": "Du beweist dir, dass du wachsen und lernen kannst. Das ist pure Selbstwirksamkeit!",
                "points": 10
            },
            8: {
                "title": "Rückschläge umdeuten",
                "exercise": "Denke an einen vergangenen 'Misserfolg'. Was hast du daraus gelernt? Wie hat er dich stärker gemacht? Ersetze das Wort 'Misserfolg' durch 'Lernchance'.",
                "reflection": "Wie verändert sich deine Sicht auf den Rückschlag, wenn du ihn als Lernchance siehst?",
                "motivation": "Rückschläge sind keine Endstation, sondern Umwege zum Erfolg. Du lernst und wächst!",
                "points": 10
            },
            9: {
                "title": "Selbstgespräch überprüfen",
                "exercise": "Achte heute auf deine innere Stimme. Jedes Mal, wenn du denkst 'Das kann ich nicht', ersetze es durch 'Ich lerne, wie ich das kann'. Zähle, wie oft dir das gelungen ist.",
                "reflection": "Wie oft hast du dich selbst sabotiert? Wie fühlte sich die neue Formulierung an? Welche Situationen machen das positive Selbstgespräch am schwersten?",
                "motivation": "Deine Worte formen deine Realität. Du trainierst dein Gehirn auf Erfolg!",
                "points": 10
            },
            10: {
                "title": "Dein Selbstwirksamkeits-Manifest",
                "exercise": "Schreibe ein persönliches Manifest: 'Ich bin fähig, weil...' Liste alle Beweise deiner Selbstwirksamkeit auf. Lies es laut vor. Nenne mindestens drei zukünftige Herausforderungen, die du mit deinen aktuellen Fähigkeiten meistern wirst.",
                "reflection": "Wie fühlt es sich an, deine Fähigkeiten laut zu bestätigen? Was glaubst du jetzt über dich selbst?",
                "motivation": "🎉 Du hast deine Selbstwirksamkeit gestärkt! Du weißt jetzt: Du kannst mehr, als du denkst.",
                "points": 10
            }
        }
    },
    "Soziale Unterstützung": {
        "icon": "🤝",
        "description": "Baue ein starkes Netzwerk auf und pflege Beziehungen",
        "color": "#2196F3",
        "expert_tip": "Soziale Resilienz bedeutet, sich aktiv um Beziehungen zu kümmern. Rufen Sie heute jemanden an, den Sie lange nicht gesprochen haben. 15 Minuten bewusste Verbindung können Ihre Resilienz mehr stärken als eine Stunde Training.",
        "days": {
            1: {
                "title": "Drei Dankbarkeitsanrufe",
                "exercise": "Sende heute 3 kurzen Textnachrichten an verschiedene Menschen, um dich für etwas Konkretes zu bedanken, das sie für dich getan haben.",
                "reflection": "Wie hat sich das Senden der Nachrichten angefühlt? Welche Reaktionen hast du erhalten?",
                "motivation": "Du investierst in die wichtigsten Anker deines Lebens – deine Beziehungen.",
                "points": 10
            },
            2: {
                "title": "Verbindungs-Inventur",
                "exercise": "Erstelle eine Liste der 5 wichtigsten Menschen in deinem Leben. Schreibe jeweils auf, welche Art von Unterstützung sie dir geben (emotional, praktisch, intellektuell).",
                "reflection": "Gibt es ein Ungleichgewicht in deiner Unterstützungsstruktur? Wer braucht heute deine Aufmerksamkeit?",
                "motivation": "Bewusstsein über dein Netzwerk ist der erste Schritt zur Stärkung der sozialen Resilienz.",
                "points": 10
            },
            3: {
                "title": "Aktives Zuhören üben",
                "exercise": "Führe heute ein 10-minütiges Gespräch, in dem du 100% aktiv zuhörst. Keine Ratschläge geben, nur Paraphrasieren ('Ich verstehe, du fühlst dich...') und Fragen stellen.",
                "reflection": "Wie schwer war es, keine Ratschläge zu geben? Was hast du durch das aktive Zuhören Neues erfahren?",
                "motivation": "Aktives Zuhören ist der Schlüssel zu tieferen, resilienteren Beziehungen.",
                "points": 10
            },
            4: {
                "title": "Gemeinschaft erleben",
                "exercise": "Nimm an einer gemeinschaftlichen Aktivität teil, auch wenn es nur kurz ist (z.B. ein kurzes Gespräch mit einem Nachbarn, ein Kommentar in einem Online-Forum, ein Lächeln beim Bäcker).",
                "reflection": "Wie hat sich die Interaktion angefühlt? Hast du dich dadurch mehr verbunden gefühlt?",
                "motivation": "Kleine Momente der Verbundenheit summieren sich zu einer starken sozialen Resilienz.",
                "points": 10
            },
            5: {
                "title": "Um Hilfe bitten",
                "exercise": "Bitte heute um eine kleine Gefälligkeit oder um Hilfe bei einer Aufgabe, die du auch allein erledigen könntest (z.B. jemanden fragen, ob er dir die Tür aufhält). Übe, empfänglich zu sein.",
                "reflection": "Wie hat es sich angefühlt, um Hilfe zu bitten? War es leichter oder schwerer als erwartet?",
                "motivation": "Um Hilfe zu bitten ist ein Zeichen von Stärke, nicht von Schwäche. Es stärkt die Beziehungen.",
                "points": 10
            },
            6: {
                "title": "Positive Verstärkung",
                "exercise": "Gib heute 5 echte Komplimente oder positive Rückmeldungen an verschiedene Menschen. Beobachte deren Reaktion.",
                "reflection": "Wie haben die Menschen reagiert? Wie hat sich das Geben von Komplimenten auf deine eigene Stimmung ausgewirkt?",
                "motivation": "Positive Kommunikation nährt dein Netzwerk und stärkt deine eigene Resilienz.",
                "points": 10
            },
            7: {
                "title": "Beziehungspflege-Ritual",
                "exercise": "Überlege dir ein kleines wöchentliches Ritual, um eine wichtige Beziehung zu pflegen (z.B. Sonntagsanruf, gemeinsamer Kaffee am Freitag). Plane den ersten Schritt heute.",
                "reflection": "Welches Ritual hast du gewählt? Was macht diese Beziehung so wichtig für deine Resilienz?",
                "motivation": "Routinen der Verbundenheit bauen einen robusten Schutzschild gegen Einsamkeit.",
                "points": 10
            },
            8: {
                "title": "Konfliktlösung reflektieren",
                "exercise": "Denke an einen Konflikt der letzten Zeit. Was war dein Anteil daran? Wie hättest du durch besseres Zuhören deeskalieren können?",
                "reflection": "Was hast du über deinen Konfliktstil gelernt? Wie kannst du in Zukunft ruhiger reagieren?",
                "motivation": "Gesunde Konfliktlösung macht Beziehungen tiefer, nicht schwächer. Du lernst ständig dazu.",
                "points": 10
            },
            9: {
                "title": "Empathie trainieren",
                "exercise": "Stelle dir heute bei einer Interaktion aktiv die Frage: 'Wie fühlt sich die andere Person gerade und warum?' Versuche, ihre Perspektive einzunehmen.",
                "reflection": "War es einfach, die Perspektive zu wechseln? Wie hat sich dein eigenes Verhalten dadurch verändert?",
                "motivation": "Empathie ist der Klebstoff der Resilienz. Du baust Brücken zu anderen.",
                "points": 10
            },
            10: {
                "title": "Dein Support-Netzwerk-Plan",
                "exercise": "Erstelle eine Kontaktliste mit Ansprechpartnern für verschiedene Situationen (z.B. 'Zuhören bei Kummer', 'Praktische Hilfe', 'Inspiration').",
                "reflection": "Wie fühlt es sich an, diesen Plan zu haben? Worauf kannst du dich im Notfall verlassen?",
                "motivation": "🎉 Du hast deinen sozialen Resilienz-Pfad gemeistert! Dein Netzwerk ist dein Superkraft.",
                "points": 10
            }
        }
    }
}

# --- 3. STREAMLIT APP LOGIK ---

# --- Initialisierung des Session State und Mock-Daten ---
def init_session_state():
    """Initialisiert den Streamlit Session State mit Standardwerten."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home" # home, selection, challenge, summary
    if 'user_id' not in st.session_state:
        st.session_state.user_id = "mock_user_123" # Mock-ID
    if 'user_data' not in st.session_state:
        # Mock-Datenstruktur für den Benutzer
        st.session_state.user_data = {
            "total_points": 0,
            "current_path": None, # Key aus RESILIENCE_PATHS
            "current_day": 0,    # 1 bis 10
            "completed_paths": [], # Liste der abgeschlossenen Pfade
            "daily_reflections": {} # {path_key: {day_num: reflection_text}}
        }

def save_user_data(data):
    """Speichert Benutzerdaten (hier im Session State)."""
    st.session_state.user_data.update(data)
    
def get_user_data():
    """Gibt die aktuellen Benutzerdaten zurück."""
    return st.session_state.user_data

# --- UI Komponenten und Navigation ---

def render_bottom_nav():
    """Rendert die untere Navigationsleiste."""
    # Definiere die Navigationsziele
    nav_items = [
        {"key": "home", "icon": "🏠", "label": "Start"},
        {"key": "selection", "icon": "✨", "label": "Pfad"},
        {"key": "summary", "icon": "🏆", "label": "Bilanz"},
    ]
    
    # Nutze Columns, um die Buttons zu rendern
    cols = st.columns(len(nav_items))
    
    for i, item in enumerate(nav_items):
        with cols[i]:
            is_active = st.session_state.current_page == item['key']
            
            # Button Styling (mit Custom CSS nicht ganz so wichtig, aber für Klick notwendig)
            button_style = "background-color: var(--primary-color);" if is_active else "background-color: #f0f2f6;"
            label_style = "color: white;" if is_active else "color: var(--text-color);"
            
            if st.button(f"{item['icon']} {item['label']}", key=f"nav_{item['key']}", use_container_width=True):
                st.session_state.current_page = item['key']
                st.rerun()

    # Platzhalter für die fixe Nav (die CSS-Nav ist nur visuell, Streamlit braucht die Buttons)
    st.markdown("<br><br>", unsafe_allow_html=True) 

def render_progress_bar(current_day, max_days, points):
    """Rendert die Fortschrittsleiste."""
    progress = (current_day / max_days) * 100
    st.markdown(f"""
        <div class='progress-container'>
            <div class='progress-bar' style='width: {progress:.0f}%;'>
                Tag {current_day} / {max_days} | 🏅 {points} Pkt.
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_header(user_data):
    """Rendert den Haupt-Header der App."""
    if user_data['current_path']:
        st.markdown(f"<h1>{RESILIENCE_PATHS[user_data['current_path']]['icon']} {user_data['current_path']} Pfad</h1>", unsafe_allow_html=True)
    
    col_points, col_paths, col_empty = st.columns([1, 1, 2])
    with col_points:
        st.markdown(f"**Gesamtpunkte:** <span style='color: var(--primary-color); font-size: 1.2em;'>{user_data['total_points']}</span>", unsafe_allow_html=True)
    with col_paths:
        st.markdown(f"**Abgeschlossene Pfade:** <span style='color: var(--success-color); font-size: 1.2em;'>{len(user_data['completed_paths'])}</span>", unsafe_allow_html=True)

    # Rendert nur, wenn ein Pfad aktiv ist
    if user_data['current_path'] and user_data['current_day'] <= len(RESILIENCE_PATHS[user_data['current_path']]['days']):
        max_days = len(RESILIENCE_PATHS[user_data['current_path']]['days'])
        render_progress_bar(user_data['current_day'], max_days, user_data['total_points'])
        st.markdown(f"<div class='expert-tip'><b>💡 Experten-Tipp:</b> {RESILIENCE_PATHS[user_data['current_path']]['expert_tip']}</div>", unsafe_allow_html=True)
    st.divider()

# --- Hauptseiten der App ---

def page_home():
    """Rendert die Homepage (Dashboard)."""
    user_data = get_user_data()
    
    st.markdown("<h1>Willkommen bei VitaBoost!</h1>", unsafe_allow_html=True)
    st.markdown("Ihr persönlicher Coach für mentale Stärke und Resilienz.")

    st.subheader("Ihre aktuelle Resilienz-Reise")
    
    if user_data['current_path']:
        current_path = RESILIENCE_PATHS[user_data['current_path']]
        st.info(f"Sie befinden sich im **{user_data['current_path']}** Pfad ({current_path['icon']}). Tag {user_data['current_day']} von {len(current_path['days'])}.")
        if st.button("Weiter zur heutigen Übung", key="home_to_challenge"):
            st.session_state.current_page = "challenge"
            st.rerun()
    else:
        st.warning("Sie haben noch keinen Resilienz-Pfad ausgewählt. Starten Sie jetzt Ihre Reise!")
        if st.button("Pfad wählen", key="home_to_selection"):
            st.session_state.current_page = "selection"
            st.rerun()

    # Übersicht der Pfade
    st.subheader("Alle verfügbaren Pfade")
    cols = st.columns(len(RESILIENCE_PATHS))
    
    for i, (key, path) in enumerate(RESILIENCE_PATHS.items()):
        with cols[i]:
            completed = key in user_data['completed_paths']
            
            st.markdown(f"""
                <div style='
                    background-color: {path['color']}1A; 
                    border: 2px solid {path['color']}; 
                    border-radius: 12px; 
                    padding: 15px; 
                    text-align: center;
                    opacity: {0.5 if completed else 1};
                '>
                    <span style='font-size: 30px;'>{path['icon']}</span>
                    <h4>{key}</h4>
                    <p>{'✅ Abgeschlossen' if completed else path['description']}</p>
                </div>
            """, unsafe_allow_html=True)

def page_path_selection():
    """Rendert die Seite zur Pfadauswahl."""
    user_data = get_user_data()
    st.markdown("<h1>✨ Pfad auswählen</h1>", unsafe_allow_html=True)
    st.markdown("Wählen Sie den Bereich, in dem Sie Ihre Resilienz am liebsten stärken möchten.")

    # Pfadauswahl-Logik
    for key, path in RESILIENCE_PATHS.items():
        # Zeige den Pfad nur, wenn er noch nicht abgeschlossen wurde oder der aktuelle ist
        if key not in user_data['completed_paths'] or key == user_data['current_path']:
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"<span style='font-size: 60px;'>{path['icon']}</span>", unsafe_allow_html=True)

            with col2:
                st.subheader(key)
                st.markdown(f"*{path['description']}*")
                
                if key == user_data['current_path']:
                    st.success(f"**Aktiver Pfad:** Tag {user_data['current_day']} von {len(path['days'])}")
                    if st.button(f"Weiter zu Tag {user_data['current_day']}", key=f"continue_{key}"):
                        st.session_state.current_page = "challenge"
                        st.rerun()
                elif key in user_data['completed_paths']:
                    st.markdown(f"**Abgeschlossen** ✅")
                else:
                    if st.button(f"Diesen Pfad starten ({len(path['days'])} Tage)", key=f"start_{key}"):
                        # Initialisiere die Reflexionen für diesen Pfad, falls noch nicht geschehen
                        if key not in user_data['daily_reflections']:
                            user_data['daily_reflections'][key] = {}
                            
                        save_user_data({
                            "current_path": key,
                            "current_day": 1,
                            "daily_reflections": user_data['daily_reflections'] # Speichere die aktualisierte Struktur
                        })
                        st.session_state.current_page = "challenge"
                        st.rerun()
            st.divider()

def page_daily_challenge():
    """Rendert die tägliche Herausforderung."""
    user_data = get_user_data()
    
    if not user_data['current_path']:
        st.warning("Bitte wählen Sie zuerst einen Pfad.")
        st.session_state.current_page = "selection"
        st.rerun()
        return

    path_key = user_data['current_path']
    day_num = user_data['current_day']
    path_data = RESILIENCE_PATHS[path_key]
    
    if day_num > len(path_data['days']):
        # Pfad abgeschlossen
        st.session_state.current_page = "summary"
        st.rerun()
        return

    challenge = path_data['days'][day_num]
    
    # Header
    render_header(user_data)
    
    st.subheader(f"Tag {day_num}: {challenge['title']}")
    
    st.markdown("---")
    st.markdown(f"### 🎯 Übung")
    st.info(challenge['exercise'])

    st.markdown(f"### 📝 Reflexion")
    st.markdown(f"*{challenge['reflection']}*")
    
    # Zustand der Aufgabe prüfen
    reflection_key = f"reflection_{path_key}_{day_num}"
    completed = path_key in user_data['daily_reflections'] and day_num in user_data['daily_reflections'][path_key]

    default_value = user_data['daily_reflections'].get(path_key, {}).get(day_num, "")

    user_reflection = st.text_area(
        "Ihre Gedanken und Erkenntnisse (mind. 50 Zeichen):",
        value=default_value,
        height=150,
        disabled=completed,
        key=reflection_key
    )

    col_btn, col_mot = st.columns([1, 3])

    if col_btn.button("Aufgabe abschliessen und Punkte sammeln", disabled=completed or len(user_reflection) < 50):
        # Aktualisiere die Daten
        new_points = user_data['total_points'] + challenge['points']
        
        # Speichere Reflexion
        if path_key not in user_data['daily_reflections']:
            user_data['daily_reflections'][path_key] = {}
            
        user_data['daily_reflections'][path_key][day_num] = user_reflection

        # Bestimme den nächsten Tag oder schließe den Pfad ab
        next_day = day_num + 1
        new_path = path_key
        
        if next_day > len(path_data['days']):
            # Pfad abgeschlossen
            new_path = None
            user_data['completed_paths'].append(path_key)
            st.session_state.current_page = "summary"
            st.balloons()
            st.success(f"🎉 Pfad '{path_key}' erfolgreich abgeschlossen! Sie haben {challenge['points']} Punkte gesammelt.")
            next_day = 0
        else:
            st.success(f"Gut gemacht! Du hast {challenge['points']} Punkte gesammelt. Bereit für Tag {next_day}!")
        
        save_user_data({
            "total_points": new_points,
            "current_day": next_day,
            "current_path": new_path,
        })
        st.rerun()

    with col_mot:
        if completed:
             st.info(f"**Motivation für morgen:** {challenge['motivation']}")
        elif len(user_reflection) < 50:
            st.error(f"Bitte schreiben Sie mindestens {50 - len(user_reflection)} Zeichen, um die Reflexion abzuschließen.")
        else:
            st.markdown(f"<div style='margin-top: 10px; padding: 10px; background-color: var(--secondary-color); border-radius: 8px;'>{challenge['motivation']}</div>", unsafe_allow_html=True)


def page_summary():
    """Rendert die Bilanz- und Trophäen-Seite."""
    user_data = get_user_data()
    st.markdown("<h1>🏆 Ihre Resilienz-Bilanz</h1>", unsafe_allow_html=True)
    
    col_p, col_c = st.columns(2)
    with col_p:
        st.markdown(f"<h2>Gesamtpunkte: <span style='color: var(--primary-color);'>{user_data['total_points']}</span></h2>", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"<h2>Abgeschlossene Pfade: <span style='color: var(--success-color);'>{len(user_data['completed_paths'])}</span></h2>", unsafe_allow_html=True)

    st.markdown("---")
    
    st.subheader("Ihre Trophäen")
    
    if user_data['completed_paths']:
        trophy_cols = st.columns(len(user_data['completed_paths']))
        
        for i, path_key in enumerate(user_data['completed_paths']):
            path = RESILIENCE_PATHS[path_key]
            with trophy_cols[i]:
                st.markdown(f"""
                    <div class='trophy-card'>
                        <span class='trophy-icon'>{path['icon']}</span>
                        <h4>{path_key}-Meister</h4>
                        <p>10-Tages-Pfad abgeschlossen</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Noch keine Pfade abgeschlossen. Zeit, Ihre erste Trophäe zu verdienen!")

    st.subheader("Persönliche Rückschau")
    st.markdown("Werfen Sie einen Blick auf Ihre gesammelten Erkenntnisse.")
    
    # Anzeige der Reflexionen
    if user_data['daily_reflections']:
        for path_key in user_data['daily_reflections'].keys():
            path_reflections = user_data['daily_reflections'].get(path_key, {})
            
            with st.expander(f"Reflexionen: {RESILIENCE_PATHS[path_key]['icon']} {path_key}"):
                if path_reflections:
                    for day_num in sorted(path_reflections.keys()):
                        day_num = int(day_num) # Stelle sicher, dass es ein Int ist
                        challenge_title = RESILIENCE_PATHS[path_key]['days'][day_num]['title']
                        st.markdown(f"**Tag {day_num} – {challenge_title}**")
                        st.write(path_reflections[day_num])
                        st.markdown("---")
                else:
                    st.markdown("Noch keine abgeschlossenen Reflexionen in diesem Pfad.")
    else:
        st.info("Ihre Reflexionen werden hier angezeigt, sobald Sie Aufgaben abschließen.")
                
# --- Hauptfunktion der App ---

def main():
    """Die Hauptfunktion, die die Streamlit-App ausführt."""
    init_session_state()
    
    # Mapping der Seiten
    pages = {
        "home": page_home,
        "selection": page_path_selection,
        "challenge": page_daily_challenge,
        "summary": page_summary
    }

    # Rendern der aktuellen Seite
    pages.get(st.session_state.current_page, page_home)()

    # Rendern der Navigationsleiste
    render_bottom_nav()
/**
 * Konfigurationsdaten für die 10-Tage-Challenge zur persönlichen Entwicklung.
 * Die Struktur ermöglicht eine einfache Iteration durch die Kategorien und Tage.
 */
const CHALLENGE_DATA = {
    "Selbstbild stärken": {
        "icon": "🌟",
        "description": "Entwickle ein positives und realistisches Selbstbild durch gezielte Übungen zur Selbstreflexion und Überwindung des inneren Kritikers.",
        "color": "#9C27B0", // Lila
        "expert_tip": "Negative Gedanken wie 'Das kann ich nicht' sind nur Gewohnheiten. Fragen Sie sich: 'Was ist das Gegenteil dieses Gedankens?' Ersetzen Sie ihn durch eine neutrale oder positive Alternative, wie 'Ich lerne und werde besser.'",
        "days": {
            1: {
                "title": "Selbstbild-Check",
                "exercise": "Schreibe 10 Adjektive auf, die beschreiben, wie du dich selbst siehst. Sei ehrlich, sowohl positiv als auch negativ.",
                "reflection": "Überwiegen positive oder negative Begriffe? Was sagt das über dein Selbstbild aus?",
                "motivation": "Bewusstsein ist der erste Schritt zur Veränderung. Du schaust mutig hin!",
                "points": 10
            },
            2: {
                "title": "Innerer Kritiker vs. innerer Unterstützer",
                "exercise": "Identifiziere eine Situation, in der dein innerer Kritiker laut war. Was hat er gesagt? Schreibe eine Antwort von deinem inneren Unterstützer.",
                "reflection": "Wie unterscheidet sich die Perspektive? Welche Stimme fühlte sich wahrer an?",
                "motivation": "Du lernst, deinem inneren Kritiker Paroli zu bieten. Das ist Selbstliebe in Aktion!",
                "points": 10
            },
            3: {
                "title": "Stärken-Fokus",
                "exercise": "Erstelle eine Liste mit 15 deiner Stärken. Wenn es schwerfällt, frage: 'Was würden meine Freunde sagen?'",
                "reflection": "Welche Stärke nutzt du zu wenig? Wie könntest du sie mehr einsetzen?",
                "motivation": "Du bist voller Stärken! Sie zu erkennen ist der Grundstein für ein positives Selbstbild.",
                "points": 10
            },
            4: {
                "title": "Vergleichsfalle vermeiden",
                "exercise": "Beobachte heute, wann du dich mit anderen vergleichst. Halte an und frage: 'Was ist mein eigener Maßstab?'",
                "reflection": "Wie oft hast du verglichen? Was löst das in dir aus? Wie fühlte es sich an, eigene Maßstäbe zu setzen?",
                "motivation": "Dein einziger Vergleich solltest du gestern sein. Du definierst deinen eigenen Erfolg!",
                "points": 10
            },
            5: {
                "title": "Komplimente annehmen",
                "exercise": "Wenn dir heute jemand ein Kompliment macht, nimm es einfach an mit 'Danke'. Keine Abschwächung, keine Rechtfertigung.",
                "reflection": "Wie schwer war es, ein Kompliment anzunehmen? Was hindert dich normalerweise daran?",
                "motivation": "Du verdienst Anerkennung! Komplimente anzunehmen stärkt dein Selbstbild.",
                "points": 10
            },
            6: {
                "title": "Selbstmitgefühl üben",
                "exercise": "Schreibe einen Brief an dich selbst, so wie du ihn an deinen besten Freund schreiben würdest, der gerade kämpft. Mit Mitgefühl und Verständnis.",
                "reflection": "Wie hat es sich angefühlt, freundlich zu dir selbst zu sein? Was macht es so schwer oder leicht?",
                "motivation": "Selbstmitgefühl ist keine Schwäche, sondern die Basis für echte Stärke. Du lernst, dein eigener Freund zu sein!",
                "points": 10
            },
            7: {
                "title": "Perfektionismus hinterfragen",
                "exercise": "Identifiziere einen Bereich, in dem du perfekt sein willst. Frage dich: Warum? Was würde passieren, wenn ich 'gut genug' akzeptiere?",
                "reflection": "Woher kommt dieser Perfektionsdruck? Was könntest du gewinnen, wenn du ihn loslässt?",
                "motivation": "Perfektion ist eine Illusion. Du bist 'gut genug' – und das ist mehr als genug!",
                "points": 10
            },
            8: {
                "title": "Deine Werte leben",
                "exercise": "Liste deine Top 5 Werte auf. Reflektiere: Lebe ich nach diesen Werten? Wo stimmen meine Handlungen mit meinen Werten überein?",
                "reflection": "Wo gibt es Diskrepanzen? Was könntest du ändern, um authentischer zu leben?",
                "motivation": "Authentizität stärkt dein Selbstbild. Du lernst, dir selbst treu zu sein!",
                "points": 10
            },
            9: {
                "title": "Körperliche Selbstakzeptanz",
                "exercise": "Stelle dich vor den Spiegel. Finde 5 Dinge an deinem Körper, für die du dankbar bist (z.B. 'Meine Beine tragen mich', 'Meine Hände erschaffen').",
                "reflection": "Wie hat diese Übung deine Beziehung zu deinem Körper verändert?",
                "motivation": "Dein Körper ist dein Zuhause. Dankbarkeit dafür ist ein Akt der Selbstliebe!",
                "points": 10
            },
            10: {
                "title": "Dein neues Selbstbild",
                "exercise": "Schreibe ein neues, realistisches und liebevolles Selbstbild. Wer bist du wirklich? Nicht zu hart, nicht zu idealisiert – einfach wahr.",
                "reflection": "Wie unterscheidet sich dieses Selbstbild von dem zu Beginn? Was hat sich verändert?",
                "motivation": "🎉 Du hast ein stärkeres Selbstbild entwickelt! Du siehst dich jetzt mit freundlicheren Augen.",
                "points": 10
            }
        }
    },
    "Verbundenheit": {
        "icon": "🤝",
        "description": "Baue tiefere und bedeutungsvollere Beziehungen auf, indem du lernst, aktiv zuzuhören, Grenzen zu setzen und Verletzlichkeit zu zeigen.",
        "color": "#2196F3", // Blau
        "expert_tip": "Wahre Nähe entsteht oft erst, wenn wir uns verletzlich zeigen. Das Teilen einer ehrlichen Sorge oder eines kleinen Moments der Unsicherheit ist keine Schwäche, sondern ein Akt des Vertrauens, der Ihre Beziehungen vertiefen kann.",
        "days": {
            1: {
                "title": "Beziehungs-Inventur",
                "exercise": "Liste alle wichtigen Menschen in deinem Leben auf. Bewerte auf einer Skala von 1-10, wie nah du dich ihnen fühlst.",
                "reflection": "Welche Beziehungen sind erfüllend? Welche möchtest du vertiefen? Welche kosten dich mehr Energie, als sie geben?",
                "motivation": "Du schaust bewusst auf deine Beziehungen. Das ist der erste Schritt zu mehr Verbundenheit!",
                "points": 10
            },
            2: {
                "title": "Aktives Zuhören",
                "exercise": "Führe heute ein Gespräch, in dem du nur zuhörst. Keine Ratschläge, keine Unterbrechungen – nur volle Aufmerksamkeit.",
                "reflection": "Wie schwer war es, nur zuzuhören? Was hast du über die Person gelernt?",
                "motivation": "Zuhören ist ein Geschenk. Du schenkst heute jemandem deine volle Präsenz!",
                "points": 10
            },
            3: {
                "title": "Verletzlichkeit zeigen",
                "exercise": "Teile heute mit einer Person, der du vertraust, eine kleine Sorge oder Unsicherheit. Nichts Dramatisches, nur ehrlich.",
                "reflection": "Wie fühlte es sich an, dich verletzlich zu zeigen? Wie hat die Person reagiert?",
                "motivation": "Verletzlichkeit ist Mut, nicht Schwäche. Du baust echte Nähe auf!",
                "points": 10
            },
            4: {
                "title": "Dankbarkeit ausdrücken",
                "exercise": "Schreibe oder sage 3 Menschen, wofür du ihnen dankbar bist. Sei spezifisch: 'Danke, dass du...' ",
                "reflection": "Wie haben die Menschen reagiert? Wie hat es sich für dich angefühlt, Dankbarkeit auszudrücken?",
                "motivation": "Dankbarkeit vertieft Beziehungen. Du investierst in deine Verbindungen!",
                "points": 10
            },
            5: {
                "title": "Quality Time planen",
                "exercise": "Plane ein bewusstes Treffen mit einer Person, die dir wichtig ist. Keine Ablenkung, keine Smartphones – nur ihr beide.",
                "reflection": "Wie unterschied sich dieses Treffen von euren üblichen Interaktionen? Was hat es mit eurer Verbindung gemacht?",
                "motivation": "Qualität schlägt Quantität. Du nährst eine wichtige Beziehung!",
                "points": 10
            },
            6: {
                "title": "Grenzen kommunizieren",
                "exercise": "Identifiziere eine Grenze in einer Beziehung, die du setzen möchtest. Kommuniziere sie klar und liebevoll.",
                "reflection": "Wie hat die Person reagiert? Wie fühlst du dich nach dem Setzen der Grenze?",
                "motivation": "Grenzen sind gesund und notwendig. Du schützt deine Beziehungen, indem du sie setzt!",
                "points": 10
            },
            7: {
                "title": "Empathie üben",
                "exercise": "Wenn heute jemand etwas sagt oder tut, das dich irritiert, pausiere. Frage dich: 'Was könnte diese Person gerade durchmachen?'",
                "reflection": "Hat diese Perspektive deine Reaktion verändert? Wie hat sich Empathie angefühlt?",
                "motivation": "Empathie ist die Brücke zu echter Verbundenheit. Du übst, die Welt durch andere Augen zu sehen!",
                "points": 10
            },
            8: {
                "title": "Alte Verbindungen wiederbeleben",
                "exercise": "Kontaktiere heute eine Person, mit der du den Kontakt verloren hast, aber die dir wichtig war. Ein einfaches 'Hey, ich habe an dich gedacht'.",
                "reflection": "Wie hat es sich angefühlt, den Kontakt wiederherzustellen? Wie hat die Person reagiert?",
                "motivation": "Verbindungen können wiederbelebt werden. Du zeigst, dass dir Menschen wichtig sind!",
                "points": 10
            },
            9: {
                "title": "Konflikt konstruktiv angehen",
                "exercise": "Gibt es einen ungelösten Konflikt in deinem Leben? Überlege, wie du ihn ansprechen könntest – mit Ich-Botschaften und dem Wunsch nach Lösung.",
                "reflection": "Was hält dich davon ab, den Konflikt anzusprechen? Was wäre das Beste, das passieren könnte?",
                "motivation": "Konflikte anzugehen ist ein Zeichen von Reife. Du investierst in gesunde Beziehungen!",
                "points": 10
            },
            10: {
                "title": "Dein Beziehungs-Manifest",
                "exercise": "Schreibe auf, was dir in Beziehungen wichtig ist. Was brauchst du? Was kannst du geben? Wie willst du in Beziehungen sein?",
                "reflection": "Wie klar sind dir deine Beziehungswerte jetzt? Was wirst du anders machen?",
                "motivation": "🎉 Du hast Verbundenheit vertieft! Du weißt jetzt, wie du echte Nähe aufbaust.",
                "points": 10
            }
        }
    }
};
  "Optimismus": {
        "icon": "☀️",
        "description": "Kultiviere eine positive Lebenseinstellung ohne Realitätsverlust",
        "color": "#FFEB3B",
        "expert_tip": "Optimismus bedeutet nicht, Probleme zu ignorieren, sondern zu glauben, dass Lösungen gefunden werden können. Es ist die Überzeugung, dass Schwierigkeiten vorübergehend sind und dass Sie die Ressourcen haben, sie zu meistern.",
        "days": {
            "1": {
                "title": "Dankbarkeits-Ritual",
                "exercise": "Schreibe jeden Abend diese Woche 3 Dinge auf, für die du heute dankbar bist. Auch winzige Dinge zählen.",
                "reflection": "Wie verändert diese Praxis deinen Blick auf den Tag? Was fällt dir auf?",
                "motivation": "Dankbarkeit trainiert dein Gehirn auf Positives. Du legst das Fundament für Optimismus!",
                "points": 10
            },
            "2": {
                "title": "Positive Umdeutung",
                "exercise": "Denke an eine aktuelle Herausforderung. Finde 3 mögliche positive Aspekte oder Lernchancen darin.",
                "reflection": "Wie verändert sich deine Emotion zur Herausforderung durch diese Perspektive?",
                "motivation": "Du lernst, in Problemen Chancen zu sehen. Das ist die Essenz von Optimismus!",
                "points": 10
            },
            "3": {
                "title": "Best-Case-Szenario",
                "exercise": "Für eine Situation, vor der du Angst hast, male dir das best-mögliche Szenario aus. Was wäre, wenn alles gut geht?",
                "reflection": "Wie realistisch ist dieses positive Szenario? Wie fühlt es sich an, es dir vorzustellen?",
                "motivation": "Du gibst deinem Gehirn Erlaubnis, positive Ausgänge zu erwarten. Das ist nicht naiv, sondern heilsam!",
                "points": 10
            },
            "4": {
                "title": "Pessimismus-Detektor",
                "exercise": "Achte heute auf pessimistische Gedanken. Jedes Mal, wenn du einen bemerkst, notiere ihn und formuliere eine optimistische Alternative.",
                "reflection": "Wie oft warst du pessimistisch? Was sind deine typischen pessimistischen Muster?",
                "motivation": "Bewusstsein ist Macht. Du durchbrichst negative Denkmuster!",
                "points": 10
            },
            "5": {
                "title": "Inspirierende Geschichten",
                "exercise": "Lies, höre oder schau dir heute eine inspirierende Geschichte von jemandem an, der Schwierigkeiten überwunden hat.",
                "reflection": "Was hat dich an dieser Geschichte berührt? Welche Lektion nimmst du mit?",
                "motivation": "Geschichten der Hoffnung nähren deinen Optimismus. Du tankst Inspiration!",
                "points": 10
            },
            "6": {
                "title": "Zukunfts-Vision",
                "exercise": "Schreibe einen Brief aus der Zukunft (1 Jahr von jetzt). Beschreibe, wie gut es dir geht und was du alles erreicht hast.",
                "reflection": "Wie fühlte es sich an, diese positive Zukunft zu visualisieren? Was brauchst du, um dahin zu kommen?",
                "motivation": "Du erschaffst eine positive Vision. Dein Gehirn arbeitet jetzt darauf hin!",
                "points": 10
            },
            "7": {
                "title": "Positives Selbstgespräch",
                "exercise": "Heute nur positive Selbstgespräche. Ertappst du dich bei Selbstkritik, korrigiere es sofort zu etwas Aufbauendem.",
                "reflection": "Wie oft musstest du korrigieren? Wie hat sich deine Stimmung im Laufe des Tages entwickelt?",
                "motivation": "Deine innere Stimme formt deine Realität. Du wählst jetzt bewusst Optimismus!",
                "points": 10
            },
            "8": {
                "title": "Lächeln als Werkzeug",
                "exercise": "Lächle heute bewusst – auch ohne Grund. Schau, was es mit dir und deiner Umgebung macht.",
                "reflection": "Wie hat das Lächeln deine Stimmung beeinflusst? Wie haben andere reagiert?",
                "motivation": "Ein Lächeln verändert deine Chemie und die Welt um dich herum. Du verbreitest Positivität!",
                "points": 10
            },
            "9": {
                "title": "Ressourcen-Check",
                "exercise": "Liste alle inneren und äußeren Ressourcen auf, die du hast, um mit Schwierigkeiten umzugehen (Fähigkeiten, Menschen, Erfahrungen).",
                "reflection": "Wie gut ausgestattet bist du wirklich? Verändert diese Liste dein Selbstvertrauen?",
                "motivation": "Du bist nicht hilflos – du hast so viele Ressourcen! Das ist der Grund für realistischen Optimismus.",
                "points": 10
            },
            "10": {
                "title": "Dein Optimismus-Anker",
                "exercise": "Erstelle einen 'Optimismus-Anker': ein Objekt, Bild oder Zitat, das dich an deine optimistische Grundhaltung erinnert. Platziere es sichtbar.",
                "reflection": "Was hast du gewählt? Warum? Wie wirst du es nutzen, wenn es schwierig wird?",
                "motivation": "🎉 Du hast gelernt, Optimismus zu kultivieren! Du siehst jetzt Möglichkeiten, wo andere Hindernisse sehen.",
                "points": 10
            }
        }
    },
    "Konfliktlösung": {
        "icon": "🕊️",
        "description": "Entwickle Fähigkeiten für konstruktive Konfliktbewältigung",
        "color": "#E91E63",
        "expert_tip": "Konflikte sind nicht das Problem – wie wir mit ihnen umgehen, entscheidet. Gute Konfliktlösung bedeutet, die Bedürfnisse aller Beteiligten zu hören und nach Lösungen zu suchen, bei denen niemand sein Gesicht verliert.",
        "days": {
            "1": {
                "title": "Konflikt-Muster erkennen",
                "exercise": "Reflektiere über vergangene Konflikte. Wie reagierst du typischerweise? Vermeidung, Angriff, Rückzug, Kompromiss?",
                "reflection": "Was ist dein Konflikt-Standard-Modus? Wie gut funktioniert er? Was möchtest du ändern?",
                "motivation": "Selbsterkenntnis ist der erste Schritt zu besserer Konfliktlösung. Du schaust mutig hin!",
                "points": 10
            },
            "2": {
                "title": "Ich-Botschaften üben",
                "exercise": "Übe, Ich-Botschaften zu formulieren: 'Ich fühle X, wenn Y passiert, weil Z.' Schreibe 5 Beispiele aus deinem Leben.",
                "reflection": "Wie unterscheiden sich Ich-Botschaften von 'Du'-Vorwürfen? Wie würde das Konflikte verändern?",
                "motivation": "Du lernst, deine Bedürfnisse auszudrücken, ohne anzugreifen. Das ist Kommunikations-Gold!",
                "points": 10
            },
            "3": {
                "title": "Perspektivwechsel",
                "exercise": "Denke an einen aktuellen oder vergangenen Konflikt. Schreibe die Situation aus der Perspektive der anderen Person.",
                "reflection": "Was siehst du jetzt, das du vorher nicht gesehen hast? Verändert das deine Emotion?",
                "motivation": "Empathie ist der Schlüssel zur Konfliktlösung. Du öffnest dein Herz für andere Sichtweisen!",
                "points": 10
            },
            "4": {
                "title": "Pausieren lernen",
                "exercise": "Wenn du heute in eine Konfliktsituation gerätst (oder eine simulierst), übe zu pausieren, bevor du reagierst. Tief atmen, zählen, dann antworten.",
                "reflection": "Wie schwer war es zu pausieren? Was veränderte sich durch die Pause?",
                "motivation": "Zwischen Reiz und Reaktion liegt deine Macht. Du lernst, bewusst zu reagieren!",
                "points": 10
            },
            "5": {
                "title": "Aktives Zuhören im Konflikt",
                "exercise": "Übe die Technik des 'Spiegelns': 'Wenn ich dich richtig verstehe, sagst du...' Probiere es in einem Gespräch.",
                "reflection": "Wie hat die andere Person reagiert, als du wirklich zugehört hast? Was hat es mit dem Konflikt gemacht?",
                "motivation": "Verstanden zu werden ist ein Grundbedürfnis. Du schenkst das heute jemandem!",
                "points": 10
            },
            "6": {
                "title": "Bedürfnisse identifizieren",
                "exercise": "Bei einem Konflikt: Grabe tiefer als die Positionen. Was ist das zugrunde liegende Bedürfnis – bei dir und beim anderen?",
                "reflection": "Welches Bedürfnis steht hinter dem Konflikt? Wie könnte man beide Bedürfnisse erfüllen?",
                "motivation": "Hinter jedem Konflikt stehen Bedürfnisse. Du lernst, die Wurzel zu finden!",
                "points": 10
            },
            "7": {
                "title": "Win-Win denken",
                "exercise": "Nimm einen Konflikt und brainstorme 5 mögliche Win-Win-Lösungen. Kreativität ist erlaubt!",
                "reflection": "Wie viele Lösungen hast du gefunden? Welche ist die beste für alle Beteiligten?",
                "motivation": "Es gibt fast immer eine Lösung, bei der alle gewinnen. Du denkst in Möglichkeiten!",
                "points": 10
            },
            "8": {
                "title": "Entschuldigung üben",
                "exercise": "Eine echte Entschuldigung hat 3 Teile: 'Es tut mir leid für X. Ich verstehe, dass es Y verursacht hat. Ich werde Z tun.' Schreibe eine.",
                "reflection": "Wie fühlt es sich an, Verantwortung zu übernehmen? Für was in deinem Leben möchtest du dich entschuldigen?",
                "motivation": "Sich zu entschuldigen ist Stärke, nicht Schwäche. Du baust Brücken!",
                "points": 10
            },
            "9": {
                "title": "Grenzen im Konflikt",
                "exercise": "Identifiziere, wann ein Konflikt nicht konstruktiv ist (Respektlosigkeit, Gewalt). Übe zu sagen: 'Ich möchte das klären, aber nicht so. Lass uns pausieren.'",
                "reflection": "Wo sind deine Grenzen in Konflikten? Wie kannst du sie schützen?",
                "motivation": "Nicht jeder Konflikt kann sofort gelöst werden. Du lernst, dich zu schützen!",
                "points": 10
            },
            "10": {
                "title": "Dein Konfliktlösungs-Toolkit",
                "exercise": "Erstelle ein persönliches Toolkit: Welche 5 Strategien helfen dir in Konflikten? Schreibe sie als Notfallplan auf.",
                "reflection": "Was sind deine effektivsten Konfliktlösungs-Tools? Wie wirst du sie nutzen?",
                "motivation": "🎉 Du bist jetzt ein Friedensstifter! Du hast gelernt, Konflikte als Chance für Wachstum zu sehen.",
                "points": 10
            }
        }
    }
}

# --- 3. ZUSTAND DER APP VERWALTEN (SESSION STATE) ---

def init_session_state():
    """
    Initialisiert alle notwendigen Variablen im Streamlit Session State, 
    sofern sie noch nicht existieren.
    """
    
    # Zentrale Initialisierung der Standardwerte
    # st.session_state.setdefault(key, default_value) setzt den Wert nur, 
    # wenn der Schlüssel noch nicht existiert (die App läuft nicht neu).
    
    # Allgemeine Anwendungs- und Problem-Analyse-Zustände
    st.session_state.setdefault('page', 'start')
    st.session_state.setdefault('problem', "")
    st.session_state.setdefault('problem_category', "Wähle eine Kategorie")
    st.session_state.setdefault('options', ["", ""]) # z.B. Option A, Option B
    st.session_state.setdefault('selected_values', [])
    st.session_state.setdefault('values_rating', {})
    st.session_state.setdefault('emotions', "")
    
    # Entscheidungs-Matrix Zustände (Pro/Contra)
    st.session_state.setdefault('pro_a', "")
    st.session_state.setdefault('contra_a', "")
    st.session_state.setdefault('pro_b', "")
    st.session_state.setdefault('contra_b', "")
    st.session_state.setdefault('creative_options', "")
    
    # Zukunfts-Visualisierung und erster Schritt
    st.session_state.setdefault('future_scenario_a', "")
    st.session_state.setdefault('future_scenario_b', "")
    st.session_state.setdefault('first_step', "")
    
    # Resilienz-Test und Analyse-Zustände (alt)
    st.session_state.setdefault('resilience_answers', {})
    st.session_state.setdefault('resilience_score', None)
    st.session_state.setdefault('resilience_analysis', None)
    st.session_state.setdefault('processing_analysis', False)
    
    # Zustände für die Resilienz-Pfade / 10-Tage-Challenge (neu)
    st.session_state.setdefault('total_points', 0)
    st.session_state.setdefault('current_path', None) # Z.B. "Selbstbild stärken"
    st.session_state.setdefault('current_day', 1) # Der aktuelle Tag in diesem Pfad
    st.session_state.setdefault('path_progress', {}) # Speichert den Fortschritt pro Pfad/Tag
    st.session_state.setdefault('completed_paths', []) # Liste der abgeschlossenen Pfade
    st.session_state.setdefault('trophies', [])
    st.session_state.setdefault('day_completed', False) # Flag, ob die heutige Übung abgeschlossen ist

# Funktion sofort aufrufen, um den Zustand bei App-Start zu initialisieren
init_session_state()

def next_page(page_name):
    """Ändert die aktuelle Seite im Session State."""
    st.session_state.page = page_name

def reset_app():
    """Löscht den gesamten Zustand und initialisiert ihn neu."""
    st.session_state.clear()
    init_session_state()

# --- 4. DYNAMISCHE INHALTE FÜR JEDE KATEGORIE (DECISION JOURNEY) ---
# Dieses Dictionary enthält die spezifischen Werte und kognitiven Verzerrungen,
# die in den Entscheidungs-Tools für die jeweilige Problemkategorie verwendet werden.
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

# --- FRAGEBOGEN & ANALYSE-LOGIK ---

# Fragen für den Resilienz-Fragebogen (33 Fragen im Likert-Format)
resilience_questions = [
    "Ich bin mir meiner Stärken und Schwächen bewusst.",
    "Ich kenne meine Emotionen und kann sie benennen.",
    "Ich erkenne, wie meine Gedanken mein Verhalten beeinflussen.",
    "Ich bin überzeugt, dass ich schwierige Situationen meistern kann.",
    "Ich glaube an meine Fähigkeit, Probleme zu lösen.",
    "Ich fühle mich kompetent, um meine Ziele zu erreichen.",
    "Ich habe Menschen, auf die ich mich in Krisen verlassen kann.",
    "Ich suche aktiv den Kontakt zu Freunden und Familie, wenn ich Unterstützung brauche.",
    "Ich fühle mich in meinen Beziehungen geborgen und angenommen.",
    "Ich kann mit starken Gefühlen wie Wut oder Trauer umgehen, ohne dass sie mich überfordern.",
    "Ich finde gesunde Wege, um mich nach einem stressigen Tag zu entspannen.",
    "Ich erlaube mir, alle meine Gefühle zu spüren, ohne sie zu bewerten.",
    "Ich habe Techniken, um mich in stressigen Momenten zu beruhigen.",
    "Ich kann Prioritäten setzen, um Stress zu reduzieren.",
    "Ich weiß, wie ich meine Energiereserven wieder aufladen kann.",
    "Ich gehe Problemen aktiv und systematisch an, anstatt sie zu ignorieren.",
    "Ich kann eine Situation aus verschiedenen Perspektiven betrachten, um eine Lösung zu finden.",
    "Ich bin kreativ in der Suche nach neuen Lösungen.",
    "Ich bin optimistisch, was meine Zukunft angeht.",
    "Ich kann mir positive Entwicklungen für mein Leben vorstellen.",
    "Ich habe klare Ziele, die mir Orientierung geben.",
    "Ich kann Dinge akzeptieren, die ich nicht ändern kann.",
    "Ich vergebe mir selbst für Fehler, die ich gemacht habe.",
    "Ich nehme Herausforderungen als Teil des Lebens an.",
    "Ich finde meine Handlungen auch in schwierigen Zeiten sinnvoll.",
    "Ich spüre eine Verbindung zu etwas Größerem als mir selbst.",
    "Meine Werte leiten mich durchs Leben.",
    "Ich bin offen für neue Ideen und unkonventionelle Lösungen.",
    "Ich nutze meine Vorstellungskraft, um aus einer schwierigen Situation herauszukommen.",
    "Ich kann mich von starren Denkmustern lösen.",
    "Ich kann auch in schwierigen Situationen noch lachen.",
    "Ich nutze Humor als Ventil, um Anspannung zu lösen.",
    "Ich kann über mich selbst lachen, ohne mich zu verurteilen."
]

# Vorab definierte Analysen basierend auf dem Score
def get_canned_analysis(score, max_score):
    """
    Liefert einen vordefinierten Analysetext basierend auf dem erreichten Resilienz-Score.

    Args:
        score (int): Der vom Nutzer erreichte Resilienz-Score.
        max_score (int): Der maximal mögliche Score.

    Returns:
        str: Der Analysetext für die entsprechende Resilienz-Stufe.
    """
    if score <= max_score * 0.4:
        return """
**Deine Resilienz: Fundament aufbauen**

Deine aktuelle Punktzahl deutet darauf hin, dass du dich in einigen Bereichen deiner Resilienz noch im Aufbau befindest. Das ist eine wichtige Erkenntnis! Es zeigt, dass du das Potenzial hast, deine Widerstandsfähigkeit gezielt zu stärken und dich besser auf künftige Herausforderungen vorzubereiten. Die Arbeit an diesen Faktoren kann einen großen Unterschied in deinem Wohlbefinden machen.

**Tipps zur Stärkung deiner Resilienz:**

1.  **Selbstwahrnehmung & Selbstfürsorge**: Beginne damit, dich selbst besser kennenzulernen. Frage dich, wie du dich fühlst und was du wirklich brauchst. Integriere kleine Rituale in deinen Alltag, die nur dir gewidmet sind, sei es ein 10-minütiger Spaziergang, eine Tasse Tee in Ruhe oder ein heißes Bad.
2.  **Soziale Beziehungen aktiv pflegen**: Suche den Kontakt zu Menschen, die dir guttun und denen du vertraust. Ein offenes Gespräch über deine Gefühle kann eine enorme Last von deinen Schultern nehmen.
3.  **Realistische Ziele setzen**: Große Probleme können überwältigend wirken. Zerlege sie in kleine, überschaubare Schritte. Wenn du zum Beispiel eine neue Fähigkeit lernen willst, fange mit einem 15-minütigen Online-Tutorial an, anstatt direkt einen ganzen Kurs zu planen.
4.  **Umgang mit Gefühlen lernen**: Gefühle sind Wegweiser. Versuche, sie ohne Urteil zu beobachten, anstatt sie zu unterdrücken. Ein Emotionstagebuch kann dir helfen, Muster zu erkennen.
5.  **Perspektivwechsel üben**: Wenn eine Situation aussichtslos erscheint, versuche sie aus einem anderen Blickwinkel zu betrachten. Wie würde ein Freund die Situation sehen? Welche Lektion kannst du daraus lernen?
"""
    elif score <= max_score * 0.7:
        return """
**Deine Resilienz: Solides Fundament**

Deine Punktzahl zeigt, dass du bereits über ein solides Fundament an Resilienz verfügst. Du bist in der Lage, mit Herausforderungen umzugehen und hast bereits einige der wichtigsten Resilienzfaktoren in deinem Leben integriert. Das ist eine großartige Ausgangslage, um deine Fähigkeiten gezielt weiter auszubauen.

**Tipps zur Stärkung deiner Resilienz:**

1.  **Soziales Netz bewusst stärken**: Pflege deine Beziehungen aktiv. Organisiere regelmäßige Treffen, sei ein guter Zuhörer und biete deine Hilfe an. Ein starkes soziales Netz ist dein wichtigster Puffer in schwierigen Zeiten.
2.  **Kreative Problemlösung**: Wenn du vor einem Problem stehst, gehe es nicht nur auf dem naheliegendsten Weg an. Brainstorme unkonventionelle Lösungen, denke "out of the box". Manchmal liegt die Lösung in einer völlig unerwarteten Idee.
3.  **Sinn und Werte vertiefen**: Reflektiere regelmäßig darüber, was dir im Leben wirklich wichtig ist. Wenn du deine Handlungen an deinen Werten ausrichtest, gewinnst du an innerer Stärke und Orientierung. Überlege, wie du dein Handeln noch besser mit deinen tiefsten Überzeugungen in Einklang bringen kannst.
4.  **Optimismus kultivieren**: Übe dich darin, auch in schwierigen Situationen nach den positiven Aspekten zu suchen, ohne die Realität zu leugnen. Welche Lektion kannst du aus dieser Erfahrung lernen? Betrachte Krisen als Wachstumschancen.
5.  **Humor einsetzen**: Nimm das Leben nicht immer zu ernst. Humor ist ein mächtiges Werkzeug, um Anspannung zu lösen und eine positive Perspektive zu bewahren. Suche bewusst nach Gelegenheiten zum Lachen, sei es durch Filme, Witze oder einfach das Teilen lustiger Anekdoten.
"""
    else:
        return """
**Deine Resilienz: Hohe Widerstandsfähigkeit**

Herzlichen Glückwunsch! Deine hohe Punktzahl zeigt, dass du über eine **starke Resilienz** verfügst. Du bist gut gerüstet, um mit Rückschlägen und Krisen umzugehen und kannst diese sogar als Chance für Wachstum nutzen. Deine Fähigkeiten in Bereichen wie Selbstwahrnehmung, Problemlösung und sozialen Beziehungen sind gut ausgeprägt.

**Tipps zur Aufrechterhaltung und Weiterentwicklung:**

1.  **Mentoring und Wissensaustausch**: Nutze deine Stärke, um auch anderen zu helfen. Indem du deine Erfahrungen teilst, stärkst du nicht nur dein eigenes Fundament, sondern unterstützt auch dein Umfeld und schaffst ein Netzwerk der gegenseitigen Unterstützung.
2.  **Aktivität in den Lebensbereichen**: Setze dir bewusst Ziele in Bereichen, die du vielleicht bisher vernachlässigt hast. Ob es darum geht, ein neues Hobby zu beginnen, eine neue Sprache zu lernen oder dich ehrenamtlich zu engagieren – du hast die Fähigkeit, dich anzupassen und zu wachsen.
3.  **Lebenssinn vertiefen**: Reflektiere, wie deine täglichen Handlungen zu deinem größeren Lebenssinn beitragen. Wenn du eine starke Sinnorientierung hast, kannst du auch die größten Stürme überstehen, ohne dein Ziel aus den Augen zu verlieren.
4.  **Kreativität als Lebenshaltung**: Nutze deine Kreativität nicht nur zur Problemlösung, sondern auch als Ausdruck deiner Persönlichkeit. Malen, schreiben, Musik machen oder einfach nur das Finden unkonventioneller Wege im Alltag können deine innere Stärke weiter festigen.
5.  **Humor als Resilienzanker**: Integriere Humor bewusst in deinen Alltag. Lache über dich selbst, teile lustige Momente mit anderen und nutze Humor, um Anspannung zu reduzieren. Humor ist eine der stärksten Waffen gegen Widrigkeiten.
"""

# --- SIMULIERTE ABHÄNGIGKEITEN FÜR DIESEN CODEBLOCK ---
# (In Ihrer vollständigen App sollten diese aus der State-Management-Datei importiert werden)

# Annahme: st.session_state existiert und ist initialisiert (wie in Datei 1/2)
if 'page' not in st.session_state: st.session_state.page = 'start'
if 'total_points' not in st.session_state: st.session_state.total_points = 0
if 'trophies' not in st.session_state: st.session_state.trophies = []
if 'path_progress' not in st.session_state: st.session_state.path_progress = {}
if 'completed_paths' not in st.session_state: st.session_state.completed_paths = []
if 'current_path' not in st.session_state: st.session_state.current_path = None
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'day_completed' not in st.session_state: st.session_state.day_completed = False

def next_page(page_name):
    """Navigations-Funktion, die den Zustand 'page' ändert."""
    st.session_state.page = page_name

# Mock-Daten für Resilienz-Pfade (Muss in der echten App vollständig definiert sein!)
RESILIENCE_PATHS = {
    "Selbstwahrnehmung stärken": {
        "icon": "🧠",
        "description": "Erkenne deine Emotionen und Denkmuster, um souveräner zu handeln.",
        "days": {
            1: {"title": "Der innere Kompass", "task": "Notiere 3 Momente heute, in denen du eine starke Emotion gespürt hast. Welche Gedanken waren damit verbunden?"},
            2: {"title": "Gedankenstopp", "task": "Erkenne einen negativen Gedanken und ersetze ihn durch eine neutrale Beobachtung."},
            10: {"title": "Abschluss-Check", "task": "Wie hat sich dein Gefühl der Selbstwahrnehmung verändert?"},
        }
    },
    "Optimismus kultivieren": {
        "icon": "☀️",
        "description": "Lerne, Herausforderungen als Chancen zu sehen und eine positive Grundhaltung zu entwickeln.",
        "days": {
            1: {"title": "Die Dankbarkeitsübung", "task": "Schreibe 5 Dinge auf, für die du heute dankbar bist."},
            2: {"title": "Worst-Case-Analyse", "task": "Was ist das Schlimmste, was passieren kann? Wie realistisch ist das?"},
            10: {"title": "Abschluss-Check", "task": "Fühlst du dich optimistischer? Warum oder warum nicht?"},
        }
    }
}

# --- HILFSFUNKTIONEN FÜR RESILIENZ-PFADE ---

def complete_day():
    """Wird nach Abschluss einer Tagesaufgabe aufgerufen."""
    path_name = st.session_state.current_path
    current_day = st.session_state.current_day
    
    # 1. Fortschritt aktualisieren
    st.session_state.path_progress[path_name] = current_day
    st.session_state.total_points += 10 # Punkte vergeben
    st.session_state.day_completed = True
    
    # 2. Prüfen, ob der Pfad abgeschlossen ist
    if current_day >= 10:
        if path_name not in st.session_state.completed_paths:
            st.session_state.completed_paths.append(path_name)
            
            # Trophäe hinzufügen
            trophy_icons = ["⭐", "🏅", "👑", "🚀", "💎"]
            new_trophy = f"{random.choice(trophy_icons)} {path_name} Meister"
            st.session_state.trophies.append(new_trophy)
            st.success(f"🎉 Pfad **{path_name}** abgeschlossen! Du hast die Trophäe '{new_trophy}' erhalten.")

    # 3. Zum nächsten Tag navigieren (oder zur Pfad-Auswahl, wenn fertig)
    if current_day < 10:
        st.session_state.current_day += 1
        st.session_state.day_completed = False
        st.experimental_rerun() # Neu laden, um den neuen Tag anzuzeigen
    else:
        st.session_state.current_path = None
        next_page('resilience_path_selection')


# --- 5. SEITEN-INHALT RENDERN ---

def render_start_page():
    """Startseite mit Auswahl der drei Hauptpfade."""
    st.title("VitaBoost – Stärke deine Entscheidungen")
    
    # Image (mit Platzhalter-URL) und Slogan
    st.image("https://placehold.co/1200x250/FFF8E1/E2B060?text=St%C3%A4rke+deine+Entscheidungen%2C+st%C3%A4rke+dein+Leben", 
             caption="Wähle den passenden Pfad für deine Situation.")
    
    st.markdown("---")
    
    # Punktestand anzeigen
    if st.session_state.total_points > 0:
        st.info(f"### 🏆 Deine Gesamtpunkte: **{st.session_state.total_points}**")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Entscheidungsreise")
        st.markdown("Strukturiere deine Gedanken und Gefühle, um eine **fundierte Entscheidung** zu treffen.")
        st.button("Starte die Entscheidungsreise", on_click=next_page, args=['step_1'], key="start_decision", use_container_width=True)

    with col2:
        st.markdown("### Werte-Reflexion")
        st.markdown("Du steckst gerade in einer Krise? Finde heraus, was deine **zentralen Resilienzfaktoren** sind.")
        st.button("Starte die Werte-Reflexion", on_click=next_page, args=['wert_reflexion'], key="start_reflection", use_container_width=True)
        
    with col3:
        st.markdown("### Resilienz-Pfad")
        st.markdown("Stärke deine Widerstandsfähigkeit mit **10-Tages-Challenges** zu verschiedenen Lebensthemen.")
        st.button("Starte den Resilienz-Pfad", on_click=next_page, args=['resilience_path_selection'], key="start_path", use_container_width=True)
        
    st.markdown("---")
    
    # Trophäen-Galerie Button
    if st.session_state.trophies:
        st.button("🏆 Meine Trophäen ansehen", on_click=next_page, args=['trophy_gallery'], key="view_trophies")

# --- RESILIENCE PATH PAGES ---

def render_resilience_path_selection():
    """Seite zur Auswahl des Resilienz-Pfades."""
    st.title("🌱 Wähle deinen Resilienz-Pfad")
    st.markdown("Jeder Pfad enthält eine 10-Tages-Challenge mit täglichen Übungen, Reflexionen und Expertentipps.")
    
    # Punktestand
    st.markdown(f"**Deine Gesamtpunkte:** **{st.session_state.total_points}**")
    st.markdown("---")
    
    paths = list(RESILIENCE_PATHS.keys())
    
    # Pfade in 2 Spalten anzeigen
    for i in range(0, len(paths), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(paths):
                path_name = paths[i + j]
                path_data = RESILIENCE_PATHS[path_name]
                
                with col:
                    # Verwende st.container() für bessere optische Abgrenzung
                    with st.container(border=True): 
                        # Icon und Titel
                        st.markdown(f"## {path_data['icon']} {path_name}")
                        st.markdown(path_data['description'])
                        
                        progress = st.session_state.path_progress.get(path_name, 0)
                        
                        # Fortschritt anzeigen
                        if progress > 0:
                            st.progress(progress / 10, text=f"**Fortschritt: {progress}/10 Tage**")
                        
                        # Status
                        if path_name in st.session_state.completed_paths:
                            st.success("✅ Abgeschlossen! Du hast alle Tage gemeistert.")
                        elif progress > 0:
                            st.info(f"📍 In Bearbeitung (Tag {progress} abgeschlossen)")
                        
                        # Button zum Starten/Fortsetzen
                        button_text = "Pfad Fortsetzen" if progress > 0 and progress < 10 else "Pfad Starten (Tag 1)"
                        if path_name in st.session_state.completed_paths:
                            button_text = "Pfad Wiederholen"
                            
                        # Logik für den Button
                        if st.button(button_text, key=f"path_{path_name}", use_container_width=True):
                            st.session_state.current_path = path_name
                            
                            # Wenn abgeschlossen oder neu starten, beginne bei Tag 1
                            if path_name in st.session_state.completed_paths:
                                st.session_state.current_day = 1
                                st.session_state.path_progress[path_name] = 0
                                st.session_state.completed_paths.remove(path_name) # Entfert, falls wiederholt wird
                            else:
                                # Setze beim nächsten Tag fort (progress + 1)
                                st.session_state.current_day = progress + 1 
                                
                            st.session_state.day_completed = False
                            next_page('resilience_path_day')
    
    st.markdown("---")
    st.button("🏠 Zurück zur Startseite", on_click=next_page, args=['start'])

def render_resilience_path_day():
    """Seite zur Anzeige der Tagesaufgabe und zum Abschluss."""
    if not st.session_state.current_path:
        next_page('resilience_path_selection')
        return
    
    path_name = st.session_state.current_path
    
    # Prüfen, ob der Pfad in den Mock-Daten existiert
    if path_name not in RESILIENCE_PATHS:
        st.error("Fehler: Resilienz-Pfad nicht gefunden.")
        next_page('resilience_path_selection')
        return

    path_data = RESILIENCE_PATHS[path_name]
    current_day = st.session_state.current_day
    
    # Prüfen, ob der Tag in den Mock-Daten existiert
    if current_day not in path_data['days']:
        # Fallback auf Tag 10, falls die Tagesdaten unvollständig sind
        day_data = path_data['days'][10] 
        current_day = 10
    else:
        day_data = path_data['days'][current_day]
    
    # Header
    st.title(f"{path_data['icon']} {path_name}")
    st.subheader(f"Tag {current_day}/10: {day_data['title']}")
    
    # Fortschrittsbalken (Verwendung des nativen Streamlit-Balkens)
    # Wenn Tag 1, dann Fortschritt = 0.
    days_completed = st.session_state.path_progress.get(path_name, 0)
    
    if days_completed >= current_day:
        # Dies sollte nicht passieren, wenn die Logik in 'complete_day' korrekt ist.
        # Es bedeutet, der Tag ist schon in der letzten Sitzung abgeschlossen worden.
        st.progress(days_completed / 10, text=f"**Tag {days_completed} von 10 abgeschlossen**")
    else:
        st.progress(days_completed / 10, text=f"**Aktueller Fortschritt: {days_completed}/10 Tage**")


    st.markdown("---")
    
    st.markdown(f"### Deine Aufgabe für heute:")
    st.info(f"📝 {day_data['task']}")
    
    st.markdown("---")
    
    if st.session_state.day_completed:
        st.success(f"🥳 Du hast Tag {current_day} erfolgreich abgeschlossen! Gut gemacht.")
        # Button, um zur nächsten Aufgabe zu gehen
        if current_day < 10:
             st.button(f"Nächste Aufgabe (Tag {current_day + 1})", on_click=complete_day, key="next_day", use_container_width=True)
        else:
             st.button("Pfad abschließen und zur Auswahl zurück", on_click=complete_day, key="finish_path", use_container_width=True)
    else:
        # Eingabefeld zur Bestätigung/Reflexion
        user_reflection = st.text_area("Schreibe eine kurze Reflexion (optional, aber empfohlen):", key="day_reflection")

        # Button zum Abschluss der Tagesaufgabe
        st.button("✅ Tagesaufgabe abschließen (10 Punkte erhalten)", on_click=complete_day, key="complete_day", use_container_width=True)

    st.markdown("---")
    st.button("Zurück zur Pfadauswahl", on_click=next_page, args=['resilience_path_selection'])

    
   # Mock-Daten für Category Content (aus Datei 1)
category_content = {
    "Karriere & Beruf": {
        "values": ["Finanzielle Sicherheit", "Wachstum", "Autonomie", "Einfluss", "Anerkennung", "Work-Life-Balance"],
        "cognitive_biases": {"title": "Denkfehler", "biases": [("Bias", "Frage")]},
    },
    "Persönliches Wachstum": {
        "values": ["Selbstverwirklichung", "Kreativität", "Lernen", "Soziale Bindungen", "Entwicklung", "Freiheit"],
        "cognitive_biases": {"title": "Denkfehler", "biases": [("Bias", "Frage")]},
    },
    "Beziehungen & Familie": {
        "values": ["Soziale Bindungen", "Harmonie", "Vertrauen", "Empathie", "Stabilität", "Zugehörigkeit"],
        "cognitive_biases": {"title": "Denkfehler", "biases": [("Bias", "Frage")]},
    }
}

# Erweiterte Mock-Daten für Resilienz-Pfade
RESILIENCE_PATHS = {
    "Selbstwahrnehmung stärken": {
        "icon": "🧠",
        "expert_tip": "Beginne jeden Tag mit drei tiefen Atemzügen und benenne, wie du dich *jetzt* fühlst. Nur benennen, nicht bewerten!",
        "description": "Erkenne deine Emotionen und Denkmuster, um souveräner zu handeln.",
        "days": {
            1: {"title": "Der innere Kompass", "exercise": "Notiere 3 Momente heute, in denen du eine starke Emotion gespürt hast.", "reflection": "Welche Gedanken waren mit diesen Emotionen verbunden?", "points": 10, "motivation": "Der Anfang ist gemacht! Du hast den wichtigsten Schritt zur Veränderung getan."},
            2: {"title": "Gedankenstopp", "exercise": "Erkenne einen negativen Gedanken und ersetze ihn durch eine neutrale Beobachtung.", "reflection": "Wie schwer fiel dir der Perspektivwechsel?", "points": 15, "motivation": "Großartig! Du lernst, deine mentale Steuerung zu übernehmen."},
            10: {"title": "Abschluss-Check", "exercise": "Reflektiere deine größten Erkenntnisse aus den letzten 10 Tagen.", "reflection": "Wie hat sich dein Gefühl der Selbstwahrnehmung verändert?", "points": 30, "motivation": "Geschafft! Du bist mental stärker und klarer geworden."},
        }
    },
}

# Navigations- und State-Funktion (aus Datei 2)
def next_page(page_name):
    """Navigations-Funktion, die den Zustand 'page' ändert."""
    st.session_state.page = page_name
    st.session_state.day_completed = False

# State-Initialisierung (falls nicht bereits erfolgt)
if 'total_points' not in st.session_state: st.session_state.total_points = 0
if 'trophies' not in st.session_state: st.session_state.trophies = []
if 'path_progress' not in st.session_state: st.session_state.path_progress = {}
if 'completed_paths' not in st.session_state: st.session_state.completed_paths = []
if 'current_path' not in st.session_state: st.session_state.current_path = None
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'day_completed' not in st.session_state: st.session_state.day_completed = False

# State für Entscheidungsreise
if 'problem' not in st.session_state: st.session_state.problem = ""
if 'problem_category' not in st.session_state: st.session_state.problem_category = "Wähle eine Kategorie"
if 'options' not in st.session_state: st.session_state.options = ["", ""]
if 'selected_values' not in st.session_state: st.session_state.selected_values = []
if 'values_rating' not in st.session_state: st.session_state.values_rating = {}

# --- HILFSFUNKTIONEN FÜR RESILIENZ-PFAD ---

def handle_day_completion(path_name, current_day, path_data):
    """Logik zum Abschließen eines Tages (Punkte, Fortschritt, Trophäe)."""
    
    day_points = path_data['days'][current_day]['points']
    st.session_state.total_points += day_points
    st.session_state.path_progress[path_name] = current_day
    st.session_state.day_completed = True

    if current_day == 10:
        if path_name not in st.session_state.completed_paths:
            st.session_state.completed_paths.append(path_name)
            
            # Trophäe hinzufügen (mit aktuellem Datum)
            st.session_state.trophies.append({
                'path': path_name,
                'icon': path_data['icon'],
                'completed_date': datetime.now().strftime("%d.%m.%Y")
            })
            st.success(f"🎉 Pfad **{path_name}** abgeschlossen! Du hast eine neue Trophäe erhalten.")
    
    st.rerun()

def handle_next_day(current_day):
    """Logik zum Wechseln zum nächsten Tag oder zur Auswahl."""
    if current_day < 10:
        st.session_state.current_day += 1
        st.session_state.day_completed = False
        st.rerun()
    else:
        # Pfad abgeschlossen, zurück zur Auswahl
        st.session_state.current_path = None
        next_page('resilience_path_selection')

# --- 5. SEITEN-INHALT RENDERN (KORRIGIERT & ERWEITERT) ---

# --- A. RESILIENZ-PFAD TAG ANSICHT ---

def render_resilience_path_day():
    """Seite zur Anzeige der Tagesaufgabe, Reflexion und Abschluss."""
    if not st.session_state.current_path or st.session_state.current_path not in RESILIENCE_PATHS:
        next_page('resilience_path_selection')
        return

    path_name = st.session_state.current_path
    path_data = RESILIENCE_PATHS[path_name]
    
    # Stellen Sie sicher, dass current_day im gültigen Bereich ist, auch wenn die Daten unvollständig sind
    current_day = st.session_state.current_day
    current_day = min(current_day, 10) # Max Tag 10
    
    # Fallback für Tag-Daten
    day_data = path_data['days'].get(current_day, path_data['days'][1])

    # Header
    st.title(f"{path_data['icon']} {path_name}")
    st.subheader(f"Tag {current_day}/10: {day_data['title']}")

    # Fortschrittsbalken
    days_completed = st.session_state.path_progress.get(path_name, 0)
    progress_display = days_completed / 10 if days_completed >= current_day else (current_day - 1) / 10 
    st.progress(progress_display, text=f"**Aktueller Fortschritt: {days_completed}/10 Tage**")

    st.markdown("---")
    
    # CSS für Expertentipp (Inline-Styling für Streamlit)
    st.markdown("""
    <style>
    .expert-tip {
        background-color: #f0f8ff; /* Light blue background */
        border-left: 5px solid #E2B060; /* VitaBoost color border */
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 4px;
        font-size: 16px;
    }
    .expert-tip strong {
        color: #E2B060;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Expertentipp am Anfang (Tag 1)
    if current_day == 1:
        st.markdown(f"""
        <div class="expert-tip">
            <strong>💡 Expertentipp für diesen Pfad:</strong><br>
            {path_data['expert_tip']}
        </div>
        """, unsafe_allow_html=True)
    
    # Tagesübung
    with st.container(border=True):
        st.markdown("#### 📋 Deine heutige Übung")
        st.markdown(day_data['exercise'])
    
    # Reflexionsfragen
    with st.container(border=True):
        st.markdown("#### 🤔 Reflexion")
        st.markdown(day_data['reflection'])
        
        # User-Eingabe (unabhängig vom Abschluss-Status)
        reflection_text = st.text_area(
            "Deine Gedanken und Erkenntnisse (optional zur Speicherung):",
            height=150,
            key=f"reflection_{path_name}_{current_day}",
            disabled=st.session_state.day_completed
        )
    
    st.markdown("---")

    # Tag abschließen / Status anzeigen
    if not st.session_state.day_completed:
        # Hier wird die Logik der Funktion handle_day_completion() aufgerufen
        st.button(
            f"✅ Tag {current_day} abschließen ({day_data['points']} Punkte)", 
            key="complete_day_action",
            on_click=handle_day_completion, 
            args=(path_name, current_day, path_data),
            use_container_width=True
        )
    
    # Motivierender Spruch nach Abschluss
    if st.session_state.day_completed:
        st.success("🎉 Tag abgeschlossen! Deine Erkenntnisse wurden gespeichert.")
        
        # Motivations-Banner
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E2B060 0%, #FFD700 100%); 
                      border-radius: 12px; padding: 20px; text-align: center; color: white; margin: 20px 0;">
            <h3 style="color: white; margin: 0;">💫 {day_data['motivation']}</h3>
            <p style="margin-top: 10px; font-size: 18px;"><strong>+{day_data['points']} Punkte!</strong></p>
            <p>Gesamtpunkte: {st.session_state.total_points}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            button_text = "🏆 Pfad abgeschlossen!" if current_day == 10 else f"➡️ Nächster Tag ({current_day + 1})"
            st.button(
                button_text, 
                key="next_or_finish_day",
                on_click=handle_next_day,
                args=(current_day,),
                use_container_width=True
            )
        
        with col2:
            st.button("🏠 Zurück zur Übersicht", on_click=next_page, args=['resilience_path_selection'], key="back_to_paths", use_container_width=True)

# --- B. TROPHÄEN-GALERIE ---

def render_trophy_gallery():
    """Zeigt alle gesammelten Trophäen und Statistiken an."""
    
    # CSS für die Trophäen-Karten
    st.markdown("""
    <style>
    .trophy-card {
        background: linear-gradient(145deg, #333 0%, #000 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        height: 100%;
    }
    .trophy-icon {
        font-size: 40px;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 5px #FFD700);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏆 Deine Trophäen-Galerie")
    st.markdown(f"### Gesamtpunkte: **{st.session_state.total_points}**")
    
    if not st.session_state.trophies:
        st.info("Du hast noch keine Trophäen gesammelt. Schließe einen Resilienz-Pfad ab, um deine erste Trophäe zu erhalten!")
    else:
        st.markdown("---")
        st.markdown("### 🎖️ Abgeschlossene Pfade")
        
        # Trophäen in Grid anzeigen (max. 3 pro Zeile)
        cols = st.columns(3)
        for idx, trophy in enumerate(st.session_state.trophies):
            with cols[idx % 3]:
                # Sicherstellen, dass trophy ein Dict ist, falls mit der alten Logik ein String gespeichert wurde
                path_name = trophy['path'] if isinstance(trophy, dict) else trophy
                icon = trophy.get('icon', '⭐') if isinstance(trophy, dict) else '⭐'
                completed_date = trophy.get('completed_date', 'Datum unbekannt') if isinstance(trophy, dict) else ''
                
                st.markdown(f"""
                <div class="trophy-card">
                    <div class="trophy-icon">{icon}</div>
                    <h4 style="color: white; margin: 10px 0;">{path_name}</h4>
                    <p style="color: #FFD700; margin: 0; font-weight: bold;">Abgeschlossen am</p>
                    <p style="color: white; margin: 0; font-size: 14px;">{completed_date}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Statistiken
        st.markdown("---")
        st.markdown("### 📊 Deine Statistiken")
        col1, col2, col3 = st.columns(3)
        
        # Anzahl abgeschlossener Pfade
        with col1:
            st.metric("Abgeschlossene Pfade", len(st.session_state.completed_paths))
            
        # Absolvierte Tage
        with col2:
            total_days = sum(st.session_state.path_progress.values())
            st.metric("Absolvierte Tage", total_days)
            
        # Gesammelte Punkte
        with col3:
            st.metric("Gesammelte Punkte", st.session_state.total_points)
    
    st.markdown("---")
    st.button("🏠 Zurück zur Startseite", on_click=next_page, args=['start'])

# --- C. ENTSCHEIDUNGSREISE (SCHRITTE) ---

def render_wert_reflexion_page():
    """Dummy-Seite für Werte-Reflexion (sollte später den Fragebogen enthalten)."""
    st.title("Werte-Reflexion & Das große Bild")
    st.markdown("""
    Dies ist ein Bereich mit Potenzial, um **deine täglichen Handlungen mit deinen tiefsten Werten und deinem Lebenssinn in Einklang zu bringen**.
    """)

    st.subheader("Strategien zur Verbesserung:")
    
    st.markdown("""
    **1. Werte identifizieren:**
    Nimm dir Zeit, um zu identifizieren, was dir wirklich wichtig ist. Schreibe deine zentralen Werte auf, wie z.B. Familie, Ehrlichkeit, Kreativität oder Erfolg.
    """)
    
    st.markdown("""
    **2. Zusammenhänge verstehen:**
    Wenn du mit einem kleinen Problem konfrontiert bist, versuche, es in einen größeren Kontext zu stellen. Versuche, Verhaltensweisen von Menschen oder Ereignisse aus einem anderen Blickwinkel zu betrachten.
    """)
    
    st.markdown("""
    **3. Sinn finden:**
    Suche nach Wegen, wie du deinen Alltag als sinnvoller empfinden kannst, z.B. indem du deine Arbeit mit deinen persönlichen Werten verknüpfst.
    """)
    if st.button("Zurück zur Startseite"):
      next_page('start')

def render_step_1():
    """Schritt 1 der Entscheidungsreise: Problem und Optionen definieren."""
    st.title("Step 1: Dein Problem & deine Optionen")
    
    with st.container(border=True):
        st.markdown("#### Problem und Kategorie")
        st.session_state.problem = st.text_area(
            "Was ist die Entscheidung, die dich beschäftigt?",
            value=st.session_state.problem,
            key="problem_input",
            height=100
        )
        
        options = ["Wähle eine Kategorie"] + list(category_content.keys())
        # Index-Verwaltung für Selectbox
        try:
            current_index = options.index(st.session_state.problem_category)
        except ValueError:
            current_index = 0
            
        st.session_state.problem_category = st.selectbox(
            "Wähle die Kategorie, zu der deine Entscheidung gehört:",
            options=options,
            index=current_index
        )
    
    with st.container(border=True):
        st.markdown("#### Optionen")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.options[0] = st.text_area("Option A (z.B. 'Job wechseln'):", value=st.session_state.options[0], height=100, key="option_a_input")
        with col2:
            st.session_state.options[1] = st.text_area("Option B (z.B. 'Im aktuellen Job bleiben'):", value=st.session_state.options[1], height=100, key="option_b_input")
    
    # Validierung
    is_valid = all([st.session_state.problem, st.session_state.options[0], st.session_state.options[1], st.session_state.problem_category != "Wähle eine Kategorie"])
    
    st.markdown("---")
    st.button("➡️ Weiter zu Step 2: Werte & Motivation", disabled=not is_valid, on_click=next_page, args=['step_2'], use_container_width=True)
    st.button("🏠 Zurück zur Startseite", on_click=next_page, args=['start'])

def render_step_2():
    """Schritt 2 der Entscheidungsreise: Werte-basiertes Rating und erste Berechnung."""
    st.title("Step 2: Werte & Motivation")
    selected_category = st.session_state.problem_category
    
    # Sicherstellen, dass die Kategorie gültig ist, bevor auf values zugegriffen wird
    if selected_category == "Wähle eine Kategorie":
        st.error("Bitte wähle in Step 1 zuerst eine gültige Kategorie aus.")
        st.button("Zurück zu Step 1", on_click=next_page, args=['step_1'])
        return

    all_values = category_content.get(selected_category, {}).get("values", [])
    
    with st.container(border=True):
        st.markdown(f"#### Psychologische Werte für '{selected_category}'")
        st.markdown(f"Wähle alle Werte aus, die für deine Entscheidung relevant sind.")
        
        # Checkboxen in 3 Spalten anzeigen
        current_selected_values = st.session_state.selected_values.copy()
        cols = st.columns(3)
        temp_selected_values = []
        for i, value in enumerate(all_values):
            col = cols[i % 3]
            is_checked = col.checkbox(value, value=value in current_selected_values, key=f"checkbox_{value}")
            if is_checked:
                temp_selected_values.append(value)
        
        st.session_state.selected_values = temp_selected_values

    # Nur fortfahren, wenn Werte ausgewählt sind
    if st.session_state.selected_values:
        total_score_a = 0
        total_score_b = 0

        with st.container(border=True):
            st.markdown("#### Werte-Bewertung (Deine Entscheidungsmatrix)")
            st.markdown("Bewerte auf einer Skala von 0 bis 10, wie gut jede Option deinen gewählten Wert erfüllt. **(0=erfüllt gar nicht, 10=erfüllt perfekt)**.")
            
            for value in st.session_state.selected_values:
                st.subheader(f"⚖️ Wert: {value}")
                
                # Option A Slider
                col_a, col_b = st.columns(2)
                with col_a:
                    rating_a = st.slider(
                        f"**Option A ({st.session_state.options[0]}):**",
                        0, 10, st.session_state.values_rating.get(f"{value}_A", 5), key=f"slider_a_{value}"
                    )
                    st.session_state.values_rating[f"{value}_A"] = rating_a
                    total_score_a += rating_a
                
                # Option B Slider
                with col_b:
                    rating_b = st.slider(
                        f"**Option B ({st.session_state.options[1]}):**",
                        0, 10, st.session_state.values_rating.get(f"{value}_B", 5), key=f"slider_b_{value}"
                    )
                    st.session_state.values_rating[f"{value}_B"] = rating_b
                    total_score_b += rating_b
        
        st.markdown("---")
        
        # Berechnung und Darstellung des Zwischenergebnisses
        with st.container():
            st.markdown("### 📊 Zwischenergebnis (Werte-Gewichtung)")
            
            max_score = len(st.session_state.selected_values) * 10
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric(f"Option A: {st.session_state.options[0]}", f"{total_score_a} / {max_score}", delta=f"{round(total_score_a / max_score * 100)} %")
                st.progress(total_score_a / max_score)
                
            with col_b:
                st.metric(f"Option B: {st.session_state.options[1]}", f"{total_score_b} / {max_score}", delta=f"{round(total_score_b / max_score * 100)} %")
                st.progress(total_score_b / max_score)

        st.markdown("---")
        st.button("➡️ Weiter zu Step 3: Kognitive Verzerrungen prüfen", on_click=next_page, args=['step_3'], use_container_width=True)
    else:
        st.warning("Bitte wähle mindestens einen relevanten Wert aus, um fortzufahren und die Entscheidungsmatrix zu erstellen.")
    
    st.button("⬅️ Zurück zu Step 1", on_click=next_page, args=['step_1'])

# --- MOCK START PAGE FÜR NAVIGATION ---

def render_start_page():
    st.title("VitaBoost – Stärke deine Entscheidungen")
    st.button("Starte die Entscheidungsreise", on_click=next_page, args=['step_1'])
    st.button("Starte den Resilienz-Pfad", on_click=next_page, args=['resilience_path_selection'])
    if st.session_state.trophies:
        st.button("🏆 Meine Trophäen ansehen", on_click=next_page, args=['trophy_gallery'])

# --- MAIN RENDERER (NUR ZUM TESTEN) ---

# if st.session_state.page == 'start':
#     render_start_page()
# elif st.session_state.page == 'resilience_path_day':
#     render_resilience_path_day()
# elif st.session_state.page == 'trophy_gallery':
#     render_trophy_gallery()
# elif st.session_state.page == 'step_1':
#     render_step_1()
# elif st.session_state.page == 'step_2':
#     render_step_2()
# else:
#     # Fallback für die Pfadauswahl
#     pass


   # --- HILFSFUNKTIONEN ---

def next_page(page_name):
    """Ändert den aktuellen Seitenstatus in der Session State."""
    st.session_state.page = page_name
    st.rerun()

def reset_app():
    """Setzt alle entscheidungsrelevanten Session States zurück."""
    st.session_state.page = 'start'
    st.session_state.problem = ""
    st.session_state.options = ["Option 1 (z.B. Bleiben)", "Option 2 (z.B. Wechseln)"]
    st.session_state.problem_category = list(category_content.keys())[0]
    st.session_state.selected_values = []
    st.session_state.values_rating = {}
    st.session_state.emotions = ""
    st.session_state.pro_a = ""
    st.session_state.pro_b = ""
    st.session_state.contra_a = ""
    st.session_state.contra_b = ""
    st.session_state.creative_options = ""
    st.session_state.future_scenario_a = ""
    st.session_state.future_scenario_b = ""
    st.session_state.first_step = ""
    st.rerun()

def get_canned_analysis(score, max_score):
    """Liefert eine Analyse basierend auf dem Resilienz-Score."""
    if score >= max_score * 0.8:
        return "### **Hohe Resilienz (Exzellent)**\nDeine Punktzahl deutet auf eine **ausgeprägte Widerstandsfähigkeit** hin. Du verfügst über starke innere Ressourcen, um mit Stress und Rückschlägen umzugehen. Du bist wahrscheinlich sehr lösungsorientiert und nutzt dein Netzwerk effektiv. Halte diese Praktiken bei!"
    elif score >= max_score * 0.6:
        return "### **Mittlere bis hohe Resilienz (Gut)**\nDu hast eine **gute Basis an Resilienzfaktoren**. In herausfordernden Zeiten zeigst du Stärke, aber es gibt Bereiche, in denen du noch wachsen kannst. Weiter so!"
    else:
        return "### **Wachstumspotenzial (Fokus auf Entwicklung)**\nDeine Punktzahl deutet darauf hin, dass du möglicherweise **Schwierigkeiten hast**, dich schnell von Rückschlägen zu erholen. Konzentriere dich auf den Aufbau von Achtsamkeit und die Definition kleiner, erreichbarer Ziele."

def initialize_session_state():
    """Initialisiert alle notwendigen Session State Variablen."""
    defaults = {
        'page': 'start',
        'problem': "",
        'options': ["Option 1 (z.B. Bleiben)", "Option 2 (z.B. Wechseln)"],
        'problem_category': list(category_content.keys())[0],
        'selected_values': [],
        'values_rating': {},
        'emotions': "",
        'pro_a': "",
        'pro_b': "",
        'contra_a': "",
        'contra_b': "",
        'creative_options': "",
        'future_scenario_a': "",
        'future_scenario_b': "",
        'first_step': "",
        'resilience_score': None,
        'resilience_analysis': None,
        'core_values': ["Wachstum", "Sicherheit", "Freiheit", "Familie", "Gesundheit", "Anerkennung", "Geld"],
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Spezielle Initialisierung für Resilienz-Antworten
    if 'resilience_answers' not in st.session_state:
        st.session_state.resilience_answers = {i: 3 for i in range(len(resilience_questions))}


# --- INHALTSDEFINITIONEN ---

category_content = {
    "Karriere & Finanzen": {
        "cognitive_biases": {
            "biases": [
                ("Bestätigungsfehler (Confirmation Bias)", "Neigst du dazu, nur nach Informationen zu suchen, die deine bevorzugte Option bestätigen?"),
                ("Verlustaversion (Loss Aversion)", "Ist die Angst, etwas zu verlieren (Job, Status), stärker als die Freude, etwas zu gewinnen (neue Chance)?")
            ]
        }
    },
    "Beziehungen & Familie": {
        "cognitive_biases": {
            "biases": [
                ("Ankereffekt (Anchoring)", "Wirst du von deinem ersten emotionalen Eindruck zu stark beeinflusst?"),
                ("Status-quo-Bias", "Wählst du die Option, die alles beim Alten lässt, nur weil sie bequemer ist?")
            ]
        }
    },
}

resilience_questions = [
    "Ich bin überzeugt, dass ich Herausforderungen meistern kann.",
    "Ich habe starke, unterstützende Beziehungen in meinem Leben.",
    "Ich kann meine Emotionen auch in stressigen Situationen regulieren.",
    "Ich sehe Misserfolge als Gelegenheiten zum Lernen.",
    "Ich habe klare, realistische Ziele für meine Zukunft."
]


# --- SEITEN-RENDERER ---

def render_start():
    st.title("Dein Entscheidungshelfer 🧭")
    st.markdown("""
    Willkommen! Dieses Tool führt dich durch einen strukturierten Prozess, um schwierige Entscheidungen zu treffen.
    Wir nutzen Methoden wie die **Sechs Denkhüte** von Edward de Bono und das **Regret Minimization Framework** von Jeff Bezos.
    
    Wähle deinen Weg:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Entscheidungsreise starten")
        st.markdown("Führe eine strukturierte Analyse deiner aktuellen Situation und Optionen durch.")
        if st.button("▶️ Starte Entscheidung", use_container_width=True):
            next_page('step_1')
    
    with col2:
        st.subheader("2. Resilienz reflektieren")
        st.markdown("Reflektiere deine innere Stärke und dein Wachstumspotenzial.")
        if st.button("🧘 Starte Reflexion", use_container_width=True):
            next_page('resilience_questions')
            
    st.markdown("---")
    st.markdown("Eine klare Entscheidung beginnt mit einem klaren Kopf. Lass uns loslegen!")


def render_step_1():
    st.title("Step 1: Das Problem & Optionen (Der 'Weiße Hut')")
    st.markdown("#### Fakten sammeln & Problem definieren")
    
    st.session_state.problem = st.text_area(
        "Beschreibe deine Entscheidungssituation kurz und präzise (z.B. Jobwechsel, Umzug, Beziehungsstatus):", 
        value=st.session_state.problem,
        height=100
    )
    
    st.markdown("#### Definiere deine zwei Hauptoptionen")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.session_state.options[0] = st.text_input(
            "Option A:",
            value=st.session_state.options[0]
        )
    with col_b:
        st.session_state.options[1] = st.text_input(
            "Option B:",
            value=st.session_state.options[1]
        )
        
    st.markdown("#### Wähle die Kategorie, die am besten passt")
    st.session_state.problem_category = st.selectbox(
        "Kategorie (hilft bei der Reflexion von Denkfehlern):",
        options=list(category_content.keys()),
        index=list(category_content.keys()).index(st.session_state.problem_category) if st.session_state.problem_category in category_content else 0
    )

    problem_defined = bool(st.session_state.problem.strip())
    option_a_defined = bool(st.session_state.options[0].strip())
    option_b_defined = bool(st.session_state.options[1].strip())
    
    st.markdown("---")
    if st.button("Weiter"):
        if not (problem_defined and option_a_defined and option_b_defined):
            st.warning("Bitte beschreibe das Problem und beide Optionen, bevor du fortfährst.")
        else:
            next_page('step_2')


def render_step_2():
    st.title("Step 2: Werte-Matrix (Der 'Weiße Hut' & 'Blaue Hut')")
    st.markdown("""
    #### Werte auswählen
    Wähle die **drei bis fünf wichtigsten Werte** aus, die von dieser Entscheidung am stärksten betroffen sind.
    """)

    st.session_state.selected_values = st.multiselect(
        "Deine Kernwerte:",
        options=st.session_state.core_values,
        default=st.session_state.selected_values,
        max_selections=5
    )

    st.markdown("#### Werte bewerten (Skala 1 - 10)")
    st.markdown(f"Bewerte, wie gut **Option A ({st.session_state.options[0]})** und **Option B ({st.session_state.options[1]})** mit jedem deiner ausgewählten Werte übereinstimmen.")
    st.markdown("_1 = gar nicht kompatibel, 10 = vollständig kompatibel_")

    if st.session_state.selected_values:
        cols = st.columns([1, 3, 3])
        cols[1].markdown(f"**Option A: {st.session_state.options[0]}**")
        cols[2].markdown(f"**Option B: {st.session_state.options[1]}**")

        for value in st.session_state.selected_values:
            st.markdown("---")
            col_val, col_rate_a, col_rate_b = st.columns([1, 3, 3])
            
            # Rating for Option A
            rating_a_key = f"{value}_A"
            initial_rating_a = st.session_state.values_rating.get(rating_a_key, 5)
            new_rating_a = col_rate_a.slider(
                f"**{value}**", 
                1, 10, initial_rating_a, key=rating_a_key, label_visibility="collapsed"
            )
            st.session_state.values_rating[rating_a_key] = new_rating_a
            
            # Rating for Option B
            rating_b_key = f"{value}_B"
            initial_rating_b = st.session_state.values_rating.get(rating_b_key, 5)
            new_rating_b = col_rate_b.slider(
                f"**{value}**", 
                1, 10, initial_rating_b, key=rating_b_key, label_visibility="collapsed"
            )
            st.session_state.values_rating[rating_b_key] = new_rating_b
            
            # Value label
            col_val.write(f"**{value}**")

    st.markdown("---")
    
    # KORRIGIERTE LOGIK AUS DEINEM SNIPPET
    if st.button("Weiter"):
        if not st.session_state.selected_values:
            st.warning("Bitte wähle mindestens einen Wert aus, bevor du fortfährst.")
        else:
            next_page('step_3')
    # ENDE KORRIGIERTE LOGIK


def render_step_3():
    st.title("Step 3: Emotionen & Denkfehler (Der 'Rote Hut')")
    with st.container():
        st.markdown("#### Dein Bauchgefühl")
        st.markdown("Schreibe auf, welche Gefühle und intuitiven Gedanken du zu den Optionen hast. Es geht nicht um Logik, sondern um Emotionen.")
        st.session_state.emotions = st.text_area(
            "Deine Gedanken:", 
            value=st.session_state.emotions, 
            height=150, 
            key="emotions_area"
        )
    
    selected_content = category_content.get(st.session_state.problem_category, {})
    biases = selected_content.get("cognitive_biases", {}).get("biases", [])
    
    if biases:
        with st.container():
            st.markdown("#### Reflektiere über Denkfehler")
            st.markdown("Versuche, mögliche kognitive Verzerrungen zu identifizieren, die deine emotionale Bewertung beeinflussen könnten.")
            for bias_title, bias_question in biases:
                with st.expander(f"**{bias_title}**"):
                    st.markdown(bias_question)

    st.markdown("---")
    if st.button("Weiter"):
        next_page('step_4')


def render_step_4():
    st.title("Step 4: Pro/Contra & Zukunft")
    
    with st.container():
        st.markdown(f"#### Vorteile (Der 'Gelbe Hut')")
        st.session_state.pro_a = st.text_area(
            f"Was spricht für Option A: '{st.session_state.options[0]}'? (Maximales Positives Denken)",
            value=st.session_state.pro_a,
            key="pro_a_area", height=100
        )
        st.session_state.pro_b = st.text_area(
            f"Was spricht für Option B: '{st.session_state.options[1]}'? (Maximales Positives Denken)",
            value=st.session_state.pro_b,
            key="pro_b_area", height=100
        )
    
    st.markdown("---")
    with st.container():
        st.markdown(f"#### Nachteile (Der 'Schwarze Hut')")
        st.session_state.contra_a = st.text_area(
            f"Was spricht gegen Option A: '{st.session_state.options[0]}'? (Worst-Case-Szenario & Risiken)",
            value=st.session_state.contra_a,
            key="contra_a_area", height=100
        )
        st.session_state.contra_b = st.text_area(
            f"Was spricht gegen Option B: '{st.session_state.options[1]}'? (Worst-Case-Szenario & Risiken)",
            value=st.session_state.contra_b,
            key="contra_b_area", height=100
        )
        
    st.markdown("---")
    with st.container():
        st.markdown("#### Kreative Optionen (Der 'Grüne Hut')")
        st.markdown("Gibt es noch andere, unkonventionelle Optionen, die du bisher nicht in Betracht gezogen hast? (z.B. Kombinationen, Aufschieben, Dritte Option).")
        st.session_state.creative_options = st.text_area(
            "Andere Ideen:",
            value=st.session_state.creative_options,
            key="creative_options_area", height=100
        )

    st.markdown("---")
    with st.container():
        st.markdown(f"#### Zukunftsszenario (Regret Minimization Framework)")
        st.markdown("Stelle dir vor, du bist **80 Jahre alt**. Welche Entscheidung würdest du am meisten bereuen, **nicht** getroffen zu haben? Betrachte die langfristigen Auswirkungen.")
        st.session_state.future_scenario_a = st.text_area(
            f"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option A entscheidest?",
            value=st.session_state.future_scenario_a,
            key="scenario_a", height=150
        )
        st.session_state.future_scenario_b = st.text_area(
            f"Wie sieht dein Leben in 1, 3 und 5 Jahren aus, wenn du dich für Option B entscheidest?",
            value=st.session_state.future_scenario_b,
            key="scenario_b", height=150
        )

    st.markdown("---")
    if st.button("Weiter"):
        next_page('step_5')

def render_step_5():
    st.title("Step 5: Zusammenfassung & Abschluss (Der 'Blaue Hut')")
    
    with st.container():
        st.markdown("#### Übersicht")
        st.subheader("Deine Entscheidungssituation:")
        st.info(st.session_state.problem)
        st.subheader("Deine Optionen:")
        st.write(f"**Option A:** {st.session_state.options[0]}")
        st.write(f"**Option B:** {st.session_state.options[1]}")

    st.markdown("---")
    if st.session_state.selected_values:
        with st.container():
            st.markdown("#### Quantitative Auswertung (Werte-Matrix):")
            data = []
            score_a = 0
            score_b = 0
            for value in st.session_state.selected_values:
                # Sicherstellen, dass die Keys existieren, um Fehler zu vermeiden
                rating_a = st.session_state.values_rating.get(f"{value}_A", 0)
                rating_b = st.session_state.values_rating.get(f"{value}_B", 0)
                score_a += rating_a
                score_b += rating_b
                data.append({
                    "Wert": value,
                    "Option": st.session_state.options[0],
                    "Bewertung (1-10)": rating_a
                })
                data.append({
                    "Wert": value,
                    "Option": st.session_state.options[1],
                    "Bewertung (1-10)": rating_b
                })
            
            df = pd.DataFrame(data)
            
            st.write(f"**Gesamtpunktzahl Option A ({st.session_state.options[0]}):** **{score_a}**")
            st.write(f"**Gesamtpunktzahl Option B ({st.session_state.options[1]}):** **{score_b}**")

            if not df.empty:
                chart = alt.Chart(df).mark_bar(opacity=0.8, size=15).encode(
                    x=alt.X('Wert', title='Werte', axis=None),
                    y=alt.Y('Bewertung (1-10)', title='Kompatibilitätsscore (1-10)'),
                    color=alt.Color('Option', legend=alt.Legend(title="Option")),
                    column=alt.Column('Option', header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
                    tooltip=['Wert', 'Option', 'Bewertung (1-10)']
                ).properties(
                    title="Werte-Bewertung im Vergleich"
                ).configure_header(
                    titleFontSize=16,
                    labelFontSize=14
                )
                
                st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    with st.container():
        st.markdown("#### Qualitative Analyse:")
        
        st.markdown("##### Emotionen & Bauchgefühl:")
        st.info(st.session_state.emotions if st.session_state.emotions else "_Keine Emotionen eingetragen._")
        
        col_summary_a, col_summary_b = st.columns(2)
        
        with col_summary_a:
            st.markdown(f"##### Pro/Contra für Option A: {st.session_state.options[0]}")
            st.markdown("**Vorteile:**")
            st.write(st.session_state.pro_a if st.session_state.pro_a else "_Keine Vorteile eingetragen._")
            st.markdown("**Nachteile/Risiken:**")
            st.write(st.session_state.contra_a if st.session_state.contra_a else "_Keine Nachteile eingetragen._")
        
        with col_summary_b:
            st.markdown(f"##### Pro/Contra für Option B: {st.session_state.options[1]}")
            st.markdown("**Vorteile:**")
            st.write(st.session_state.pro_b if st.session_state.pro_b else "_Keine Vorteile eingetragen._")
            st.markdown("**Nachteile/Risiken:**")
            st.write(st.session_state.contra_b if st.session_state.contra_b else "_Keine Nachteile eingetragen._")

        st.markdown("---")
        st.markdown("##### Zukunftsszenarien (Regret Minimization):")
        st.write(f"**Szenario A:** {st.session_state.future_scenario_a if st.session_state.future_scenario_a else '_Kein Szenario eingetragen._'}")
        st.write(f"**Szenario B:** {st.session_state.future_scenario_b if st.session_state.future_scenario_b else '_Kein Szenario eingetragen._'}")

        if st.session_state.creative_options:
            st.markdown("##### Weitere Ideen (Grüner Hut)")
            st.write(st.session_state.creative_options)
    
    st.markdown("---")
    with st.container():
        st.markdown("#### Dein erster konkreter Schritt")
        st.markdown("""
        Nutze die **SMART-Methode**, um deinen ersten Schritt zu planen: **S**pezifisch, **M**essbar, **A**ttraktiv, **R**ealistisch, **T**erminiert.
        """)
        st.session_state.first_step = st.text_area(
            "Dein erster konkreter SMART-Schritt:",
            value=st.session_state.first_step,
            key="final_step_area"
        )
        
        st.markdown("---")
        if st.button("🎉 Entscheidung abschließen und speichern", use_container_width=True):
            st.success("Deine Entscheidungsreise wurde abgeschlossen! Du hast nun eine klare Basis für deine nächsten Schritte.")
        
    st.button("Neue Entscheidungsreise starten", on_click=reset_app)


def render_resilience_questions_page():
    st.title("Resilienz-Fragebogen")
    st.warning("Disclaimer: Dieses Tool dient der Selbsterkenntnis und ersetzt keine professionelle psychologische Beratung.")
    st.markdown("Bewerte auf einer Skala von **1 (stimme gar nicht zu)** bis **5 (stimme voll und ganz zu)**, wie sehr die folgenden Aussagen auf dich zutreffen.")

    for i, question in enumerate(resilience_questions):
        st.session_state.resilience_answers[i] = st.slider(
            question,
            1, 5, st.session_state.resilience_answers.get(i, 3), key=f"resilience_q_{i}"
        )
    
    st.markdown("---")
    if st.button("Fragebogen abschließen", use_container_width=True):
        # Berechne den Score vor dem Seitenwechsel
        total_score = sum(st.session_state.resilience_answers.values())
        st.session_state.resilience_score = total_score
        st.session_state.resilience_analysis = get_canned_analysis(total_score, len(resilience_questions) * 5)
        next_page('resilience_results')


def render_resilience_results_page():
    st.title("Deine Resilienz-Analyse")
    st.warning("Disclaimer: Dieser Fragebogen ist ein nicht-klinisches Werkzeug zur Selbsterkenntnis und ersetzt keine professionelle psychologische Beratung.")
    
    if st.session_state.resilience_score is None:
        st.warning("Bitte fülle zuerst den Fragebogen aus.")
        if st.button("Zum Fragebogen zurückkehren"):
            next_page('resilience_questions')
        return

    total_score = st.session_state.resilience_score
    max_score = len(resilience_questions) * 5
    st.markdown(f"**Deine Gesamtpunktzahl:** **{total_score}** von **{max_score}**")
    
    if st.session_state.resilience_analysis:
        st.markdown(st.session_state.resilience_analysis, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("#### Empfohlene nächste Schritte")
    st.markdown("""
    * **Tagebuch führen:** Schreibe täglich drei Dinge auf, die gut gelaufen sind.
    * **Achtsamkeit:** Probiere eine 5-minütige Meditationsübung aus.
    * **Soziale Kontakte:** Triff dich diese Woche bewusst mit einer unterstützenden Person.
    """)

    if st.button("Neue Reflexion starten oder zur Home-Seite"):
        next_page('start')


def render_bottom_nav():
    """Rendert die feste Navigationsleiste am unteren Bildschirmrand."""
    # Definiere die aktiven Seiten für jede Hauptkategorie
    is_decide_active = st.session_state.page in ['step_1', 'step_2', 'step_3', 'step_4', 'step_5']
    is_reflect_active = st.session_state.page in ['resilience_questions', 'resilience_results']
    is_start_active = st.session_state.page == 'start'
    
    # Der Grow-Pfad existiert in diesem Code nicht, wird aber für die Navigation beibehalten.
    is_grow_active = False 
    
    nav_html = f"""
    <div class="bottom-nav">
        <a href="javascript:void(0);" onclick="Streamlit.set
        ComponentValue('page', 'start')" class="nav-item {'active' if is_start_active else ''}">
            <span class="icon">🏠</span> Home
        </a>
        <a href="javascript:void(0);" onclick="Streamlit.set
        ComponentValue('page', 'step_1')" class="nav-item {'active' if is_decide_active else ''}">
            <span class="icon">🧠</span> Entscheiden
        </a>
        <a href="javascript:void(0);" onclick="Streamlit.set
        ComponentValue('page', 'resilience_questions')" class="nav-item {'active' if is_reflect_active else ''}">
            <span class="icon">🧘</span> Reflektieren
        </a>
        <a href="javascript:void(0);" class="nav-item {'active' if is_grow_active else ''}">
            <span class="icon">🌱</span> Wachstum
        </a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)


# --- MAIN APP LOGIC ---

def main():
    st.set_page_config(
        page_title="Entscheidungshelfer",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    initialize_session_state()

    # Custom CSS für Styling und Bottom Navigation
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }

        /* Haupt-Button-Styling */
        .stButton>button {
            border-radius: 8px;
            border: 1px solid #4CAF50;
            color: #1E8449; /* Dunkleres Grün */
            background-color: #E9F7EF; /* Sehr helles Grün */
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #D6EADF; /* Leicht dunkleres Hover */
            color: #145A32;
        }
        
        /* Überschriften-Farbe */
        .stTitle, .stSubheader {
            color: #1E8449;
        }
        
        /* Bottom Navigation Bar Styles */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
            background-color: #f7f9fc;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        .nav-item {
            text-decoration: none;
            color: #333;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 15px;
            border-radius: 50px;
            transition: background-color 0.3s, color 0.3s;
            display: flex;
            align-items: center;
            gap: 5px;
            cursor: pointer; /* Wichtig für Streamlit.setComponentValue */
        }
        .nav-item:hover {
            background-color: #e0e6ef;
        }
        .nav-item.active {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .icon {
            font-size: 1.2em;
        }

        /* Haupt-Content-Bereich anpassen */
        .main {
            padding-bottom: 70px; /* Platz für die Bottom Nav Bar */
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Seiten-Dispatcher
    page = st.session_state.page
    
    if page == 'start':
        render_start()
    elif page == 'step_1':
        render_step_1()
    elif page == 'step_2':
        render_step_2()
    elif page == 'step_3':
        render_step_3()
    elif page == 'step_4':
        render_step_4()
    elif page == 'step_5':
        render_step_5()
    elif page == 'resilience_questions':
        render_resilience_questions_page()
    elif page == 'resilience_results':
        render_resilience_results_page()
        
    # Navigation nur auf den Hauptschritten anzeigen
    if page in ['step_1', 'step_2', 'step_3', 'step_4', 'step_5']:
        render_bottom_nav()

if __name__ == '__main__':
    main()


import streamlit as st

# --- MAIN APP LOGIC ---

def main():
    # 1. Session State initialisieren
    # Setzt die Startseite, falls 'page' noch nicht im Session State existiert.
    if 'page' not in st.session_state:
        st.session_state.page = 'start'

    # 2. Query Parameter auslesen und Session State überschreiben
    query_params = st.query_params
    if 'page' in query_params:
        # Aktualisiert den Zustand basierend auf dem ersten Wert des Query-Parameters
        st.session_state.page = query_params['page'][0]

    # 3. Routing-Map: Seitenname auf die zugehörige Render-Funktion mappen
    # Dies ersetzt die lange elif-Kette.
    page_routes = {
        'start': render_start_page,
        'step_1': render_step_1,
        'step_2': render_step_2,
        'step_3': render_step_3,
        'step_4': render_step_4,
        'step_5': render_step_5,
        'wert_reflexion': render_resilience_questions_page,
        'resilience_results': render_resilience_results_page,
        'resilience_path_selection': render_resilience_path_selection,
        'resilience_path_day': render_resilience_path_day,
        'trophy_gallery': render_trophy_gallery,
    }

    # 4. Aktuelle Seite rendern
    current_page = st.session_state.page
    
    if current_page in page_routes:
        # Ruft die im Dictionary hinterlegte Funktion auf
        page_routes[current_page]()
    else:
        # Fallback-Mechanismus, falls eine unbekannte Seite aufgerufen wird
        st.error(f"Fehler: Seite '{current_page}' nicht gefunden. Zurück zur Startseite.")
        st.session_state.page = 'start'
        page_routes['start']()

    # 5. Bottom Navigation rendern
    # Die Logik bleibt: render_bottom_nav() nur anzeigen, wenn es nicht die Startseite ist.
    if st.session_state.page != 'start':
        render_bottom_nav()

# HINWEIS: Die Funktionen (z.B. render_start_page) müssen in Ihrem vollständigen
# Streamlit-Skript an dieser Stelle definiert oder importiert werden.

if __name__ == "__main__":
    main()
