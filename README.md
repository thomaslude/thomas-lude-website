# thomas-lude-website

Grundgerüst für die Website von Thomas Lude (Kartenlegen). Static Site mit **Astro** –
Ergebnis ist am Ende reines HTML/CSS/JS, kein Server, kein CMS-Backend nötig.

## Lokal starten

```bash
npm install
npm run dev
```

Läuft dann unter `http://localhost:4321`.

## Struktur

```
src/
  content/landingpages/   ← eine .md-Datei pro Themen-Landingpage (siehe beispiel-thema.md)
  layouts/BaseLayout.astro ← gemeinsames Grundgerüst (Head, Header, Footer)
  components/              ← Header, Footer
  pages/
    index.astro            ← Startseite
    ueber-mich.astro
    leistungen.astro
    kontakt.astro
    impressum.astro         ← MUSS vor Livegang mit echten Angaben gefüllt werden (Pflicht in DE)
    datenschutz.astro       ← MUSS vor Livegang mit echter Datenschutzerklärung gefüllt werden
    themen/
      index.astro           ← Übersicht aller Landingpages (automatisch aus content/landingpages)
      [slug].astro          ← rendert automatisch jede Datei aus content/landingpages
  styles/global.css         ← Farben/Abstände zentral über CSS-Variablen oben in der Datei
```

## Neue Themen-Landingpage anlegen

1. `src/content/landingpages/beispiel-thema.md` kopieren, umbenennen (Dateiname = URL-Slug,
   z. B. `liebe-beziehung.md` → erreichbar unter `/themen/liebe-beziehung`).
2. Frontmatter ausfüllen (`title`, `metaTitle`, `metaDescription`, `keyword`).
3. Text darunter schreiben (normales Markdown).
4. `draft: false` setzen, sobald die Seite live gehen soll.

Kein Code nötig – neue Themenseiten sind reine Markdown-Dateien.

## Deploy (kostenlos)

Build-Output liegt nach `npm run build` in `dist/`.

**Empfohlen: GitHub-Repo (auf Thomas' Account) → Cloudflare Pages oder Netlify verbinden**
- Build command: `npm run build`
- Output directory: `dist`
- Bei jedem `git push` wird automatisch neu deployed.

Danach bei IONOS im Domain-Panel unter "Nameserver" auf den jeweiligen Anbieter umstellen,
damit `thomas-lude.de` auf das Deployment zeigt. Kostenloses SSL-Zertifikat wird automatisch
ausgestellt.

## Kontaktformular

Aktuell nur ein Platzhalter-Formular in `src/pages/kontakt.astro` ohne Versandanbindung.
Je nach Deploy-Ziel:
- **Netlify:** `data-netlify="true"` zum `<form>`-Tag hinzufügen – fertig, kein Backend nötig
  (kostenlos bis 100 Einsendungen/Monat).
- **Cloudflare Pages:** kostenlosen Dienst wie [web3forms.com](https://web3forms.com) einbinden.
