# -*- coding: utf-8 -*-
"""
Wellity – Mentale Gesundheits-App
Kompletter Neuaufbau mit:
  1. Entscheidungsreise (6 Schritte)
  2. Resilienz-Check (11 Faktoren, Radar-Diagramm, personalisierte Auswertung)
  3. Resilienz-Training (Tägliche Challenges, Badges, Streak-System)
  4. Monetarisierung: Free / Pro / B2B Tiers
"""

import streamlit as st
import pandas as pd
import json
import time
import math
import copy
from datetime import date, datetime, timedelta
import random

# ──────────────────────────────────────────────────────────────────────────────
# 1.  PAGE CONFIG & GLOBAL CSS
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Wellity",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,600;0,800;1,300&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --sage:    #7A9E7E;
    --sage-lt: #B8D4BB;
    --cream:   #FAF7F2;
    --warm:    #F0E6D3;
    --gold:    #C8963E;
    --gold-lt: #F5D99A;
    --clay:    #C4714F;
    --ink:     #2C2C2C;
    --muted:   #7A7A6E;
    --white:   #FFFFFF;
    --card-shadow: 0 2px 20px rgba(44,44,44,0.07);
    --radius:  18px;
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background-color: var(--cream) !important; color: var(--ink); }
body { font-family: 'DM Sans', sans-serif; }
.stApp { padding-bottom: 80px; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 4rem !important; max-width: 860px; margin: auto; }

/* ── Typography ── */
h1 { font-family: 'Fraunces', serif; font-weight: 800; color: var(--ink); font-size: 2.6rem; letter-spacing: -0.02em; }
h2 { font-family: 'Fraunces', serif; font-weight: 600; color: var(--ink); font-size: 1.6rem; margin-bottom: 0.3rem; }
h3 { font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 1.1rem; color: var(--ink); }
p, li { color: var(--muted); font-size: 0.97rem; line-height: 1.6; }

/* ── Cards ── */
.vb-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    box-shadow: var(--card-shadow);
    margin-bottom: 1.2rem;
    border: 1px solid rgba(0,0,0,0.04);
}
.vb-card-warm {
    background: var(--warm);
    border-radius: var(--radius);
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.2rem;
}
.vb-card-sage {
    background: linear-gradient(135deg, #EBF2EC 0%, #D6E8D8 100%);
    border-radius: var(--radius);
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.2rem;
}

/* ── Hero Banner ── */
.vb-hero {
    background: linear-gradient(135deg, #2C2C2C 0%, #3D4A3E 60%, #7A9E7E 100%);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.vb-hero::before {
    content: '';
    position: absolute; top: -40%; right: -10%;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(200,150,62,0.25) 0%, transparent 70%);
}
.vb-hero h1 { color: var(--cream) !important; font-size: 3rem; margin: 0; }
.vb-hero p  { color: rgba(250,247,242,0.75) !important; font-size: 1.1rem; margin-top: 0.5rem; }

/* ── Feature Cards (Home) ── */
.feature-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin: 1.5rem 0; }
.feature-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.6rem 1.4rem;
    box-shadow: var(--card-shadow);
    border-top: 4px solid var(--sage);
    transition: transform 0.2s;
    cursor: pointer;
}
.feature-card:nth-child(2) { border-top-color: var(--gold); }
.feature-card:nth-child(3) { border-top-color: var(--clay); }
.feature-card:hover { transform: translateY(-3px); }
.feature-icon { font-size: 2rem; margin-bottom: 0.6rem; }
.feature-card h3 { margin: 0 0 0.4rem; color: var(--ink); }
.feature-card p  { font-size: 0.88rem; margin: 0; }
.feature-badge {
    display: inline-block;
    font-size: 0.7rem; font-weight: 600;
    background: var(--gold-lt); color: var(--gold);
    border-radius: 20px; padding: 2px 10px;
    margin-top: 0.6rem; text-transform: uppercase; letter-spacing: 0.05em;
}

/* ── Progress Stepper ── */
.stepper {
    display: flex; align-items: center;
    gap: 6px; margin-bottom: 2rem;
}
.step-dot {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700;
    background: var(--warm); color: var(--muted);
    flex-shrink: 0;
}
.step-dot.active  { background: var(--sage); color: white; }
.step-dot.done    { background: var(--sage-lt); color: var(--sage); }
.step-line { flex: 1; height: 2px; background: var(--warm); border-radius: 1px; }
.step-line.done   { background: var(--sage-lt); }

/* ── Buttons ── */
.stButton > button {
    background: var(--sage) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 2px 8px rgba(122,158,126,0.35) !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    background: #5D8562 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(122,158,126,0.45) !important;
}
.stButton > button:disabled {
    background: #C8C8C2 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    background: var(--warm) !important;
    border: 1.5px solid transparent !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--ink) !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--sage) !important;
    box-shadow: 0 0 0 3px rgba(122,158,126,0.15) !important;
}
.stSelectbox > div > div {
    background: var(--warm) !important;
    border-radius: 12px !important;
    border: 1.5px solid transparent !important;
}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: var(--sage) !important;
    border-color: var(--sage) !important;
}

/* ── Metric / Score display ── */
.score-ring {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    width: 120px; height: 120px; border-radius: 50%;
    background: conic-gradient(var(--sage) var(--pct, 50%), var(--warm) 0);
    margin: 0 auto 1rem;
    position: relative;
}
.score-ring-inner {
    position: absolute;
    width: 88px; height: 88px; border-radius: 50%;
    background: white;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.score-number { font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 800; color: var(--ink); line-height: 1; }
.score-label  { font-size: 0.6rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Factor bars ── */
.factor-bar-wrap { margin-bottom: 0.9rem; }
.factor-bar-header { display: flex; justify-content: space-between; margin-bottom: 4px; }
.factor-bar-label  { font-size: 0.85rem; font-weight: 600; color: var(--ink); }
.factor-bar-score  { font-size: 0.85rem; color: var(--muted); }
.factor-bar-bg { height: 8px; background: var(--warm); border-radius: 10px; overflow: hidden; }
.factor-bar-fill { height: 100%; border-radius: 10px; background: var(--sage); transition: width 0.6s ease; }
.factor-bar-fill.strength { background: var(--sage); }
.factor-bar-fill.potential { background: var(--gold); }
.factor-bar-fill.neutral   { background: var(--sage-lt); }

/* ── Badge / Trophy ── */
.badge-grid { display: flex; flex-wrap: wrap; gap: 0.8rem; margin-top: 0.5rem; }
.badge-item {
    display: flex; flex-direction: column; align-items: center;
    width: 80px; text-align: center;
}
.badge-icon {
    width: 56px; height: 56px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    background: var(--warm);
    border: 3px solid var(--warm);
    transition: all 0.2s;
}
.badge-icon.earned { background: var(--gold-lt); border-color: var(--gold); box-shadow: 0 2px 12px rgba(200,150,62,0.3); }
.badge-icon.locked { filter: grayscale(1); opacity: 0.45; }
.badge-name { font-size: 0.68rem; color: var(--muted); margin-top: 0.4rem; font-weight: 500; }

/* ── Streak counter ── */
.streak-box {
    background: linear-gradient(135deg, var(--gold-lt), var(--warm));
    border-radius: 14px;
    padding: 1rem 1.2rem;
    display: flex; align-items: center; gap: 1rem;
}
.streak-flame { font-size: 2.4rem; }
.streak-count { font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 800; color: var(--gold); line-height: 1; }
.streak-text  { font-size: 0.8rem; color: var(--muted); }

/* ── Challenge card ── */
.challenge-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.3rem 1.5rem;
    box-shadow: var(--card-shadow);
    border-left: 5px solid var(--sage);
    margin-bottom: 1rem;
}
.challenge-card.gold-border  { border-left-color: var(--gold); }
.challenge-card.clay-border  { border-left-color: var(--clay); }
.challenge-tag {
    display: inline-block;
    font-size: 0.68rem; font-weight: 700;
    background: var(--sage-lt); color: var(--sage);
    border-radius: 20px; padding: 2px 10px;
    text-transform: uppercase; letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
}
.challenge-tag.gold { background: var(--gold-lt); color: #996C20; }
.challenge-tag.clay { background: #FADDD3; color: var(--clay); }
.challenge-title { font-size: 1rem; font-weight: 600; color: var(--ink); margin: 0.2rem 0 0.4rem; }
.challenge-desc  { font-size: 0.87rem; color: var(--muted); margin: 0; }

/* ── Pricing cards ── */
.pricing-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; }
.pricing-card {
    background: var(--white); border-radius: var(--radius);
    padding: 1.8rem 1.5rem;
    box-shadow: var(--card-shadow);
    border: 2px solid transparent;
    text-align: center;
}
.pricing-card.featured { border-color: var(--sage); }
.pricing-price { font-family: 'Fraunces', serif; font-size: 2.4rem; font-weight: 800; color: var(--ink); }
.pricing-period { font-size: 0.8rem; color: var(--muted); }
.pricing-feat { font-size: 0.85rem; color: var(--muted); text-align: left; margin: 0.3rem 0; }
.pricing-feat::before { content: '✓  '; color: var(--sage); font-weight: 700; }

/* ── Bottom Nav ── */
.bottom-nav {
    position: fixed; bottom: 0; left: 0; width: 100%;
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(12px);
    border-top: 1px solid rgba(0,0,0,0.07);
    display: flex; justify-content: space-around;
    padding: 10px 0 14px; z-index: 999;
}
.nav-btn {
    display: flex; flex-direction: column; align-items: center;
    font-size: 0.68rem; font-weight: 600;
    color: var(--muted); cursor: pointer;
    text-decoration: none; gap: 3px;
    transition: color 0.2s;
    background: none; border: none; padding: 0;
    font-family: 'DM Sans', sans-serif;
}
.nav-btn.active { color: var(--sage); }
.nav-btn span { font-size: 1.35rem; }

/* ── Expander ── */
details { background: var(--white); border-radius: 14px; padding: 0 1.2rem; margin-bottom: 0.6rem; border: 1px solid rgba(0,0,0,0.05); }
summary { padding: 1rem 0; cursor: pointer; font-weight: 600; font-size: 0.95rem; color: var(--ink); }

/* ── Info / warning banners ── */
.stAlert { border-radius: 12px !important; }

/* ── Divider ── */
.vb-divider { height: 1px; background: var(--warm); margin: 1.5rem 0; border: none; }

/* ── Pro badge ── */
.pro-lock {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--gold-lt); color: #8a6010;
    font-size: 0.75rem; font-weight: 700;
    border-radius: 20px; padding: 3px 12px;
    text-transform: uppercase; letter-spacing: 0.06em;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# 2.  SESSION STATE INITIALISATION
# ──────────────────────────────────────────────────────────────────────────────

DEFAULTS = dict(
    page="home",
    plan="free",           # "free" | "pro" | "b2b"

    # ── Entscheidungsreise ──
    dj_problem="", dj_category="Wähle eine Kategorie",
    dj_option_a="", dj_option_b="",
    dj_values_selected=[], dj_values_rating={},
    dj_emotions="",
    dj_pro_a="", dj_contra_a="", dj_pro_b="", dj_contra_b="",
    dj_creative="",
    dj_future_a="", dj_future_b="",
    dj_first_step="",

    # ── Resilienz-Check ──
    rc_answers={},          # factor_key -> list of 3 scores
    rc_done=False,
    rc_scores={},           # factor_key -> total (3-15)
    rc_page=0,              # which factor page we're on (0-10)

    # ── Training ──
    tr_streak=0,
    tr_last_date=None,
    tr_completed_today=[],  # list of challenge ids completed today
    tr_total_done=0,
    tr_badges_earned=[],
    tr_challenge_log=[],    # list of {date, challenge_id, factor}

    # ── Lebensübergänge ──
    lu_type=None,           # aktuell gewählter Übergangstyp (Key aus TRANSITIONS)
    lu_step=0,               # aktueller Reflexionsschritt innerhalb des Typs
    lu_answers={},           # typ -> {schritt_label: antworttext}

    # ── Werte-Kompass ──
    wk_wheel={},             # lebensbereich -> zufriedenheit (0-10)
    wk_values=[],            # ausgewählte Top-Werte (max. 5)
    wk_values_reflection="",
    wk_journal=[],           # list of {date, prompt, text}
)

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        # deepcopy: verhindert, dass alle Sessions dieselben list/dict-Objekte
        # aus DEFAULTS teilen (sonst könnten sich Nutzer:innen z. B. Journal-
        # Einträge gegenseitig überschreiben, da DEFAULTS nur einmal beim
        # Modulimport erstellt wird).
        st.session_state[k] = copy.deepcopy(v)


def go(page):
    st.session_state.page = page
    st.rerun()

def reset_dj():
    for k in list(DEFAULTS.keys()):
        if k.startswith("dj_"):
            st.session_state[k] = copy.deepcopy(DEFAULTS[k])
    go("home")

def reset_rc():
    for k in list(DEFAULTS.keys()):
        if k.startswith("rc_"):
            st.session_state[k] = copy.deepcopy(DEFAULTS[k])
    go("home")

def reset_lu():
    for k in list(DEFAULTS.keys()):
        if k.startswith("lu_"):
            st.session_state[k] = copy.deepcopy(DEFAULTS[k])
    go("lu_intro")


# ──────────────────────────────────────────────────────────────────────────────
# 3.  DATA  –  categories, resilience factors, challenges, badges
# ──────────────────────────────────────────────────────────────────────────────

CATEGORIES = {
    "Karriere & Beruf": {
        "values": ["Finanzielle Sicherheit", "Wachstum", "Autonomie", "Einfluss", "Anerkennung", "Work-Life-Balance"],
        "biases": [
            ("Verlustaversion", "Konzentriere ich mich mehr auf das, was ich verlieren könnte, als auf das, was ich gewinnen könnte?"),
            ("Ankereffekt", "Hänge ich zu sehr an einem ersten Angebot fest, das mich daran hindert, bessere Optionen zu sehen?"),
            ("Bestätigungsfehler", "Suche ich nur Informationen, die meine bereits getroffene Entscheidung bestätigen?"),
        ],
    },
    "Persönliches Wachstum": {
        "values": ["Selbstverwirklichung", "Kreativität", "Lernen", "Soziale Bindungen", "Entwicklung", "Freiheit"],
        "biases": [
            ("Status-quo-Verzerrung", "Ziehe ich die einfachere Option vor, weil ich Angst vor Veränderung habe?"),
            ("Bestätigungsfehler", "Suche ich nur nach Belegen, dass etwas zu schwer ist?"),
            ("Verfügbarkeitsheuristik", "Stütze ich meine Entscheidung auf spektakuläre, aber seltene Beispiele?"),
        ],
    },
    "Beziehungen & Familie": {
        "values": ["Soziale Bindungen", "Harmonie", "Vertrauen", "Empathie", "Stabilität", "Zugehörigkeit"],
        "biases": [
            ("Rosinenpicken", "Ignoriere ich alle negativen Aspekte, um eine schwierige Situation zu umgehen?"),
            ("Sunk Cost Fallacy", "Bleibe ich in einer Situation, nur weil ich schon so viel investiert habe?"),
            ("Bestätigungsfehler", "Höre ich nur auf Freunde, die meine Meinung teilen?"),
        ],
    },
    "Gesundheit & Wohlbefinden": {
        "values": ["Vitalität", "Selbstfürsorge", "Balance", "Energie", "Langlebigkeit", "Achtsamkeit"],
        "biases": [
            ("Optimismus-Bias", "Glaube ich, dass mich schlechte Folgen nicht treffen werden?"),
            ("Gegenwartspräferenz", "Bevorzuge ich kurzfristigen Genuss gegenüber langfristiger Gesundheit?"),
            ("Kontrollillusion", "Überschätze ich meinen Einfluss auf äußere Gesundheitsfaktoren?"),
        ],
    },
}

RC_FACTORS = [
    {
        "key": "coping",
        "name": "Bewältigungsstrategien",
        "icon": "🛡️",
        "short": "Coping",
        "questions": [
            "Wenn ich unter Stress stehe, kann ich ruhig bleiben und eine Lösung finden.",
            "Ich habe Strategien, um mit negativen Gefühlen wie Wut oder Trauer umzugehen.",
            "Ich bin in der Lage, bei Problemen aktiv zu handeln, anstatt sie zu erdulden.",
        ],
        "tips_strength": [
            "Teile deine Strategien als Mentor:in mit anderen.",
            "Erstelle einen schriftlichen Krisenplan, um auch unter extremem Druck vorbereitet zu sein.",
            "Probiere neue kreative Ausdrucksformen wie Schreiben oder Malen als zusätzliches Ventil.",
        ],
        "tips_growth": [
            "Starte klein: Liste bei Frustration alle möglichen Lösungen auf – auch absurde.",
            "Lerne die 4-7-8-Atemtechnik (4 s einatmen, 7 s halten, 8 s ausatmen) für Akutsituationen.",
            "Führe ein Gefühls-Tagebuch, um Emotionen zu benennen und Muster zu erkennen.",
        ],
    },
    {
        "key": "spirituality",
        "name": "Spiritualität & Sinn",
        "icon": "✨",
        "short": "Sinn",
        "questions": [
            "Mein Glaube oder meine spirituellen Praktiken geben mir in schwierigen Zeiten Kraft.",
            "Ich habe das Gefühl, dass es einen größeren Sinn gibt, der mir hilft, Krisen zu überwinden.",
            "Ich finde Trost in meiner Verbindung zu etwas Größerem als mir selbst.",
        ],
        "tips_strength": [
            "Vertiefte dich in deine spirituelle Gemeinschaft und stärke andere dort.",
            "Integriere eine tägliche Dankbarkeitsübung, die auf deinen Überzeugungen basiert.",
            "Schaffe persönliche Rituale für besondere Herausforderungen.",
        ],
        "tips_growth": [
            "Überlege, was deinem Leben Sinn gibt – Natur, Kunst, Musik, Helfen.",
            "Probiere 5 Minuten Achtsamkeit im Freien täglich.",
            "Lies inspirierende Bücher oder Podcasts über Philosophie oder Lebenssinn.",
        ],
    },
    {
        "key": "selfesteem",
        "name": "Selbstwertgefühl",
        "icon": "💛",
        "short": "Selbstwert",
        "questions": [
            "Ich habe ein gutes Gefühl für meinen eigenen Wert und meine Fähigkeiten.",
            "Ich kann meine Erfolge anerkennen, auch wenn ich mit Rückschlägen konfrontiert bin.",
            "Ich bin stolz auf die Person, die ich bin.",
        ],
        "tips_strength": [
            "Führe ein Erfolgsjournal – halte auch kleine Meilensteine fest.",
            "Gib anderen auf positive Weise Feedback und ermutige sie.",
            "Nimm bewusst neue Herausforderungen an, die dich aus der Komfortzone bringen.",
        ],
        "tips_growth": [
            "Behandle dich selbst mit der Freundlichkeit, die du einem guten Freund zeigen würdest.",
            "Schreibe eine Liste deiner Talente und positiven Eigenschaften.",
            "Sprich täglich positive Affirmationen aus: 'Ich bin wertvoll. Ich kann das.'",
        ],
    },
    {
        "key": "selfefficacy",
        "name": "Selbstwirksamkeit",
        "icon": "🚀",
        "short": "Wirksamkeit",
        "questions": [
            "Ich bin zuversichtlich, dass ich schwierige Aufgaben meistern kann.",
            "Wenn ich mir ein Ziel setze, bin ich überzeugt, dass ich es erreichen werde.",
            "Ich weiß, wie ich meine Fähigkeiten einsetzen kann, um Probleme zu lösen.",
        ],
        "tips_strength": [
            "Setze dir absichtlich neue, herausfordernde Ziele, um dich weiterzuentwickeln.",
            "Sei Rollenmodell: Unterstütze andere dabei, ihre Ziele zu erreichen.",
            "Nutze deine lösungsorientierte Denkweise aktiv, wenn Freunde Rat suchen.",
        ],
        "tips_growth": [
            "Schreibe jeden Abend eine Sache auf, die du heute gut gemacht hast.",
            "Zerlege große Ziele in kleine, machbare Schritte.",
            "Visualisiere vor der Umsetzung, wie du das Problem erfolgreich löst.",
        ],
    },
    {
        "key": "social",
        "name": "Soziale Unterstützung",
        "icon": "🤝",
        "short": "Sozial",
        "questions": [
            "Ich kann mich jederzeit auf Freunde oder Familie verlassen, wenn ich Hilfe brauche.",
            "Ich fühle mich in meinen sozialen Beziehungen verstanden und unterstützt.",
            "Ich habe Menschen in meinem Leben, die mir in Krisenzeiten emotionalen Halt geben.",
        ],
        "tips_strength": [
            "Organisiere regelmäßige Treffen und bleibe aktiv in Kontakt.",
            "Biete Unterstützung an – Geben stärkt die Verbindung genauso wie Empfangen.",
            "Sei offen, neue Menschen kennenzulernen und dein Netzwerk zu erweitern.",
        ],
        "tips_growth": [
            "Übe aktives Zuhören ohne sofort Ratschläge zu geben.",
            "Beginne mit einer Person: Ruf einen alten Freund an oder lad einen Kollegen zum Kaffee ein.",
            "Tritt einem Verein oder einer Freiwilligengruppe bei.",
        ],
    },
    {
        "key": "hope",
        "name": "Hoffnung",
        "icon": "🌅",
        "short": "Hoffnung",
        "questions": [
            "Ich glaube, dass die Zukunft besser sein wird als die Gegenwart.",
            "Ich habe klare Ziele und bin zuversichtlich, Wege zu finden, sie zu erreichen.",
            "Selbst in schwierigen Momenten halte ich an der Überzeugung fest, dass sich die Dinge zum Guten wenden.",
        ],
        "tips_strength": [
            "Erstelle eine Visionstafel mit Bildern deiner Zukunftsziele.",
            "Hilf Freunden, die Hoffnung verloren haben, indem du ihnen Wege aufzeigst.",
            "Definiere klare SMART-Ziele und entwickle konkrete Pläne.",
        ],
        "tips_growth": [
            "Setze diese Woche ein kleines, erreichbares Ziel.",
            "Lies Biografien inspirierender Persönlichkeiten, die Widrigkeiten überwunden haben.",
            "Schreibe in ein Zukunfts-Tagebuch über deine Hoffnungen und Träume.",
        ],
    },
    {
        "key": "optimism",
        "name": "Optimismus",
        "icon": "☀️",
        "short": "Optimismus",
        "questions": [
            "Ich konzentriere mich meistens auf die positiven Aspekte einer Situation.",
            "Ich erwarte, dass gute Dinge passieren werden.",
            "Ich sehe Rückschläge eher als vorübergehend und nicht als dauerhaft an.",
        ],
        "tips_strength": [
            "Helfe Freunden, gemeinsam einen Silberstreifen in Problemen zu finden.",
            "Reduziere bewusst negativen Nachrichtenkonsum.",
            "Suche den Kontakt zu positiven Menschen und plane Freude-Aktivitäten.",
        ],
        "tips_growth": [
            "Schreibe jeden Abend drei Dinge auf, für die du dankbar bist.",
            "Frage bei Rückschlägen: 'Was kann ich daraus lernen?'",
            "Stoppe negative Gedanken bewusst und ersetze sie durch positive.",
        ],
    },
    {
        "key": "posemotions",
        "name": "Positive Emotionen",
        "icon": "😊",
        "short": "Pos. Emotionen",
        "questions": [
            "Ich kann Freude und Zufriedenheit empfinden, auch wenn ich unter Druck stehe.",
            "Ich versuche aktiv, positive Gefühle zu kultivieren, z. B. durch Hobbys.",
            "Ich bin gut darin, die positiven Aspekte einer Krise zu erkennen.",
        ],
        "tips_strength": [
            "Organisiere Aktivitäten, die dir und anderen Freude bereiten.",
            "Teile schöne Momente aktiv mit anderen.",
            "Schaffe regelmäßige Freude-Rituale (z. B. Morgenmusik).",
        ],
        "tips_growth": [
            "Mache jeden Tag ein Foto von etwas, das dich lächeln lässt.",
            "Entdecke ein Hobby, das dich in einen Flow-Zustand versetzt.",
            "Verbringe Zeit mit Menschen, die dich zum Lachen bringen.",
        ],
    },
    {
        "key": "locus",
        "name": "Kontrollüberzeugung",
        "icon": "🎯",
        "short": "Kontrolle",
        "questions": [
            "Ich glaube, dass ich mein Leben und die Dinge, die mir passieren, selbst in der Hand habe.",
            "Ich sehe meine Handlungen als entscheidend für meinen Erfolg.",
            "Ich bin davon überzeugt, dass meine Bemühungen einen Unterschied machen.",
        ],
        "tips_strength": [
            "Übernimm bei Projekten bewusst die volle Verantwortung.",
            "Triff bewusste Entscheidungen und stehe dazu.",
            "Übe darin, loszulassen – nicht alles lässt sich kontrollieren.",
        ],
        "tips_growth": [
            "Schreibe zwei Listen: 'Was kann ich kontrollieren?' und 'Was nicht?' – fokussiere auf Liste 1.",
            "Hinterfrage Glaubenssätze, die dir das Gefühl geben, machtlos zu sein.",
            "Erreiche ein kleines Ziel heute und spüre, wie es sich anfühlt, die Kontrolle zu haben.",
        ],
    },
    {
        "key": "hardiness",
        "name": "Widerstandsfähigkeit",
        "icon": "💪",
        "short": "Hardiness",
        "questions": [
            "Ich fühle mich in der Lage, die Herausforderungen meines Lebens zu kontrollieren.",
            "Ich bin voll engagiert in dem, was ich im Leben tue.",
            "Ich betrachte neue Erfahrungen eher als Chance denn als Bedrohung.",
        ],
        "tips_strength": [
            "Such bewusst neue, herausfordernde Projekte – beruflich wie privat.",
            "Teile deine Wachstumsperspektive mit anderen.",
            "Verlasse deine Komfortzone und probiere etwas völlig Neues.",
        ],
        "tips_growth": [
            "Führe ein Stress-Tagebuch, um Auslöser und Muster zu erkennen.",
            "Frage bei Problemen: 'Was kann ich hieraus lernen?'",
            "Gehe ein kleines Risiko ein (z. B. im Restaurant etwas Neues bestellen).",
        ],
    },
    {
        "key": "coherence",
        "name": "Kohärenzgefühl",
        "icon": "🔗",
        "short": "Kohärenz",
        "questions": [
            "Ich verstehe die Welt um mich herum und die Ereignisse in meinem Leben.",
            "Ich bin zuversichtlich, dass ich die Ressourcen habe, um Lebensanforderungen zu bewältigen.",
            "Ich sehe die Herausforderungen des Lebens als lohnenswert und bedeutungsvoll.",
        ],
        "tips_strength": [
            "Hilf anderen, die Welt verständlicher zu machen – durch Lehren oder Mentoring.",
            "Reflektiere, wie deine täglichen Handlungen mit deinen Werten übereinstimmen.",
            "Stelle kleine Probleme in einen größeren Lebenskontext.",
        ],
        "tips_growth": [
            "Schreibe deine zentralen Werte auf (Familie, Ehrlichkeit, Kreativität…).",
            "Betrachte Ereignisse bewusst aus einem anderen Blickwinkel.",
            "Finde Wege, deinen Alltag sinnvoller zu gestalten – verbinde Arbeit mit Werten.",
        ],
    },
]

# Alle Challenges (faktor-gebunden)
CHALLENGES = [
    # Coping
    {"id": "c01", "factor": "coping",      "title": "Atem-Pause",         "desc": "Führe die 4-7-8-Atemübung 3x durch, wann immer du heute gestresst bist.",    "color": "green", "xp": 20},
    {"id": "c02", "factor": "coping",      "title": "Gefühls-Scan",       "desc": "Schreibe am Abend auf: Welche 3 Emotionen habe ich heute am stärksten gespürt?", "color": "green", "xp": 15},
    {"id": "c03", "factor": "coping",      "title": "Lösungsliste",       "desc": "Wähle ein aktuelles Problem und liste 10 mögliche Lösungsansätze auf – egal wie verrückt.",  "color": "green", "xp": 25},
    # Optimismus
    {"id": "o01", "factor": "optimism",    "title": "Dankbarkeits-Trio",  "desc": "Schreibe heute Abend 3 konkrete Dinge auf, für die du dankbar bist.",        "color": "gold",  "xp": 15},
    {"id": "o02", "factor": "optimism",    "title": "Silberstreifen",     "desc": "Nimm ein aktuelles Problem und schreibe einen positiven Aspekt oder eine Lernerfahrung dazu.", "color": "gold", "xp": 20},
    {"id": "o03", "factor": "optimism",    "title": "Gute Nachrichten",   "desc": "Suche heute aktiv eine gute Nachricht oder inspirierende Geschichte und teile sie mit jemandem.", "color": "gold", "xp": 15},
    # Selbstwirksamkeit
    {"id": "s01", "factor": "selfefficacy","title": "Mini-Sieg",          "desc": "Setze dir heute Morgen ein kleines, erreichbares Ziel. Erledige es und feiere es bewusst.",   "color": "green", "xp": 20},
    {"id": "s02", "factor": "selfefficacy","title": "Erfolgs-Rückblick",  "desc": "Schreibe 5 Dinge auf, die du in den letzten 6 Monaten erfolgreich gemeistert hast.",         "color": "green", "xp": 20},
    {"id": "s03", "factor": "selfefficacy","title": "Schritt für Schritt", "desc": "Nimm ein großes Ziel und zerlege es in 5 konkrete kleine Schritte.",                          "color": "green", "xp": 25},
    # Soziale Verbindung
    {"id": "n01", "factor": "social",      "title": "Echte Verbindung",   "desc": "Schreibe oder rufe heute eine Person an, die dir wichtig ist, nur um zu hören, wie es ihr geht.", "color": "clay", "xp": 25},
    {"id": "n02", "factor": "social",      "title": "Zuhör-Übung",        "desc": "Führe heute ein Gespräch, in dem du nur zuhörst – ohne Ratschläge zu geben.",                   "color": "clay", "xp": 20},
    {"id": "n03", "factor": "social",      "title": "Dankeschön sagen",   "desc": "Danke heute jemandem explizit für etwas, das er oder sie für dich getan hat.",                  "color": "clay", "xp": 15},
    # Hoffnung
    {"id": "h01", "factor": "hope",        "title": "Vision-Blick",       "desc": "Schreibe in 10 Minuten auf, wie dein ideales Leben in 3 Jahren aussieht.",                     "color": "gold",  "xp": 25},
    {"id": "h02", "factor": "hope",        "title": "SMART-Ziel",         "desc": "Definiere ein SMART-Ziel für die nächsten 30 Tage.",                                           "color": "gold",  "xp": 30},
    # Positive Emotionen
    {"id": "p01", "factor": "posemotions", "title": "Freuden-Foto",       "desc": "Mache heute ein Foto von etwas, das dich anlächelt. Speichere es bewusst.",                    "color": "clay",  "xp": 10},
    {"id": "p02", "factor": "posemotions", "title": "Flow finden",        "desc": "Widme dir 20 Minuten einem Hobby oder einer Tätigkeit, die dich vollständig einsaugt.",        "color": "clay",  "xp": 20},
    # Kohärenz
    {"id": "k01", "factor": "coherence",   "title": "Werte-Kompass",      "desc": "Schreibe deine 5 wichtigsten persönlichen Werte auf und begründe, warum sie dir wichtig sind.", "color": "green", "xp": 25},
    {"id": "k02", "factor": "coherence",   "title": "Perspektivwechsel",  "desc": "Nimm eine aktuelle Herausforderung und beschreibe sie aus der Sicht eines weisen Freundes.",    "color": "green", "xp": 20},
]

BADGES = [
    {"id": "first_step",   "name": "Erster Schritt",   "icon": "🌱", "desc": "Erste Challenge abgeschlossen",     "condition": lambda s: s["total"] >= 1},
    {"id": "streak3",      "name": "3 Tage am Stück",  "icon": "🔥", "desc": "3 Tage Streak erreicht",           "condition": lambda s: s["streak"] >= 3},
    {"id": "streak7",      "name": "Eine Woche",        "icon": "🏅", "desc": "7 Tage Streak erreicht",           "condition": lambda s: s["streak"] >= 7},
    {"id": "streak30",     "name": "Ein Monat",         "icon": "🥇", "desc": "30 Tage Streak erreicht",          "condition": lambda s: s["streak"] >= 30},
    {"id": "total10",      "name": "Fleißige Biene",    "icon": "🐝", "desc": "10 Challenges abgeschlossen",      "condition": lambda s: s["total"] >= 10},
    {"id": "total50",      "name": "Resilienz-Profi",   "icon": "⭐", "desc": "50 Challenges abgeschlossen",      "condition": lambda s: s["total"] >= 50},
    {"id": "all_factors",  "name": "Ganzheitlich",      "icon": "🌈", "desc": "Aus allen 11 Faktoren trainiert",  "condition": lambda s: len(s["factors"]) >= 11},
    {"id": "social_star",  "name": "Sozial-Star",       "icon": "🤝", "desc": "5 soziale Challenges erledigt",    "condition": lambda s: s["factor_counts"].get("social", 0) >= 5},
]

# Lebensübergänge – geführte Reflexionspfade je Situationstyp.
# Letzter Schritt hat prompt=None und wird als Zusammenfassung gerendert
# (gleiches Prinzip wie die Entscheidungsreise-Schritte 1-6).
TRANSITIONS = {
    "Jobverlust": {
        "icon": "💼",
        "steps": [
            ("Situation", "Was genau ist passiert, und wie hast du davon erfahren?"),
            ("Gefühle", "Welche Gefühle kommen hoch, wenn du daran denkst? Alle sind erlaubt."),
            ("Gedanken", "Welche Gedanken oder Befürchtungen gehen dir durch den Kopf?"),
            ("Ressourcen", "Wer oder was hat dir schon einmal durch eine schwierige Phase geholfen?"),
            ("Nächste Schritte", "Was ist ein kleiner, machbarer nächster Schritt – diese Woche?"),
            ("Zusammenfassung", None),
        ],
    },
    "Trennung": {
        "icon": "💔",
        "steps": [
            ("Situation", "Wie hat sich die Trennung entwickelt, und wo stehst du gerade?"),
            ("Gefühle", "Was fühlst du gerade – Trauer, Wut, Erleichterung, ein Mix?"),
            ("Gedanken", "Welche Geschichte erzählst du dir gerade über dich und die Beziehung?"),
            ("Ressourcen", "Wer aus deinem Umfeld tut dir gerade gut?"),
            ("Nächste Schritte", "Was würde dir diese Woche etwas Halt geben?"),
            ("Zusammenfassung", None),
        ],
    },
    "Umzug": {
        "icon": "📦",
        "steps": [
            ("Situation", "Was verändert sich durch den Umzug konkret in deinem Alltag?"),
            ("Gefühle", "Was löst der Umzug in dir aus – Vorfreude, Angst, Wehmut?"),
            ("Gedanken", "Was befürchtest du zu verlieren, und was erhoffst du dir?"),
            ("Ressourcen", "Was hat dir bei früheren Veränderungen geholfen, anzukommen?"),
            ("Nächste Schritte", "Welcher erste Schritt macht den neuen Ort ein bisschen vertrauter?"),
            ("Zusammenfassung", None),
        ],
    },
    "Trauer": {
        "icon": "🕯️",
        "steps": [
            ("Situation", "Wen oder was hast du verloren? Du musst hier nicht ins Detail gehen, wenn du nicht willst."),
            ("Gefühle", "Welche Gefühle sind gerade da? Es gibt kein 'richtig' oder 'falsch'."),
            ("Gedanken", "Gibt es unausgesprochene Dinge, die dich beschäftigen?"),
            ("Ressourcen", "Was oder wer hält dich gerade?"),
            ("Nächste Schritte", "Was würde dir heute guttun – und sei es nur eine Kleinigkeit?"),
            ("Zusammenfassung", None),
        ],
    },
    "Ausbildungsende": {
        "icon": "🎓",
        "steps": [
            ("Situation", "Was liegt hinter dir, und was liegt jetzt vor dir?"),
            ("Gefühle", "Stolz, Unsicherheit, Erleichterung – was überwiegt gerade?"),
            ("Gedanken", "Welche Erwartungen (eigene oder fremde) spürst du gerade am stärksten?"),
            ("Ressourcen", "Welche Fähigkeiten hast du dir in dieser Zeit erarbeitet?"),
            ("Nächste Schritte", "Was ist ein realistischer erster Schritt in den nächsten Lebensabschnitt?"),
            ("Zusammenfassung", None),
        ],
    },
}

# Werte-Kompass – Lebensrad, Werte-Klärung, Identitäts-Journaling
LIFE_DOMAINS = [
    "Beruf/Karriere", "Beziehungen", "Gesundheit", "Finanzen",
    "Pers. Wachstum", "Freizeit/Erholung", "Familie", "Sinn/Spiritualität",
]

VALUES_POOL = [
    "Freiheit", "Sicherheit", "Kreativität", "Familie", "Gesundheit",
    "Anerkennung", "Gerechtigkeit", "Abenteuer", "Verbindung", "Wachstum",
    "Verlässlichkeit", "Autonomie", "Erfolg", "Ruhe", "Neugier",
    "Ehrlichkeit", "Mitgefühl", "Ordnung", "Spiritualität", "Einfluss",
]

JOURNAL_PROMPTS = [
    "Was beschäftigt mich gerade am meisten?",
    "Welcher Teil von mir zeigt sich in letzter Zeit stärker als früher?",
    "Wovon möchte ich mich gerade lösen?",
    "Was würde ich tun, wenn ich wüsste, es geht nicht schief?",
    "Wer war ich vor 5 Jahren – wer bin ich heute?",
    "Was gibt mir gerade Halt?",
    "Wofür bin ich diese Woche dankbar?",
    "Welche Entscheidung schiebe ich gerade vor mir her?",
]

# Krisenkompass – immer über die Bottom-Nav ("🆘") erreichbar
HOTLINES = [
    {"name": "Telefonseelsorge (kostenlos, anonym, 24/7)", "phone": "0800 111 0 111"},
    {"name": "Telefonseelsorge (Alternativnummer)", "phone": "0800 111 0 222"},
    {"name": "Nummer gegen Kummer – Kinder- & Jugendtelefon", "phone": "116 111"},
    {"name": "Krisenchat.de", "url": "https://krisenchat.de"},
    {"name": "Ärztlicher Bereitschaftsdienst", "phone": "116 117"},
    {"name": "Bei akuter Lebensgefahr: Notruf", "phone": "112"},
]

FIVE_SENSES = [
    ("👀 Sehen", "Nenne 5 Dinge, die du gerade siehst."),
    ("✋ Fühlen", "Nenne 4 Dinge, die du gerade körperlich spürst."),
    ("👂 Hören", "Nenne 3 Geräusche, die du gerade hörst."),
    ("👃 Riechen", "Nenne 2 Dinge, die du riechen kannst."),
    ("👅 Schmecken", "Nenne 1 Sache, die du schmecken kannst."),
]


# ──────────────────────────────────────────────────────────────────────────────
# 4.  HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def check_badges():
    """Update earned badges based on current state."""
    total = st.session_state.tr_total_done
    streak = st.session_state.tr_streak
    factor_counts = {}
    for entry in st.session_state.tr_challenge_log:
        factor_counts[entry["factor"]] = factor_counts.get(entry["factor"], 0) + 1
    factors_used = set(e["factor"] for e in st.session_state.tr_challenge_log)

    stats = {"total": total, "streak": streak, "factors": factors_used, "factor_counts": factor_counts}
    earned = []
    for badge in BADGES:
        try:
            if badge["condition"](stats):
                earned.append(badge["id"])
        except Exception:
            pass
    st.session_state.tr_badges_earned = earned


def update_streak():
    today = date.today().isoformat()
    last = st.session_state.tr_last_date
    if last is None:
        pass  # first time
    elif last == today:
        return  # already counted today
    elif last == (date.today() - timedelta(days=1)).isoformat():
        st.session_state.tr_streak += 1
    else:
        st.session_state.tr_streak = 1
    st.session_state.tr_last_date = today


def complete_challenge(ch_id, factor):
    today = date.today().isoformat()
    if ch_id not in st.session_state.tr_completed_today:
        st.session_state.tr_completed_today.append(ch_id)
        st.session_state.tr_total_done += 1
        st.session_state.tr_challenge_log.append({"date": today, "challenge_id": ch_id, "factor": factor})
        update_streak()
        check_badges()
        st.rerun()


def get_factor_score(key):
    answers = st.session_state.rc_answers.get(key, [3, 3, 3])
    return sum(answers)


def get_top_factors(n=3):
    scores = {f["key"]: get_factor_score(f["key"]) for f in RC_FACTORS}
    return sorted(scores.items(), key=lambda x: -x[1])[:n]


def get_bottom_factors(n=2):
    scores = {f["key"]: get_factor_score(f["key"]) for f in RC_FACTORS}
    return sorted(scores.items(), key=lambda x: x[1])[:n]


def factor_label(score):
    if score <= 5:  return "Sehr niedrig"
    if score <= 8:  return "Niedrig"
    if score <= 11: return "Durchschnittlich"
    if score <= 14: return "Hoch"
    return "Sehr hoch"


def score_color(score):
    if score <= 5:  return "#C4714F"
    if score <= 8:  return "#C8963E"
    if score <= 11: return "#7A9E7E"
    if score <= 14: return "#5D8562"
    return "#3A6640"


def bar_class(key, tops, bots):
    top_keys = [k for k, _ in tops]
    bot_keys = [k for k, _ in bots]
    if key in top_keys: return "strength"
    if key in bot_keys: return "potential"
    return "neutral"


def render_stepper(current_step, total_steps, labels=None):
    dots = ""
    for i in range(1, total_steps + 1):
        if i < current_step:
            cls = "done"
        elif i == current_step:
            cls = "active"
        else:
            cls = ""
        dots += f'<div class="step-dot {cls}">{i}</div>'
        if i < total_steps:
            line_cls = "done" if i < current_step else ""
            dots += f'<div class="step-line {line_cls}"></div>'
    st.markdown(f'<div class="stepper">{dots}</div>', unsafe_allow_html=True)


def render_factor_bar(factor, score, bar_cls):
    pct = (score / 15) * 100
    st.markdown(f"""
    <div class="factor-bar-wrap">
        <div class="factor-bar-header">
            <span class="factor-bar-label">{factor['icon']} {factor['name']}</span>
            <span class="factor-bar-score">{score}/15 – {factor_label(score)}</span>
        </div>
        <div class="factor-bar-bg">
            <div class="factor-bar-fill {bar_cls}" style="width:{pct:.0f}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_life_wheel_bar(domain, score):
    """Wie render_factor_bar, aber für die 0-10-Skala des Lebensrads (Werte-Kompass)."""
    pct = (score / 10) * 100
    st.markdown(f"""
    <div class="factor-bar-wrap">
        <div class="factor-bar-header">
            <span class="factor-bar-label">{domain}</span>
            <span class="factor-bar-score">{score}/10</span>
        </div>
        <div class="factor-bar-bg">
            <div class="factor-bar-fill neutral" style="width:{pct:.0f}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_bottom_nav():
    pages = [("🏠", "Home",     "home"),
             ("🧠", "Decide",   "dj_step1"),
             ("💚", "Resilienz","rc_intro"),
             ("🏆", "Training", "training"),
             ("🆘", "SOS",      "sos"),
             ("⭐", "Pro",      "pricing")]
    active = st.session_state.page
    nav_html = '<div class="bottom-nav">'
    for icon, label, pg in pages:
        is_active = "active" if (active == pg or active.startswith(pg[:4])) else ""
        nav_html += f'''
        <form action="" method="get" style="margin:0;padding:0;">
          <button class="nav-btn {is_active}" name="nav" value="{pg}" type="submit">
            <span>{icon}</span>{label}
          </button>
        </form>'''
    nav_html += '</div>'
    st.markdown(nav_html, unsafe_allow_html=True)

    # Handle nav via query params
    params = st.query_params
    if "nav" in params:
        target = params["nav"]
        st.query_params.clear()
        go(target)


# ──────────────────────────────────────────────────────────────────────────────
# 5.  PAGES
# ──────────────────────────────────────────────────────────────────────────────

def page_home():
    st.markdown("""
    <div class="vb-hero">
        <h1>Wellity 🌱</h1>
        <p>Dein persönlicher Begleiter für mentale Stärke & gesunde Entscheidungen.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3>Entscheidungsreise</h3>
            <p>Strukturierte Analyse deiner Optionen mit bewährten Psychologie-Methoden.</p>
            <span class="feature-badge">6 Schritte</span>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💚</div>
            <h3>Resilienz-Check</h3>
            <p>11 wissenschaftliche Faktoren · Stärken & Potenziale · Radardiagramm.</p>
            <span class="feature-badge">11 Faktoren</span>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <h3>Resilienz-Training</h3>
            <p>Tägliche Challenges · Streak-System · Badges · Personalisiert nach deinem Check.</p>
            <span class="feature-badge">Neu</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Entscheidungsreise starten →"):
            go("dj_step1")
    with col2:
        if st.button("Resilienz-Check starten →"):
            go("rc_intro")
    with col3:
        if st.button("Training & Challenges →"):
            go("training")

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🌉</div>
            <h3>Lebensübergänge</h3>
            <p>Geführte Reflexion für Jobverlust, Trennung, Umzug, Trauer und Ausbildungsende.</p>
            <span class="feature-badge">Neu</span>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🧭</div>
            <h3>Werte-Kompass</h3>
            <p>Lebensrad, Werte-Klärung und wiederkehrendes Identitäts-Journaling.</p>
            <span class="feature-badge">Neu</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("Lebensübergänge starten →"):
            go("lu_intro")
    with col5:
        if st.button("Werte-Kompass öffnen →"):
            go("wk_home")
    # col6 bleibt leer – hält die Ausrichtung zur 3-spaltigen feature-grid oben

    st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="vb-card-warm">
        <p style="margin:0">🆘 Falls es dir gerade nicht gut geht: Im Krisenkompass (unten in der Navigation)
        findest du Grounding-Übungen und Hotlines.</p>
    </div>
    """, unsafe_allow_html=True)

    # Streak teaser if active
    if st.session_state.tr_streak > 0:
        st.markdown(f"""
        <div class="streak-box" style="margin-top:1.5rem">
            <span class="streak-flame">🔥</span>
            <div>
                <div class="streak-count">{st.session_state.tr_streak}</div>
                <div class="streak-text">Tage Streak aktiv</div>
            </div>
            <div style="margin-left:auto;font-size:0.85rem;color:#7A7A6E">
                {st.session_state.tr_total_done} Challenges abgeschlossen
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Pro teaser
    st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="vb-card-warm">
        <h3 style="margin:0 0 0.3rem">✨ VitaBoost Pro & B2B</h3>
        <p style="margin:0">KI-Analyse · Exportierbare Berichte · Teamdashboard für HR · Coaching-Integration</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Pläne & Preise ansehen →"):
        go("pricing")


# ── ENTSCHEIDUNGSREISE ────────────────────────────────────────────────────────

def page_dj_step1():
    st.markdown("## 🧠 Entscheidungsreise")
    render_stepper(1, 6)
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### Dein Problem & deine Optionen")

    st.session_state.dj_problem = st.text_area(
        "Was ist die Entscheidung, die dich beschäftigt?",
        value=st.session_state.dj_problem, height=100, key="dj_p")

    opts = ["Wähle eine Kategorie"] + list(CATEGORIES.keys())
    idx = opts.index(st.session_state.dj_category) if st.session_state.dj_category in opts else 0
    st.session_state.dj_category = st.selectbox("Kategorie:", opts, index=idx)

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.dj_option_a = st.text_area("Option A:", value=st.session_state.dj_option_a, height=80, key="dj_oa")
    with c2:
        st.session_state.dj_option_b = st.text_area("Option B:", value=st.session_state.dj_option_b, height=80, key="dj_ob")
    st.markdown('</div>', unsafe_allow_html=True)

    valid = all([st.session_state.dj_problem, st.session_state.dj_option_a,
                 st.session_state.dj_option_b, st.session_state.dj_category != "Wähle eine Kategorie"])
    if st.button("Weiter →", disabled=not valid):
        go("dj_step2")


def page_dj_step2():
    st.markdown("## 🧠 Entscheidungsreise")
    render_stepper(2, 6)
    cat = CATEGORIES.get(st.session_state.dj_category, {})
    values = cat.get("values", [])

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### Deine Werte")
    st.markdown(f"Wähle die Werte, die für deine Entscheidung relevant sind (**{st.session_state.dj_category}**).")

    selected = []
    cols = st.columns(3)
    for i, v in enumerate(values):
        if cols[i % 3].checkbox(v, key=f"dj_val_{v}",
                                value=(v in st.session_state.dj_values_selected)):
            selected.append(v)
    st.session_state.dj_values_selected = selected
    st.markdown('</div>', unsafe_allow_html=True)

    if selected:
        st.markdown('<div class="vb-card">', unsafe_allow_html=True)
        st.markdown("### Bewertungsmatrix")
        st.markdown("Wie gut erfüllt jede Option diesen Wert? (1 = gar nicht, 10 = vollständig)")
        for v in selected:
            st.markdown(f"**{v}**")
            c1, c2 = st.columns(2)
            with c1:
                st.session_state.dj_values_rating[f"{v}_A"] = st.slider(
                    f"Option A · {st.session_state.dj_option_a[:25]}",
                    1, 10, st.session_state.dj_values_rating.get(f"{v}_A", 5), key=f"vr_{v}_a")
            with c2:
                st.session_state.dj_values_rating[f"{v}_B"] = st.slider(
                    f"Option B · {st.session_state.dj_option_b[:25]}",
                    1, 10, st.session_state.dj_values_rating.get(f"{v}_B", 5), key=f"vr_{v}_b")
        st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Zurück"):
            go("dj_step1")
    with c2:
        if st.button("Weiter →", disabled=not selected):
            go("dj_step3")


def page_dj_step3():
    st.markdown("## 🧠 Entscheidungsreise")
    render_stepper(3, 6)

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🔴 Bauchgefühl – Der Rote Hut (Edward de Bono)")
    st.markdown("Schreibe auf, was du *fühlst* – nicht was du denkst. Keine Logik, nur Emotionen.")
    st.session_state.dj_emotions = st.text_area(
        "Deine Gefühle und Intuitionen:", value=st.session_state.dj_emotions, height=130, key="dj_em")
    st.markdown('</div>', unsafe_allow_html=True)

    cat = CATEGORIES.get(st.session_state.dj_category, {})
    biases = cat.get("biases", [])
    if biases:
        st.markdown('<div class="vb-card">', unsafe_allow_html=True)
        st.markdown("### 🕵️ Denkfehler-Reflexion")
        st.markdown("Überprüfe, ob einer dieser häufigen Denkfehler deine Entscheidung beeinflusst:")
        for title, question in biases:
            with st.expander(f"**{title}**"):
                st.markdown(question)
        st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Zurück"): go("dj_step2")
    with c2:
        if st.button("Weiter →"): go("dj_step4")


def page_dj_step4():
    st.markdown("## 🧠 Entscheidungsreise")
    render_stepper(4, 6)

    opt_a = st.session_state.dj_option_a
    opt_b = st.session_state.dj_option_b

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🟡 Vorteile – Der Gelbe Hut")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Option A: {opt_a}**")
        st.session_state.dj_pro_a = st.text_area("Vorteile:", value=st.session_state.dj_pro_a, height=120, key="dj_pa")
    with c2:
        st.markdown(f"**Option B: {opt_b}**")
        st.session_state.dj_pro_b = st.text_area("Vorteile:", value=st.session_state.dj_pro_b, height=120, key="dj_pb")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### ⚫ Nachteile – Der Schwarze Hut")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.dj_contra_a = st.text_area("Nachteile:", value=st.session_state.dj_contra_a, height=120, key="dj_ca")
    with c2:
        st.session_state.dj_contra_b = st.text_area("Nachteile:", value=st.session_state.dj_contra_b, height=120, key="dj_cb")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🟢 Kreative Optionen – Der Grüne Hut")
    st.markdown("Gibt es noch andere, unkonventionelle Optionen, die du bisher nicht bedacht hast?")
    st.session_state.dj_creative = st.text_area(
        "Weitere Ideen:", value=st.session_state.dj_creative, height=100, key="dj_cr")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Zurück"): go("dj_step3")
    with c2:
        if st.button("Weiter →"): go("dj_step5")


def page_dj_step5():
    st.markdown("## 🧠 Entscheidungsreise")
    render_stepper(5, 6)

    opt_a = st.session_state.dj_option_a
    opt_b = st.session_state.dj_option_b

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### ⏳ Zukunftsszenarien – Das Regret Minimization Framework")
    st.markdown("*Jeff Bezos:* Stelle dir vor, du bist 80 Jahre alt. Welche Entscheidung würdest du **am wenigsten bereuen**?")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Option A: {opt_a}**")
        st.markdown("Wie sieht dein Leben in 1, 3 und 5 Jahren aus?")
        st.session_state.dj_future_a = st.text_area(
            "", value=st.session_state.dj_future_a, height=160, key="dj_fa", label_visibility="collapsed")
    with c2:
        st.markdown(f"**Option B: {opt_b}**")
        st.markdown("Wie sieht dein Leben in 1, 3 und 5 Jahren aus?")
        st.session_state.dj_future_b = st.text_area(
            "", value=st.session_state.dj_future_b, height=160, key="dj_fb", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Zurück"): go("dj_step4")
    with c2:
        if st.button("Zur Zusammenfassung →"): go("dj_step6")


def page_dj_step6():
    st.markdown("## 🧠 Zusammenfassung")
    render_stepper(6, 6)

    opt_a = st.session_state.dj_option_a
    opt_b = st.session_state.dj_option_b

    # Quantitative Auswertung
    if st.session_state.dj_values_selected:
        score_a = sum(st.session_state.dj_values_rating.get(f"{v}_A", 0)
                      for v in st.session_state.dj_values_selected)
        score_b = sum(st.session_state.dj_values_rating.get(f"{v}_B", 0)
                      for v in st.session_state.dj_values_selected)
        winner = opt_a if score_a >= score_b else opt_b
        col1, col2, col3 = st.columns(3)
        col1.metric(f"Option A: {opt_a[:20]}", f"{score_a} Punkte")
        col2.metric(f"Option B: {opt_b[:20]}", f"{score_b} Punkte")
        col3.metric("Werte-Tendenz", winner[:20], delta="Höhere Wert-Erfüllung")

        # Bar chart via HTML
        max_s = max(score_a, score_b, 1)
        w_a = (score_a / max_s) * 100
        w_b = (score_b / max_s) * 100
        st.markdown(f"""
        <div class="vb-card" style="margin-top:0.5rem">
            <div style="margin-bottom:0.6rem">
                <div class="factor-bar-header">
                    <span class="factor-bar-label">{opt_a}</span>
                    <span class="factor-bar-score">{score_a} Punkte</span>
                </div>
                <div class="factor-bar-bg"><div class="factor-bar-fill strength" style="width:{w_a:.0f}%"></div></div>
            </div>
            <div>
                <div class="factor-bar-header">
                    <span class="factor-bar-label">{opt_b}</span>
                    <span class="factor-bar-score">{score_b} Punkte</span>
                </div>
                <div class="factor-bar-bg"><div class="factor-bar-fill potential" style="width:{w_b:.0f}%"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Qualitative Zusammenfassung
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Deine Gedanken auf einen Blick")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**✅ Vorteile {opt_a}**")
        st.write(st.session_state.dj_pro_a or "–")
        st.markdown(f"**❌ Nachteile {opt_a}**")
        st.write(st.session_state.dj_contra_a or "–")
        st.markdown(f"**🔭 Zukunft {opt_a}**")
        st.write(st.session_state.dj_future_a or "–")
    with c2:
        st.markdown(f"**✅ Vorteile {opt_b}**")
        st.write(st.session_state.dj_pro_b or "–")
        st.markdown(f"**❌ Nachteile {opt_b}**")
        st.write(st.session_state.dj_contra_b or "–")
        st.markdown(f"**🔭 Zukunft {opt_b}**")
        st.write(st.session_state.dj_future_b or "–")
    if st.session_state.dj_creative:
        st.markdown("**🟢 Weitere kreative Ideen**")
        st.write(st.session_state.dj_creative)
    if st.session_state.dj_emotions:
        st.markdown("**🔴 Bauchgefühl**")
        st.write(st.session_state.dj_emotions)
    st.markdown('</div>', unsafe_allow_html=True)

    # SMART-Ziel
    st.markdown('<div class="vb-card-sage">', unsafe_allow_html=True)
    st.markdown("### 🔵 Dein erster Schritt – Der Blaue Hut & SMART-Ziele")
    st.markdown("""
**S** – Spezifisch: Was genau?  **M** – Messbar: Woran erkennst du Erfolg?
**A** – Attraktiv: Warum ist es dir wichtig?  **R** – Realistisch: Ist es erreichbar?  **T** – Terminiert: Bis wann?
    """)
    st.session_state.dj_first_step = st.text_input(
        "Dein erster konkreter SMART-Schritt:",
        value=st.session_state.dj_first_step)

    if st.button("🎉 Entscheidungsreise abschließen"):
        st.success("Herzlichen Glückwunsch! Deine Entscheidungsreise ist abgeschlossen. 🌱")
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Zurück"): go("dj_step5")
    with c2:
        if st.button("Neue Entscheidungsreise"): reset_dj()


# ── RESILIENZ-CHECK ───────────────────────────────────────────────────────────

def page_rc_intro():
    st.markdown("## 💚 Resilienz-Check")
    st.markdown("""
    <div class="vb-card">
        <h3 style="margin:0 0 0.5rem">Was erwartet dich?</h3>
        <p>Du beantwortest für jeden der <strong>11 wissenschaftlich fundierten Resilienzfaktoren</strong> 3 Aussagen.
        Am Ende erhältst du:</p>
        <ul>
            <li>Eine <strong>persönliche Stärkenanalyse</strong> mit deinen Top-Faktoren</li>
            <li>Deine <strong>Wachstumsbereiche</strong> mit konkreten Übungen</li>
            <li>Ein <strong>Überblicks-Balkendiagramm</strong> aller 11 Faktoren</li>
            <li>Personalisierte <strong>Challenge-Empfehlungen</strong> für dein Training</li>
        </ul>
        <p style="margin-bottom:0"><em>Ca. 5–8 Minuten · Kein Account erforderlich</em></p>
    </div>
    """, unsafe_allow_html=True)
    st.info("⚠️ Disclaimer: Dieser Fragebogen ist ein nicht-klinisches Werkzeug zur Selbsterkenntnis und ersetzt keine professionelle psychologische Beratung.")
    if st.button("Check starten →"):
        st.session_state.rc_page = 0
        go("rc_questions")


def page_rc_questions():
    factor_idx = st.session_state.rc_page
    if factor_idx >= len(RC_FACTORS):
        # All done
        go("rc_results")
        return

    factor = RC_FACTORS[factor_idx]
    total = len(RC_FACTORS)

    st.markdown(f"## {factor['icon']} {factor['name']}")
    render_stepper(factor_idx + 1, total)

    st.markdown(f"""
    <div class="vb-card-warm">
        <p style="margin:0;font-size:0.9rem">Faktor {factor_idx+1} von {total} · Bewertungsskala: 1 = stimme gar nicht zu → 5 = stimme voll zu</p>
    </div>
    """, unsafe_allow_html=True)

    current = st.session_state.rc_answers.get(factor["key"], [3, 3, 3])

    answers = []
    for i, q in enumerate(factor["questions"]):
        st.markdown(f'<div class="vb-card" style="margin-bottom:0.7rem">', unsafe_allow_html=True)
        st.markdown(f"**{q}**")
        val = st.slider("", 1, 5, current[i], key=f"rc_{factor['key']}_{i}",
                        format="%d",
                        help="1 = Stimme gar nicht zu · 5 = Stimme voll zu")
        answers.append(val)
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.rc_answers[factor["key"]] = answers

    c1, c2 = st.columns([1, 3])
    with c1:
        if factor_idx > 0:
            if st.button("← Zurück"):
                st.session_state.rc_page -= 1
                st.rerun()
    with c2:
        btn_label = "Weiter →" if factor_idx < total - 1 else "Auswertung ansehen →"
        if st.button(btn_label):
            st.session_state.rc_page += 1
            st.rerun()


def page_rc_results():
    st.markdown("## 💚 Deine Resilienz-Auswertung")
    st.info("⚠️ Disclaimer: Dieses Ergebnis ist ein nicht-klinisches Werkzeug zur Selbsterkenntnis.")

    scores = {f["key"]: get_factor_score(f["key"]) for f in RC_FACTORS}
    total_score = sum(scores.values())
    max_total = len(RC_FACTORS) * 15

    # Overall score ring (CSS conic-gradient)
    pct = (total_score / max_total) * 100
    st.markdown(f"""
    <div style="text-align:center;margin:1.5rem 0">
        <div style="display:inline-flex;flex-direction:column;align-items:center;justify-content:center;
                    width:140px;height:140px;border-radius:50%;
                    background: conic-gradient(#7A9E7E {pct:.0f}%, #F0E6D3 0%);
                    position:relative;">
            <div style="position:absolute;width:104px;height:104px;border-radius:50%;
                        background:white;display:flex;flex-direction:column;
                        align-items:center;justify-content:center;">
                <div style="font-family:'Fraunces',serif;font-size:1.8rem;font-weight:800;color:#2C2C2C;line-height:1">{total_score}</div>
                <div style="font-size:0.6rem;color:#7A7A6E;text-transform:uppercase;letter-spacing:0.08em">von {max_total}</div>
            </div>
        </div>
        <p style="margin-top:0.8rem;font-weight:600;color:#2C2C2C">Gesamt-Resilienz</p>
    </div>
    """, unsafe_allow_html=True)

    tops = get_top_factors(3)
    bots = get_bottom_factors(3)
    top_keys = [k for k, _ in tops]
    bot_keys = [k for k, _ in bots]

    # ── Stärken ──
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🌟 Deine größten Stärken")
    st.markdown("Hier schöpfst du Kraft – nutze diese Faktoren bewusst in schwierigen Situationen.")
    for key, score in tops:
        factor = next(f for f in RC_FACTORS if f["key"] == key)
        render_factor_bar(factor, score, "strength")
        # Tips button
        with st.expander(f"So nutzt du deine Stärke: **{factor['name']}**"):
            for tip in factor["tips_strength"]:
                st.markdown(f"• {tip}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Wachstumspotenziale ──
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🌱 Dein Potenzial – Bereiche zum Stärken")
    st.markdown("Hier liegt dein größtes Wachstumspotenzial. Konkrete Übungen für jeden Bereich:")
    for key, score in bots:
        factor = next(f for f in RC_FACTORS if f["key"] == key)
        render_factor_bar(factor, score, "potential")
        with st.expander(f"Jetzt Resilienz stärken: **{factor['name']}**"):
            for tip in factor["tips_growth"]:
                st.markdown(f"• {tip}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Vollständiger Überblick ──
    with st.expander("📊 Vollständige Ergebnisse aller 11 Faktoren anzeigen"):
        for factor in RC_FACTORS:
            score = scores[factor["key"]]
            bc = bar_class(factor["key"], tops, bots)
            render_factor_bar(factor, score, bc)

    # ── CTA: Training ──
    st.markdown("""
    <div class="vb-card-sage" style="text-align:center;padding:2rem">
        <h3 style="margin:0 0 0.4rem">Stärke jetzt deine Resilienz!</h3>
        <p style="margin:0 0 1rem">Personalisierte tägliche Challenges basierend auf deinen Wachstumsbereichen.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Training & Challenges starten"):
        go("training")

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Erneut ausfüllen"):
            reset_rc()
    with c2:
        if st.button("Zur Startseite"):
            go("home")


# ── TRAINING ─────────────────────────────────────────────────────────────────

def page_training():
    st.markdown("## 🏆 Resilienz-Training")

    # Streak & Stats
    streak = st.session_state.tr_streak
    total  = st.session_state.tr_total_done
    done_today = st.session_state.tr_completed_today

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Streak", f"{streak} Tage")
    col2.metric("✅ Gesamt", f"{total} Challenges")
    col3.metric("📅 Heute", f"{len(done_today)} erledigt")

    # Personalisierte Empfehlungen (basierend auf RC-Check)
    rc_done = bool(st.session_state.rc_answers)
    if rc_done:
        bots = get_bottom_factors(3)
        priority_keys = [k for k, _ in bots]
        recommended = [c for c in CHALLENGES if c["factor"] in priority_keys]
        other = [c for c in CHALLENGES if c["factor"] not in priority_keys]
    else:
        recommended = CHALLENGES[:6]
        other = CHALLENGES[6:]

    # ── Empfohlene Challenges ──
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    if rc_done:
        st.markdown("### 🎯 Empfohlen für dich")
        st.markdown("Basierend auf deinem Resilienz-Check – diese Bereiche haben das meiste Potenzial.")
    else:
        st.markdown("### 🎯 Tägliche Challenges")
        st.markdown("Mache den [Resilienz-Check](#) für personalisierte Empfehlungen.")

    for ch in recommended[:6]:
        color_map = {"green": "", "gold": "gold-border", "clay": "clay-border"}
        tag_map    = {"green": "", "gold": "gold", "clay": "clay"}
        border_cls = color_map.get(ch["color"], "")
        tag_cls    = tag_map.get(ch["color"], "")
        done = ch["id"] in done_today

        factor_name = next((f["name"] for f in RC_FACTORS if f["key"] == ch["factor"]), ch["factor"])
        done_badge = "✅ Erledigt" if done else f"+{ch['xp']} XP"

        st.markdown(f"""
        <div class="challenge-card {border_cls}">
            <span class="challenge-tag {tag_cls}">{factor_name}</span>
            <div style="float:right;font-size:0.75rem;font-weight:700;
                        color:{'#5D8562' if done else '#C8963E'}">{done_badge}</div>
            <div class="challenge-title">{ch['title']}</div>
            <div class="challenge-desc">{ch['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if not done:
            if st.button(f"✓ Abschließen  –  {ch['title']}", key=f"ch_{ch['id']}"):
                complete_challenge(ch["id"], ch["factor"])

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Alle anderen Challenges (Akkordeon) ──
    if other:
        with st.expander("Weitere Challenges ansehen"):
            for ch in other:
                done = ch["id"] in done_today
                factor_name = next((f["name"] for f in RC_FACTORS if f["key"] == ch["factor"]), ch["factor"])
                st.markdown(f"**{ch['title']}** · *{factor_name}*")
                st.markdown(f"<small>{ch['desc']}</small>", unsafe_allow_html=True)
                if not done:
                    if st.button(f"✓ {ch['title']}", key=f"ch2_{ch['id']}"):
                        complete_challenge(ch["id"], ch["factor"])
                else:
                    st.markdown("✅ Heute erledigt")
                st.markdown('<hr class="vb-divider" style="margin:0.5rem 0">', unsafe_allow_html=True)

    # ── Badges ──
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🏅 Deine Badges")
    badge_html = '<div class="badge-grid">'
    for badge in BADGES:
        earned = badge["id"] in st.session_state.tr_badges_earned
        cls = "earned" if earned else "locked"
        badge_html += f"""
        <div class="badge-item">
            <div class="badge-icon {cls}">{badge['icon']}</div>
            <div class="badge-name">{badge['name']}</div>
        </div>"""
    badge_html += '</div>'
    st.markdown(badge_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Progress toward next badge ──
    next_badges = [b for b in BADGES if b["id"] not in st.session_state.tr_badges_earned]
    if next_badges:
        nb = next_badges[0]
        st.markdown(f"""
        <div class="vb-card-warm">
            <p style="margin:0;font-size:0.85rem;color:#7A7A6E">
                Nächstes Badge: <strong>{nb['icon']} {nb['name']}</strong> – {nb['desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Pro CTA ──
    if st.session_state.plan == "free":
        st.markdown("""
        <div class="vb-card" style="border:2px dashed #C8963E;background:var(--gold-lt) !important;">
            <span class="pro-lock">🔒 PRO</span>
            <h3 style="margin:0.5rem 0 0.3rem">Mehr mit VitaBoost Pro</h3>
            <p style="margin:0">Detaillierter Fortschrittsbericht · Wöchentliche Coach-Sessions ·
            Team-Dashboard für HR · Exportierbare PDF-Berichte</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pro freischalten →"):
            go("pricing")


# ── PRICING ───────────────────────────────────────────────────────────────────

def page_pricing():
    st.markdown("## ⭐ Pläne & Preise")
    st.markdown("Wähle den Plan, der zu dir oder deinem Unternehmen passt.")

    st.markdown("""
    <div class="pricing-grid">
        <div class="pricing-card">
            <div style="font-size:1.5rem;margin-bottom:0.5rem">🌱</div>
            <h3 style="margin:0">Free</h3>
            <div class="pricing-price">0 €</div>
            <div class="pricing-period">für immer kostenlos</div>
            <hr class="vb-divider">
            <p class="pricing-feat">Entscheidungsreise (alle 6 Schritte)</p>
            <p class="pricing-feat">Resilienz-Check (11 Faktoren)</p>
            <p class="pricing-feat">6 tägliche Challenges</p>
            <p class="pricing-feat">Streak & Basis-Badges</p>
        </div>
        <div class="pricing-card featured">
            <div style="font-size:1.5rem;margin-bottom:0.5rem">⭐</div>
            <h3 style="margin:0">Pro</h3>
            <div class="pricing-price">9 €</div>
            <div class="pricing-period">pro Monat · jederzeit kündbar</div>
            <hr class="vb-divider">
            <p class="pricing-feat">Alles aus Free</p>
            <p class="pricing-feat">Alle 18+ Challenges (täglich neu)</p>
            <p class="pricing-feat">KI-Analyse deiner Antworten</p>
            <p class="pricing-feat">Wöchentliche Fortschrittsberichte (PDF)</p>
            <p class="pricing-feat">Personalisierter Trainingsplan</p>
            <p class="pricing-feat">Unbegrenzte Badge-Sammlung</p>
            <p class="pricing-feat">E-Mail-Erinnerungen & Streak-Schutz</p>
        </div>
        <div class="pricing-card">
            <div style="font-size:1.5rem;margin-bottom:0.5rem">🏢</div>
            <h3 style="margin:0">B2B / HR</h3>
            <div class="pricing-price">auf Anfrage</div>
            <div class="pricing-period">ab 20 Mitarbeiter·innen</div>
            <hr class="vb-divider">
            <p class="pricing-feat">Alles aus Pro (pro Seat)</p>
            <p class="pricing-feat">Team-Resilienz-Dashboard</p>
            <p class="pricing-feat">Anonymisierte HR-Berichte</p>
            <p class="pricing-feat">Burnout-Frühwarnsystem</p>
            <p class="pricing-feat">SSO & DSGVO-konform</p>
            <p class="pricing-feat">Onboarding & Schulungen</p>
            <p class="pricing-feat">Dedicated Account Manager</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Weiter kostenlos nutzen"):
            go("home")
    with col2:
        if st.button("🚀 Pro jetzt starten (Demo)"):
            st.session_state.plan = "pro"
            st.success("Demo-Modus: Pro aktiviert! ✨")
            time.sleep(1)
            go("training")
    with col3:
        if st.button("📧 B2B-Anfrage senden"):
            st.success("Danke! Wir melden uns innerhalb von 24h. (Demo-Modus)")

    st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="vb-card-warm">
        <h3 style="margin:0 0 0.5rem">💼 Warum VitaBoost für Unternehmen?</h3>
        <p>Burnout kostet Unternehmen durchschnittlich <strong>9.000 € pro betroffener Person</strong> (Fehlzeiten, Produktivität, Fluktuation).
        VitaBoost hilft Mitarbeiter·innen, ihre Resilienz proaktiv zu stärken –
        messbar, datenschutzkonform und skalierbar.</p>
        <p style="margin:0"><strong>ROI-Beispiel:</strong> Bei 50 Mitarbeiter·innen und 15 % Burnout-Reduktion → <em>~67.500 € Ersparnis/Jahr</em>.</p>
    </div>
    """, unsafe_allow_html=True)


# ── LEBENSÜBERGÄNGE ───────────────────────────────────────────────────────────

def page_lu_intro():
    st.markdown("## 🌉 Lebensübergänge")
    st.markdown("""
    <div class="vb-card">
        <h3 style="margin:0 0 0.5rem">Geführte Reflexion für Phasen, die dein Leben gerade auf den Kopf stellen</h3>
        <p style="margin:0">Wähle die Situation, die dich aktuell am meisten beschäftigt. Du durchläufst
        dieselben 6 Reflexionsschritte wie in der Entscheidungsreise – zugeschnitten auf deine Situation.</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("⚠️ Disclaimer: Diese Reflexion ersetzt keine Therapie oder ärztliche Behandlung. Falls es dir gerade sehr schlecht geht, findest du unter 🆘 SOS Soforthilfe.")

    keys = list(TRANSITIONS.keys())
    cols = st.columns(3)
    for i, key in enumerate(keys):
        with cols[i % 3]:
            if st.button(f"{TRANSITIONS[key]['icon']} {key}", key=f"lu_pick_{key}"):
                st.session_state.lu_type = key
                st.session_state.lu_step = 0
                go("lu_flow")

    if st.session_state.lu_type and st.session_state.lu_answers.get(st.session_state.lu_type):
        st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)
        if st.button(f"Weiter mit „{st.session_state.lu_type}" + "“ →"):
            go("lu_flow")


def page_lu_flow():
    ttype = st.session_state.lu_type
    if not ttype or ttype not in TRANSITIONS:
        go("lu_intro")
        return

    steps = TRANSITIONS[ttype]["steps"]
    step_idx = st.session_state.lu_step
    total = len(steps)

    st.markdown(f"## {TRANSITIONS[ttype]['icon']} {ttype}")
    render_stepper(step_idx + 1, total)

    if st.button("← Andere Situation wählen", key="lu_back_to_intro"):
        go("lu_intro")

    label, prompt = steps[step_idx]
    answers = st.session_state.lu_answers.setdefault(ttype, {})

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    if prompt is not None:
        st.markdown(f"### {label}")
        answers[label] = st.text_area(
            prompt, value=answers.get(label, ""), height=140, key=f"lu_{ttype}_{label}")
    else:
        st.markdown("### 📋 Deine Reflexion im Überblick")
        for lbl, _ in steps[:-1]:
            st.markdown(f"**{lbl}**")
            st.write(answers.get(lbl) or "–")
        st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)
        st.markdown(
            "Du kannst diese Reflexion jederzeit erneut durchlaufen – Übergänge "
            "verändern sich oft, während man sie durchlebt."
        )
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        if step_idx > 0:
            if st.button("← Zurück", key="lu_prev"):
                st.session_state.lu_step -= 1
                st.rerun()
    with c2:
        if step_idx < total - 1:
            if st.button("Weiter →", key="lu_next"):
                st.session_state.lu_step += 1
                st.rerun()
        else:
            if st.button("Neue Reflexion starten", key="lu_restart"):
                reset_lu()


# ── WERTE-KOMPASS ─────────────────────────────────────────────────────────────

def page_werte_kompass():
    st.markdown("## 🧭 Werte-Kompass")
    st.markdown("""
    <div class="vb-card">
        <p style="margin:0">Wer bin ich gerade? Lebensrad, Werte-Klärung und wiederkehrendes Journaling
        – statt eines Einmal-Tests.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Lebensrad ──
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🎡 Lebensrad")
    st.markdown("Wie zufrieden bist du gerade in jedem Bereich? (0 = gar nicht, 10 = sehr)")
    cols = st.columns(2)
    for i, domain in enumerate(LIFE_DOMAINS):
        with cols[i % 2]:
            score = st.slider(domain, 0, 10, st.session_state.wk_wheel.get(domain, 5), key=f"wk_wheel_{domain}")
            st.session_state.wk_wheel[domain] = score
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    for domain in LIFE_DOMAINS:
        render_life_wheel_bar(domain, st.session_state.wk_wheel.get(domain, 5))
    lowest = min(LIFE_DOMAINS, key=lambda d: st.session_state.wk_wheel.get(d, 5))
    st.markdown(
        f"<p style='margin-top:0.5rem'>Größtes Entwicklungspotenzial siehst du aktuell bei "
        f"<strong>{lowest}</strong> ({st.session_state.wk_wheel.get(lowest, 5)}/10).</p>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Werte-Klärung ──
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Meine Top-5-Werte")
    selected = st.multiselect(
        "Wähle bis zu 5 Werte, die dich aktuell am meisten leiten:",
        options=VALUES_POOL, max_selections=5, key="wk_values_widget")
    st.session_state.wk_values = selected
    if selected:
        st.markdown(" · ".join(f"**{v}**" for v in selected))
        st.session_state.wk_values_reflection = st.text_area(
            "Wo in deinem Alltag lebst du diese Werte bereits? Wo (noch) nicht?",
            value=st.session_state.wk_values_reflection, height=110, key="wk_reflection_widget")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Identitäts-Journaling ──
    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 📓 Identitäts-Journaling")
    prompt_idx = date.today().toordinal() % len(JOURNAL_PROMPTS)
    todays_prompt = JOURNAL_PROMPTS[prompt_idx]
    st.markdown(f"**Heutiger Impuls:** {todays_prompt}")
    entry_text = st.text_area("Deine Antwort", key="wk_journal_input", height=140)

    if st.button("Eintrag speichern", key="wk_journal_save"):
        if entry_text.strip():
            st.session_state.wk_journal.append(
                {"date": date.today().isoformat(), "prompt": todays_prompt, "text": entry_text})
            del st.session_state["wk_journal_input"]
            st.success("Gespeichert (für diese Sitzung).")
            st.rerun()
        else:
            st.warning("Leerer Eintrag wurde nicht gespeichert.")

    if st.session_state.wk_journal:
        st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)
        for entry in reversed(st.session_state.wk_journal):
            with st.expander(f"{entry['date']} – {entry['prompt']}"):
                st.write(entry["text"])
        export_text = "\n\n".join(
            f"{e['date']} - {e['prompt']}\n{e['text']}" for e in st.session_state.wk_journal)
        st.download_button(
            "Journal als Textdatei exportieren", data=export_text,
            file_name="identitaets_journal.txt", mime="text/plain")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Zur Startseite", key="wk_home_btn"):
        go("home")


# ── KRISENKOMPASS (SOS) ───────────────────────────────────────────────────────

def page_sos():
    st.markdown("## 🆘 Krisenkompass")
    st.markdown("""
    <div class="vb-card-warm">
        <p style="margin:0">Diese App ersetzt keine Therapie oder ärztliche Behandlung. Wenn es dir gerade
        nicht gut geht, sind das erste Schritte – kein Behandlungsangebot, sondern ein Sicherheitsnetz.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🌬️ Atemübung – 4-7-8")
    st.markdown("4 Sek. einatmen · 7 Sek. halten · 8 Sek. ausatmen.")
    if st.button("Übung starten", key="sos_breathing"):
        placeholder = st.empty()
        for phase, seconds in [("Einatmen …", 4), ("Halten …", 7), ("Ausatmen …", 8)]:
            for remaining in range(seconds, 0, -1):
                placeholder.markdown(f"#### {phase} {remaining}")
                time.sleep(1)
        placeholder.markdown("#### Fertig. Wiederhole gern noch 2–3 Runden.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 🖐️ 5-4-3-2-1 Grounding")
    st.markdown("Geh die Sinne der Reihe nach durch – das holt dich ins Hier und Jetzt.")
    for label, prompt in FIVE_SENSES:
        st.text_input(f"{label}: {prompt}", key=f"sos_{label}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="vb-card">', unsafe_allow_html=True)
    st.markdown("### 📞 Hilfe holen")
    for entry in HOTLINES:
        parts = [f"**{entry['name']}**"]
        if "phone" in entry:
            tel = entry["phone"].replace(" ", "")
            parts.append(f"📞 [{entry['phone']}](tel:{tel})")
        if "url" in entry:
            parts.append(f"🔗 [{entry['url']}]({entry['url']})")
        st.markdown(" · ".join(parts))
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Zurück", key="sos_back"):
        go("home")


# ──────────────────────────────────────────────────────────────────────────────
# 6.  ROUTER
# ──────────────────────────────────────────────────────────────────────────────

PAGE_MAP = {
    "home":       page_home,
    "dj_step1":   page_dj_step1,
    "dj_step2":   page_dj_step2,
    "dj_step3":   page_dj_step3,
    "dj_step4":   page_dj_step4,
    "dj_step5":   page_dj_step5,
    "dj_step6":   page_dj_step6,
    "rc_intro":   page_rc_intro,
    "rc_questions": page_rc_questions,
    "rc_results": page_rc_results,
    "training":   page_training,
    "pricing":    page_pricing,
    "lu_intro":   page_lu_intro,
    "lu_flow":    page_lu_flow,
    "wk_home":    page_werte_kompass,
    "sos":        page_sos,
}

current = st.session_state.page
if current in PAGE_MAP:
    PAGE_MAP[current]()
else:
    page_home()

# Bottom nav always visible (except home)
render_bottom_nav()
