# Thomas Lude – Kartenlegen am Bodensee

Statische Website für **thomas-lude.de**, gebaut für **GitHub Pages**.
Kein WordPress, keine Datenbank, kein Server nötig – nur HTML, CSS, JS und Bilder.

---

## 1. Website auf GitHub Pages veröffentlichen

### Schritt 1: Repository anlegen

1. Auf [github.com](https://github.com) einloggen (oder kostenlos registrieren).
2. Oben rechts auf **„+“ → „New repository“** klicken.
3. Name z. B. `thomas-lude-website`, Sichtbarkeit: **Public** (kostenlos) oder Private mit GitHub Pro.
4. **„Create repository“** klicken.

### Schritt 2: Dateien hochladen

**Variante A – ganz ohne Installation (Browser):**

1. Im neuen Repository auf **„uploading an existing file“** klicken.
2. **Alle Dateien und Ordner aus diesem Paket** (inkl. `assets/`, allen Seitenordnern, `index.html`, `404.html`, `.nojekyll` usw.) per Drag & Drop hineinziehen.
3. Unten **„Commit changes“** klicken.

**Variante B – per Git (Kommandozeile):**

```bash
cd thomas-lude-website
git init
git add .
git commit -m "Website Thomas Lude – erster Stand"
git branch -M main
git remote add origin https://github.com/DEIN-NAME/thomas-lude-website.git
git push -u origin main
```

### Schritt 3: GitHub Pages aktivieren

1. Im Repository auf **„Settings“ → „Pages“** (linkes Menü).
2. Unter **„Build and deployment“**: Source = **„Deploy from a branch“**.
3. Branch = **„main“**, Ordner = **„/ (root)“** → **„Save“**.
4. Nach ca. 1–2 Minuten ist die Seite unter `https://DEIN-NAME.github.io/thomas-lude-website/` erreichbar.

> **Wichtig:** Die Datei `.nojekyll` muss mit hochgeladen werden (liegt bei).
> Sie sorgt dafür, dass GitHub die Dateien unverändert ausliefert.

### Schritt 4: Eigene Domain thomas-lude.de verbinden

1. In **„Settings“ → „Pages“** unter **„Custom domain“** `thomas-lude.de` eintragen und speichern.
2. Beim Domain-Anbieter (z. B. IONOS) die DNS-Einträge setzen:
   - **A-Records** für `thomas-lude.de` auf die GitHub-IPs:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Optional **CNAME** für `www.thomas-lude.de` auf `DEIN-NAME.github.io`
3. Nach der DNS-Prüfung in den Pages-Einstellungen **„Enforce HTTPS“** aktivieren.
4. Alternativ: Datei `CNAME` mit Inhalt `thomas-lude.de` ins Repository legen (erledigt Schritt 1 automatisch).

---

## 2. Inhalte ändern (Baukasten-Prinzip)

Die Website wird mit einem Python-Skript erzeugt. Alle Texte und zentralen
Daten stehen an **einer** Stelle:

```
python3 build.py
```

Das Skript baut alle Seiten neu. Danach die geänderten Dateien wieder zu
GitHub hochladen (`git add . && git commit -m "Update" && git push`) –
GitHub Pages aktualisiert die Seite automatisch.

### Zentrale Einstellungen oben in `build.py`

| Variable | Bedeutung | Stand |
|---|---|---|
| `PHONE` | Telefonnummer (überall auf der Seite) | +49 1523 3701979 ✔ |
| `WHATSAPP` | WhatsApp-Nummer (nur Ziffern, z. B. `4915233701979`) | 4915233701979 ✔ |
| `EMAIL` | E-Mail-Adresse | **DUMMY – ersetzen!** |
| `CITY` / `AREA` | Ort / Region | Friedrichshafen |
| `SHOW_GENERATION` | „3. Generation“-Texte einblenden | `False` – erst nach Bestätigung auf `True` setzen |
| `SITE_URL` | Domain | `https://thomas-lude.de` |

Texte der einzelnen Seiten stehen weiter unten in `build.py` in den
jeweiligen `..._body()`-Funktionen bzw. in der Liste `LANDING_PAGES`.

---

## 3. Kontaktformular anschließen (Formspree)

GitHub Pages kann keine E-Mails versenden – das Formular läuft daher über
den kostenlosen Dienst **Formspree**:

1. Auf [formspree.io](https://formspree.io) kostenlos registrieren.
2. **„New form“** anlegen, Ziel-E-Mail-Adresse angeben.
3. Formspree zeigt eine Adresse wie `https://formspree.io/f/abcdefgh`.
4. In `build.py` den Platzhalter `https://formspree.io/f/DEIN-FORMULAR-CODE`
   durch diese Adresse ersetzen (Suche nach `formspree` – kommt in
   `kontakt_body()` vor).
5. Neu bauen: `python3 build.py`, hochladen, fertig.

---

## 4. Checkliste vor dem Livegang

Diese Platzhalter **unbedingt** ersetzen bzw. prüfen:

- [x] `PHONE` – echte Telefonnummer eingetragen (+49 1523 3701979)
- [x] `WHATSAPP` – echte WhatsApp-Nummer eingetragen, inkl. grünem
      Floating-Button auf jeder Seite
- [ ] `EMAIL` – echte E-Mail-Adresse eintragen
- [ ] Formspree-Code im Kontaktformular (siehe Punkt 3)
- [ ] **Impressum** (`impressum_body()` in `build.py`): vollständiger Name,
      Anschrift und Pflichtangaben nach § 5 DDG eintragen
- [ ] **Erfahrungsberichte**: aktuell mit Hinweis „Beispiel“ gekennzeichnet –
      durch echte Kundenstimmen ersetzen (mit Einverständnis!) oder Abschnitt entfernen
- [ ] **Preise**: Platzhalter auf der Kontaktseite durch echte Preise ersetzen
- [ ] `SHOW_GENERATION = True` setzen, falls „Kartenlegen in 3. Generation“ stimmt
- [ ] Regionen/Orte in den Texten prüfen (aktuell Friedrichshafen & Bodensee)
- [ ] Nach allen Änderungen: `python3 build.py` ausführen und hochladen

---

## 5. Struktur des Projekts

```
├── index.html                  Startseite
├── 404.html                    Fehlerseite
├── .nojekyll                   wichtig für GitHub Pages – nicht löschen!
├── sitemap.xml                 Sitemap für Google
├── robots.txt                  Anweisungen für Suchmaschinen
├── llms.txt                    Kurzbeschreibung für KI-Systeme
├── build.py                    Baukasten: erzeugt alle Seiten neu
├── assets/
│   ├── css/main.css            Design (Farben, Schrift, Layout)
│   ├── js/main.js              Menü & Animationen
│   ├── fonts/                  Schriften (lokal, DSGVO-konform)
│   └── img/                    Fotos (WebP, mehrere Größen)
├── kartenlegen-friedrichshafen/
├── kartenlegen-bodensee/
├── kartenlegen-liebe-partnerschaft/
├── kartenlegen-entscheidung-zukunft/
├── kartenlegen-beruf-veraenderung/
├── kartenlegen-familie/
├── kartenlegen-orientierung-selbstfindung/
├── kartenlegen-telefonisch/
├── kartenlegen-junggesellinnenabschied-bodensee/
├── events/
├── tier-mensch/
├── ueber-thomas-lude/
├── erfahrungen/
├── faq-kartenlegen/
├── ratgeber/
├── kontakt-termin/
├── impressum/
└── datenschutz/
```

Jeder Ordner enthält eine `index.html` – so entstehen saubere Adressen
wie `thomas-lude.de/kartenlegen-bodensee/`.

## 6. Technik im Überblick

- Reines HTML/CSS/JS – keine Cookies, kein Tracking, keine externen Dienste
  (Schriften lokal eingebunden → DSGVO-freundlich)
- Suchmaschinen-Optimierung: Meta-Titel & -Beschreibungen, strukturierte
  Daten (Schema.org), Sitemap, kanonische Adressen
- Schnell: Bilder als WebP in mehreren Größen, Schriften vorgeladen
- Barrierearm: Tastatur-Navigation, Skip-Link, ausreichende Kontraste
