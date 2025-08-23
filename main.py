let currentPath = null;
let currentStageIndex = 0;
let totalPoints = 0;
let pathPoints = {};
let collectedTrophies = new Set();
let messageTimeout;

const appElement = document.getElementById('app');

// Initialisiert die App-Daten und den Zustand
function initializeAppData() {
    // Lade den gespeicherten Zustand aus dem lokalen Speicher, falls vorhanden
    try {
        const savedState = JSON.parse(localStorage.getItem('resilienceApp'));
        if (savedState) {
            totalPoints = savedState.totalPoints;
            pathPoints = savedState.pathPoints;
            collectedTrophies = new Set(savedState.collectedTrophies);
        }
    } catch (e) {
        console.error("Fehler beim Laden des lokalen Speichers:", e);
    }
    // Stelle sicher, dass für jeden Pfad ein Punktewert existiert
    for (const pathKey in appData.paths) {
        if (!(pathKey in pathPoints)) {
            pathPoints[pathKey] = 0;
        }
    }
}

// Speichert den aktuellen Zustand der App im lokalen Speicher
function saveState() {
    const stateToSave = {
        totalPoints,
        pathPoints,
        collectedTrophies: Array.from(collectedTrophies)
    };
    localStorage.setItem('resilienceApp', JSON.stringify(stateToSave));
}

// Rendert die Startseite mit den Pfad-Optionen
function renderHomePage() {
    currentPath = null;
    appElement.innerHTML = `
        <div class="container card text-center p-8 m-4 max-w-lg w-full flex flex-col items-center">
            <h1 class="text-3xl font-bold mb-4 text-gray-800">Ihre Resilienz-Reise</h1>
            <p class="text-gray-600 mb-6">Wählen Sie einen Pfad und starten Sie Ihre tägliche Übung.</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mb-6">
                ${Object.keys(appData.paths).map(pathKey => `
                    <button onclick="renderPath('${pathKey}')" class="btn btn-secondary flex flex-col items-center p-4">
                        <span class="text-3xl mb-2">${getTrophyIcon(pathKey)}</span>
                        <span class="text-lg font-semibold text-gray-800">${appData.paths[pathKey].title}</span>
                        <span class="text-sm text-gray-500 mt-1">${appData.paths[pathKey].description}</span>
                        <span class="text-xs text-gray-500 mt-2">Ihre Punkte: ${pathPoints[pathKey]}</span>
                    </button>
                `).join('')}
            </div>
            <div id="trophy-section" class="w-full">
                <h2 class="text-2xl font-bold mb-4 text-gray-800">Ihre Trophäen</h2>
                <div id="trophy-list" class="flex flex-wrap justify-center gap-4">
                    ${appData.trophies.map(trophy => `
                        <span class="text-4xl ${collectedTrophies.has(trophy.id) ? '' : 'grayscale opacity-30'}" title="${trophy.name}: ${trophy.description}">${trophy.icon}</span>
                    `).join('')}
                </div>
            </div>
            <div id="total-points" class="mt-6 text-xl font-bold text-gray-700">
                Gesamtpunkte: ${totalPoints}
            </div>
        </div>
    `;
    // Scrollen zur Trophäen-Sektion, falls eine neue Trophäe freigeschaltet wurde
    if (sessionStorage.getItem('newTrophyUnlocked') === 'true') {
        setTimeout(() => {
            const trophySection = document.getElementById('trophy-section');
            if (trophySection) {
                trophySection.scrollIntoView({ behavior: 'smooth' });
            }
            sessionStorage.removeItem('newTrophyUnlocked');
        }, 500);
    }
}

// Rendert den ausgewählten Pfad
function renderPath(pathKey) {
    currentPath = pathKey;
    currentStageIndex = 0;
    updateUI();
}

// Zeigt die aktuelle Stufe an
function updateUI() {
    const pathData = appData.paths[currentPath];
    if (!pathData) {
        renderHomePage();
        return;
    }

    const currentStage = pathData.stages[currentStageIndex];
    const expertTip = currentStage.expertTip ? `<div class="bg-blue-50 border-l-4 border-blue-400 text-blue-800 p-4 rounded-lg mt-4 text-sm expert-tip" role="alert">
        <p class="font-bold">Expertentipp:</p>
        <p>${currentStage.expertTip}</p>
    </div>` : '';

    appElement.innerHTML = `
        <div class="container card p-8 m-4 w-full">
            <button onclick="renderHomePage()" class="btn btn-secondary mb-6 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
                </svg>
                Zurück
            </button>
            <h2 class="text-2xl font-bold mb-2 text-center text-gray-800">${pathData.title}</h2>
            <p class="text-sm text-gray-500 text-center mb-4">Tag ${currentStageIndex + 1} von ${pathData.stages.length}</p>

            <div class="w-full bg-gray-200 rounded-full h-2.5 mb-6">
                <div class="bg-indigo-500 h-2.5 rounded-full transition-all duration-500" style="width: ${((currentStageIndex + 1) / pathData.stages.length) * 100}%"></div>
            </div>
            
            <div id="stage-content" class="text-center">
                <h3 class="text-xl font-bold text-gray-700 mb-2">${currentStage.title}</h3>
                <p class="text-gray-600 mb-4">${currentStage.description}</p>
                <button id="complete-btn" class="btn btn-primary mt-4" onclick="completeStage()">
                    Stufe abschließen und ${currentStage.points} Punkte sammeln
                </button>
                ${expertTip}
            </div>

            <div id="message-area" class="mt-6"></div>
        </div>
    `;
}

// Schließt die aktuelle Stufe ab und geht zur nächsten
function completeStage() {
    const pathData = appData.paths[currentPath];
    const currentStage = pathData.stages[currentStageIndex];

    // Punkte hinzufügen
    totalPoints += currentStage.points;
    pathPoints[currentPath] += currentStage.points;

    // Nachricht anzeigen
    displayMessage(currentStage.message, currentStage.vibrate);

    // Nächste Stufe vorbereiten
    currentStageIndex++;
    saveState();
    checkTrophies();

    if (currentStageIndex < pathData.stages.length) {
        // Zeige nächste Stufe nach kurzer Verzögerung
        setTimeout(updateUI, 2000);
    } else {
        // Pfad abgeschlossen
        setTimeout(() => {
            appElement.innerHTML = `
                <div class="container card text-center p-8 m-4 w-full">
                    <h2 class="text-2xl font-bold text-gray-800 mb-4">Pfad abgeschlossen!</h2>
                    <p class="text-gray-600 mb-6">Sie haben den Pfad "${pathData.title}" erfolgreich abgeschlossen und Ihre Resilienz gestärkt.</p>
                    <p class="text-lg font-semibold text-gray-700 mb-6">Sie haben insgesamt ${totalPoints} Punkte gesammelt.</p>
                    <button onclick="renderHomePage()" class="btn btn-primary">
                        Zurück zur Startseite
                    </button>
                </div>
            `;
        }, 2000);
    }
}

// Zeigt eine Meldung an und vibriert, falls nötig
function displayMessage(text, shouldVibrate) {
    const messageArea = document.getElementById('message-area');
    if (messageArea) {
        messageArea.innerHTML = `
            <div class="message-box bg-green-50 border-l-4 border-green-400 text-green-800 p-4 rounded-lg" role="alert">
                <p class="font-bold">Erfolg!</p>
                <p>${text}</p>
            </div>
        `;
        // Vibriere das Gerät, wenn es unterstützt wird
        if (shouldVibrate && navigator.vibrate) {
            navigator.vibrate(200);
        }
        
        // Entferne die Nachricht nach einer Weile
        clearTimeout(messageTimeout);
        messageTimeout = setTimeout(() => {
            messageArea.innerHTML = '';
        }, 2000);
    }
}

// Überprüft, ob Trophäen freigeschaltet wurden
function checkTrophies() {
    appData.trophies.forEach(trophy => {
        let unlocked = false;
        if (trophy.id.startsWith("path-trophy-")) {
            const pathKey = trophy.id.replace("path-trophy-", "");
            if (pathPoints[pathKey] >= trophy.pointsNeeded) {
                unlocked = true;
            }
        } else if (trophy.id.startsWith("milestone-")) {
            if (totalPoints >= trophy.pointsNeeded) {
                unlocked = true;
            }
        }

        if (unlocked && !collectedTrophies.has(trophy.id)) {
            collectedTrophies.add(trophy.id);
            sessionStorage.setItem('newTrophyUnlocked', 'true');
            showTrophyToast(trophy);
        }
    });
    saveState();
}

// Zeigt eine Trophäen-Benachrichtigung an
function showTrophyToast(trophy) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 left-1/2 -translate-x-1/2 bg-white rounded-xl shadow-lg p-4 flex items-center space-x-4 z-50 animate-bounceIn';
    toast.innerHTML = `
        <div class="trophy-badge">${trophy.icon}</div>
        <div>
            <div class="font-bold text-gray-800">Neue Trophäe freigeschaltet!</div>
            <div class="text-sm text-gray-600">${trophy.name}</div>
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Hilfsfunktion, um das Pfad-Trophäen-Icon zu erhalten
function getTrophyIcon(pathKey) {
    const trophy = appData.trophies.find(t => t.id === `path-trophy-${pathKey}`);
    return collectedTrophies.has(trophy.id) ? trophy.icon : '◻️';
}

// Startet die App, wenn das Dokument vollständig geladen ist
document.addEventListener('DOMContentLoaded', () => {
    initializeAppData();
    renderHomePage();
});
