/* Importiert eine schlanke Google-Schriftart für die Benutzeroberfläche */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* Globale Stile für den Body */
body {
    font-family: 'Inter', sans-serif;
    background-color: #f0f4f8;
    color: #1a202c;
    line-height: 1.6;
}

/* Stil für den Haupt-Container der App */
.container {
    max-width: 600px;
    margin: auto;
    padding: 1.5rem;
}

/* Stil für die Karten-Elemente */
.card {
    background-color: #ffffff;
    border-radius: 1.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Grundstil für alle Buttons */
.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 9999px;
    font-weight: 600;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    text-align: center;
}

/* Hover-Effekt für Buttons */
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Stil für den primären Button */
.btn-primary {
    background-color: #6366f1;
    color: #ffffff;
}

/* Stil für den sekundären Button */
.btn-secondary {
    background-color: #e2e8f0;
    color: #4a5568;
}

/* Stil für Trophäen-Badges mit Animation */
.trophy-badge {
    font-size: 2rem;
    animation: bounceIn 0.8s ease-out;
}

/* Animation, die beim Erscheinen der Trophäe abgespielt wird */
@keyframes bounceIn {
    0% { transform: scale(0.3); opacity: 0; }
    50% { transform: scale(1.1); opacity: 1; }
    70% { transform: scale(0.9); }
    100% { transform: scale(1); }
}

/* Stil für die Nachrichtenbox mit Animation */
.message-box {
    animation: fadeIn 0.5s ease-out;
}

/* Animation, die beim Erscheinen der Nachrichtenbox abgespielt wird */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
