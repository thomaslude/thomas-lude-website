Prompt zum Copy-Pasten in Kimi (oder ein anderes Chat-Tool), um die Inhalte für die
Website von Thomas Lude schreiben zu lassen. Fünf Themen sind als Vorschlag markiert –
vor dem Absenden anpassen, falls Thomas andere Schwerpunkte setzt.

---

Du schreibst Website-Texte (Deutsch) für Thomas Lude, Kartenleger. Zielgruppe: Menschen,
die mit einer konkreten Lebensfrage oder emotionalen Belastung kommen (Liebe, Beruf,
Neuanfang, Familie, Orientierung) und Klarheit oder eine neue Perspektive suchen.

Tonalität: warm, ruhig, vertrauenswürdig, auf Augenhöhe. Klar und konkret, keine
esoterischen Kitsch-Floskeln, keine leeren Versprechen ("garantiert", "sofort alles
lösen"). Der Leser soll sich ernst genommen fühlen, nicht verkauft.

Ich brauche Texte für folgende Seiten. Bitte jede Seite als eigenen Markdown-Block,
klar mit Dateiname überschrieben, damit ich sie 1:1 in die Website-Dateien einsetzen kann.

## 1. Startseite (Datei: src/pages/index.astro)
- Eine Headline (kurz, emotional, kein Fachjargon)
- Eine Subline (1-2 Sätze, was Thomas Lude anbietet und für wen)

## 2. Über mich (Datei: src/pages/ueber-mich.astro)
- Kurzer Text (150-250 Wörter): Wer ist Thomas Lude, welche Erfahrung/Haltung bringt er mit,
  warum macht er das.

## 3. Leistungen (Datei: src/pages/leistungen.astro)
- Übersicht: welche Art von Kartenlegen/Sitzungen er anbietet, Ablauf, ca. Dauer.
  (Preise lasse ich erstmal offen / als Platzhalter, falls nicht klar.)

## 4. Fünf Themen-Landingpages (Dateien: src/content/landingpages/<slug>.md)
Vorschlag für die 5 Themen (bei Bedarf anpassen):
- `liebe-beziehung.md` – Liebe & Beziehung
- `beruf-karriere.md` – Beruf & Karriere
- `neuanfang-veraenderung.md` – Neuanfang & Lebensveränderung
- `familie.md` – Familie
- `orientierung-selbstfindung.md` – Orientierung & Selbstfindung

Für jede dieser 5 Seiten brauche ich, jeweils als eigener Block:

```
---
title: "..."
metaTitle: "... | Thomas Lude"
metaDescription: "... (max. 155 Zeichen, für Google-Suchergebnis)"
keyword: "kartenlegen <thema>"
draft: false
---

<Fließtext, 300-500 Wörter, Struktur:>
1. Einstieg – wo steht der Leser emotional gerade, welche Frage treibt ihn um
2. Was Kartenlegen bei genau diesem Thema konkret leisten kann
3. Kurzer Ablauf einer Sitzung
4. Warum Thomas Lude
5. Call to Action (Termin/Kontakt)
```

## 5. Kontaktseite (Datei: src/pages/kontakt.astro)
- Kurzer, einladender Einleitungssatz (1-2 Sätze) über dem Kontaktformular.

---

Bitte alle Texte auf Deutsch, SEO-freundlich (das jeweilige `keyword` natürlich im Text
unterbringen, nicht künstlich wiederholen), und ohne Platzhalter wie "[hier einfügen]" –
wenn Informationen fehlen (z. B. genaue Preise, Ausbildung/Zertifikate von Thomas), das
bitte als offene Frage am Ende auflisten statt zu erfinden.
