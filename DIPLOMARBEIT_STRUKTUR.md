# Gliederung für die Diplomarbeit

---

## I. Formaler Rahmen (Pre-Content)
*   **Eidesstattliche Erklärung**
*   **Kurzbeschreibung (Deutsch)**
*   **Abstract (Englisch)**
*   **Vorwort**
*   **Inhaltsverzeichnis**

---

## 1. Einleitung
*Hier wird der Leser abgeholt und das Ziel definiert.*

*   **1.1 Motivation:** Warum wird dieses System benötigt? (z.B. Automatisierung von Zufahrtskontrollen, statistische Erhebung)
*   **1.2 Aufgabenstellung:** Klare Definition, was im Rahmen der Arbeit zu tun war (Pflichtenheft)
*   **1.3 Zielsetzung:** Abgrenzung (Was soll das System können, was nicht?)
*   **1.4 Aufbau der Arbeit:** Kurzer Wegweiser durch die Kapitel

## 2. Theoretische Grundlagen
*Kurzer Abriss der Technologien, um das Verständnis für die späteren Entscheidungen zu schaffen.*

*   **2.1 Microservices Architektur:** Prinzipien und Abgrenzung zum Monolithen
*   **2.2 Containerisierung (Docker):** Vorteile für Deployment und Isolation
*   **2.3 ALPR (Automatic License Plate Recognition):** Grundfunktionsweise der Kennzeichenerkennung (Technologie, nicht Code)

## 3. Hardwareauswahl und Systemumgebung

*   **3.1 Anforderungsanalyse an die Hardware:**
    *   Umgebungsbedingungen (Außenbereich, Wetter, Lichtverhältnisse)
    *   Leistungsanforderungen (Verarbeitungsgeschwindigkeit, Netzwerk)
*   **3.2 Evaluierung der Komponenten:**
    *   **Kamera:** Vergleich verschiedener Modelle (z.B. Synology vs. andere IP-Cams)
        *   *Kriterien:* Auflösung, Nachtsicht, API-Verfügbarkeit, Kosten
    *   **Server/Recheneinheit:** (z.B. Raspberry Pi vs. Mini-PC vs. Cloud vs. NAS)
*   **3.3 Begründung der Entscheidung:**
    *   Detaillierte Darlegung, warum genau diese Hardware gewählt wurde (Kosten-Nutzen-Analyse, technische Notwendigkeit)
*   **3.4 Netzwerkinfrastruktur:** Wie sind Kamera und Server verbunden

## 4. Systementwurf und Architektur
*Das Konzept VOR der Programmierung.*

*   **4.1 Gesamtarchitektur:**
    *   Diagramm der Microservices (Auth, Data Collection, Analytics, Notification, Web)
    *   Kommunikationswege (REST API, interne Kommunikation)
*   **4.2 Datenbankdesign:**
    *   ER-Diagramm (Entity Relationship)
    *   Erklärung der wichtigsten Entitäten (`VehicleObservation`, `User`, `Preferences`)
*   **4.3 Sicherheitskonzept:**
    *   Authentifizierung (JWT, User-Rollen) -> Olivia
    *   Datenschutz (Umgang mit Kennzeichen-Daten)

## 5. Implementierung

*   **5.1 Data Collection Service:**
    *   Ablaufdiagramm: Von der Kamera-Triggerung bis zum Speichern in der DB.
    *   Besonderheit: Integration der Kamera-API (Code-Snippet: Wichtige Logik aus `camera_handler.py`).
    *   Verarbeitung von "Municipalities" (Bezirkserkennung).
*   **5.2 Analytics & Reporting:** -> Olivia
    *   Logik hinter den Auswertungen.
*   **5.3 Notification Service:**
    *   Trigger-Logik für Benachrichtigungen (wann wird eine Mail gesendet?).
*   **5.4 Frontend (Web Service):** -> Olivia
    *   Struktur der Next.js Applikation.
    *   Visualisierung der Daten.
*   **5.5 Wichtige Algorithmen/Lösungen:**
    *   Herausragende Code-Teile

## 6. Infrastruktur, Deployment und Betrieb

*   **6.1 Container-Orchestrierung:**
    *   Erläuterung der `docker-compose` Strategie (Dev vs. Prod).
*   **6.2 CI/CD Pipelines:**
    *   Automatisierung mit GitHub Actions (Build & Test).
*   **6.3 Monitoring & Logging:**
    *   Einsatz von Grafana zur Überwachung der "Vehicle Observations".
*   **6.4 Backup-Strategie:**
    *   Erklärung der Backup-Skripte und des Wiederherstellungsprozesses (Disaster Recovery).

## 7. Qualitätssicherung und Tests
*   **7.1 Teststrategie:** Unit-Tests (Pytest) vs. Integrationstests.
*   **7.2 Validierung:** Überprüfung der Hardware/Software-Kombination in der Praxis (Erkennungsraten).

## 8. Fazit und Ausblick
*   **8.1 Zusammenfassung der Ergebnisse.**
*   **8.2 Kritische Reflexion:** Was lief gut, was würde man heute anders machen (Hardware oder Software)?
*   **8.3 Ausblick:** Erweiterungsmöglichkeiten (z.B. KI-Modelle direkt auf der Hardware, App-Anbindung)

---

## II. Verzeichnisse (Post-Content)
*   **Abbildungsverzeichnis**
*   **Quellcodeverzeichnis** (falls Listings im Text referenziert sind)
*   **Glossar** (Erklärung von Begriffen wie ANPR, JWT, Docker Container)
*   **Literaturverzeichnis**

## III. Anhang
*   Große Diagramme
*   Konfigurationsdateien (Auszüge)
