<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Life Manager App</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
        /* Mobile-First-Design für die Navigation */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #ffffff;
            border-top: 1px solid #e5e7eb;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        .nav-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 12px 0;
            cursor: pointer;
            transition: color 0.2s ease;
        }
        .nav-item.active {
            color: #2563eb;
        }
        /* Style für die aktiven Seitencontainer */
        .page-container {
            display: none;
        }
        .page-container.active {
            display: block;
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col items-center justify-between p-4 pb-20">

    <div id="app-container" class="bg-white p-6 rounded-2xl shadow-xl w-full max-w-md my-4">
        <!-- Seitencontainer -->
        <div id="home-page" class="page-container active">
            <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Willkommen! 🚀</h1>
            <div class="space-y-4">
                <button onclick="goToPage('decide-page')" class="w-full p-4 bg-blue-600 text-white font-bold rounded-2xl shadow-md hover:bg-blue-700 transition duration-300 transform hover:scale-105">
                    Entscheidungsreise
                </button>
                <button onclick="goToPage('resilience-page')" class="w-full p-4 bg-green-600 text-white font-bold rounded-2xl shadow-md hover:bg-green-700 transition duration-300 transform hover:scale-105">
                    Resilienz-Fragebogen
                </button>
                <button onclick="goToPage('health-paths-page')" class="w-full p-4 bg-purple-600 text-white font-bold rounded-2xl shadow-md hover:bg-purple-700 transition duration-300 transform hover:scale-105">
                    Gesundheitspfade
                </button>
                <button onclick="goToPage('todo-page')" class="w-full p-4 bg-yellow-600 text-white font-bold rounded-2xl shadow-md hover:bg-yellow-700 transition duration-300 transform hover:scale-105">
                    Meine To-Do-Liste
                </button>
            </div>
        </div>

        <div id="decide-page" class="page-container">
            <!-- Inhalt der Entscheidungsreise -->
            <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Entscheidungsreise 🧠</h1>
            <div id="decide-steps" class="space-y-4">
                <!-- Schritte werden hier dynamisch eingefügt -->
            </div>
        </div>

        <div id="resilience-page" class="page-container">
            <!-- Inhalt des Resilienz-Fragebogens -->
            <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Resilienz-Fragebogen 🧘</h1>
            <div id="resilience-questions" class="space-y-6">
                <!-- Fragen werden dynamisch hier gerendert -->
            </div>
        </div>

        <div id="health-paths-page" class="page-container">
            <!-- Inhalt der Gesundheitspfade -->
            <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Gesundheitspfade 🏆</h1>
            <div id="health-paths-list" class="space-y-4">
                <!-- Pfade werden dynamisch hier gerendert -->
            </div>
        </div>

        <div id="trophy-gallery-page" class="page-container">
            <!-- Inhalt der Trophäen-Galerie -->
            <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Trophäen-Galerie 🏅</h1>
            <div id="trophy-list" class="space-y-4 text-center">
                <!-- Trophäen werden dynamisch hier gerendert -->
            </div>
            <button onclick="goToPage('health-paths-page')" class="w-full p-3 bg-purple-600 text-white font-bold rounded-xl mt-6 hover:bg-purple-700 transition duration-300">
                Zurück zu den Pfaden
            </button>
        </div>

        <div id="todo-page" class="page-container">
            <!-- Inhalt der To-Do-Liste -->
            <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Meine To-Do-Liste ✅</h1>
            <div class="flex space-x-2 mb-4">
                <input type="text" id="newTaskInput" placeholder="Neue Aufgabe hinzufügen..." class="flex-1 p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-500">
                <button id="addTaskButton" class="p-3 bg-yellow-600 text-white rounded-xl shadow-md hover:bg-yellow-700 transition duration-300">
                    Hinzufügen
                </button>
            </div>
            <ul id="taskList" class="space-y-3"></ul>
            <button id="clearTasksButton" class="w-full mt-6 p-3 bg-red-500 text-white rounded-xl shadow-md hover:bg-red-600 transition duration-300 hidden">
                Alle Aufgaben löschen
            </button>
        </div>
    </div>

    <!-- Untere Navigationsleiste -->
    <nav class="bottom-nav flex justify-around items-center">
        <div id="nav-home" class="nav-item active" onclick="goToPage('home-page')">
            <span class="text-2xl">🏠</span>
            <span class="text-xs mt-1">Home</span>
        </div>
        <div id="nav-decide" class="nav-item" onclick="goToPage('decide-page')">
            <span class="text-2xl">🧠</span>
            <span class="text-xs mt-1">Decide</span>
        </div>
        <div id="nav-reflect" class="nav-item" onclick="goToPage('resilience-page')">
            <span class="text-2xl">🧘</span>
            <span class="text-xs mt-1">Reflect</span>
        </div>
        <div id="nav-grow" class="nav-item" onclick="goToPage('health-paths-page')">
            <span class="text-2xl">🏆</span>
            <span class="text-xs mt-1">Grow</span>
        </div>
        <div id="nav-todo" class="nav-item" onclick="goToPage('todo-page')">
            <span class="text-2xl">✅</span>
            <span class="text-xs mt-1">To-Do</span>
        </div>
    </nav>

    <script>
        // Anwendungs-Zustand, der alle Daten speichert
        let appState = {
            currentPage: 'home-page',
            decide: {
                problem: '',
                category: 'Wähle eine Kategorie',
                options: ['', ''],
                selectedValues: [],
                valuesRating: {},
                emotions: '',
                prosA: '', consA: '', prosB: '', consB: '',
                creativeOptions: '',
                futureA: '', futureB: '',
                firstStep: ''
            },
            resilience: {
                questions: [
                    "Ich bin überzeugt, dass ich mein Leben selbst gestalten kann.",
                    "Ich kann mich schnell von Rückschlägen erholen.",
                    "Ich sehe Schwierigkeiten als Herausforderungen an, die ich meistern kann.",
                    "Ich kann gut mit Unsicherheit umgehen.",
                    "Ich finde in schwierigen Zeiten Trost und Unterstützung bei anderen."
                ],
                answers: {},
                score: null,
                analysis: ''
            },
            health: {
                paths: {
                    'Stressabbau': 0, 'Selbstbild stärken': 0,
                    'Selbstwirksamkeitserwartung': 0, 'Verbundenheit': 0, 'Konfliktlösung': 0
                },
                challenges: {
                    'Stressabbau': [
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
                    'Selbstbild stärken': [
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
                    'Selbstwirksamkeitserwartung': [
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
                    'Verbundenheit': [
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
                    'Konfliktlösung': [
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
                },
                currentPath: null,
                trophies: [],
                totalPoints: 0
            },
            todo: {
                tasks: []
            }
        };

        // DOM-Elemente
        const pages = document.querySelectorAll('.page-container');
        const navItems = document.querySelectorAll('.nav-item');
        const appContainer = document.getElementById('app-container');

        // Navigationslogik
        function goToPage(pageId) {
            appState.currentPage = pageId;
            renderPage();
        }

        function renderPage() {
            pages.forEach(page => {
                page.classList.remove('active');
            });
            navItems.forEach(item => {
                item.classList.remove('active');
            });

            document.getElementById(appState.currentPage).classList.add('active');
            document.querySelector(`#nav-${appState.currentPage.split('-')[0]}`).classList.add('active');

            // Spezifische Render-Funktionen für jede Seite
            if (appState.currentPage === 'decide-page') {
                renderDecidePage();
            } else if (appState.currentPage === 'resilience-page') {
                renderResiliencePage();
            } else if (appState.currentPage === 'health-paths-page') {
                renderHealthPathsPage();
            } else if (appState.currentPage === 'trophy-gallery-page') {
                renderTrophyGalleryPage();
            } else if (appState.currentPage === 'todo-page') {
                renderTodoPage();
            }
        }

        // --- Logik für die Entscheidungsreise ---
        function renderDecidePage() {
            // Hier wird der mehrstufige Formularprozess für die Entscheidungsreise gerendert.
            const decideContainer = document.getElementById('decide-steps');
            decideContainer.innerHTML = '<h1>Decide Page Coming Soon!</h1>';
            // Zukünftiger Code würde hier die Formularelemente einfügen und die Eingaben verarbeiten.
            // Aufgrund der Komplexität wird hier nur ein Platzhalter angezeigt, um die Struktur zu zeigen.
        }

        // --- Logik für den Resilienz-Fragebogen ---
        function renderResiliencePage() {
            const resilienceContainer = document.getElementById('resilience-questions');
            resilienceContainer.innerHTML = '';
            
            appState.resilience.questions.forEach((q, index) => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'bg-gray-50 p-4 rounded-xl shadow-sm';
                questionDiv.innerHTML = `
                    <p class="mb-2">${q}</p>
                    <div class="flex justify-between items-center text-sm text-gray-500">
                        <span>1</span>
                        <input type="range" min="1" max="5" value="${appState.resilience.answers[index] || 3}" data-index="${index}" class="w-2/3">
                        <span>5</span>
                    </div>
                `;
                resilienceContainer.appendChild(questionDiv);
                
                questionDiv.querySelector('input').addEventListener('input', (e) => {
                    appState.resilience.answers[index] = parseInt(e.target.value);
                });
            });

            const submitButton = document.createElement('button');
            submitButton.className = 'w-full p-3 bg-blue-600 text-white font-bold rounded-xl mt-6 hover:bg-blue-700 transition duration-300';
            submitButton.innerText = 'Fragebogen abschließen';
            submitButton.addEventListener('click', () => {
                let score = Object.values(appState.resilience.answers).reduce((sum, val) => sum + val, 0);
                appState.resilience.score = score;
                alert(`Dein Resilienz-Score: ${score} von ${appState.resilience.questions.length * 5}`);
            });
            resilienceContainer.appendChild(submitButton);
        }

        // --- Logik für die Gesundheitspfade ---
        function renderHealthPathsPage() {
            const pathsContainer = document.getElementById('health-paths-list');
            pathsContainer.innerHTML = '';

            Object.keys(appState.health.paths).forEach(pathName => {
                const progress = appState.health.paths[pathName];
                const isCompleted = progress >= 10;
                
                const pathDiv = document.createElement('div');
                pathDiv.className = `p-4 rounded-xl shadow-md text-center cursor-pointer transition-colors duration-200 ${isCompleted ? 'bg-green-200' : 'bg-blue-200 hover:bg-blue-300'}`;
                pathDiv.onclick = () => {
                    if (!isCompleted) {
                        alert(`Du startest den Pfad: ${pathName}!`);
                        startHealthChallenge(pathName);
                    } else {
                        alert(`Diesen Pfad hast du bereits abgeschlossen!`);
                    }
                };

                const progressPercentage = (progress / 10) * 100;
                pathDiv.innerHTML = `
                    <h2 class="font-bold text-lg mb-2">${pathName}</h2>
                    <div class="w-full bg-gray-300 rounded-full h-2.5">
                        <div class="bg-blue-600 h-2.5 rounded-full" style="width: ${progressPercentage}%"></div>
                    </div>
                    <p class="text-sm mt-1 text-gray-600">${progress} / 10 Challenges</p>
                `;
                pathsContainer.appendChild(pathDiv);
            });

            const trophyButton = document.createElement('button');
            trophyButton.className = 'w-full p-3 bg-purple-600 text-white font-bold rounded-xl mt-6 hover:bg-purple-700 transition duration-300';
            trophyButton.innerText = 'Trophäen anzeigen';
            trophyButton.onclick = () => goToPage('trophy-gallery-page');
            pathsContainer.appendChild(trophyButton);
        }

        function startHealthChallenge(pathName) {
            const challenges = appState.health.challenges[pathName];
            const currentChallengeIndex = appState.health.paths[pathName];
            
            if (currentChallengeIndex < challenges.length) {
                const challengeText = challenges[currentChallengeIndex];
                const expertTip = challengeText.split('. Expertentipp: ')[1];
                const userConfirmed = confirm(`Deine heutige Challenge:\n${challengeText}\n\nAls Belohnung bekommst du 10 Punkte.`);
                
                if (userConfirmed) {
                    appState.health.paths[pathName]++;
                    appState.health.totalPoints += 10;
                    alert(`Challenge abgeschlossen! Du hast jetzt ${appState.health.totalPoints} Punkte.`);
                    
                    if (appState.health.paths[pathName] === 10) {
                        alert(`Herzlichen Glückwunsch! Du hast den Pfad '${pathName}' abgeschlossen!`);
                        appState.health.trophies.push(pathName);
                        appState.health.totalPoints += 50; // Bonus
                    }
                }
            } else {
                 alert(`Diesen Pfad hast du bereits abgeschlossen!`);
            }
            renderHealthPathsPage(); // UI neu rendern
        }

        function renderTrophyGalleryPage() {
            const trophyContainer = document.getElementById('trophy-list');
            trophyContainer.innerHTML = '';
            
            if (appState.health.trophies.length === 0) {
                trophyContainer.innerHTML = '<p class="text-gray-500">Noch keine Trophäen gesammelt.</p>';
            } else {
                appState.health.trophies.forEach(trophy => {
                    const trophyDiv = document.createElement('div');
                    trophyDiv.className = 'p-4 rounded-xl bg-yellow-100 shadow-sm';
                    trophyDiv.innerHTML = `<span class="text-4xl">🏆</span><p class="mt-2 font-bold">${trophy}</p>`;
                    trophyContainer.appendChild(trophyDiv);
                });
            }
        }

        // --- Logik für die To-Do-Liste ---
        function renderTodoPage() {
            const taskList = document.getElementById('taskList');
            const newTaskInput = document.getElementById('newTaskInput');
            const addTaskButton = document.getElementById('addTaskButton');
            const clearTasksButton = document.getElementById('clearTasksButton');

            // UI-Rendering basierend auf dem Zustand
            taskList.innerHTML = '';
            appState.todo.tasks.forEach((task, index) => {
                const li = document.createElement('li');
                li.className = `flex items-center justify-between p-3 rounded-xl shadow-sm transition duration-300 ${task.completed ? 'bg-green-100 text-gray-400 line-through' : 'bg-gray-50'}`;
                li.innerHTML = `
                    <span class="flex-1 truncate">${task.text}</span>
                    <div class="flex items-center space-x-2">
                        <button class="complete-btn p-2 rounded-full hover:bg-gray-200 transition-colors duration-200" data-index="${index}" aria-label="Aufgabe abschließen">
                            <svg class="h-5 w-5 ${task.completed ? 'text-green-500' : 'text-gray-400'}" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                        <button class="delete-btn p-2 rounded-full hover:bg-gray-200 transition-colors duration-200" data-index="${index}" aria-label="Aufgabe löschen">
                            <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M9 2a1 1 0 011-1h.25a1 1 0 011 1V2a2 2 0 012 2v.25a1 1 0 01-1 1H8a1 1 0 01-1-1V4a2 2 0 012-2zM4 5h12v13a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 2a1 1 0 00-1 1v7a1 1 0 102 0V8a1 1 0 00-1-1zm4 0a1 1 0 00-1 1v7a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                `;
                taskList.appendChild(li);
            });

            // Event-Listener für 'complete' und 'delete'
            document.querySelectorAll('.complete-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const index = e.currentTarget.dataset.index;
                    appState.todo.tasks[index].completed = !appState.todo.tasks[index].completed;
                    renderTodoPage();
                });
            });

            document.querySelectorAll('.delete-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const index = e.currentTarget.dataset.index;
                    appState.todo.tasks.splice(index, 1);
                    renderTodoPage();
                });
            });

            // Sichtbarkeit des Löschen-Buttons aktualisieren
            clearTasksButton.classList.toggle('hidden', appState.todo.tasks.length === 0);
        }

        // To-Do-Listen-Funktionen
        document.getElementById('addTaskButton').addEventListener('click', () => {
            const input = document.getElementById('newTaskInput');
            const taskText = input.value.trim();
            if (taskText !== '') {
                appState.todo.tasks.push({ text: taskText, completed: false });
                input.value = '';
                renderTodoPage();
            }
        });

        document.getElementById('newTaskInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('addTaskButton').click();
            }
        });

        document.getElementById('clearTasksButton').addEventListener('click', () => {
            appState.todo.tasks = [];
            renderTodoPage();
        });

        // App starten
        document.addEventListener('DOMContentLoaded', () => {
            renderPage();
        });
    </script>
</body>
</html>
