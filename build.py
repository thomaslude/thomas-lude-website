# -*- coding: utf-8 -*-
"""
Build-Skript für thomas-lude.de (statische Website).

Generiert alle HTML-Seiten aus diesem einen Skript.
Aufruf:  python3 build.py
Danach:  Ordnerinhalt nach GitHub pushen (siehe README.md).

ZENTRALE KONTAKTDATEN – nur hier unten an einer Stelle pflegen:
ACHTUNG: Alle Werte sind aktuell DUMMYS und müssen vor dem Go-Live ersetzt werden!
"""
import html
import json
import os
import shutil

from blog_content import BLOG_POSTS

# ----------------------------------------------------------------------------
# ZENTRALE EINSTELLUNGEN (DUMMY-WERTE – vor Go-Live ersetzen!)
# ----------------------------------------------------------------------------
SITE_URL   = "https://thomas-lude.de"
SITE_NAME  = "Thomas Lude – Kartenlegen am Bodensee"
PHONE      = "+49 1523 3701979"       # echte Nummer (Stand: Sep 2026)
PHONE_HINT = ""                        # Hinweis-Text neben der Nummer (leer = keiner)
WHATSAPP   = "4915233701979"          # nur Ziffern, ohne + und Leerzeichen
EMAIL      = "info@thomas-lude.de"    # bestätigt aktive Domain-Mailadresse (thomas@thomas-lude.de ebenfalls aktiv)
CITY       = "Friedrichshafen"
AREA       = "Friedrichshafen & Bodensee"
SHOW_GENERATION = True                 # „Kartenlegen in 3. Generation" von Thomas bestätigt
# ----------------------------------------------------------------------------

TEL_HREF = "tel:" + PHONE.replace(" ", "").replace("-", "")
WA_HREF  = "https://wa.me/" + WHATSAPP
MAIL_HREF = "mailto:" + EMAIL

OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Icons (inline SVG)
# ----------------------------------------------------------------------------
def icon(name, size=22):
    paths = {
        "pin": '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 14.5 9 2.5 2.5 0 0 1 12 11.5Z"/>',
        "phone": '<path d="M6.6 10.8a15.6 15.6 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .57 3.6 1 1 0 0 1-.25 1Z"/>',
        "users": '<path d="M16 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-8 0a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0 2c-2.7 0-8 1.3-8 4v2h9v-2a5.2 5.2 0 0 1 1.9-4A12.3 12.3 0 0 0 8 13Zm8 0c-.3 0-.6 0-1 .06a6.4 6.4 0 0 1 2 4.94v2h7v-2c0-2.7-5.3-5-8-5Z"/>',
        "lotus": '<path d="M12 3c1.8 2 2.8 4.3 2.8 6.6A4.7 4.7 0 0 1 12 13a4.7 4.7 0 0 1-2.8-3.4C9.2 7.3 10.2 5 12 3Zm-8.6 4.2c2.4-.3 4.8.5 6.4 2.1a6.8 6.8 0 0 1-1.4 7.4A6.9 6.9 0 0 1 2.9 14c-.6-2.4-.4-4.9.5-6.8Zm17.2 0c.9 1.9 1.1 4.4.5 6.8a6.9 6.9 0 0 1-5.5 2.7 6.8 6.8 0 0 1-1.4-7.4c1.6-1.6 4-2.4 6.4-2.1ZM12 15.5c-2.9 0-5.5 1.2-7.3 3.1A9.9 9.9 0 0 0 12 21a9.9 9.9 0 0 0 7.3-2.4A9.7 9.7 0 0 0 12 15.5Z"/>',
        "shield": '<path d="M12 2 4 5v6c0 5.1 3.4 9.8 8 11 4.6-1.2 8-5.9 8-11V5Zm-1.5 13.6-3-3 1.4-1.4 1.6 1.6 4.1-4.1 1.4 1.4Z"/>',
        "waves": '<path d="M2 8c2.5 0 2.5 2 5 2s2.5-2 5-2 2.5 2 5 2 2.5-2 5-2v2.5c-2.5 0-2.5 2-5 2s-2.5-2-5-2-2.5 2-5 2-2.5-2-5-2Zm0 7c2.5 0 2.5 2 5 2s2.5-2 5-2 2.5 2 5 2 2.5-2 5-2v2.5c-2.5 0-2.5 2-5 2s-2.5-2-5-2-2.5 2-5 2-2.5-2-5-2Z"/>',
        "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1Z"/>',
        "chevron": '<path d="M7.4 8.6 12 13.2l4.6-4.6L18 10l-6 6-6-6Z"/>',
        "whatsapp": '<path d="M12 2a10 10 0 0 0-8.7 14.9L2 22l5.3-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.6-1.2a.5.5 0 0 0 0-.5c-.1-.1-.6-1.4-.8-1.9s-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4 5.3 5.3 0 0 0 3.2.7 2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/>',
        "mail": '<path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5Z"/>',
        "calendar": '<path d="M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 16H5V10h14ZM5 8V6h14v2Z"/>',
    }
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" fill="currentColor" aria-hidden="true">%s</svg>'
            % (size, size, paths[name]))

# ----------------------------------------------------------------------------
# Bilder (responsive WebP aus assets/img)
# ----------------------------------------------------------------------------
IMG_META = {
    "thomas-lude-kartenleger-friedrichshafen-bodensee": (1122, 1402),
    "thomas-lude-kartenlegen-liebe-beziehung":          (1122, 1402),
    "thomas-lude-tierbegleitung-bodensee":              (1122, 1402),
    "thomas-lude-portrait-hund-friedrichshafen":        (1122, 1402),
    "thomas-lude-ueber-thomas-kartenlegen":             (768, 1376),
    "thomas-lude-kartenlegen-jga-bodensee":             (1536, 1024),
    "thomas-lude-kartenlegen-beratung-am-tisch":        (688, 1406),
    "blog-hellfuehligkeit-frage-vor-karten":            (1536, 1024),
    "blog-feinfuehliger-mensch-haus":                   (1536, 1024),
    "blog-geboren-mit-der-gabe":                        (1536, 1024),
    "blog-geister-die-ich-rief":                        (1536, 1024),
    "blog-verlust-wiedergeburt-sinnfragen":             (1536, 1024),
    "blog-karmische-aufgaben":                          (1536, 1024),
    "vortexkey-thomas-lude-weiche":                     (1672, 941),
    "kartenlegen-hauskauf-umzug":                        (1672, 941),
}

def img(base, alt, sizes="(max-width: 768px) 100vw, 50vw", loading="lazy", fetchpriority="", css_class=""):
    w, h = IMG_META[base]
    variants = []
    for width in (480, 768, 1200):
        f = "assets/img/%s-%dw.webp" % (base, width)
        if os.path.exists(os.path.join(OUT, f)):
            variants.append("/%s %dw" % (f, width))
    full = "assets/img/%s-full.webp" % base
    if os.path.exists(os.path.join(OUT, full)):
        variants.append("/%s %dw" % (full, w))
    src = "/" + full if os.path.exists(os.path.join(OUT, full)) else "/assets/img/%s-768w.webp" % base
    fp = ' fetchpriority="%s"' % fetchpriority if fetchpriority else ""
    cl = ' class="%s"' % css_class if css_class else ""
    return ('<img src="%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s" loading="%s" decoding="async"%s%s>'
            % (src, ", ".join(variants), sizes, w, h, alt, loading, fp, cl))

# ----------------------------------------------------------------------------
# Wiederverwendbare Bausteine
# ----------------------------------------------------------------------------
def faq_html(items):
    chev = icon("chevron", 20)
    out = ['<div class="faq-grid">']
    for q, a in items:
        out.append('<details class="faq-item"><summary>%s%s</summary>'
                   '<div class="faq-answer"><p>%s</p></div></details>' % (q, chev, a))
    out.append('</div>')
    return "\n".join(out)

FAQ_MAIN = [
    ("Was kann ich Thomas fragen?",
     "Alles, was dich beschäftigt: Liebe und Beziehung, Entscheidungen, berufliche Veränderungen, Familie oder deine ganz persönliche Lebensrichtung. Es gibt keine falsche Frage – wichtig ist nur, dass sie dich wirklich interessiert."),
    ("Wie lange dauert eine Kartenlegung?",
     "Das hängt von deinem Thema ab. Plane für eine persönliche Beratung etwa 45 bis 60 Minuten ein. Die genaue Dauer besprecht ihr am besten direkt bei der Terminanfrage."),
    ("Was kostet eine Beratung?",
     "30 Minuten 79 €, 60 Minuten 149 € (das meistgewählte Format), 90 Minuten 219 €, 120 Minuten 289 € – persönlich wie telefonisch. Zeigt sich im Gespräch mehr Bedarf, ist eine Verlängerung unkompliziert möglich."),
    ("Muss ich an Kartenlegen glauben?",
     "Nein. Du musst an nichts glauben. Viele kommen einfach mit einer offenen Frage und der Bereitschaft, einen anderen Blick darauf zu werfen. Das reicht völlig."),
    ("Kann ich Thomas auch telefonisch sprechen?",
     "Ja. Wenn du nicht persönlich nach Friedrichshafen kommen kannst oder möchtest, ist eine Kartenberatung auch am Telefon möglich – nach Terminvereinbarung, genauso persönlich und diskret."),
    ("Wie funktioniert ein Kartenabend für mehrere Personen?",
     "Thomas kommt zu euch – in die Ferienwohnung, ins Hotel oder zu euch nach Hause. Jede Person bekommt ihren eigenen Moment mit den Karten, die anderen sind dabei oder genießen den Abend. Ideal für JGA, Mädelsabende und Geburtstage am Bodensee."),
    ("Kann Thomas meine Zukunft sicher vorhersagen?",
     "Nein – und das sagt er dir auch ehrlich. Die Karten können Zusammenhänge, Tendenzen und mögliche Entwicklungen sichtbar machen. Was du daraus machst, bleibt immer deine Entscheidung."),
    ("Und wenn ich unsicher bin, ob das das Richtige für mich ist?",
     "Dann schreib einfach kurz. Ein unverbindliches Vorgespräch kostet nichts – und du merkst schnell, ob es sich richtig anfühlt."),
    ("Bietet Thomas auch Hausbesuche an?",
     "Ja, im Bodenseeraum. Dabei bezieht Thomas auch die Atmosphäre deines Zuhauses in die Beratung ein – auf Wunsch auch als energetische Raumklärung."),
]

def cta_band(title, text, whatsapp_msg="Hallo Thomas, ich interessiere mich für eine Beratung."):
    return """
<section class="section">
  <div class="container">
    <div class="cta-band">
      <h2>%s</h2>
      <p>%s</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="/kontakt-termin/">Termin anfragen</a>
        <a class="btn btn-outline-light" href="%s?text=%s" target="_blank" rel="noopener">%s Bei WhatsApp schreiben</a>
        <a class="btn btn-outline-light" href="%s">%s Anrufen</a>
      </div>
    </div>
  </div>
</section>""" % (title, text, WA_HREF, _urlencode(whatsapp_msg), icon("whatsapp", 18),
                 TEL_HREF, icon("phone", 18))

def _urlencode(s):
    from urllib.parse import quote
    return quote(s)

# ----------------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------------
NAV = [
    ("/", "Startseite"),
    ("/kartenlegen-friedrichshafen/", "Kartenlegen"),
    ("/events/", "Events"),
    ("/tier-mensch/", "Tier &amp; Mensch"),
    ("/ueber-thomas-lude/", "Über mich"),
    ("/erfahrungen/", "Erfahrungen"),
    ("/blog/", "Blog"),
    ("/kontakt-termin/", "Kontakt"),
]

def layout(slug, title, meta_desc, body, hero_preload="", extra_schema=None):
    """slug: '' für Startseite, sonst 'kartenlegen-friedrichshafen' etc."""
    canonical = SITE_URL + "/" + (slug + "/" if slug else "")
    nav_items = []
    for href, label in NAV:
        current = ""
        if (href == "/" and slug == "") or (href != "/" and href.strip("/") == slug):
            current = ' aria-current="page"'
        nav_items.append('<li><a href="%s"%s>%s</a></li>' % (href, current, label))
    nav_html = "\n        ".join(nav_items)

    preload = ('<link rel="preload" as="image" href="%s" fetchpriority="high">' % hero_preload) if hero_preload else ""

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": SITE_URL + "/#thomas-lude",
                "name": "Thomas Lude",
                "jobTitle": "Kartenleger",
                "description": "Thomas Lude ist Kartenleger aus Friedrichshafen. Er bietet persönliche Kartenberatung, telefonische Beratung, Kartenabende für Events und energetische Tierbegleitung am Bodensee an.",
                "url": SITE_URL + "/",
                "image": SITE_URL + "/assets/img/thomas-lude-ueber-thomas-kartenlegen-768w.webp",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": CITY,
                    "addressRegion": "Baden-Württemberg",
                    "addressCountry": "DE",
                },
            },
            {
                "@type": "ProfessionalService",
                "@id": SITE_URL + "/#beratung",
                "name": SITE_NAME,
                "url": SITE_URL + "/",
                "telephone": PHONE,
                "email": EMAIL,
                "founder": {"@id": SITE_URL + "/#thomas-lude"},
                "areaServed": [
                    {"@type": "City", "name": CITY},
                    {"@type": "Place", "name": "Bodensee"},
                ],
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": CITY,
                    "addressRegion": "Baden-Württemberg",
                    "addressCountry": "DE",
                },
            },
            {
                "@type": "WebSite",
                "@id": SITE_URL + "/#website",
                "url": SITE_URL + "/",
                "name": SITE_NAME,
                "inLanguage": "de-DE",
            },
        ],
    }
    if slug:
        schema["@graph"].append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Startseite", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0]},
            ],
        })
    if extra_schema:
        schema["@graph"].extend(extra_schema)

    return """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<meta property="og:locale" content="de_DE">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%(sitename)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(site)s/assets/img/thomas-lude-kartenleger-friedrichshafen-bodensee-768w.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/thomas-lude-kartenlegen-beratung-am-tisch-480w.webp">
<link rel="preload" href="/assets/fonts/CormorantGaramond-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Inter-400.woff2" as="font" type="font/woff2" crossorigin>
%(preload)s
<link rel="stylesheet" href="/assets/css/main.css">
<script type="application/ld+json">%(schema)s</script>
</head>
<body>
<a class="skip-link" href="#main">Zum Inhalt springen</a>

<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="Thomas Lude – zur Startseite">
      <span class="brand-name">Thomas Lude</span>
      <span class="brand-claim">Kartenlegen am Bodensee</span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Hauptnavigation">
      <ul class="nav-list">
        %(nav)s
      </ul>
    </nav>
    <a class="btn btn-gold header-cta" href="/kontakt-termin/">Termin anfragen</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="Menü öffnen">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<main id="main">
%(body)s
</main>

<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <p class="brand-name">Thomas Lude</p>
      <p class="brand-claim">Kartenlegen am Bodensee</p>
      <p class="footer-tagline">Persönlich. Direkt. Mit Gespür.</p>
      <p class="footer-note">Kartenlegen ist eine intuitive Beratung und ersetzt keine medizinische, juristische oder finanzielle Entscheidung.</p>
    </div>
    <nav aria-label="Footer-Navigation Beratung">
      <h2 class="footer-heading">Beratung</h2>
      <ul class="footer-list">
        <li><a href="/kartenlegen-friedrichshafen/">Kartenlegen Friedrichshafen</a></li>
        <li><a href="/kartenlegen-bodensee/">Kartenlegen Bodensee</a></li>
        <li><a href="/kartenlegen-telefonisch/">Telefonische Beratung</a></li>
        <li><a href="/kartenlegen-muenchen/">Kartenlegen München</a></li>
        <li><a href="/kartenlegen-augsburg/">Kartenlegen Augsburg</a></li>
        <li><a href="/kartenlegen-ulm/">Kartenlegen Ulm</a></li>
        <li><a href="/kartenlegen-memmingen/">Kartenlegen Memmingen</a></li>
        <li><a href="/kartenlegen-zuerich/">Kartenlegen Zürich</a></li>
        <li><a href="/hausbesuch-raumklaerung/">Hausbesuch &amp; Raumklärung</a></li>
        <li><a href="/faq-kartenlegen/">Häufige Fragen</a></li>
      </ul>
    </nav>
    <nav aria-label="Footer-Navigation Events">
      <h2 class="footer-heading">Events &amp; mehr</h2>
      <ul class="footer-list">
        <li><a href="/events/">Kartenlegen für Events</a></li>
        <li><a href="/kartenlegen-junggesellinnenabschied-bodensee/">JGA am Bodensee</a></li>
        <li><a href="/kartenlegen-hochzeit/">Hochzeit</a></li>
        <li><a href="/kartenlegen-firmenfeier/">Firmenfeier</a></li>
        <li><a href="/tier-mensch/">Tier &amp; Mensch</a></li>
        <li><a href="/ergaenzende-impulse/">Ergänzende Impulse</a></li>
        <li><a href="/ueber-thomas-lude/">Über Thomas</a></li>
        <li><a href="/ratgeber/">Ratgeber</a></li>
        <li><a href="/blog/">Blog</a></li>
      </ul>
    </nav>
    <div>
      <h2 class="footer-heading">Kontakt</h2>
      <ul class="footer-list">
        <li><a href="%(tel)s">%(phone)s</a></li>
        <li><a href="%(wa)s" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="%(mail)s">%(email)s</a></li>
        <li>%(area)s</li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; Thomas Lude · %(city)s am Bodensee · Website von <a href="https://vortexkey.de" target="_blank" rel="noopener">VortexKey</a></p>
    <nav class="footer-legal" aria-label="Rechtliches">
      <a href="/impressum/">Impressum</a>
      <a href="/datenschutz/">Datenschutz</a>
    </nav>
  </div>
</footer>

<nav class="mobile-bar" aria-label="Schnellkontakt">
  <a href="%(wa)s?text=%(wamsg)s" target="_blank" rel="noopener" class="mobile-bar-item">%(waicon)s<span>WhatsApp</span></a>
  <a href="%(tel)s" class="mobile-bar-item">%(phoneicon)s<span>Anrufen</span></a>
  <a href="/kontakt-termin/" class="mobile-bar-item gold">%(calicon)s<span>Termin</span></a>
</nav>

<a class="wa-float" href="%(wa)s?text=%(wamsg)s" target="_blank" rel="noopener" aria-label="Direkt per WhatsApp Kontakt aufnehmen">
  <span class="wa-float-ring" aria-hidden="true"></span>
  %(waiconbig)s
  <span class="wa-float-text">WhatsApp</span>
</a>

<script data-goatcounter="https://thomaslude.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
""" % {
        "title": title, "desc": meta_desc, "canonical": canonical,
        "sitename": SITE_NAME, "site": SITE_URL, "preload": preload,
        "schema": json.dumps(schema, ensure_ascii=False),
        "nav": nav_html, "body": body,
        "tel": TEL_HREF, "phone": PHONE, "wa": WA_HREF, "mail": MAIL_HREF,
        "email": EMAIL, "area": AREA, "city": CITY,
        "wamsg": _urlencode("Hallo Thomas, ich interessiere mich für eine Beratung."),
        "waicon": icon("whatsapp", 20), "phoneicon": icon("phone", 20), "calicon": icon("calendar", 20),
        "waiconbig": icon("whatsapp", 30),
    }

# ----------------------------------------------------------------------------
# Seiten schreiben
# ----------------------------------------------------------------------------
def write_page(slug, title, meta_desc, body, hero_preload="", extra_schema=None):
    path = OUT if not slug else os.path.join(OUT, slug)
    os.makedirs(path, exist_ok=True)
    html = layout(slug, title, meta_desc, body, hero_preload, extra_schema)
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("gebaut:", "/" + (slug + "/" if slug else ""))

def faq_schema(items):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


# ----------------------------------------------------------------------------
# STARTSEITE
# ----------------------------------------------------------------------------
def home_body():
    generation_item = ""
    if SHOW_GENERATION:
        generation_item = """
      <div class="trust-item">%s
        <div><strong>Kartenlegen in 3. Generation</strong><span>Erfahrung, Intuition und eine lange Familientradition.</span></div>
      </div>""" % icon("lotus", 30)
    else:
        generation_item = """
      <div class="trust-item">%s
        <div><strong>Erfahrung, die man spürt</strong><span>Ruhig, klar und ohne Show – mit beiden Beinen am Boden.</span></div>
      </div>""" % icon("lotus", 30)

    stars = icon("star", 16) * 5

    return """
<!-- HERO -->
<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">Kartenlegen in Friedrichshafen · Bodensee</p>
        <h1>Manchmal braucht es einen anderen Blick.</h1>
        <p class="lead hero-text-strong">Persönliche Kartenberatung mit Thomas Lude. Direkt, diskret und ohne großes Theater.</p>
        <p class="lead">Für Liebe &amp; Beziehung, Entscheidungen, Veränderungen und die Fragen, die dich gerade nicht loslassen.</p>
        <div class="cta-row">
          <a class="btn btn-gold" href="/kontakt-termin/">Termin anfragen →</a>
          <a class="btn btn-outline-light" href="/ueber-thomas-lude/">Thomas kennenlernen</a>
        </div>
      </div>
      <div class="hero-image">
        %(hero_img)s
      </div>
    </div>
    <div class="hero-trust">
      <div class="hero-trust-item">%(pin)s Persönlich in Friedrichshafen</div>
      <div class="hero-trust-item">%(phonehero)s Telefonisch – bundesweit</div>
      <div class="hero-trust-item">%(users)s Events am Bodensee</div>
    </div>
  </div>
</section>

<!-- TRUST-BAR -->
<div class="trust-bar">
  <div class="container trust-bar-inner">
    %(generation)s
    <div class="trust-item">%(shield)s
      <div><strong>Persönlich &amp; diskret</strong><span>Was besprochen wird, bleibt zwischen uns.</span></div>
    </div>
    <div class="trust-item">%(waves)s
      <div><strong>Mitten am Bodensee</strong><span>Persönliche Beratung in Friedrichshafen und telefonisch darüber hinaus.</span></div>
    </div>
  </div>
</div>

<!-- THEMEN -->
<section class="section" id="themen">
  <div class="container">
    <div class="section-head">
      <h2>Was möchtest du klarer sehen?</h2>
    </div>
    <div class="card-grid three">
      <article class="card">
        <a class="card-image" href="/kartenlegen-liebe-partnerschaft/">%(card_liebe)s</a>
        <div class="card-body">
          <h3><a href="/kartenlegen-liebe-partnerschaft/">Liebe &amp; Beziehung</a></h3>
          <p>Was verbindet euch? Wo steht ihr? Welche Entwicklung zeichnet sich ab?</p>
          <a class="link-more" href="/kartenlegen-liebe-partnerschaft/">Mehr erfahren</a>
        </div>
      </article>
      <article class="card">
        <a class="card-image" href="/kartenlegen-entscheidung-zukunft/">%(card_entscheidung)s</a>
        <div class="card-body">
          <h3><a href="/kartenlegen-entscheidung-zukunft/">Entscheidung &amp; Veränderung</a></h3>
          <p>Manchmal stehen mehrere Wege offen. Ein anderer Blick kann helfen.</p>
          <a class="link-more" href="/kartenlegen-entscheidung-zukunft/">Mehr erfahren</a>
        </div>
      </article>
      <article class="card">
        <a class="card-image" href="/kartenlegen-beruf-veraenderung/">%(card_beruf)s</a>
        <div class="card-body">
          <h3><a href="/kartenlegen-beruf-veraenderung/">Beruf &amp; Zukunft</a></h3>
          <p>Neue Richtung, Veränderung oder eine wichtige Entscheidung?</p>
          <a class="link-more" href="/kartenlegen-beruf-veraenderung/">Mehr erfahren</a>
        </div>
      </article>
      <article class="card">
        <a class="card-image" href="/kartenlegen-hauskauf-umzug/">%(card_hauskauf)s</a>
        <div class="card-body">
          <h3><a href="/kartenlegen-hauskauf-umzug/">Hauskauf &amp; Umzug</a></h3>
          <p>Kaufen, mieten, umziehen oder neu anfangen – ein Blick auf die persönliche Seite der Entscheidung.</p>
          <a class="link-more" href="/kartenlegen-hauskauf-umzug/">Mehr erfahren</a>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ÜBER THOMAS -->
<section class="section section-white" id="ueber-thomas">
  <div class="container split">
    <div class="split-media">%(ueber_img)s</div>
    <div>
      <h2>Ich bin Thomas.</h2>
      <p><strong>Und ich sage dir nicht einfach das, was du hören möchtest.</strong></p>
      <p>Seit vielen Jahren begleite ich Menschen, wenn das Leben Fragen stellt. Die Karten können Zusammenhänge, Tendenzen und Möglichkeiten aufzeigen – ehrlich, klar und einfühlsam. Was du daraus machst, bleibt deine Entscheidung.</p>
      <p>Kartenlegen ist für mich eine Berufung, die schon in meiner Familie verwurzelt ist – ich lege die Karten in dritter Generation. Heute verbinde ich diese Tradition mit meiner Erfahrung, meiner Intuition und einer bodenständigen, lebensnahen Art.</p>
      <p class="tag-note">Kartenlegen · Hellfühlige Beratung · Friedrichshafen am Bodensee</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="/ueber-thomas-lude/">Mehr über Thomas →</a>
      </div>
    </div>
  </div>
</section>

<!-- MEHR ALS KARTENLEGEN -->
<section class="section section-soft" id="hellfuehlig">
  <div class="container prose" style="max-width:760px;">
    <p class="eyebrow">Mehr als Kartenlegen</p>
    <h2>Die Karten sind eines meiner Werkzeuge – nicht das einzige.</h2>
    <p>Thomas beschreibt sich selbst als ausgesprochen hellfühlig. In einer Beratung verbindet er seine intuitive Wahrnehmung mit der Kartenlegung – manches nimmt er schon wahr, bevor überhaupt eine Karte auf dem Tisch liegt. Besonders intensiv erlebt er diese Wahrnehmung bei <a href="/hausbesuch-raumklaerung/">Hausbesuchen</a>, weil er dort auch die Umgebung und Atmosphäre eines Zuhauses kennenlernt.</p>
    <p>Was sich dabei zeigt, versteht Thomas nicht als feste Zukunftsvorhersage, sondern als Einladung, genauer hinzuschauen. Die Karten geben Orientierung und machen Zusammenhänge sichtbar – sie ersetzen keine Entscheidung, sie können aber einen Impuls geben, der sich stimmig anfühlt.</p>
  </div>
</section>

<!-- EVENTS / JGA -->
<section class="section section-dark" id="events">
  <div class="container split reverse">
    <div>
      <p class="eyebrow">Etwas anderes erleben</p>
      <h2>Ihr habt den Prosecco.<br>Thomas bringt die Karten.</h2>
      <p class="lead">Kartenlegen für JGA, Mädelsabend, Geburtstag &amp; besondere Momente am Bodensee.</p>
      <p>Ihr sucht einen Programmpunkt, über den ihr noch lange sprecht? Thomas kommt zu euch – ins Ferienhaus, zur Feier oder an einen vereinbarten Ort – und nimmt sich für jede Teilnehmerin persönlich Zeit.</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="/kartenlegen-junggesellinnenabschied-bodensee/">Kartenabend anfragen →</a>
      </div>
      <ul class="chips">
        <li>Junggesellinnenabschied</li>
        <li>Mädelsabend</li>
        <li>Geburtstag</li>
        <li>Freundinnen-Wochenende</li>
        <li>Private Feier</li>
      </ul>
    </div>
    <div class="split-media">%(jga_img)s</div>
  </div>
</section>

<!-- TIER & MENSCH -->
<section class="section section-white" id="tier-mensch">
  <div class="container split">
    <div class="split-media">%(tier_img)s</div>
    <div>
      <p class="eyebrow">Tier &amp; Mensch</p>
      <h2>Manchmal braucht auch ein Tier einfach Ruhe.</h2>
      <p><strong>Energetische Begleitung für Tiere und ihre Menschen.</strong></p>
      <p>Tiere nehmen Veränderungen und Stimmungen oft sehr fein wahr. In meiner energetischen Tierbegleitung geht es um Aufmerksamkeit, Ruhe und Verbindung – ergänzend, nicht als Ersatz für tierärztliche Behandlung.</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="/tier-mensch/">Tierbegleitung kennenlernen →</a>
      </div>
      <p class="tag-note">Energetische Begleitung ersetzt keine tierärztliche Diagnose oder Behandlung.</p>
    </div>
  </div>
</section>

<!-- ERGÄNZENDE IMPULSE -->
<section class="section" id="ergaenzende-impulse">
  <div class="container prose" style="max-width:760px;text-align:center;">
    <p class="eyebrow">Ergänzende Impulse</p>
    <h2>Manchmal hilft ein zweiter Blick.</h2>
    <p>Für manche Fragen reicht ein Termin. Für andere – eine berufliche Weichenstellung, ein wiederkehrendes Muster, eine Entscheidung mit langer Tragweite – lohnt sich mitunter eine zweite, ergänzende Perspektive. Dafür verweise ich, wo es passt, auch auf ausgewählte andere Systeme.</p>
      <div class="cta-row" style="justify-content:center;">
        <a class="btn btn-gold" href="/ergaenzende-impulse/">Ergänzende Impulse ansehen →</a>
      </div>
  </div>
</section>

<!-- ABLAUF -->
<section class="section section-soft" id="ablauf">
  <div class="container">
    <div class="section-head">
      <h2>So läuft eine Beratung ab</h2>
    </div>
    <ol class="steps">
      <li class="step">
        <h3>Du nimmst Kontakt auf</h3>
        <p>Per WhatsApp, Telefon oder Kontaktformular.</p>
      </li>
      <li class="step">
        <h3>Du erzählst dein Thema</h3>
        <p>Du brauchst keine perfekte Frage. Es reicht, was dich beschäftigt.</p>
      </li>
      <li class="step">
        <h3>Wir schauen gemeinsam hin</h3>
        <p>Thomas legt die Karten und bespricht mit dir, welche Zusammenhänge er erkennt.</p>
      </li>
      <li class="step">
        <h3>Du entscheidest</h3>
        <p>Du nimmst mit, was für dich hilfreich ist. Keine Abhängigkeit, kein „Du musst“.</p>
      </li>
    </ol>
  </div>
</section>

<!-- VERTRAUEN (Fakten statt erfundener Zitate, bis echte Bewertungen vorliegen) -->
<section class="section" id="erfahrungen">
  <div class="container">
    <div class="section-head left" style="text-align:left;">
      <h2>Warum Menschen Thomas vertrauen</h2>
    </div>
    <div class="card-grid three">
      <article class="card">
        <div class="card-body">
          <h3>Kartenlegen in dritter Generation</h3>
          <p>Eine Tradition, die in der Familie gewachsen ist – verbunden mit eigener Erfahrung und einer bodenständigen, ehrlichen Art.</p>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3>Kunden aus Deutschland, Österreich und der Schweiz</h3>
          <p>Persönlich am Bodensee, telefonisch weit darüber hinaus – über die Region hinaus bekannt, vor allem durch Weiterempfehlung.</p>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3>Diskretion als Grundprinzip</h3>
          <p>Was am Kartentisch oder am Telefon besprochen wird, bleibt vertraulich – ohne Ausnahme.</p>
        </div>
      </article>
    </div>
    <p class="tag-note" style="margin-top:1.6rem;">Bewertungen folgen in Kürze – sobald erste Kundinnen und Kunden öffentlich Rückmeldung geben.</p>
  </div>
</section>

<!-- BODENSEE / LOCAL -->
<section class="section section-soft" id="region">
  <div class="container split">
    <div class="split-media">%(local_img)s</div>
    <div>
      <p class="eyebrow">Zuhause am Bodensee</p>
      <h2>Persönlich in Friedrichshafen. Verbunden weit darüber hinaus.</h2>
      <p>Termine in Friedrichshafen und nach Vereinbarung in der Region Bodensee. Telefonisch erreichst du Thomas von überall – auch aus München, Augsburg, Ulm, Memmingen oder der Schweiz. Für Kartenabende kommt Thomas zu Gruppen.</p>
      <p class="tag-note">Friedrichshafen · Meersburg · Überlingen · Konstanz · Lindau · Ravensburg · <a href="/kartenlegen-muenchen/">München</a> · <a href="/kartenlegen-augsburg/">Augsburg</a> · <a href="/kartenlegen-ulm/">Ulm</a> · <a href="/kartenlegen-memmingen/">Memmingen</a> · <a href="/kartenlegen-zuerich/">Zürich</a></p>
      <div class="cta-row">
        <a class="btn btn-outline-dark" href="/kartenlegen-friedrichshafen/">Kartenlegen in Friedrichshafen</a>
      </div>
    </div>
  </div>
</section>

<!-- BLOG -->
<section class="section section-white" id="blog">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Aus dem Blog</p>
      <h2>Texte über Wahrnehmung, Räume und die Fragen dazwischen</h2>
      <p class="lead">Persönliche Erfahrungen, ruhige Erklärungen und ehrliche Grenzen – für Menschen, die tiefer verstehen möchten, wie Thomas arbeitet.</p>
    </div>
    <div class="card-grid three">
      %(blog_cards)s
    </div>
    <div class="center" style="margin-top:2.2rem;">
      <a class="btn btn-outline-dark" href="/blog/">Alle Beiträge lesen</a>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="section" id="faq">
  <div class="container">
    <div class="section-head left" style="text-align:left;">
      <h2>Häufige Fragen</h2>
    </div>
    %(faq)s
  </div>
</section>

<!-- SCHLUSS-CTA -->
<section class="section section-white" id="kontakt">
  <div class="container split">
    <div class="split-media">%(cta_img)s</div>
    <div>
      <h2>Was möchtest du wissen?</h2>
      <p><strong>Manchmal beginnt Klarheit mit einem Gespräch.</strong></p>
      <p>Erzähl Thomas kurz, worum es geht. Gemeinsam findet ihr heraus, welche Form der Beratung zu deinem Anliegen passt.</p>
      <div class="cta-row">
        <a class="btn btn-whatsapp" href="%(wa)s?text=%(wamsg)s" target="_blank" rel="noopener">%(waicon)s Bei WhatsApp schreiben</a>
        <a class="btn btn-gold" href="/kontakt-termin/">Termin anfragen</a>
        <a class="btn btn-outline-dark" href="%(tel)s">%(phoneicon)s Anrufen</a>
      </div>
      <div class="final-cta-list">
        <div class="final-cta-item">%(phoneicon2)s <div><strong>%(phone)s</strong><small>%(phonehint)s</small></div></div>
        <div class="final-cta-item">%(pin)s <div><strong>Friedrichshafen</strong><small>am Bodensee</small></div></div>
        <div class="final-cta-item">%(mailicon)s <div><strong>%(email)s</strong></div></div>
      </div>
    </div>
  </div>
</section>
""" % {
        "hero_img": img("thomas-lude-kartenleger-friedrichshafen-bodensee",
                        "Thomas Lude legt einer Frau am Kartentisch die Karten, warmes Licht, Blick über ihre Schulter",
                        sizes="(max-width: 920px) 100vw, 50vw", loading="eager", fetchpriority="high"),
        "pin": icon("pin", 20), "phonehero": icon("phone", 20), "users": icon("users", 20),
        "generation": generation_item, "shield": icon("shield", 30), "waves": icon("waves", 30),
        "card_liebe": img("thomas-lude-kartenlegen-liebe-beziehung", "Thomas Lude legt Karten zu einer Frage rund um Liebe und Beziehung"),
        "card_entscheidung": img("thomas-lude-kartenlegen-beratung-am-tisch", "Thomas Lude am runden Kartentisch mit ausgelegten Karten und Kerze"),
        "card_beruf": img("thomas-lude-ueber-thomas-kartenlegen", "Thomas Lude bei einer Beratung im hellen Wintergarten am Bodensee"),
        "card_hauskauf": img("kartenlegen-hauskauf-umzug", "Schreibtisch mit Kartenset, Kompass und Hausschlüssel vor einem Wegweiser mit den Richtungen Kaufen, Vermieten, Umzug und Neu beginnen"),
        "ueber_img": img("thomas-lude-ueber-thomas-kartenlegen", "Thomas Lude sitzt freundlich an seinem Kartentisch und lächelt"),
        "jga_img": img("thomas-lude-kartenlegen-jga-bodensee", "Kartenabend mit Thomas Lude bei einem Junggesellinnenabschied: Braut mit Schleier und Freundinnen am gedeckten Tisch"),
        "tier_img": img("thomas-lude-tierbegleitung-bodensee", "Thomas Lude legt einem entspannten Golden Retriever ruhig die Hände auf"),
        "stars": stars,
        "blog_cards": "\n".join(blog_card(p) for p in BLOG_POSTS[:3]),
        "local_img": img("thomas-lude-kartenlegen-beratung-am-tisch", "Thomas Lude am Kartentisch mit Salzsteinlampe und Kerze in seinem Beratungsraum"),
        "faq": faq_html(FAQ_MAIN),
        "cta_img": img("thomas-lude-portrait-hund-friedrichshafen", "Thomas Lude lacht freundlich in die Kamera, sein Golden Retriever entspannt neben ihm"),
        "wa": WA_HREF, "wamsg": _urlencode("Hallo Thomas, ich interessiere mich für eine Beratung."),
        "waicon": icon("whatsapp", 18), "tel": TEL_HREF, "phoneicon": icon("phone", 18),
        "phoneicon2": icon("phone", 22), "phone": PHONE, "phonehint": PHONE_HINT,
        "mailicon": icon("mail", 22), "email": EMAIL,
    }


# ----------------------------------------------------------------------------
# LANDINGPAGES (Aufbau: Einstieg – Nutzen – Ablauf – Warum Thomas – CTA)
# ----------------------------------------------------------------------------
def landing_body(eyebrow, h1, lead, image, image_alt, prose, faq_items=None,
                 whatsapp_msg="Hallo Thomas, ich interessiere mich für eine Beratung.",
                 cta_title="Manchmal beginnt Klarheit mit einem Gespräch.",
                 cta_text="Schreib kurz, worum es geht – Thomas meldet sich persönlich."):
    breadcrumb_title = h1
    faq_block = ""
    if faq_items:
        faq_block = """
<section class="section section-soft">
  <div class="container">
    <div class="section-head left" style="text-align:left;">
      <h2>Häufige Fragen</h2>
    </div>
    %s
  </div>
</section>""" % faq_html(faq_items)

    return """
<header class="page-hero">
  <div class="container page-hero-split">
    <div>
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>%(breadcrumb)s</span></nav>
      <p class="eyebrow">%(eyebrow)s</p>
      <h1>%(h1)s</h1>
      <p class="lead">%(lead)s</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="/kontakt-termin/">Termin anfragen</a>
        <a class="btn btn-outline-dark" href="%(wa)s?text=%(wamsg)s" target="_blank" rel="noopener">%(waicon)s WhatsApp</a>
      </div>
    </div>
    <div>%(image)s</div>
  </div>
</header>

<section class="section">
  <div class="container prose">
    %(prose)s
  </div>
</section>

%(faq)s
%(cta)s
""" % {
        "breadcrumb": breadcrumb_title, "eyebrow": eyebrow, "h1": h1, "lead": lead,
        "wa": WA_HREF, "wamsg": _urlencode(whatsapp_msg), "waicon": icon("whatsapp", 18),
        "image": img(image, image_alt, sizes="(max-width: 920px) 100vw, 45vw", loading="eager", fetchpriority="high"),
        "prose": prose, "faq": faq_block,
        "cta": cta_band(cta_title, cta_text, whatsapp_msg),
    }


LANDING_PAGES = [
    # --- Region: Friedrichshafen ---
    {
        "slug": "kartenlegen-friedrichshafen",
        "title": "Kartenlegen in Friedrichshafen mit Thomas Lude | Thomas Lude",
        "desc": "Persönliches Kartenlegen in Friedrichshafen am Bodensee: diskret, direkt und ohne großes Theater. Termin bei Thomas Lude anfragen.",
        "eyebrow": "Persönliche Beratung vor Ort",
        "h1": "Kartenlegen in Friedrichshafen mit Thomas Lude",
        "lead": "Du suchst einen Kartenleger in Friedrichshafen? Thomas berät dich persönlich am Kartentisch – direkt, diskret und ohne großes Theater.",
        "image": "thomas-lude-kartenleger-friedrichshafen-bodensee",
        "alt": "Thomas Lude bei einer persönlichen Kartenberatung mit einer Frau in Friedrichshafen",
        "prose": """
<h2>Kartenberatung – persönlich und auf Augenhöhe</h2>
<p>Bei Thomas gibt es keine dunklen Vorhänge und keine großen Versprechen. Du kommst mit deiner Frage, ihr setzt euch an den Tisch, und gemeinsam schaut ihr, was die Karten sichtbar machen: Zusammenhänge, Tendenzen und mögliche Entwicklungen.</p>
<p>Ob Liebe und Beziehung, eine anstehende Entscheidung, berufliche Veränderung oder einfach das Gefühl, dass sich etwas sortieren muss – Thomas nimmt sich Zeit für dein Thema.</p>
<h2>Worum es in einer Beratung gehen kann</h2>
<ul class="tick-list">
  <li>Liebe, Partnerschaft, Trennung und Ex-Partner</li>
  <li>Entscheidungen und persönliche Veränderungen</li>
  <li>Familie und nahe Beziehungen</li>
  <li>Beruf und Neuorientierung</li>
  <li>Zukunft und Lebensrichtung</li>
</ul>
<h2>Ablauf deines Termins in Friedrichshafen</h2>
<ol>
  <li><strong>Kontakt aufnehmen</strong> – kurz per WhatsApp, Telefon oder über das Formular.</li>
  <li><strong>Termin vereinbaren</strong> – ihr findet einen Zeitpunkt, der passt.</li>
  <li><strong>Beratung</strong> – du erzählst dein Thema, Thomas legt die Karten und ihr besprecht, was sich zeigt.</li>
  <li><strong>Mitnehmen, was passt</strong> – was du daraus machst, bleibt deine Entscheidung.</li>
</ol>
<h2>Wo findet die Beratung statt?</h2>
<p>In Friedrichshafen am Bodensee – den genauen Beratungsort bekommst du bei der Terminvereinbarung. 30 Minuten 79 €, 60 Minuten 149 €, 90 Minuten 219 €, 120 Minuten 289 €. Wenn du nicht persönlich kommen kannst, ist eine <a href="/kartenlegen-telefonisch/">Beratung am Telefon</a> zum gleichen Preis genauso möglich.</p>
""",
        "faq": [
            ("Muss ich mich auf die Beratung vorbereiten?",
             "Nein. Es reicht, wenn du deine Frage oder dein Thema ungefähr kennst. Alles Weitere ergibt sich im Gespräch."),
            ("Wie lange dauert eine Kartenlegung?",
             "Plane etwa 45 bis 60 Minuten ein. Die genaue Dauer hängt von deinem Thema ab und wird bei der Anfrage besprochen."),
            ("Bleibt das, was ich erzähle, vertraulich?",
             "Ja. Diskretion ist bei Thomas selbstverständlich – was am Kartentisch besprochen wird, bleibt am Kartentisch."),
        ],
        "wa": "Hallo Thomas, ich interessiere mich für eine Beratung in Friedrichshafen.",
    },
    # --- Region: Bodensee ---
    {
        "slug": "kartenlegen-bodensee",
        "title": "Kartenlegen am Bodensee – persönlich mit Thomas Lude | Thomas Lude",
        "desc": "Kartenlegen am Bodensee: persönliche Beratung in Friedrichshafen, telefonisch überall und als mobiler Kartenabend für Gruppen rund um den See.",
        "eyebrow": "Zuhause am See",
        "h1": "Kartenlegen am Bodensee – persönlich mit Thomas Lude",
        "lead": "Thomas lebt und arbeitet am Bodensee. Persönliche Beratungen in Friedrichshafen, telefonische Beratung überall – und mobile Kartenabende für Gruppen rund um den See.",
        "image": "thomas-lude-ueber-thomas-kartenlegen",
        "alt": "Thomas Lude an seinem Kartentisch mit Blick in den Garten, Bodensee-Region",
        "prose": """
<h2>Ein Kartenleger, der hier zuhause ist</h2>
<p>Thomas ist kein anonymer Anbieter aus dem Internet – er ist am Bodensee verwurzelt. Das merkt man an der Art, wie er berät: ruhig, bodenständig und direkt. Wer ihn persönlich erleben möchte, kommt nach <a href="/kartenlegen-friedrichshafen/">Friedrichshafen</a>.</p>
<h2>So erreichst du Thomas am Bodensee</h2>
<ul class="tick-list">
  <li><strong>Persönliche Beratung</strong> – am Kartentisch in Friedrichshafen</li>
  <li><strong>Telefonische Beratung</strong> – nach Termin, egal von wo</li>
  <li><strong>Kartenabende für Gruppen</strong> – Thomas kommt zu euch, rund um den Bodensee nach Absprache</li>
  <li><strong>Energetische Tierbegleitung</strong> – für Tiere und ihre Menschen in der Region</li>
</ul>
<h2>Für Gruppen rund um den See</h2>
<p>Ihr plant einen <a href="/kartenlegen-junggesellinnenabschied-bodensee/">Junggesellinnenabschied</a>, einen Mädelsabend oder ein Wochenende mit Freundinnen am Bodensee? Thomas kommt mit den Karten zu euch – in die Ferienwohnung, ins Hotel oder in eure Location. Mehr dazu auf der <a href="/events/">Event-Seite</a>.</p>
<h2>Und wenn du weiter weg wohnst?</h2>
<p>Dann funktioniert es genauso gut <a href="/kartenlegen-telefonisch/">am Telefon</a>. Viele Themen lassen sich in einem ruhigen Gespräch genauso klar betrachten wie am Tisch.</p>
""",
    },
    # --- Thema: Liebe & Partnerschaft ---
    {
        "slug": "kartenlegen-liebe-partnerschaft",
        "title": "Kartenlegen für Liebe & Partnerschaft | Thomas Lude",
        "desc": "Kartenlegen bei Liebe, Beziehung und Trennung: Thomas Lude am Bodensee hilft dir, deine Situation klarer zu sehen – ehrlich und diskret.",
        "eyebrow": "Das Herzensthema",
        "h1": "Kartenlegen für Liebe &amp; Partnerschaft",
        "lead": "Wenn es um Beziehung, Trennung oder die Frage „Wo stehen wir eigentlich?“ geht, hilft manchmal ein anderer Blick.",
        "image": "thomas-lude-kartenlegen-liebe-beziehung",
        "alt": "Thomas Lude bespricht mit einer Kundin Karten zu einer Liebesfrage, warmes Abendlicht",
        "prose": """
<h2>Wenn das Herz Fragen stellt</h2>
<p>Liebe ist das Thema, mit dem die meisten Menschen zu Thomas kommen. Vielleicht stehst du gerade am Anfang von etwas Neuem und fragst dich, was daraus werden kann. Vielleicht steckst du in einer Beziehung fest, die sich nicht mehr richtig anfühlt. Oder eine Trennung liegt hinter dir – und sie lässt dich einfach nicht los.</p>
<p>Diese Fragen verdienen Raum. Keine schnellen Antworten, keine Floskeln – sondern jemanden, der zuhört und mit dir gemeinsam hinschaut.</p>
<h2>Was Kartenlegen bei Liebesfragen leisten kann</h2>
<p>Die Karten können Muster, Tendenzen und mögliche Entwicklungen sichtbar machen – auch deine eigene Rolle in einer Situation. Oft liegt genau in diesem Blick die Klarheit, die du suchst. Typische Themen sind:</p>
<ul class="tick-list">
  <li>Beziehung – wo stehen wir, wohin geht es?</li>
  <li>Kennenlernen – was entwickelt sich daraus?</li>
  <li>Trennung – was hilft mir beim Weitergehen?</li>
  <li>Ex-Partner – warum lässt mich das nicht los?</li>
  <li>Unsicherheit und Missverständnisse in der Kommunikation</li>
</ul>
<h2>So läuft eine Beratung ab</h2>
<p>Du erzählst in ein paar Sätzen, worum es geht – mehr braucht es nicht. Thomas legt die Karten, bespricht mit dir, was sich zeigt, und beantwortet deine Fragen ehrlich. Persönlich in <a href="/kartenlegen-friedrichshafen/">Friedrichshafen</a> oder diskret <a href="/kartenlegen-telefonisch/">am Telefon</a>.</p>
<h2>Warum Thomas Lude</h2>
<p>Thomas behauptet nicht, die Gedanken eines anderen Menschen sicher lesen zu können – und er verspricht keine Wunder. Er hilft dir, deine Situation klarer zu sehen, damit du besser entscheiden kannst. Was ihr besprecht, bleibt unter euch.</p>
""",
        "faq": [
            ("Kann mir Thomas sagen, ob mein Ex zurückkommt?",
             "Eine Garantie gibt es nicht – und die wäre auch unseriös. Thomas kann mit den Karten Tendenzen und Zusammenhänge sichtbar machen und mit dir besprechen, was das für dich bedeuten kann."),
            ("Kann ich eine Frage stellen, ohne Details preiszugeben?",
             "Ja. Du entscheidest, wie viel du erzählen möchtest. Oft reichen schon wenige Sätze, um in ein Thema einzusteigen."),
            ("Was, wenn mir etwas Negatives gezeigt wird?",
             "Thomas macht keine Angst. Es geht darum, Möglichkeiten zu sehen – nicht darum, Schreckensszenarien zu malen."),
        ],
        "wa": "Hallo Thomas, ich habe eine Frage zu Liebe und Beziehung.",
    },
    # --- Thema: Entscheidung & Zukunft ---
    {
        "slug": "kartenlegen-entscheidung-zukunft",
        "title": "Kartenlegen bei Entscheidungen & Veränderungen | Thomas Lude",
        "desc": "Vor einer wichtigen Entscheidung? Kartenlegen mit Thomas Lude am Bodensee hilft, Optionen und Tendenzen klarer zu sehen.",
        "eyebrow": "Wenn sich etwas bewegt",
        "h1": "Kartenlegen bei Entscheidungen &amp; Veränderungen",
        "lead": "Du stehst vor einer Wahl und drehst dich im Kreis? Ein anderer Blick kann Optionen sortieren, die du allein nicht klar siehst.",
        "image": "thomas-lude-kartenlegen-beratung-am-tisch",
        "alt": "Thomas Lude legt Karten bei einer Beratung zu einer anstehenden Entscheidung",
        "prose": """
<h2>Entscheidungen werden leichter, wenn man sie sieht</h2>
<p>Vielleicht kennst du das: Zwei Wege liegen vor dir, und beide fühlen sich irgendwie richtig und irgendwie falsch an. Im Kopf dreht sich alles im Kreis, und je länger du nachdenkst, desto unklarer wird es. Genau in solchen Momenten kann ein Blick von außen helfen.</p>
<h2>Was Kartenlegen bei Entscheidungen leisten kann</h2>
<p>Die Karten ersetzen keine Pro-und-Contra-Liste – aber sie können Perspektiven sichtbar machen, die im Alltag untergehen: Welche Optionen trägst du eigentlich in dir? Was spricht für welchen Weg? Welche Tendenzen zeigen sich? Typische Situationen:</p>
<ul class="tick-list">
  <li>Zwei Optionen, beide fühlen sich halb richtig an</li>
  <li>Eine Veränderung steht an – privat oder im Umfeld</li>
  <li>Das Gefühl, festzustecken, ohne zu wissen warum</li>
  <li>Eine wichtige Entscheidung, die man nicht allein treffen will</li>
</ul>
<h2>So läuft eine Beratung ab</h2>
<p>Du schilderst deine Situation, Thomas legt die Karten und bespricht mit dir, was er sieht – ehrlich und auf den Punkt. Am Ende gehst du nicht mit einer Anweisung, sondern mit mehr Klarheit nach Hause.</p>
<h2>Warum Thomas Lude</h2>
<p>Thomas trifft keine Entscheidung für dich – und keine seriöse Beratung sollte das. Er zeigt, was sich zeigt, und sagt ehrlich, was er sieht. Manchmal liegt die Antwort schon vor uns. Wir sehen sie nur noch nicht.</p>
""",
    },
    # --- Thema: Beruf & Veränderung ---
    {
        "slug": "kartenlegen-beruf-veraenderung",
        "title": "Kartenlegen zu Beruf, Veränderung & neuer Richtung | Thomas Lude",
        "desc": "Berufliche Neuorientierung oder Jobwechsel? Kartenlegen mit Thomas Lude hilft, die eigene Situation zu sortieren – ohne Erfolgsversprechen.",
        "eyebrow": "Neue Richtung",
        "h1": "Kartenlegen zu Beruf, Veränderung &amp; neuer Richtung",
        "lead": "Jobwechsel, Neuorientierung oder das leise Gefühl, dass etwas nicht mehr passt – gemeinsam sortieren, was sich gerade bewegt.",
        "image": "thomas-lude-ueber-thomas-kartenlegen",
        "alt": "Thomas Lude in einer ruhigen Beratung zu beruflichen Fragen",
        "prose": """
<h2>Wenn sich beruflich etwas sortieren muss</h2>
<p>Kündigen oder bleiben? Sich selbstständig machen oder nicht? Bewerben oder warten? Berufliche Fragen sind selten nur sachlich – sie hängen mit Sicherheit, Familie und der Frage zusammen, wer man eigentlich sein will. Genau deshalb hilft ein Blick, der nicht nur auf Zahlen schaut.</p>
<h2>Was Kartenlegen bei Berufsfragen leisten kann</h2>
<ul class="tick-list">
  <li>Berufliche Neuorientierung und Richtungswechsel sortieren</li>
  <li>Entscheidungen zwischen konkreten Optionen klären</li>
  <li>Konflikte und Dynamiken am Arbeitsplatz besser verstehen</li>
  <li>Den richtigen Zeitpunkt und die eigene Rolle erkennen</li>
</ul>
<h2>Geschäftliche Entscheidungen</h2>
<p>Manche Entscheidungen lassen sich nicht allein mit Zahlen oder Listen lösen. Für Selbstständige und Unternehmer, die vor wichtigen Weichenstellungen stehen, kann eine Beratung helfen, die eigene Intuition bewusster mit einzubeziehen – neben Kopf auch Bauch.</p>
<h2>So läuft eine Beratung ab</h2>
<p>Du erzählst, wo du stehst und was dich beschäftigt. Thomas legt die Karten und bespricht mit dir, welche Tendenzen und Möglichkeiten sich zeigen – persönlich in Friedrichshafen oder am Telefon.</p>
<h2>Warum Thomas Lude</h2>
<p>Thomas ist Kartenleger, kein Finanz-, Karriere-, Rechts- oder Immobilienberater. Er gibt keine Erfolgsgarantien und keine Empfehlung zum Kauf, Verkauf oder Halten von Geldanlagen, Wertpapieren oder Immobilien. Was er kann: dir helfen, deine Situation klarer zu sehen – damit du deine Entscheidung eigenverantwortlich und mit mehr Ruhe triffst, gegebenenfalls nach Rücksprache mit entsprechend qualifizierten Fachleuten.</p>
<p>Steht eher ein Hauskauf, Umzug oder Neubeginn an? Dafür gibt es eine <a href="/kartenlegen-hauskauf-umzug/">eigene Seite zu Hauskauf, Umzug &amp; finanziellen Entscheidungen</a>.</p>
""",
    },
    # --- Thema: Hauskauf, Umzug & finanzielle Entscheidungen ---
    {
        "slug": "kartenlegen-hauskauf-umzug",
        "title": "Kartenlegen bei Hauskauf, Umzug & finanziellen Entscheidungen | Thomas Lude",
        "desc": "Kaufen, mieten, umziehen oder neu anfangen? Kartenlegen mit Thomas Lude gibt einen intuitiven Blick auf die persönliche Seite der Entscheidung – ohne Anlage- oder Rechtsberatung.",
        "eyebrow": "Neuer Lebensabschnitt",
        "h1": "Kartenlegen bei Hauskauf, Umzug &amp; finanziellen Entscheidungen",
        "lead": "Kaufen oder mieten? Bleiben oder umziehen? Neu anfangen? Bei Entscheidungen mit langer Tragweite hilft manchmal ein Blick auf die persönliche Seite dahinter.",
        "image": "kartenlegen-hauskauf-umzug",
        "alt": "Schreibtisch mit Kartenset, Kompass, Bauplan und Hausschlüssel vor einem Wegweiser mit den Richtungen Kaufen, Vermieten, Umzug und Neu beginnen, im Hintergrund ein Haus am Bodensee bei Sonnenuntergang",
        "prose": """
<h2>Wenn eine Entscheidung über den Alltag hinausgeht</h2>
<p>Hauskauf, Umzug, ein Ortswechsel oder eine größere finanzielle Weichenstellung – solche Entscheidungen wirken nüchtern, sind es aber selten. Sie berühren Sicherheit, Familie und die Frage, wo und wie man leben möchte. Ein Blick, der nicht nur auf Zahlen schaut, kann helfen, die eigene Haltung dazu klarer zu sehen.</p>
<h2>Was Kartenlegen bei diesen Fragen leisten kann</h2>
<ul class="tick-list">
  <li>Kaufen, mieten oder abwarten – die eigene Haltung dazu sortieren</li>
  <li>Umzug oder Ortswechsel: was wirklich dahintersteckt</li>
  <li>Neubeginn nach Trennung, Jobwechsel oder Lebensveränderung</li>
  <li>Finanzielle Entscheidungen mit Bauchgefühl statt nur mit Kopf betrachten</li>
</ul>
<h2>Kaufen, mieten oder abwarten</h2>
<p>Die Frage nach Eigentum oder Miete ist oft mehr als eine Rechenaufgabe – sie hängt mit Sicherheit, Bindung und dem Bild vom eigenen Leben zusammen. Ich schaue mit dir auf die persönliche Seite dieser Entscheidung, nicht auf Marktwert oder Finanzierung.</p>
<h2>Umzug &amp; Neubeginn</h2>
<p>Ein Ortswechsel bringt oft mehr durcheinander als gedacht – alte Bindungen, neue Erwartungen, die Frage, ob der Schritt wirklich stimmt. Ein Kartenlegen kann helfen, diese Gedanken zu ordnen, bevor die Entscheidung fällt.</p>
<h2>So läuft eine Beratung ab</h2>
<p>Du erzählst, wo du stehst und was dich beschäftigt. Thomas legt die Karten und bespricht mit dir, welche Tendenzen und Möglichkeiten sich zeigen – persönlich in Friedrichshafen oder am Telefon.</p>
<h2>Warum Thomas Lude</h2>
<p>Thomas ist Kartenleger, kein Finanz-, Rechts- oder Immobilienberater. Er gibt keine Kauf-, Verkaufs- oder Anlageempfehlung und keine Erfolgsgarantie. Was er kann: dir helfen, deine Situation klarer zu sehen – damit du deine Entscheidung eigenverantwortlich triffst, gegebenenfalls nach Rücksprache mit entsprechend qualifizierten Fachleuten (Makler, Notar, Finanzberatung).</p>
""",
        "faq": [
            ("Kann Kartenlegen bei der Entscheidung für oder gegen einen Hauskauf helfen?",
             "Kartenlegen ersetzt keine Finanzierungs- oder Marktanalyse. Es kann aber helfen, die eigene Haltung zur Entscheidung klarer zu sehen – ob Kaufen, Mieten oder Warten sich für dich gerade richtig anfühlt."),
            ("Gibt Thomas eine Empfehlung zu Kauf, Verkauf oder Geldanlage?",
             "Nein. Thomas ist Kartenleger, keine Finanz-, Rechts- oder Immobilienberatung. Für die fachliche Seite einer Entscheidung sind entsprechend qualifizierte Fachleute die richtige Anlaufstelle."),
            ("Hilft eine Kartenlegung auch bei einem Umzug oder Neubeginn?",
             "Ja. Viele kommen genau in solchen Übergangsphasen – wenn vieles gleichzeitig in Bewegung ist und der eigene Kopf etwas Ordnung gebrauchen kann."),
        ],
        "wa": "Hallo Thomas, ich interessiere mich für eine Beratung zu einer wichtigen Entscheidung (Hauskauf/Umzug).",
        "cta_title": "Bevor die Entscheidung fällt.",
        "cta_text": "Schreib kurz, worum es geht – Thomas meldet sich persönlich.",
    },
    # --- Thema: Familie ---
    {
        "slug": "kartenlegen-familie",
        "title": "Kartenlegen bei Familienfragen | Thomas Lude",
        "desc": "Konflikte in der Familie, Sorgen um Kinder oder Eltern? Kartenlegen mit Thomas Lude am Bodensee gibt Raum für das, was beschäftigt.",
        "eyebrow": "Die nächsten Menschen",
        "h1": "Kartenlegen bei Fragen rund um die Familie",
        "lead": "Familie ist selten einfach. Wenn Konflikte, Sorgen oder Veränderungen dich beschäftigen, hilft manchmal ein ruhiger Blick von außen.",
        "image": "thomas-lude-kartenlegen-liebe-beziehung",
        "alt": "Thomas Lude in einer vertrauensvollen Kartenberatung bei warmem Licht",
        "prose": """
<h2>Familie: nah, wichtig – und manchmal schwer</h2>
<p>Keine Beziehungen berühren uns so sehr wie die in der Familie. Konflikte mit den Eltern, Sorgen um die Kinder, Geschwister, mit denen man sich entfremdet hat, oder Veränderungen, die das ganze Gefüge bewegen – das alles kann einen nachts wachhalten.</p>
<h2>Was Kartenlegen bei Familienthemen leisten kann</h2>
<p>Die Karten können helfen, die eigene Position im Gefüge zu erkennen: Was liegt in meiner Hand, was nicht? Wo bin ich zu nah dran, um klar zu sehen? Typische Themen sind:</p>
<ul class="tick-list">
  <li>Konflikte und wiederkehrende Muster in der Familie</li>
  <li>Sorgen um Kinder, Eltern oder Geschwister</li>
  <li>Veränderungen wie Umzug, Trennung oder Neuanfang im Familienkreis</li>
  <li>Die eigene Rolle finden – zwischen Fürsorge und Abgrenzung</li>
</ul>
<h2>So läuft eine Beratung ab</h2>
<p>Du erzählst so viel, wie du möchtest. Thomas hört zu, legt die Karten und bespricht mit dir, was sich zeigt – ruhig, wertfrei und diskret. In Friedrichshafen oder am Telefon.</p>
<h2>Warum Thomas Lude</h2>
<p>Thomas urteilt nicht und nimmt niemandem eine Entscheidung ab. Er schafft Raum für das, was dich beschäftigt – und hilft dir, die Dinge wieder zu sortieren.</p>
""",
        "wa": "Hallo Thomas, ich habe eine Frage zu einem Familienthema.",
    },
    # --- Thema: Orientierung & Selbstfindung ---
    {
        "slug": "kartenlegen-orientierung-selbstfindung",
        "title": "Kartenlegen für Orientierung & Selbstfindung | Thomas Lude",
        "desc": "Du suchst deine Richtung? Kartenlegen mit Thomas Lude am Bodensee hilft bei Fragen zu Sinn, Orientierung und dem eigenen Weg.",
        "eyebrow": "Der eigene Weg",
        "h1": "Kartenlegen für Orientierung &amp; Selbstfindung",
        "lead": "Manchmal ist keine konkrete Frage da – nur das Gefühl, dass sich etwas ändern muss. Auch damit kannst du kommen.",
        "image": "thomas-lude-kartenlegen-beratung-am-tisch",
        "alt": "Thomas Lude am Kartentisch in ruhiger Atmosphäre mit Kerze und Salzsteinlampe",
        "prose": """
<h2>Wenn die Richtung fehlt</h2>
<p>Nicht jede Beratung beginnt mit einer klaren Frage. Manchmal ist da nur ein Gefühl: Es läuft, aber es passt nicht mehr. Du funktionierst, aber du lebst nicht wirklich. Solche Phasen sind kein Zeichen von Schwäche – oft sind sie der Anfang von etwas Neuem.</p>
<h2>Was Kartenlegen bei der Selbstfindung leisten kann</h2>
<ul class="tick-list">
  <li>Benennen, was sich gerade in dir bewegt</li>
  <li>Erkennen, welche Themen wirklich deine sind</li>
  <li>Klarheit über den nächsten kleinen Schritt statt des großen Plans</li>
  <li>Ein ehrlicher Spiegel – ohne Ratschläge, die nicht zu dir passen</li>
</ul>
<h2>So läuft eine Beratung ab</h2>
<p>Du musst nichts vorbereiten und nichts richtig formulieren. Ihr setzt euch an den Tisch (oder sprecht am Telefon), Thomas legt die Karten, und das Gespräch findet seinen Weg zu dem, was gerade wichtig ist.</p>
<h2>Warum Thomas Lude</h2>
<p>Thomas ist bodenständig statt abgehoben. Keine großen Versprechungen, keine spirituelle Show – nur ein erfahrener Blick, echtes Zuhören und die Ehrlichkeit, auch Dinge auszusprechen, die man nicht gern hört.</p>
""",
        "wa": "Hallo Thomas, ich suche gerade nach Orientierung und würde gern eine Beratung vereinbaren.",
    },
    # --- Telefonische Beratung ---
    {
        "slug": "kartenlegen-telefonisch",
        "title": "Kartenlegen am Telefon mit Thomas Lude | Thomas Lude",
        "desc": "Kartenberatung am Telefon: diskret, persönlich und von überall erreichbar. Telefontermin bei Thomas Lude am Bodensee vereinbaren.",
        "eyebrow": "Von überall erreichbar",
        "h1": "Kartenlegen am Telefon mit Thomas Lude",
        "lead": "Du wohnst nicht am Bodensee oder möchtest nicht persönlich kommen? Eine Beratung am Telefon ist genauso persönlich – und genauso diskret.",
        "image": "thomas-lude-kartenlegen-beratung-am-tisch",
        "alt": "Thomas Lude am Kartentisch – so arbeitet er auch während einer telefonischen Beratung",
        "prose": """
<h2>So läuft eine telefonische Beratung ab</h2>
<ol>
  <li><strong>Anfragen</strong> – per WhatsApp, Anruf oder Formular. Sag kurz, worum es geht.</li>
  <li><strong>Termin vereinbaren</strong> – ihr findet eine ruhige Zeit, die passt.</li>
  <li><strong>Beratung am Telefon</strong> – du erzählst dein Thema, Thomas legt die Karten und bespricht mit dir, was sich zeigt.</li>
  <li><strong>Danach</strong> – du entscheidest, was du mitnimmst. Keine Verpflichtung, kein Abo.</li>
</ol>
<h2>Für wen ist die Telefonberatung geeignet?</h2>
<ul class="tick-list">
  <li>Für alle, die nicht am Bodensee wohnen</li>
  <li>Für alle, die lieber von zuhause aus sprechen</li>
  <li>Für Themen, die nicht bis zum nächsten freien Termin vor Ort warten sollen</li>
  <li>Für alle, die es besonders diskret halten möchten</li>
</ul>
<h2>Dauer, Preis &amp; Diskretion</h2>
<p>30 Minuten 79 €, 60 Minuten 149 €, 90 Minuten 219 €, 120 Minuten 289 € – gleicher Preis wie bei einer persönlichen Beratung. Zahlungsmöglichkeiten bespricht ihr bei der Terminvereinbarung. Was du am Telefon besprichst, bleibt vertraulich.</p>
""",
        "faq": [
            ("Funktioniert Kartenlegen am Telefon wirklich?",
             "Ja. Entscheidend ist das Gespräch und deine Frage – nicht der Ort. Viele Beratungen finden seit jeher am Telefon statt."),
            ("Welche Fragen kann ich am Telefon stellen?",
             "Die gleichen wie persönlich: Liebe, Entscheidungen, Beruf, Familie, Veränderungen – alles, was dich beschäftigt."),
            ("Wie bezahle ich eine Telefonberatung?",
             "Die Zahlungsmöglichkeiten besprecht ihr bei der Terminvereinbarung. Thomas informiert dich vorab transparent."),
        ],
        "wa": "Hallo Thomas, ich interessiere mich für eine telefonische Beratung.",
        "cta_title": "Ein Anruf genügt.",
        "cta_text": "Vereinbare deinen Telefontermin mit Thomas.",
    },
    # --- Region: München ---
    {
        "slug": "kartenlegen-muenchen",
        "title": "Kartenlegen für München | Telefonische Beratung mit Thomas Lude",
        "desc": "Kartenlegen für Menschen aus München: telefonische Beratung mit Thomas Lude vom Bodensee, oder persönlich nach Vereinbarung in Friedrichshafen.",
        "eyebrow": "Auch aus München erreichbar",
        "h1": "Kartenlegen für Menschen aus München",
        "lead": "Du wohnst in München und suchst eine ehrliche Kartenberatung? Thomas berät dich telefonisch – oder persönlich, wenn du den Weg an den Bodensee auf dich nimmst.",
        "image": "thomas-lude-kartenlegen-beratung-am-tisch",
        "alt": "Thomas Lude bei einer Kartenberatung am Tisch – auch für Kundinnen und Kunden aus München per Telefon erreichbar",
        "prose": """
<h2>Kartenlegen, wenn München nicht gleich um die Ecke ist</h2>
<p>München und Friedrichshafen trennen rund zwei Stunden Fahrzeit. Für ein einzelnes Gespräch ist das oft schlicht unpraktisch – deshalb nutzen die meisten Kundinnen und Kunden aus München die telefonische Beratung. Am Telefon zählt das Gespräch, nicht der Ort.</p>
<h2>Persönlich oder telefonisch – deine Entscheidung</h2>
<p>Manche nehmen die Fahrt trotzdem auf sich, wenn sie Thomas lieber persönlich am Tisch gegenübersitzen möchten. Beides ist möglich, beides ist gleichwertig – was am besten passt, hängt von dir und deinem Thema ab.</p>
<ul class="tick-list">
  <li>Telefonische Beratung – ohne Anfahrt, genauso persönlich</li>
  <li>Persönlicher Termin in Friedrichshafen – nach Vereinbarung</li>
  <li>Themen: Liebe, Entscheidungen, Beruf, Familie, Orientierung</li>
</ul>
<h2>So läuft es ab</h2>
<p>Du meldest dich per WhatsApp, Anruf oder Formular, ihr vereinbart einen Termin, und Thomas nimmt sich Zeit für dein Thema – am Telefon oder am Kartentisch.</p>
<h2>Warum Thomas Lude</h2>
<p>Thomas legt die Karten in dritter Generation, bodenständig und ohne große Versprechen. Was du bekommst, ist ein ehrlicher, aufmerksamer Blick auf deine Situation – kein Orakel, keine Garantie.</p>
""",
        "faq": [
            ("Muss ich für eine Beratung extra nach Friedrichshafen kommen?",
             "Nein. Die meisten Beratungen mit Kundinnen und Kunden aus München finden telefonisch statt. Ein persönlicher Termin ist möglich, aber keine Voraussetzung."),
            ("Ist eine telefonische Beratung genauso gut wie persönlich?",
             "Ja. Entscheidend ist das Gespräch und deine Bereitschaft, hinzuschauen – nicht der Ort, an dem ihr sprecht."),
        ],
        "wa": "Hallo Thomas, ich rufe aus München und interessiere mich für eine Beratung.",
    },
    # --- Region: Augsburg ---
    {
        "slug": "kartenlegen-augsburg",
        "title": "Kartenlegen für Augsburg | Telefonische Beratung mit Thomas Lude",
        "desc": "Kartenlegen für Menschen aus Augsburg: telefonisch mit Thomas Lude vom Bodensee, oder persönlich nach Vereinbarung in Friedrichshafen.",
        "eyebrow": "Auch aus Augsburg erreichbar",
        "h1": "Kartenlegen für Menschen aus Augsburg",
        "lead": "Von Augsburg zum Bodensee ist es ein Stück Weg – deshalb bietet Thomas dir die telefonische Beratung als unkomplizierte Alternative zur persönlichen Anreise.",
        "image": "thomas-lude-ueber-thomas-kartenlegen",
        "alt": "Thomas Lude an seinem Kartentisch – Kartenlegen auch telefonisch erreichbar für Kundinnen und Kunden aus Augsburg",
        "prose": """
<h2>Kartenlegen aus der Ferne – ohne etwas zu verlieren</h2>
<p>Eine Autofahrt von Augsburg an den Bodensee dauert schnell zwei Stunden. Das muss kein Hindernis sein: Am Telefon entsteht das gleiche offene Gespräch wie am Kartentisch – nur ohne die Fahrtzeit.</p>
<h2>Was für Kundinnen und Kunden aus Augsburg gilt</h2>
<ul class="tick-list">
  <li>Telefonische Beratung – flexibel, diskret, ohne Anfahrt</li>
  <li>Persönlicher Termin in Friedrichshafen – wenn du den Weg lieber machst</li>
  <li>Gleiche Themen, gleiche Aufmerksamkeit, gleicher Preis</li>
</ul>
<h2>So läuft es ab</h2>
<p>Kurze Anfrage per WhatsApp oder Telefon, ein Termin, der passt, und ein Gespräch, in dem Thomas sich ganz auf dein Thema einlässt.</p>
<h2>Warum Thomas Lude</h2>
<p>Kein Kristallkugel-Theater, keine leeren Versprechen. Nur ein erfahrener, ehrlicher Blick – ob am Tisch in Friedrichshafen oder am Telefon nach Augsburg.</p>
""",
        "faq": [
            ("Lohnt sich eine telefonische Beratung wirklich?",
             "Ja – für die meisten Themen ist der Ort zweitrangig. Wichtig ist, dass du in Ruhe sprechen kannst."),
            ("Kann ich auch kurzfristig einen Termin bekommen?",
             "Frag einfach per WhatsApp an, wann es bei dir passt – Thomas meldet sich mit einem Terminvorschlag."),
        ],
        "wa": "Hallo Thomas, ich rufe aus Augsburg und interessiere mich für eine Beratung.",
    },
    # --- Region: Ulm ---
    {
        "slug": "kartenlegen-ulm",
        "title": "Kartenlegen für Ulm | Persönlich oder telefonisch mit Thomas Lude",
        "desc": "Kartenlegen für Menschen aus Ulm: persönlich in Friedrichshafen oder telefonisch mit Thomas Lude vom Bodensee.",
        "eyebrow": "Auch aus Ulm erreichbar",
        "h1": "Kartenlegen für Menschen aus Ulm",
        "lead": "Ulm liegt näher am Bodensee, als man denkt – eine persönliche Beratung in Friedrichshafen ist gut machbar. Wer es lieber unkompliziert mag, wählt die telefonische Beratung.",
        "image": "thomas-lude-kartenlegen-beratung-am-tisch",
        "alt": "Thomas Lude im Gespräch bei einer Kartenberatung – gut erreichbar auch für Kundinnen und Kunden aus Ulm",
        "prose": """
<h2>Von Ulm an den Bodensee – näher als gedacht</h2>
<p>Die Strecke von Ulm nach Friedrichshafen ist gut zu fahren – für viele aus der Region ein machbarer Weg für eine persönliche Beratung am Kartentisch. Wer es dennoch unkompliziert halten möchte, ist am Telefon genauso gut aufgehoben.</p>
<h2>Zwei Wege, ein Gespräch</h2>
<ul class="tick-list">
  <li>Persönlich in Friedrichshafen – direkt am Kartentisch</li>
  <li>Telefonisch – wenn dir das lieber oder einfacher ist</li>
  <li>Themen: Liebe, Beruf, Familie, Entscheidungen, Orientierung</li>
</ul>
<h2>So läuft es ab</h2>
<p>Du meldest dich, ihr vereinbart einen Termin – persönlich oder am Telefon –, und Thomas nimmt sich Zeit für das, was dich beschäftigt.</p>
<h2>Warum Thomas Lude</h2>
<p>Bodenständig, direkt und ohne große Versprechen. Thomas legt die Karten in dritter Generation und sagt dir ehrlich, was er sieht – nicht das, was du hören willst.</p>
""",
        "faq": [
            ("Wie weit ist es von Ulm nach Friedrichshafen?",
             "Rund eine Stunde mit dem Auto – für viele gut machbar, wenn du lieber persönlich kommen möchtest."),
            ("Kann ich mich vorher unverbindlich per WhatsApp melden?",
             "Ja, das ist sogar der schnellste Weg, um einen passenden Termin zu finden."),
        ],
        "wa": "Hallo Thomas, ich komme aus Ulm und interessiere mich für eine Beratung.",
    },
    # --- Region: Memmingen ---
    {
        "slug": "kartenlegen-memmingen",
        "title": "Kartenlegen für Memmingen | Thomas Lude vom Bodensee",
        "desc": "Kartenlegen für Menschen aus Memmingen und dem Allgäu: persönlich in Friedrichshafen oder telefonisch mit Thomas Lude.",
        "eyebrow": "Auch aus Memmingen erreichbar",
        "h1": "Kartenlegen für Menschen aus Memmingen",
        "lead": "Von Memmingen aus ist der Bodensee gut erreichbar. Ob persönlich in Friedrichshafen oder telefonisch – Thomas nimmt sich Zeit für dein Thema.",
        "image": "thomas-lude-ueber-thomas-kartenlegen",
        "alt": "Thomas Lude bei einer ruhigen Kartenberatung – auch für Kundinnen und Kunden aus Memmingen und dem Allgäu",
        "prose": """
<h2>Kartenlegen für Memmingen und das Allgäu</h2>
<p>Memmingen und das Allgäu liegen nah genug am Bodensee, dass eine persönliche Beratung in Friedrichshafen für viele gut machbar ist. Genauso gut funktioniert das Gespräch am Telefon, wenn dir das lieber ist.</p>
<h2>So erreichst du Thomas aus Memmingen</h2>
<ul class="tick-list">
  <li>Persönlich in Friedrichshafen – gut zu erreichen</li>
  <li>Telefonisch – ohne Anfahrt, genauso persönlich</li>
  <li>Auch als Kartenabend für Gruppen aus dem Allgäu, nach Absprache</li>
</ul>
<h2>So läuft es ab</h2>
<p>Kurze Anfrage, ein passender Termin, ein ehrliches Gespräch – am Tisch oder am Telefon.</p>
<h2>Warum Thomas Lude</h2>
<p>Ruhig, direkt und ohne Show. Thomas hört zu, legt die Karten und sagt dir, was er sieht – ehrlich, auch wenn es nicht das ist, was du erwartet hast.</p>
""",
        "faq": [
            ("Bietet Thomas auch Kartenabende im Allgäu an?",
             "Ja, für Gruppen ist das nach Absprache möglich – schreib einfach kurz, was ihr vorhabt."),
            ("Was, wenn mir eine Anreise zu aufwendig ist?",
             "Dann ist die telefonische Beratung die einfachste Lösung – genauso persönlich, ohne Fahrtzeit."),
        ],
        "wa": "Hallo Thomas, ich komme aus Memmingen und interessiere mich für eine Beratung.",
    },
    # --- Region: Zürich / Schweiz ---
    {
        "slug": "kartenlegen-zuerich",
        "title": "Kartenlegen für Zürich & die Schweiz | Thomas Lude",
        "desc": "Kartenlegen für Kundinnen und Kunden aus Zürich und der Schweiz: telefonisch mit Thomas Lude vom Bodensee, oder persönlich in Friedrichshafen.",
        "eyebrow": "Auch aus der Schweiz erreichbar",
        "h1": "Kartenlegen für Zürich und die Schweiz",
        "lead": "Der Bodensee liegt direkt an der Grenze zur Schweiz – einige Kundinnen und Kunden aus Zürich und der Ostschweiz nehmen den Weg nach Friedrichshafen bewusst auf sich. Genauso gut erreichst du Thomas telefonisch.",
        "image": "thomas-lude-kartenleger-friedrichshafen-bodensee",
        "alt": "Thomas Lude bei einer persönlichen Kartenberatung – auch Kundinnen und Kunden aus Zürich und der Schweiz kommen dafür an den Bodensee",
        "prose": """
<h2>Nur eine Grenze dazwischen</h2>
<p>Von Zürich an den Bodensee ist es nicht weit – einige Kundinnen und Kunden aus der Schweiz kommen bewusst nach Friedrichshafen, um Thomas persönlich gegenüberzusitzen. Andere entscheiden sich für die telefonische Beratung, die genauso persönlich und diskret abläuft.</p>
<h2>Zwei Wege zu Thomas</h2>
<ul class="tick-list">
  <li>Persönlich in Friedrichshafen – nur eine kurze Fahrt über die Grenze</li>
  <li>Telefonisch – ohne Anreise, aus der ganzen Schweiz erreichbar</li>
  <li>Zahlung und Ablauf werden bei der Anfrage unkompliziert geklärt</li>
</ul>
<h2>So läuft es ab</h2>
<p>Du meldest dich per WhatsApp oder Telefon, ihr vereinbart einen Termin, und Thomas nimmt sich Zeit für dein Anliegen – ganz gleich, ob du anreist oder anrufst.</p>
<h2>Warum Thomas Lude</h2>
<p>Bodenständig statt abgehoben, ehrlich statt beschönigend. Thomas verspricht keine Wunder – er hilft dir, deine Situation klarer zu sehen.</p>
""",
        "faq": [
            ("Kommen wirklich Kundinnen und Kunden aus der Schweiz zu Thomas?",
             "Ja, das kommt vor – der Bodensee liegt direkt an der Grenze, und für manche ist der persönliche Termin die Reise wert."),
            ("Wie bezahle ich als Kundin oder Kunde aus der Schweiz?",
             "Das besprecht ihr unkompliziert bei der Terminanfrage – Details dazu erfährst du direkt von Thomas."),
        ],
        "wa": "Hallo Thomas, ich komme aus Zürich und interessiere mich für eine Beratung.",
    },
    # --- Event: Hochzeit ---
    {
        "slug": "kartenlegen-hochzeit",
        "title": "Kartenmomente für eure Hochzeit | Thomas Lude",
        "desc": "Ein besonderer Programmpunkt für eure Hochzeit: Thomas Lude bringt einen stilvollen Kartentisch mit, an dem Gäste sich für einen persönlichen Moment Zeit nehmen können.",
        "eyebrow": "Ein besonderer Programmpunkt",
        "h1": "Kartenmomente für eure Hochzeit",
        "lead": "Zwischen Musik, Gesprächen und besonderen Begegnungen entsteht ein ruhiger Platz für persönliche Momente – mit einem eigenen, liebevoll gestalteten Kartentisch.",
        "image": "thomas-lude-kartenlegen-beratung-am-tisch",
        "alt": "Thomas Lude an einem stilvoll vorbereiteten Kartentisch bei einer Hochzeitsfeier",
        "prose": """
<h2>Ein ruhiger Moment mitten im Fest</h2>
<p>Thomas begleitet eure Hochzeit mit einem eigenen Kartentisch, an dem sich Gäste – ganz freiwillig und in ihrem eigenen Tempo – für einen kurzen, persönlichen Moment Zeit nehmen können. Kein Programmpunkt mit Ansage, sondern ein ruhiger Gegenpol zum Trubel, der von selbst Gespräche auslöst.</p>
<h2>Was das für eure Gäste bedeutet</h2>
<ul class="tick-list">
  <li>Kurze, persönliche Kartenimpulse – diskret und mit Feingefühl</li>
  <li>Freiwillig: wer möchte, setzt sich; niemand wird angesprochen</li>
  <li>Ein Gesprächsthema, das noch lange nachwirkt</li>
</ul>
<h2>Optional: ein Moment für das Brautpaar</h2>
<p>Auf Wunsch nimmt sich Thomas vor oder während der Feier auch einen ruhigen, privaten Moment nur für euch beide – ein symbolischer Blick auf das, was vor euch liegt.</p>
<h2>Preis</h2>
<ul class="tick-list">
  <li><strong>Ab 590 €</strong> – bis ca. 3 Stunden Anwesenheit</li>
  <li><strong>Ab 690 €</strong> – bis ca. 4 Stunden Anwesenheit</li>
  <li>Verlängerung je angefangene Stunde: 150 €</li>
  <li>Anfahrt im Bodensee-Radius inklusive, darüber hinaus nach Entfernung</li>
</ul>
<h2>So läuft die Planung ab</h2>
<p>Schreib Thomas kurz, wann und wo eure Feier stattfindet und wie viele Gäste ihr erwartet. Individuelles Setup, mehr Zeit oder größere Gruppen besprecht ihr gemeinsam.</p>
<h2>Warum Thomas Lude</h2>
<p>Kein lautes Entertainment-Programm, sondern ein stilvoller, achtsamer Akzent, der zu eurem Fest passt statt es zu überlagern.</p>
""",
        "faq": [
            ("Müssen sich alle Gäste beteiligen?",
             "Nein. Der Kartentisch ist ein freiwilliges Angebot – wer nicht möchte, geht einfach weiter feiern."),
            ("Wie viel Zeit braucht Thomas vor Ort?",
             "Das hängt von Gästezahl und Ablauf eurer Feier ab und wird gemeinsam geplant."),
        ],
        "wa": "Hallo Thomas, wir planen unsere Hochzeit und interessieren uns für Kartenmomente für unsere Gäste.",
        "cta_title": "Euer Hochzeitstag, ein besonderer Moment.",
        "cta_text": "Schreib kurz Datum, Ort und ungefähre Gästezahl – Thomas meldet sich mit einem Vorschlag.",
    },
    # --- Event: Firmenfeier ---
    {
        "slug": "kartenlegen-firmenfeier",
        "title": "Kartenmomente für Firmenfeiern & Teamevents | Thomas Lude",
        "desc": "Ein außergewöhnlicher Gesprächsanlass für Betriebsfeiern, Weihnachtsfeiern und Teamevents: persönliche Kartenimpulse mit Thomas Lude.",
        "eyebrow": "Ein besonderer Akzent für euer Event",
        "h1": "Kartenmomente für Firmenfeiern &amp; Teamevents",
        "lead": "Ein ruhiger, stilvoller Gegenpol zum Eventtrubel: Thomas bringt einen eigenen Kartentisch mit, an dem Gäste sich auf Wunsch einen kurzen, persönlichen Impuls holen können.",
        "image": "thomas-lude-ueber-thomas-kartenlegen",
        "alt": "Thomas Lude an seinem Kartentisch – ein besonderer Programmpunkt für Firmenfeiern und Teamevents",
        "prose": """
<h2>Ein außergewöhnlicher Programmpunkt</h2>
<p>Bei Weihnachtsfeiern, Teamtagen oder Kundenveranstaltungen sorgt der Kartentisch von Thomas für echte Gespräche abseits vom Alltag. Kein lautes Entertainment, sondern ein ruhiger, persönlicher Moment, der im Gedächtnis bleibt.</p>
<h2>Was Gäste erwarten können</h2>
<ul class="tick-list">
  <li>Kurze, persönliche Impulse – diskret und wertschätzend</li>
  <li>Ein Gesprächsanlass, der Menschen zusammenbringt</li>
  <li>Freiwillige Teilnahme, kein Druck</li>
</ul>
<h2>Preis</h2>
<ul class="tick-list">
  <li><strong>Ab 590 €</strong> – bis ca. 3 Stunden Anwesenheit</li>
  <li><strong>Ab 690 €</strong> – bis ca. 4 Stunden Anwesenheit</li>
  <li>Verlängerung je angefangene Stunde: 150 €</li>
  <li>Anfahrt im Bodensee-Radius inklusive, darüber hinaus nach Entfernung</li>
</ul>
<h2>So läuft die Planung ab</h2>
<p>Schreib Thomas kurz die Rahmendaten eurer Veranstaltung – Ort, Datum, ungefähre Gästezahl. Individuelles Setup oder mehr Zeit besprecht ihr gemeinsam.</p>
<h2>Warum Thomas Lude</h2>
<p>Bodenständig statt abgehoben, diskret statt aufdringlich – ein Programmpunkt, der zu einem professionellen Rahmen passt.</p>
""",
        "faq": [
            ("Passt das auch zu einem eher förmlichen Firmenevent?",
             "Ja. Thomas passt Auftreten und Tempo an den Rahmen der Veranstaltung an – zurückhaltend und professionell."),
            ("Wie viele Gäste kann Thomas an einem Abend erreichen?",
             "Das hängt von der Eventdauer ab und wird bei der Anfrage gemeinsam eingeschätzt."),
        ],
        "wa": "Hallo Thomas, wir planen eine Firmenfeier und interessieren uns für Kartenmomente für unsere Gäste.",
        "cta_title": "Euer Firmenevent, ein besonderer Akzent.",
        "cta_text": "Schreib kurz Rahmendaten eurer Veranstaltung – Thomas meldet sich mit einem Vorschlag.",
    },
    # --- Premium: Hausbesuch & Raumklärung ---
    {
        "slug": "hausbesuch-raumklaerung",
        "title": "Hausbesuch & Raumklärung am Bodensee | Thomas Lude",
        "desc": "Thomas kommt zu dir nach Hause: Kartenlegung mit Blick auf die Atmosphäre deines Zuhauses, oder energetische Raumklärung. Persönlich im Bodenseeraum.",
        "eyebrow": "Ein besonderes Format",
        "h1": "Hausbesuch &amp; Raumklärung",
        "lead": "Manche Dinge spürt man erst, wenn man den Raum betritt. Thomas kommt zu dir nach Hause – für eine Kartenlegung mit Blick auf die Atmosphäre deines Zuhauses, oder für eine energetische Raumklärung.",
        "image": "thomas-lude-ueber-thomas-kartenlegen",
        "alt": "Thomas Lude bei einem persönlichen Hausbesuch am Bodensee",
        "prose": """
<h2>Thomas bei dir zu Hause</h2>
<p>Neben Beratungen in Friedrichshafen und am Telefon bietet Thomas persönliche Hausbesuche im Bodenseeraum an. Dabei findet die Kartenlegung dort statt, wo viele der Fragen tatsächlich entstehen: in deinem eigenen Zuhause. Neben den Karten bezieht Thomas dabei auch seine Wahrnehmung der Atmosphäre vor Ort in die Beratung ein.</p>
<p>Gerade bei Fragen zu Partnerschaft, Familie, Veränderungen oder wiederkehrenden Belastungen kann daraus eine andere Form der Beratung entstehen. Bei Hausbesuchen entstehen bei Thomas häufig intuitive Eindrücke zu Themen und Spannungen, die mit den Bewohnern und ihrer aktuellen Lebenssituation verbunden sein können.</p>
<h2>Energetische Raumklärung</h2>
<p>Manche Menschen erleben bestimmte Räume als unruhig, schwer oder belastend, ohne genau benennen zu können, warum. Thomas nimmt sich Zeit für das Haus, seine Räume und die Menschen, die darin leben – ruhig, respektvoll und ohne Dramatisierung. Es geht nicht darum, etwas Schlimmes zu behaupten, sondern darum, wieder mehr Ruhe und ein stimmiges Gefühl im eigenen Zuhause zu finden.</p>
<h2>Preis</h2>
<ul class="tick-list">
  <li><strong>Ab 249 €</strong> – Hausbesuch, ca. 90 Minuten</li>
  <li><strong>Ab 349 €</strong> – Hausbesuch kombiniert mit energetischer Raumklärung</li>
  <li>Anfahrt im Bodensee-Radius inklusive, darüber hinaus nach Entfernung</li>
</ul>
<p>Genauer Umfang und Dauer hängen von Anliegen und Hausgröße ab und werden vorab am Telefon besprochen.</p>
<h2>So läuft es ab</h2>
<p>Schreib Thomas kurz, worum es geht und wo du wohnst. Ablauf, Dauer und genauer Preis werden vorab telefonisch besprochen.</p>
<div class="notice-box" style="margin-top:1.6rem;">
  <p><strong>Wichtiger Hinweis:</strong> Diese Begleitung ist eine persönliche, intuitive Beratung. Sie ersetzt keine rechtliche, steuerliche, finanzielle oder Immobilienberatung, keine bautechnische Prüfung der Bausubstanz und keine ärztliche oder psychotherapeutische Behandlung.</p>
</div>
""",
        "faq": [
            ("Muss das ganze Haus begehbar sein?",
             "Nein. Das besprecht ihr vorab – meist reicht es, die für dich wichtigen Räume zu zeigen."),
            ("Können mehrere Bewohner dabei sein?",
             "Ja, das ist möglich und wird individuell abgestimmt."),
        ],
        "wa": "Hallo Thomas, ich interessiere mich für einen Hausbesuch / eine Raumklärung.",
        "cta_title": "Dein Zuhause, ein persönlicher Blick.",
        "cta_text": "Schreib kurz, worum es geht und wo du wohnst – Thomas meldet sich mit einem Vorschlag.",
    },
]


# ----------------------------------------------------------------------------
# EVENTS-HUB
# ----------------------------------------------------------------------------
def events_body():
    return """
<header class="page-hero">
  <div class="container page-hero-split">
    <div>
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Events</span></nav>
      <p class="eyebrow">Kartenlegen für Gruppen</p>
      <h1>Kartenlegen für Events am Bodensee</h1>
      <p class="lead">Ein Programmpunkt, über den ihr später noch sprecht: Thomas kommt mit den Karten zu euch – zu JGA, Mädelsabend, Geburtstag und besonderen Anlässen.</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="/kontakt-termin/">Kartenabend anfragen</a>
      </div>
    </div>
    <div>%(hero)s</div>
  </div>
</header>

<section class="section">
  <div class="container">
    <div class="section-head">
      <h2>Für welchen Anlass?</h2>
      <p class="lead">Jedes Format hat seinen eigenen Charakter – Thomas passt den Abend an eure Gruppe an.</p>
    </div>
    <div class="card-grid two">
      <article class="card">
        <div class="card-body">
          <h3><a href="/kartenlegen-junggesellinnenabschied-bodensee/">Junggesellinnenabschied</a></h3>
          <p>Der besondere Programmpunkt vor der Hochzeit: Jede bekommt ihren Moment mit den Karten – mit viel Gelächter und ein paar Überraschungen.</p>
          <a class="link-more" href="/kartenlegen-junggesellinnenabschied-bodensee/">Mehr zum JGA</a>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3>Mädels- &amp; Freundinnenabend</h3>
          <p>Prosecco, gute Gespräche und Karten, die zum Reden bringen. Der Abend, den keine so schnell vergisst.</p>
          <a class="link-more" href="/kontakt-termin/">Mädelsabend anfragen</a>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3>Geburtstag</h3>
          <p>Der überraschende Programmpunkt für kleine Gruppen – persönlich, warm und mit garantiertem Gesprächsstoff.</p>
          <a class="link-more" href="/kontakt-termin/">Geburtstag anfragen</a>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3>Private Feier</h3>
          <p>Freundinnen-Wochenende am See, Familienfeier oder einfach ein guter Grund – Thomas bringt die Karten mit.</p>
          <a class="link-more" href="/kontakt-termin/">Feier anfragen</a>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3><a href="/kartenlegen-hochzeit/">Hochzeit</a></h3>
          <p>Ein stilvoller Kartentisch als besonderer Programmpunkt eurer Hochzeit – ruhig, persönlich, ganz freiwillig für eure Gäste.</p>
          <a class="link-more" href="/kartenlegen-hochzeit/">Mehr zur Hochzeit</a>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3><a href="/kartenlegen-firmenfeier/">Firmenfeier &amp; Teamevent</a></h3>
          <p>Ein außergewöhnlicher Gesprächsanlass für Weihnachtsfeier, Teamtag oder Kundenevent – diskret und professionell im Auftritt.</p>
          <a class="link-more" href="/kartenlegen-firmenfeier/">Mehr zur Firmenfeier</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container prose">
    <h2>So läuft ein Kartenabend ab</h2>
    <ol>
      <li><strong>Anfragen</strong> – Datum, Ort, ungefähre Personenzahl und Anlass.</li>
      <li><strong>Abstimmen</strong> – Thomas meldet sich und klärt mit euch Ablauf, Dauer und Rahmen.</li>
      <li><strong>Erleben</strong> – Thomas kommt zu euch. Jede Person bekommt ihren eigenen Moment mit den Karten.</li>
    </ol>
    <p>Thomas kommt in eure Ferienwohnung, ins Hotel, zu euch nach Hause oder in eine Location eurer Wahl. Bitte stimmt die Nutzung vorab mit eurer Unterkunft oder Location ab.</p>
    <p><strong>Ab 449 €</strong> für bis zu 6 Personen (ca. 2,5–3 Stunden), jede weitere Person 59 €. Anfahrt im Bodensee-Radius inklusive, darüber hinaus nach Vereinbarung. Genauer Ablauf, Zeitbedarf und Einsatzgebiet werden bei der Anfrage geklärt.</p>
  </div>
</section>
%(cta)s
""" % {
        "hero": img("thomas-lude-kartenlegen-jga-bodensee",
                    "Kartenabend mit Thomas Lude bei einem Junggesellinnenabschied am Bodensee",
                    sizes="(max-width: 920px) 100vw, 45vw", loading="eager", fetchpriority="high"),
        "cta": cta_band("Euer Event am Bodensee?",
                        "Schreib kurz Anlass, Datum und ungefähre Gruppengröße – Thomas meldet sich mit einem Vorschlag.",
                        "Hallo Thomas, wir planen ein Event und möchten einen Kartenabend anfragen."),
    }

# ----------------------------------------------------------------------------
# JGA-LANDINGPAGE
# ----------------------------------------------------------------------------
def jga_body():
    return """
<header class="page-hero">
  <div class="container page-hero-split">
    <div>
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>JGA am Bodensee</span></nav>
      <p class="eyebrow">Der besondere Programmpunkt</p>
      <h1>Kartenlegen für euren Junggesellinnenabschied am Bodensee</h1>
      <p class="lead"><strong>Ihr habt den Prosecco. Thomas bringt die Karten.</strong> Ein Kartenabend als JGA-Programmpunkt – persönlich, warm und garantiert in Erinnerung.</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="#anfrage">JGA mit Thomas anfragen</a>
        <a class="btn btn-outline-dark" href="%(wa)s?text=%(wamsg)s" target="_blank" rel="noopener">%(waicon)s WhatsApp</a>
      </div>
    </div>
    <div>%(hero)s</div>
  </div>
</header>

<section class="section">
  <div class="container prose">
    <h2>Warum Kartenlegen auf dem JGA funktioniert</h2>
    <p>Ein Junggesellinnenabschied soll besonders sein – nicht das Gleiche wie immer. Ein Kartenabend mit Thomas ist genau das: ruhig genug für echte Gespräche, spannend genug für Gänsehaut-Momente, und persönlich, weil jede Teilnehmerin ihren eigenen Moment mit den Karten bekommt.</p>
    <h2>So läuft euer Kartenabend ab</h2>
    <ol>
      <li><strong>Ihr fragt an</strong> – mit Datum, Ort und ungefährer Personenzahl.</li>
      <li><strong>Wir stimmen ab</strong> – Ablauf, Zeitbedarf und Rahmen werden gemeinsam geklärt.</li>
      <li><strong>Thomas kommt zu euch</strong> – in die Ferienwohnung, ins Hotel, zu euch nach Hause oder in eure Location.</li>
      <li><strong>Jede bekommt ihr Reading</strong> – ein persönlicher Moment mit den Karten, die anderen sind dabei oder genießen den Abend.</li>
    </ol>
    <h2>Gut zu wissen</h2>
    <ul class="tick-list">
      <li>Geeignet für kleine und mittlere Gruppen – Größe und Zeitbedarf bei der Anfrage abstimmen</li>
      <li>Einsatz rund um den Bodensee, nach Absprache auch darüber hinaus</li>
      <li>Möglich in Ferienwohnung, Hotel, privater Location oder einem separaten Raum – bitte vorab mit der Unterkunft abstimmen</li>
      <li>Ab 449 € für bis zu 6 Personen (ca. 2,5–3 Stunden), jede weitere Person 59 €</li>
    </ul>
    <p>Und keine Sorge: Es gibt keine düsteren Prophezeiungen und kein Theater. Thomas ist bodenständig, humorvoll und diskret – genau richtig für einen Abend unter Freundinnen.</p>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="section-head left" style="text-align:left;">
      <h2>Häufige Fragen zum JGA-Kartenabend</h2>
    </div>
    %(faq)s
  </div>
</section>

<!-- ANFRAGE -->
<section class="section" id="anfrage">
  <div class="container contact-grid">
    <div>
      <p class="eyebrow">Anfrage</p>
      <h2>Euren JGA anfragen</h2>
      <p>Schickt die wichtigsten Infos – Thomas meldet sich mit einem Vorschlag für euren Abend.</p>
      <ul class="tick-list">
        <li>Datum &amp; ungefähre Uhrzeit</li>
        <li>Ort / PLZ am Bodensee</li>
        <li>Anzahl Personen</li>
        <li>Location vorhanden? (Ferienwohnung, Hotel, privat …)</li>
      </ul>
      <div class="cta-row">
        <a class="btn btn-whatsapp" href="%(wa)s?text=%(wamsg2)s" target="_blank" rel="noopener">%(waicon)s Per WhatsApp anfragen</a>
        <a class="btn btn-outline-dark" href="%(mail)s?subject=JGA-Anfrage%%20am%%20Bodensee">%(mailicon)s Per E-Mail anfragen</a>
      </div>
    </div>
    <div class="form-card">
      <h2>Anfrageformular</h2>
      <!-- Hinweis: Dieses Formular ist statisch. Für echten Versand Formspree.io (kostenlos) einbinden
           oder die action-URL auf den eigenen Form-Endpunkt zeigen lassen. Anleitung in der README. -->
      <form action="https://formspree.io/f/DEIN-FORMULAR-CODE" method="post">
        <div class="field"><label for="jga-name">Name</label><input type="text" id="jga-name" name="name" required></div>
        <div class="field"><label for="jga-mail">E-Mail</label><input type="email" id="jga-mail" name="email" required></div>
        <div class="field"><label for="jga-tel">Telefon / WhatsApp</label><input type="tel" id="jga-tel" name="telefon"></div>
        <div class="field"><label for="jga-datum">Datum (ungefähr)</label><input type="date" id="jga-datum" name="datum"></div>
        <div class="field"><label for="jga-ort">Ort / PLZ</label><input type="text" id="jga-ort" name="ort"></div>
        <div class="field"><label for="jga-personen">Anzahl Personen</label><input type="number" id="jga-personen" name="personen" min="2" max="30"></div>
        <div class="field"><label for="jga-location">Location vorhanden?</label>
          <select id="jga-location" name="location">
            <option value="">Bitte wählen</option>
            <option value="ja">Ja, wir haben eine Location</option>
            <option value="nein">Nein, noch offen</option>
          </select>
        </div>
        <div class="field"><label for="jga-nachricht">Eure Nachricht</label><textarea id="jga-nachricht" name="nachricht"></textarea></div>
        <div class="field check">
          <input type="checkbox" id="jga-ds" name="datenschutz" required>
          <label for="jga-ds" style="font-weight:400;">Ich habe die <a href="/datenschutz/">Datenschutzerklärung</a> gelesen und bin mit der Verarbeitung meiner Daten zur Bearbeitung der Anfrage einverstanden.</label>
        </div>
        <button class="btn btn-gold" type="submit">Anfrage senden</button>
        <p class="form-note">Oder einfach direkt per WhatsApp – oft der schnellste Weg.</p>
      </form>
    </div>
  </div>
</section>

%(cta)s
""" % {
        "wa": WA_HREF,
        "wamsg": _urlencode("Hallo Thomas, wir planen einen Junggesellinnenabschied am Bodensee."),
        "wamsg2": _urlencode("Hallo Thomas, wir planen einen JGA. Datum: … | Ort: … | Personen: …"),
        "waicon": icon("whatsapp", 18), "mail": MAIL_HREF, "mailicon": icon("mail", 18),
        "hero": img("thomas-lude-kartenlegen-jga-bodensee",
                    "Junggesellinnenabschied mit Thomas Lude: Braut mit Schleier und Freundinnen beim Kartenlegen bei Prosecco",
                    sizes="(max-width: 920px) 100vw, 45vw", loading="eager", fetchpriority="high"),
        "faq": faq_html([
            ("Wie lange dauert ein Kartenabend auf dem JGA?",
             "Das hängt von der Gruppengröße ab – jede Teilnehmerin bekommt ihren eigenen Moment. Den genauen Zeitbedarf stimmt ihr bei der Anfrage mit Thomas ab."),
            ("Für wie viele Personen funktioniert das?",
             "Von kleinen Runden bis zu größeren Gruppen ist vieles möglich. Sag bei der Anfrage einfach, wie viele ihr seid – Thomas sagt euch, was gut funktioniert."),
            ("Wo findet der Kartenabend statt?",
             "Überall dort, wo ihr seid: Ferienwohnung, Hotel, zuhause oder eine angemietete Location. Bitte stimmt die Nutzung vorab mit der Unterkunft ab."),
            ("Was kostet ein JGA-Kartenabend?",
             "Ab 449 € für bis zu 6 Personen (ca. 2,5–3 Stunden), jede weitere Person 59 €. Größere Gruppen oder mehr Zeit besprecht ihr einfach bei der Anfrage."),
            ("Müssen wir an Kartenlegen glauben?",
             "Nein. Neugier reicht völlig. Der Abend funktioniert auch wunderbar, wenn manche erst mal skeptisch sind – oft sind das die größten Fans am Ende."),
        ]),
        "cta": cta_band("Ihr habt den Prosecco. Thomas bringt die Karten.",
                        "Macht euren JGA am Bodensee zu dem Abend, über den ihr später noch sprecht.",
                        "Hallo Thomas, wir planen einen Junggesellinnenabschied am Bodensee."),
    }

# ----------------------------------------------------------------------------
# TIER & MENSCH
# ----------------------------------------------------------------------------
def tier_body():
    return """
<header class="page-hero">
  <div class="container page-hero-split">
    <div>
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Tier &amp; Mensch</span></nav>
      <p class="eyebrow">Tier &amp; Mensch</p>
      <h1>Energetische Tierbegleitung am Bodensee</h1>
      <p class="lead">Manchmal braucht auch ein Tier einfach Ruhe. Thomas begleitet Tiere und ihre Menschen – ruhig, achtsam und ergänzend zur tierärztlichen Versorgung.</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="/kontakt-termin/">Tierbegleitung anfragen</a>
      </div>
    </div>
    <div>%(hero)s</div>
  </div>
</header>

<section class="section">
  <div class="container prose">
    <div class="notice-box" style="margin-bottom:2.2em;">
      <p><strong>Wichtig:</strong> Die energetische Begleitung ersetzt keine Untersuchung, Diagnose oder Behandlung durch Tierärztinnen oder Tierärzte. Bei gesundheitlichen Beschwerden ist immer zuerst tierärztlicher Rat einzuholen.</p>
    </div>
    <h2>Ruhige Begleitung für Tier und Mensch</h2>
    <p>Tiere spüren mehr, als wir oft denken. Veränderungen im Umfeld, Unruhe, neue Lebenssituationen – all das kann ein Tier beschäftigen. Thomas begleitet in solchen Phasen ruhig und achtsam: mit Zeit, Zuwendung und einem geschulten Gespür.</p>
    <h2>In welchen Situationen Menschen mit ihren Tieren kommen</h2>
    <ul class="tick-list">
      <li>Veränderungen im Umfeld – Umzug, neues Familienmitglied, neuer Alltag</li>
      <li>Unruhe oder auffällige Verhaltensänderungen (nach tierärztlicher Abklärung)</li>
      <li>Bindung zwischen Tier und Mensch stärken</li>
      <li>Abschied und Trauer – wenn ein Weg zu Ende geht</li>
      <li>Neue Lebenssituationen, die Tier und Mensch gemeinsam meistern</li>
      <li>Zeiten, in denen ein Tier einfach Ruhe und Zuwendung braucht</li>
    </ul>
    <h2>Wie eine Begleitung abläuft</h2>
    <p>Immer im Tempo des Tieres. Thomas nimmt sich Zeit, das Tier kennenzulernen, und arbeitet ruhig und ohne Druck. Was genau passiert, besprecht ihr vorab – denn jedes Tier ist anders.</p>
    <p><strong>Ca. 45–60 Minuten · 149 €.</strong></p>
    <h2>Was Thomas ausdrücklich nicht verspricht</h2>
    <p>Keine Heilung, keine Schmerzlinderung, keine Behandlung von Krankheiten. Die energetische Begleitung ist ein ergänzendes Angebot – die Gesundheit eures Tieres gehört in tierärztliche Hände.</p>
  </div>
</section>

<section class="section section-soft">
  <div class="container split">
    <div class="split-media">%(split)s</div>
    <div>
      <h2>Erst zuhören, dann begleiten</h2>
      <p>Erzähl Thomas kurz, worum es geht: Was beschäftigt dein Tier – und was beschäftigt dich dabei? Gemeinsam schaut ihr, ob und wie eine Begleitung sinnvoll ist.</p>
      <div class="cta-row">
        <a class="btn btn-whatsapp" href="%(wa)s?text=%(wamsg)s" target="_blank" rel="noopener">%(waicon)s Per WhatsApp anfragen</a>
        <a class="btn btn-outline-dark" href="/kontakt-termin/">Kontakt aufnehmen</a>
      </div>
    </div>
  </div>
</section>
%(cta)s
""" % {
        "hero": img("thomas-lude-tierbegleitung-bodensee",
                    "Thomas Lude legt einem entspannt liegenden Golden Retriever ruhig die Hände auf",
                    sizes="(max-width: 920px) 100vw, 45vw", loading="eager", fetchpriority="high"),
        "split": img("thomas-lude-portrait-hund-friedrichshafen",
                     "Thomas Lude mit seinem Golden Retriever auf dem Sofa – Nähe und Vertrauen zwischen Mensch und Tier"),
        "wa": WA_HREF, "wamsg": _urlencode("Hallo Thomas, ich interessiere mich für eine energetische Tierbegleitung."),
        "waicon": icon("whatsapp", 18),
        "cta": cta_band("Dein Tier braucht gerade Ruhe?",
                        "Schreib kurz, was los ist – Thomas meldet sich persönlich.",
                        "Hallo Thomas, ich interessiere mich für eine energetische Tierbegleitung."),
    }


# ----------------------------------------------------------------------------
# VORTEXKEY KOMPASS – Partner-Erklärung (Gastbeitrag von VortexKey)
# ----------------------------------------------------------------------------
def kompass_body():
    return """
<section class="section">
  <div class="container prose" style="max-width:760px;">
    <p class="eyebrow">Erklärung meines Kooperationspartners</p>
    <h1>Der VortexKey Kompass</h1>
    <p class="lead">Die folgende Seite ist die Erklärung meines Kooperationspartners VortexKey, in dessen eigenen Worten und eigenem Design – warum die Zusammenarbeit zwischen VortexKey und mir Sinn ergibt. Ich bleibe für dich weiterhin Kartenleger; VortexKey beschreibt hier die ergänzende Perspektive von Kristina Helwig.</p>
  </div>
</section>

<div class="kompass-page">
<style>
.kompass-page{font-family:Georgia,serif;color:#333;line-height:1.6}
.kompass-page img{max-width:100%;display:block}
.kompass-page a{color:#b8942e;text-decoration:none}
.kompass-page section{padding:64px 24px}
.kompass-page .k-container{max-width:1100px;margin:0 auto}
.kompass-page .k-label{color:#b8942e;font-size:13px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;display:block;margin-bottom:12px}
.kompass-page h2{font-size:clamp(1.6rem,3vw,2.2rem);color:#1a1a1a;margin-bottom:16px;font-family:Georgia,serif;}
.kompass-page .k-dark{background:#1a1a1a;color:#fff}
.kompass-page .k-dark h2{color:#fff}
.kompass-page .k-cream{background:#f8f5f0}
.kompass-page .k-hero{background:linear-gradient(135deg,#1a1a1a 0%,#2d2520 50%,#1a1a1a 100%);position:relative;overflow:hidden;padding:90px 24px;text-align:center;min-height:460px;display:flex;align-items:center;justify-content:center}
.kompass-page .k-hero-bg{position:absolute;top:0;left:0;width:100%;height:100%;opacity:.3;z-index:0}
.kompass-page .k-hero-bg img{width:100%;height:100%;object-fit:cover}
.kompass-page .k-hero-content{position:relative;z-index:1;max-width:800px;margin:0 auto}
.kompass-page .k-badge{display:inline-block;padding:8px 20px;border:1px solid #d4a849;color:#d4a849;border-radius:20px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:24px}
.kompass-page .k-hero h1{font-size:clamp(1.8rem,4vw,2.8rem);color:#fff;line-height:1.3;margin-bottom:24px;font-family:Georgia,serif;}
.kompass-page .k-hero h1 em{color:#d4a849;font-style:normal}
.kompass-page .k-hero p{color:rgba(255,255,255,.85);font-size:18px;line-height:1.8;margin-bottom:32px}
.kompass-page .k-btn{display:inline-block;padding:16px 32px;background:#b8942e;color:#fff;border-radius:8px;font-weight:600;margin:8px}
.kompass-page .k-btn:hover{background:#d4a849}
.kompass-page .k-btn-outline{background:transparent;border:2px solid rgba(255,255,255,.3);color:#fff}
.kompass-page .k-btn-outline:hover{border-color:#d4a849;color:#d4a849;background:rgba(184,148,46,.1)}
.kompass-page .k-card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px;margin-top:48px}
.kompass-page .k-card{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.06)}
.kompass-page .k-card-img{height:180px;overflow:hidden}
.kompass-page .k-card-img img{width:100%;height:100%;object-fit:cover}
.kompass-page .k-card-body{padding:24px}
.kompass-page .k-card-badge{width:40px;height:40px;border-radius:50%;background:#b8942e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:10px;margin-bottom:10px}
.kompass-page .k-card h3{font-size:16px;margin-bottom:8px}
.kompass-page .k-card p{font-size:14px;color:#666;line-height:1.6}
.kompass-page .k-two-col{display:grid;grid-template-columns:1fr 1fr;gap:32px}
@media(max-width:768px){.kompass-page .k-two-col{grid-template-columns:1fr}.kompass-page .k-card-grid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.kompass-page .k-card-grid{grid-template-columns:1fr}}
</style>

<section class="k-hero">
  <div class="k-hero-bg"><img src="/assets/img/kompass-zug-weichen.webp" alt="Dampfzug fährt bei Sonnenaufgang auf eine Weiche zu, an der sich die Gleise teilen"></div>
  <div class="k-hero-content">
    <div class="k-badge">VortexKey Kompass</div>
    <h1>Du siehst die Richtung.<br>Aber verstehst du auch<br><em>dein Gleis?</em></h1>
    <p>Du kommst zu Thomas, weil du wissen willst, wohin dein Weg führt. Er zeigt dir die Weichen, die sich öffnen. Und: Je klarer du verstehst, wer du wirklich bist, desto gezielter kann er mit den Karten ansetzen. Deshalb arbeitet Thomas mit Kristina zusammen.</p>
    <div>
      <a href="https://vortexkey.de/wegweiser/" class="k-btn" target="_blank" rel="noopener">VortexKey entdecken →</a>
      <a href="#metapher" class="k-btn k-btn-outline">Wie das zusammenspielt</a>
    </div>
  </div>
</section>

<section id="metapher" class="k-cream">
  <div class="k-container" style="max-width:900px">
    <div style="text-align:center;margin-bottom:40px">
      <span class="k-label">Die Weichen-Methode</span>
      <h2>Warum Kristina und Thomas zusammenarbeiten.</h2>
    </div>
    <div style="margin:32px 0;border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.12)">
      <img src="/assets/img/kompass-stellwerk.webp" alt="Blick aus einem alten Stellwerk auf die Gleise bei Abenddämmerung" style="width:100%">
      <p style="padding:12px 16px;margin:0;font-size:13px;color:#666;background:#fff;font-style:italic">Du sitzt im Zug — aber du siehst nicht die Weichen. Der Kompass will das ändern.</p>
    </div>
    <div style="font-size:17px;line-height:1.9;color:#333">
      <p style="margin-bottom:20px"><strong>Stell dir dein Leben als Zug vor.</strong></p>
      <p style="margin-bottom:16px">Ein Zug, der schon lange fährt. An manchen Stationen steigen Menschen ein. An anderen steigen sie aus. Das ist normal.</p>
      <p style="margin-bottom:16px">Aber hier ist das Problem: <strong>Du sitzt im Zug, nicht im Stellwerk.</strong> Du siehst die Gleise vor dir, aber du siehst nicht die Weichen. Du fährst weiter — und merkst erst zu spät, dass du schon wieder dieselbe Strecke genommen hast.</p>
      <div style="padding:20px;background:rgba(184,148,46,.08);border-left:3px solid #b8942e;border-radius:0 8px 8px 0;margin:20px 0">
        <strong style="color:#b8942e">Das ist der Kompass.</strong> Nicht nur Thomas' Karten. Nicht nur Kristinas Human Design. Beides zusammen.
      </div>
      <div style="margin:32px 0;padding-left:24px;border-left:2px solid #b8942e">
        <p style="margin-bottom:16px"><strong style="color:#b8942e">1. Kristina zeigt dir, wo du stehst.</strong><br>Sie liest dein Human Design. Sie erkennt die Struktur hinter deinen Mustern.</p>
        <p><strong style="color:#b8942e">2. Thomas zeigt dir, welche Richtung sich öffnet.</strong><br>Er legt die Karten für deinen Weg — aber nicht als festes Schicksal. Sondern als Möglichkeit.</p>
      </div>
      <p style="margin-bottom:16px"><strong>Und das Entscheidende:</strong> Was sich zeigt, ändert sich, wenn du dich änderst. Es ist kein festes Schicksal. Es ist dein <em>Potenzial</em>.</p>
    </div>
  </div>
</section>

<section>
  <div class="k-container">
    <div style="text-align:center;margin-bottom:40px">
      <span class="k-label">Die Reise</span>
      <h2>Vier Stationen. Eine Richtung.</h2>
    </div>
    <div class="k-card-grid">
      <div class="k-card">
        <div class="k-card-img"><img src="/assets/img/kompass-zug-weichen.webp" alt="Gleise, die sich vor einem fahrenden Zug teilen"></div>
        <div class="k-card-body">
          <div class="k-card-badge">GLEIS</div>
          <h3>Wo stehst du?</h3>
          <p><strong>Kristina</strong> liest dein Human Design. Deine Struktur. Deine Stärken.</p>
        </div>
      </div>
      <div class="k-card">
        <div class="k-card-img"><img src="/assets/img/kompass-weiche-entscheidung.webp" alt="Nahaufnahme einer Bahnweiche, an der sich zwei Gleise trennen"></div>
        <div class="k-card-body">
          <div class="k-card-badge">WEICHE</div>
          <h3>Welche Richtung?</h3>
          <p><strong>Thomas</strong> legt die Karten. Die Weichen, die sich durch deine Klarheit öffnen.</p>
        </div>
      </div>
      <div class="k-card">
        <div class="k-card-img" style="background:linear-gradient(135deg,#2d2520,#1a1a1a);display:flex;align-items:center;justify-content:center">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d4a849" stroke-width="1"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
        <div class="k-card-body">
          <div class="k-card-badge">WEG</div>
          <h3>Wohin gehst du?</h3>
          <p>Die Entscheidung ist deine — aber jetzt basiert sie auf mehr Klarheit.</p>
        </div>
      </div>
      <div class="k-card">
        <div class="k-card-img"><img src="/assets/img/kompass-bahnhof-menschen.webp" alt="Reisende auf einem historischen Bahnhof im goldenen Licht"></div>
        <div class="k-card-body">
          <div class="k-card-badge">ZUG</div>
          <h3>Wer fährt mit?</h3>
          <p>Neue Weiche, neue Strecke, neue Menschen. Platz für die Richtigen.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="k-dark">
  <div class="k-container">
    <div style="text-align:center;margin-bottom:40px">
      <span class="k-label" style="color:#d4a849">In beide Richtungen</span>
      <h2>Egal, wo du einsteigst — du kommst zu mehr Klarheit.</h2>
    </div>
    <div class="k-two-col" style="margin-top:40px">
      <div style="padding:32px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px">
        <div style="width:40px;height:40px;border-radius:50%;background:#b8942e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;margin-bottom:16px">1</div>
        <h3 style="color:#fff;font-size:18px;margin-bottom:10px">Du kommst von Kristina</h3>
        <p style="color:rgba(255,255,255,.7);font-size:15px;line-height:1.7">Du weißt, wo du stehst. Du verstehst dein Human Design. Aber du fragst dich: <em>Und jetzt?</em> Welche Weichen stehen offen?</p>
        <p style="color:rgba(255,255,255,.7);font-size:15px;line-height:1.7;margin-top:12px"><strong>Thomas zeigt dir eine Richtung.</strong> Die Karten für deinen nächsten Schritt.</p>
      </div>
      <div style="padding:32px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px">
        <div style="width:40px;height:40px;border-radius:50%;background:#b8942e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;margin-bottom:16px">2</div>
        <h3 style="color:#fff;font-size:18px;margin-bottom:10px">Du kommst von Thomas</h3>
        <p style="color:rgba(255,255,255,.7);font-size:15px;line-height:1.7">Du siehst eine Richtung. Du weißt, welche Weichen sich öffnen. Aber du fragst dich: <em>Warum bin ich hier?</em></p>
        <p style="color:rgba(255,255,255,.7);font-size:15px;line-height:1.7;margin-top:12px"><strong>Kristina zeigt dir die Struktur.</strong> Dein Human Design.</p>
      </div>
    </div>
    <div style="text-align:center;margin-top:32px;padding:20px;background:rgba(184,148,46,.1);border-radius:12px">
      <p style="font-size:15px;color:#fff;margin:0"><strong style="color:#d4a849">Das ist die Idee des Kompass:</strong> Er funktioniert vorwärts und rückwärts. Er ergänzt Kristina. Er ergänzt Thomas. Und er gibt dir mehr Klarheit.</p>
    </div>
  </div>
</section>

<section class="k-cream">
  <div class="k-container">
    <div style="text-align:center;margin-bottom:40px">
      <span class="k-label">Konkret für dich</span>
      <h2>Was passiert, wenn du beides kombinierst?</h2>
    </div>
    <div class="k-two-col">
      <div style="padding:28px;background:#fff;border-radius:12px">
        <h3 style="font-size:17px;margin-bottom:10px;color:#b8942e">Du erkennst deine Muster</h3>
        <p style="font-size:15px;line-height:1.7;color:#555">Warum ziehst du immer wieder dieselben Situationen an? Warum endet es oft ähnlich? Kristina zeigt dir die Struktur — nicht als Verurteilung, sondern als Landkarte.</p>
      </div>
      <div style="padding:28px;background:#fff;border-radius:12px">
        <h3 style="font-size:17px;margin-bottom:10px;color:#b8942e">Du siehst neue Weichen</h3>
        <p style="font-size:15px;line-height:1.7;color:#555">Die Stellen, an denen du immer wieder dieselbe Abzweigung genommen hast — jetzt siehst du sie. Und du siehst: Es gibt andere Wege.</p>
      </div>
      <div style="padding:28px;background:#fff;border-radius:12px">
        <h3 style="font-size:17px;margin-bottom:10px;color:#b8942e">Du wählst bewusst</h3>
        <p style="font-size:15px;line-height:1.7;color:#555">Nicht mehr automatisch fahren. Du weißt, wo du stehst. Du weißt, wohin du könntest. Und du entscheidest — bewusst, klar, in deinem eigenen Tempo.</p>
      </div>
      <div style="padding:28px;background:#fff;border-radius:12px">
        <h3 style="font-size:17px;margin-bottom:10px;color:#b8942e">Neue Menschen, neue Strecke</h3>
        <p style="font-size:15px;line-height:1.7;color:#555">An jeder neuen Weiche steigen Menschen ein und aus. Du darfst alte Begleiter loslassen. Du darfst Platz machen für die, die zu deiner neuen Richtung passen.</p>
      </div>
    </div>
  </div>
</section>

<section class="k-cream" style="text-align:center">
  <div class="k-container" style="max-width:520px">
    <span class="k-label">Der Kompass im Bundle</span>
    <h2>Beide zusammen, ein Preis.</h2>
    <p style="margin:16px 0 6px"><span style="font-size:40px;font-weight:700;color:#1a1a1a">309&nbsp;€</span> <span style="font-size:16px;color:#999;text-decoration:line-through">329&nbsp;€</span></p>
    <p style="font-size:14px;color:#666;margin-bottom:24px">60 Min. Kristina + 45 Min. Thomas + gemeinsames Abschlussgespräch, schriftliche Zusammenfassung und 2 Wochen WhatsApp-Begleitung. Einzeln gebucht: 180&nbsp;€ (Kristina) + 149&nbsp;€ (Thomas).</p>
    <a href="https://vortexkey.de/wegweiser/" class="k-btn" target="_blank" rel="noopener">Kompass anfragen →</a>
  </div>
</section>

<section class="k-dark" style="text-align:center">
  <div class="k-container" style="max-width:640px">
    <span class="k-label" style="color:#d4a849">Neugierig?</span>
    <h2 style="color:#fff;margin-top:8px">Lass uns deine Weichen finden.</h2>
    <p style="font-size:17px;color:rgba(255,255,255,.8);line-height:1.8;margin:24px 0">Der Kompass ist mehr als eine Kartenlegung. Er ist mehr als ein Human-Design-Reading. Er ist die Kombination beider Blickwinkel.</p>
    <div style="margin:32px 0">
      <a href="https://vortexkey.de/wegweiser/" class="k-btn" target="_blank" rel="noopener">Zu VortexKey →</a>
      <a href="/kontakt-termin/" class="k-btn k-btn-outline">Termin bei Thomas</a>
    </div>
    <p style="color:rgba(255,255,255,.4);font-size:13px;margin-top:24px">Du bleibst bei Thomas als Kartenleger. Der Kompass ergänzt seine Arbeit — er ersetzt sie nicht.</p>
  </div>
</section>
</div>
"""


# ----------------------------------------------------------------------------
# ERGÄNZENDE IMPULSE – Verweise auf andere Systeme (u.a. VortexKey)
# ----------------------------------------------------------------------------
def ergaenzende_impulse_body():
    weiche_image = img(
        "vortexkey-thomas-lude-weiche",
        "Zugstrecke mit einer Weiche vor Bergpanorama und See – Sinnbild für einen neuen Weg, sobald der alte verstanden ist",
        sizes="(max-width: 1040px) 100vw, 1040px",
        loading="lazy",
    )
    return landing_body(
        eyebrow="Ergänzende Impulse",
        h1="Wenn ein zweiter Blick hilft",
        lead="Meine Kartenlegung steht für sich. Für einzelne Themen – ein hartnäckiges Muster, eine berufliche Weichenstellung – kann eine zweite, andersartige Perspektive zusätzliche Klarheit bringen. Deshalb verweise ich hier bewusst auf ausgewählte ergänzende Systeme.",
        image="thomas-lude-ueber-thomas-kartenlegen",
        image_alt="Thomas Lude an seinem Kartentisch, konzentriert bei einer Kartenlegung",
        prose="""
<h2>Dein Weg ist nicht festgeschrieben</h2>
<p>Vielleicht bist du nicht zufällig hier. Es gibt Phasen im Leben, in denen der bisherige Weg dich nicht mehr trägt – Beziehungen, Konflikte oder Entscheidungen wiederholen sich, oder da ist eine innere Unruhe, eine Frage, die dich schon lange begleitet.</p>
<p>In meiner Beratung schaue ich mit dir auf die Entwicklungen, Entscheidungen und Möglichkeiten, die sich aus deiner gegenwärtigen Situation heraus zeigen. Doch Zukunft ist kein unveränderlicher Plan: Ein Weg kann sichtbar werden, eine Richtung sich zeigen – und trotzdem verändert sich alles in dem Moment, in dem du bewusst anders entscheidest oder handelst. Du bist nicht nur Beobachterin oder Beobachter deines Lebens, du gestaltest es mit.</p>

<h2>Wenn alte Muster den Blick nach vorn prägen</h2>
<p>Manchmal zeigt sich in einer Sitzung sehr deutlich, welche Richtung sich aus deinem bisherigen Weg ergibt – als würde eine vertraute Tür wieder zu ähnlichen Erfahrungen führen. Das ist keine Festlegung, sondern eine Einladung zur Klarheit: Sobald du erkennst, welche Muster dich bisher begleitet haben, entsteht neuer Handlungsspielraum.</p>
<p>Meine Arbeit kann dir einen Blick auf die Möglichkeiten geben, die vor dir liegen. Sie ersetzt aber nicht deine eigene innere Arbeit – Veränderung beginnt dort, wo du bereit bist, Verantwortung für deinen nächsten Schritt zu übernehmen.</p>

<h2>Ausgewählte ergänzende Systeme</h2>
<p>Ich arbeite mit den Karten – direkt, bodenständig und ohne esoterisches Theater. Für die meisten Fragen reicht das völlig aus. Wer zusätzlich noch tiefer schauen möchte, findet hier zwei Anknüpfungspunkte, die ich für sinnvoll halte.</p>

<h3>VortexKey – Muster und blinde Flecken verstehen</h3>
<p>Wenn du nicht nur nach vorn schauen, sondern auch besser verstehen möchtest, warum du heute an diesem Punkt stehst, empfehle ich dir ergänzend die Arbeit von <a href="https://vortexkey.de/wegweiser/" target="_blank" rel="noopener">VortexKey</a>. Die VortexKey-Methode richtet den Blick auf das, was im bisherigen Leben oft unbemerkt mitgewirkt hat: wiederkehrende Muster, innere Konflikte und blinde Flecken. Sie bietet einen klaren, begleiteten Rahmen, um die eigenen Erfahrungen bewusster einzuordnen.</p>

<div class="card-grid two">
  <article class="card">
    <div class="card-body">
      <h3>Meine spirituelle Begleitung</h3>
      <ul class="tick-list">
        <li>Blick auf mögliche Entwicklungen und Weggabelungen</li>
        <li>Spirituelle Impulse für deine gegenwärtigen Fragen</li>
        <li>Orientierung für anstehende Entscheidungen</li>
        <li>Neue Perspektiven auf das, was möglich werden kann</li>
      </ul>
    </div>
  </article>
  <article class="card">
    <div class="card-body">
      <h3>Begleitung mit VortexKey</h3>
      <ul class="tick-list">
        <li>Blick auf bisherige Muster, Prägungen und blinde Flecken</li>
        <li>Strukturierte Reflexion des bisherigen Weges</li>
        <li>Klarheit darüber, was dich bisher geprägt haben könnte</li>
        <li>Bewusstere Grundlage für deine nächste Entscheidung</li>
      </ul>
    </div>
  </article>
</div>

<p>Die Arbeit mit VortexKey kann vor einer Kartenlegung wertvoll sein, um innere Themen zu sortieren – oder danach, um einen Impuls tiefer in deinen Alltag zu übersetzen. Wer beide Schritte kombiniert, hat nicht nur eine Standortbestimmung, sondern auch eine Richtung: erst der Blick nach innen, dann der Blick nach vorn.</p>
<p><a href="https://vortexkey.de/wegweiser/" target="_blank" rel="noopener"><strong>Mehr über die VortexKey-Methode erfahren &rarr;</strong></a><br>
<a href="/vortexkey-kompass/"><strong>Warum die Zusammenarbeit Sinn ergibt – Erklärung von VortexKey &rarr;</strong></a></p>
""" + """
<section class="article-figure">
  <div class="container">
    <figure>
      %s
      <figcaption>Eine neue Weiche wird sichtbar, sobald der alte Weg verstanden ist.</figcaption>
    </figure>
  </div>
</section>

<h3>Wie ein Zug, der die Weiche wechselt</h3>
<p>Der bisherige Weg lässt sich mit einer Zugfahrt vergleichen: Du fährst auf vertrauten Gleisen, mit den Menschen und Gewohnheiten, die gerade mit dir unterwegs sind. VortexKey hilft dir zu erkennen, wo es in deinem Leben Weichen gibt – und warum du bisher genau diesen Weg gefahren bist.</p>
<p>Sobald diese Erkenntnis da ist und du bereit bist, sie anzunehmen, stellt sich die Weiche oft wie von selbst. Ein neuer Weg wird möglich. Manche Weggefährten steigen aus, andere kommen neu dazu – das gehört zu jeder echten Veränderung dazu.</p>
<p>Genau an diesem Punkt setze ich an: Ich schaue mit dir auf die Perspektiven, die sich auf dem neuen Gleis eröffnen können, und gebe dir Impulse für den Weg, der jetzt vor dir liegt.</p>
""" % weiche_image + """
<h3>Beruf, Hauskauf &amp; finanzielle Entscheidungen</h3>
<p>Auch bei Fragen zu Beruf, Hauskauf, Umzug oder einem finanziellen Neuanfang kann ein zweiter Blick helfen – behutsam formuliert und ausdrücklich ohne Finanz-, Rechts- oder Anlageberatung zu sein.</p>
<p><a href="/kartenlegen-beruf-veraenderung/"><strong>Zu Beruf &amp; Veränderung &rarr;</strong></a><br>
<a href="/kartenlegen-hauskauf-umzug/"><strong>Zu Hauskauf, Umzug &amp; finanziellen Entscheidungen &rarr;</strong></a></p>

<h2>Die Zukunft entsteht aus deinem nächsten Schritt</h2>
<p>Ich kann mit dir auf die Wege schauen, die sich aus deinem heutigen Leben heraus zeigen, und dir Impulse für mögliche Entwicklungen geben. Welche Tür du öffnest, bleibt jedoch deine Entscheidung.</p>
""",
        whatsapp_msg="Hallo Thomas, ich interessiere mich für eine ergänzende Perspektive zu meinem Thema.",
        cta_title="Erst Klarheit, dann Richtung.",
        cta_text="Schreib kurz, worum es geht – Thomas meldet sich persönlich.",
    )


# ----------------------------------------------------------------------------
# ÜBER THOMAS
# ----------------------------------------------------------------------------
def ueber_body():
    return """
<header class="page-hero">
  <div class="container page-hero-split">
    <div>
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Über mich</span></nav>
      <p class="eyebrow">Über Thomas</p>
      <h1>Thomas Lude – Kartenleger am Bodensee</h1>
      <p class="lead">Persönlich. Direkt. Mit Gespür. Und ohne Kristallkugel-Theater.</p>
    </div>
    <div>%(hero)s</div>
  </div>
</header>

<section class="section">
  <div class="container prose">
    <h2>Wie Thomas zum Kartenlegen kam</h2>
    <p>Das Kartenlegen wurde Thomas nicht antrainiert – es liegt in der Familie. Er legt die Karten in dritter Generation und trägt damit eine Tradition weiter, die in seiner Familie über Jahrzehnte gewachsen ist. Was er daraus mitgenommen hat, ist vor allem eine Haltung: Die Karten sind kein Orakel, das einem das Leben abnimmt. Sie sind ein Werkzeug, um gemeinsam hinzuschauen.</p>
    <p>Seit vielen Jahren begleitet er Menschen, wenn das Leben Fragen stellt: bei Liebe und Beziehung, bei Entscheidungen, bei Veränderungen. Heute berät er in Friedrichshafen am Bodensee – persönlich am Tisch, am Telefon und auf Events.</p>
    <h2>Wie er arbeitet</h2>
    <p>Ruhig, aufmerksam und direkt. Thomas hört zu, bevor er legt. Er sagt, was er sieht – auch wenn es nicht immer das ist, was man gern hören möchte. Und er lässt dich mit etwas Konkretem gehen, nicht mit vagen Andeutungen.</p>
    <h2>Was dir wichtig sein darf</h2>
    <p>Deine Frage. Deine Entscheidung. Deine Geschwindigkeit. Es gibt keine falsche Frage und keinen falschen Zeitpunkt – nur den Mut, hinzuschauen.</p>
  </div>
</section>

<section class="section section-soft">
  <div class="container card-grid two">
    <article class="card">
      <div class="card-body">
        <h3>Was du von Thomas nicht bekommst</h3>
        <ul class="tick-list">
          <li>Keine Angstmache</li>
          <li>Keine Abhängigkeit</li>
          <li>Keine Garantie einer unveränderlichen Zukunft</li>
          <li>Keine medizinischen Diagnosen</li>
          <li>Keine juristische oder finanzielle Beratung</li>
          <li>Keine Entscheidung über dein Leben</li>
        </ul>
      </div>
    </article>
    <article class="card">
      <div class="card-body">
        <h3>Was du bekommst</h3>
        <ul class="tick-list">
          <li>Aufmerksamkeit</li>
          <li>Einen anderen Blick</li>
          <li>Direkte Rückmeldung</li>
          <li>Diskretion</li>
          <li>Raum für deine Fragen</li>
        </ul>
      </div>
    </article>
  </div>
</section>

<section class="section">
  <div class="container center">
    <div style="max-width:760px;margin:0 auto;">
      <blockquote style="margin:0;font-family:var(--serif);font-size:clamp(1.5rem,3.2vw,2.2rem);line-height:1.4;color:var(--dark);">
        „Manchmal liegt die Antwort schon vor uns. Wir sehen sie nur noch nicht.“
      </blockquote>
      <p class="eyebrow" style="margin-top:1.2rem;">Thomas Lude</p>
    </div>
    <div class="cta-row center">
      <a class="btn btn-gold" href="/kontakt-termin/">Termin mit Thomas anfragen</a>
    </div>
  </div>
</section>
""" % {
        "hero": img("thomas-lude-ueber-thomas-kartenlegen",
                    "Thomas Lude an seinem Kartentisch – Kartenleger aus Friedrichshafen am Bodensee",
                    sizes="(max-width: 920px) 100vw, 45vw", loading="eager", fetchpriority="high"),
    }

# ----------------------------------------------------------------------------
# ERFAHRUNGEN (alle Stimmen = PLATZHALTER!)
# ----------------------------------------------------------------------------
def erfahrungen_body():
    return """
<header class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Erfahrungen</span></nav>
    <p class="eyebrow">Erfahrungen</p>
    <h1>Warum Menschen Thomas vertrauen</h1>
    <p class="lead">Diese Seite sammelt mit der Zeit echte Rückmeldungen von Menschen, die bei Thomas waren – persönlich, am Telefon, auf Events und mit ihren Tieren.</p>
  </div>
</header>

<section class="section">
  <div class="container">
    <div class="notice-box" style="margin-bottom:2.2rem;">
      <p><strong>Bewertungen folgen in Kürze.</strong> Statt erfundener Zitate zeigen wir hier erst echte, freigegebene Rückmeldungen, sobald sie vorliegen. Bis dahin ein paar Fakten, die für sich sprechen:</p>
    </div>
    <div class="card-grid three">
      <article class="card">
        <div class="card-body">
          <h3>Kartenlegen in dritter Generation</h3>
          <p>Eine Tradition, die in der Familie gewachsen ist – verbunden mit eigener Erfahrung und einer bodenständigen, ehrlichen Art.</p>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3>Kunden aus Deutschland, Österreich und der Schweiz</h3>
          <p>Persönlich am Bodensee, telefonisch weit darüber hinaus – über die Region hinaus bekannt, vor allem durch Weiterempfehlung.</p>
        </div>
      </article>
      <article class="card">
        <div class="card-body">
          <h3>Diskretion als Grundprinzip</h3>
          <p>Was am Kartentisch oder am Telefon besprochen wird, bleibt vertraulich – ohne Ausnahme.</p>
        </div>
      </article>
    </div>
  </div>
</section>
%(cta)s
""" % {
        "cta": cta_band("Du warst bei Thomas?", "Melde dich gern – mit deinem Einverständnis nehmen wir deine Rückmeldung hier mit auf."),
    }

# ----------------------------------------------------------------------------
# BLOG
# ----------------------------------------------------------------------------
def blog_card(post, loading="lazy"):
    tags = "".join('<span>%s</span>' % html.escape(t) for t in post["tags"][:2])
    return """      <article class="card blog-card">
        <a class="card-image" href="/blog/%(slug)s/">%(image)s</a>
        <div class="card-body">
          <div class="blog-tags">%(tags)s</div>
          <h3><a href="/blog/%(slug)s/">%(title)s</a></h3>
          <p>%(desc)s</p>
          <div class="blog-card-meta">%(date)s · %(read)s Lesezeit</div>
          <a class="link-more" href="/blog/%(slug)s/">Beitrag lesen</a>
        </div>
      </article>""" % {
        "slug": post["slug"],
        "image": img(post["image"], post["alt"], loading=loading),
        "tags": tags,
        "title": html.escape(post["title"]),
        "desc": html.escape(post["desc"]),
        "date": html.escape(post["date"]),
        "read": html.escape(post["read_time"]),
    }


def blog_schema(post):
    url = SITE_URL + "/blog/" + post["slug"] + "/"
    image_url = SITE_URL + "/assets/img/" + post["image"] + "-full.webp"
    return {
        "@type": "BlogPosting",
        "@id": url + "#artikel",
        "headline": post["title"],
        "description": post["desc"],
        "image": [image_url],
        "datePublished": post["iso_date"],
        "dateModified": post["iso_date"],
        "inLanguage": "de-DE",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@id": SITE_URL + "/#thomas-lude"},
        "publisher": {"@id": SITE_URL + "/#beratung"},
        "keywords": post["tags"],
    }


def blog_overview_schema():
    return {
        "@type": "Blog",
        "@id": SITE_URL + "/blog/#blog",
        "name": "Blog von Thomas Lude",
        "description": "Erfahrungen und Erklärungen zu Kartenlegen, Hellfühligkeit, Raumklärung, Verlust, Wiedergeburt und karmischen Aufgaben.",
        "url": SITE_URL + "/blog/",
        "inLanguage": "de-DE",
        "blogPost": [
            {"@type": "BlogPosting", "headline": p["title"], "url": SITE_URL + "/blog/" + p["slug"] + "/"}
            for p in BLOG_POSTS
        ],
    }


def blog_body():
    featured = BLOG_POSTS[0]
    rest = BLOG_POSTS[1:]
    featured_tags = "".join('<span>%s</span>' % html.escape(t) for t in featured["tags"])
    cards = "\n".join(blog_card(p) for p in rest)
    return """
<header class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Blog</span></nav>
    <p class="eyebrow">Blog &amp; Erfahrungen</p>
    <h1>Texte über Karten, Hellfühligkeit und das, was Räume erzählen</h1>
    <p class="lead">Persönliche Erfahrungen und ruhige Erklärungen von Thomas Lude – über Wahrnehmung, Raumklärung, Verlust, karmische Aufgaben und die Grenzen ehrlicher spiritueller Arbeit.</p>
  </div>
</header>

<section class="section blog-feature-section">
  <div class="container blog-feature">
    <a class="blog-feature-image" href="/blog/%(featured_slug)s/">%(featured_image)s</a>
    <div class="blog-feature-body">
      <div class="blog-tags">%(featured_tags)s</div>
      <h2><a href="/blog/%(featured_slug)s/">%(featured_title)s</a></h2>
      <p class="lead">%(featured_lead)s</p>
      <p class="blog-card-meta">%(featured_date)s · %(featured_read)s Lesezeit</p>
      <a class="btn btn-gold" href="/blog/%(featured_slug)s/">Beitrag lesen</a>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="section-head left" style="text-align:left;">
      <h2>Alle Beiträge</h2>
      <p class="lead">Jeder Beitrag geht einem einzigen Thema in Ruhe auf den Grund – zum Lesen, Wiederkommen oder als erster Schritt vor einem persönlichen Gespräch.</p>
    </div>
    <div class="card-grid three">
%(cards)s
    </div>
  </div>
</section>
%(cta)s
""" % {
        "featured_slug": featured["slug"],
        "featured_image": img(featured["image"], featured["alt"], sizes="(max-width: 920px) 100vw, 52vw", loading="eager", fetchpriority="high"),
        "featured_tags": featured_tags,
        "featured_title": html.escape(featured["title"]),
        "featured_lead": html.escape(featured["lead"]),
        "featured_date": html.escape(featured["date"]),
        "featured_read": html.escape(featured["read_time"]),
        "cards": cards,
        "cta": cta_band("Dein Thema ist noch nicht dabei?", "Schreib Thomas kurz, worum es geht – vielleicht entsteht daraus der nächste Beitrag oder dein persönliches Gespräch."),
    }


def article_body(post):
    tags = "".join('<span>%s</span>' % html.escape(t) for t in post["tags"])
    related = "\n".join(
        '          <li><a href="%s">%s</a></li>' % (url, html.escape(label))
        for label, url in post["related"]
    )
    return """
<header class="article-hero">
  <div class="container article-hero-inner">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <a href="/blog/">Blog</a> / <span>%(title)s</span></nav>
    <p class="eyebrow">%(eyebrow)s</p>
    <h1>%(title)s</h1>
    <p class="lead">%(lead)s</p>
    <div class="article-meta-line">
      <span>Thomas Lude</span><span>%(date)s</span><span>%(read)s Lesezeit</span>
    </div>
    <div class="blog-tags">%(tags)s</div>
  </div>
</header>

<section class="article-figure">
  <div class="container">
    <figure>
      %(image)s
      <figcaption>%(alt)s</figcaption>
    </figure>
  </div>
</section>

<section class="section article-section">
  <div class="container article-content">
    %(content)s
  </div>
</section>

<section class="section section-soft article-afterword">
  <div class="container article-afterword-grid">
    <div class="author-box">
      %(author_image)s
      <div>
        <p class="eyebrow">Über den Autor</p>
        <h2>Thomas Lude</h2>
        <p>Thomas arbeitet als Kartenleger und hellfühliger Berater in Friedrichshafen am Bodensee. Er verbindet Karten, intuitive Wahrnehmung und klare Gespräche – persönlich, telefonisch und bei Hausbesuchen.</p>
        <a class="link-more" href="/ueber-thomas-lude/">Mehr über Thomas</a>
      </div>
    </div>
    <div class="related-box">
      <h2>Passend dazu</h2>
      <ul>
%(related)s
      </ul>
    </div>
  </div>
</section>
%(cta)s
""" % {
        "title": html.escape(post["title"]),
        "eyebrow": html.escape(post["eyebrow"]),
        "lead": html.escape(post["lead"]),
        "date": html.escape(post["date"]),
        "read": html.escape(post["read_time"]),
        "tags": tags,
        "image": img(post["image"], post["alt"], sizes="(max-width: 960px) 100vw, 1040px", loading="eager", fetchpriority="high"),
        "alt": html.escape(post["alt"]),
        "content": post["content"],
        "author_image": img("thomas-lude-portrait-hund-friedrichshafen", "Thomas Lude mit seinem Golden Retriever", sizes="180px", css_class="author-image"),
        "related": related,
        "cta": cta_band("Möchtest du dein Thema persönlich besprechen?", "Schreib kurz, worum es geht – Thomas meldet sich persönlich und findet mit dir den passenden Rahmen."),
    }

# ----------------------------------------------------------------------------
# FAQ-SEITE
# ----------------------------------------------------------------------------
def faq_body():
    return """
<header class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Häufige Fragen</span></nav>
    <p class="eyebrow">Gut zu wissen</p>
    <h1>Häufige Fragen zum Kartenlegen mit Thomas</h1>
    <p class="lead">Kurz und ehrlich beantwortet – damit du weißt, was dich erwartet.</p>
  </div>
</header>

<section class="section">
  <div class="container">
    %(faq)s
    <div class="notice-box" style="margin-top:2.5rem;max-width:820px;">
      <p><strong>Ehrlich gesagt:</strong> Kartenlegen ist eine intuitive Beratung. Es ersetzt keine medizinische, juristische oder finanzielle Entscheidung – und keine seriöse Beratung verspricht dir eine sichere Zukunft.</p>
    </div>
  </div>
</section>
%(cta)s
""" % {
        "faq": faq_html(FAQ_MAIN),
        "cta": cta_band("Deine Frage war nicht dabei?", "Frag einfach direkt – Thomas antwortet persönlich."),
    }

# ----------------------------------------------------------------------------
# KONTAKT
# ----------------------------------------------------------------------------
def kontakt_body():
    return """
<header class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Kontakt</span></nav>
    <p class="eyebrow">Kontakt &amp; Termin</p>
    <h1>Was möchtest du wissen?</h1>
    <p class="lead">Manchmal beginnt Klarheit mit einem Gespräch. Schreib kurz, worum es geht – Thomas meldet sich persönlich zurück.</p>
  </div>
</header>

<section class="section">
  <div class="container contact-grid">
    <div>
      <h2>So erreichst du Thomas</h2>
      <p>Am schnellsten per WhatsApp – aber auch ein Anruf oder eine E-Mail ist willkommen. Sag einfach kurz, worum es geht, und ihr findet gemeinsam den passenden Rahmen.</p>
      <div class="contact-methods">
        <a class="contact-method" href="%(wa)s?text=%(wamsg)s" target="_blank" rel="noopener">
          %(waicon)s
          <div><strong>WhatsApp</strong><span>Am schnellsten – schreib einfach kurz dein Anliegen.</span></div>
        </a>
        <a class="contact-method" href="%(tel)s">
          %(phoneicon)s
          <div><strong>%(phone)s</strong><span>%(phonehint)sFür eine direkte Terminabsprache.</span></div>
        </a>
        <a class="contact-method" href="%(mail)s">
          %(mailicon)s
          <div><strong>%(email)s</strong><span>Wenn du es lieber schriftlich und in Ruhe magst.</span></div>
        </a>
      </div>
      <h2 style="margin-top:2.4rem;">Gut zu wissen</h2>
      <ul class="tick-list">
        <li>Persönliche Beratungen in Friedrichshafen – Adresse bei der Terminvereinbarung</li>
        <li>Telefonische Beratung nach Termin, von überall</li>
        <li>Kartenabende für Gruppen rund um den Bodensee</li>
        <li>30 Min. 79 € · 60 Min. 149 € · 90 Min. 219 € · 120 Min. 289 €</li>
        <li>Alles, was ihr besprecht, bleibt diskret</li>
      </ul>
    </div>
    <div class="form-card">
      <h2>Nachricht schreiben</h2>
      <!-- Hinweis: Statisches Formular. Für echten Versand Formspree.io (kostenlos) einbinden –
           siehe README.md. Alternativ funktionieren WhatsApp/E-Mail ohne weitere Einrichtung. -->
      <form action="https://formspree.io/f/DEIN-FORMULAR-CODE" method="post">
        <div class="field"><label for="k-name">Name</label><input type="text" id="k-name" name="name" required></div>
        <div class="field"><label for="k-mail">E-Mail</label><input type="email" id="k-mail" name="email" required></div>
        <div class="field"><label for="k-rueckruf">Rückrufnummer <span class="opt">(optional)</span></label><input type="tel" id="k-rueckruf" name="rueckrufnummer" placeholder="Für einen Rückruf, falls gewünscht"></div>
        <div class="field"><label for="k-thema">Worum geht es?</label>
          <select id="k-thema" name="thema">
            <option value="">Bitte wählen</option>
            <option value="beratung">Persönliche Beratung</option>
            <option value="telefon">Telefonische Beratung</option>
            <option value="event">Event / Kartenabend</option>
            <option value="tier">Tierbegleitung</option>
            <option value="sonstiges">Etwas anderes</option>
          </select>
        </div>
        <div class="field"><label for="k-personen">Anzahl Personen <span class="opt">(bei Events/Gruppen)</span></label><input type="number" id="k-personen" name="personen" min="1" max="30"></div>
        <div class="field"><label for="k-nachricht">Deine Nachricht</label><textarea id="k-nachricht" name="nachricht" required></textarea></div>
        <div class="field check">
          <input type="checkbox" id="k-ds" name="datenschutz" required>
          <label for="k-ds" style="font-weight:400;">Ich habe die <a href="/datenschutz/">Datenschutzerklärung</a> gelesen und bin mit der Verarbeitung meiner Daten zur Bearbeitung der Anfrage einverstanden.</label>
        </div>
        <button class="btn btn-gold" type="submit">Nachricht senden</button>
        <p class="form-note">Deine Nachricht wird vertraulich behandelt und nicht an Dritte weitergegeben.</p>
      </form>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container split">
    <div class="split-media">%(split)s</div>
    <div>
      <h2>Keine Frage ist zu klein.</h2>
      <p>Ob du nur kurz wissen willst, wie so eine Beratung abläuft, oder ob dich etwas Großes beschäftigt – schreib einfach. Thomas antwortet persönlich, nicht ein Callcenter.</p>
      <div class="cta-row">
        <a class="btn btn-whatsapp" href="%(wa)s" target="_blank" rel="noopener">%(waicon)s WhatsApp öffnen</a>
      </div>
    </div>
  </div>
</section>
""" % {
        "wa": WA_HREF, "wamsg": _urlencode("Hallo Thomas, ich interessiere mich für eine Beratung."),
        "waicon": icon("whatsapp", 22), "tel": TEL_HREF, "phoneicon": icon("phone", 22),
        "phone": PHONE, "phonehint": PHONE_HINT, "mail": MAIL_HREF, "mailicon": icon("mail", 22),
        "email": EMAIL,
        "split": img("thomas-lude-portrait-hund-friedrichshafen",
                     "Thomas Lude freundlich auf dem Sofa mit seinem Golden Retriever"),
    }


# ----------------------------------------------------------------------------
# RATGEBER (Übersicht – Artikel folgen nach und nach)
# ----------------------------------------------------------------------------
def ratgeber_body():
    topics = [
        ("Was passiert bei meiner ersten Kartenlegung?", "/faq-kartenlegen/"),
        ("Welche Fragen kann man beim Kartenlegen stellen?", "/faq-kartenlegen/"),
        ("Was Kartenlegen leisten kann – und was nicht", "/ueber-thomas-lude/"),
        ("Kartenlegen bei Liebe, Trennung und Beziehung", "/kartenlegen-liebe-partnerschaft/"),
        ("Kartenlegen am Telefon: Wie läuft das ab?", "/kartenlegen-telefonisch/"),
        ("Kartenlegen für einen Junggesellinnenabschied am Bodensee", "/kartenlegen-junggesellinnenabschied-bodensee/"),
        ("Ideen für einen besonderen Mädelsabend am Bodensee", "/events/"),
        ("Wie lange dauert eine Kartenlegung?", "/faq-kartenlegen/"),
        ("Was kostet Kartenlegen?", "/faq-kartenlegen/"),
        ("Energetische Tierbegleitung: Möglichkeiten und Grenzen", "/tier-mensch/"),
    ]
    cards = "\n".join(
        """      <article class="card">
        <div class="card-body">
          <h3><a href="%s">%s</a></h3>
          <p>Artikel in Vorbereitung – die wichtigsten Antworten findest du schon jetzt hier:</p>
          <a class="link-more" href="%s">Mehr erfahren</a>
        </div>
      </article>""" % (url, title, url)
        for title, url in topics
    )
    return """
<header class="page-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Startseite</a> / <span>Ratgeber</span></nav>
    <p class="eyebrow">Wissen &amp; Ratgeber</p>
    <h1>Ratgeber rund ums Kartenlegen</h1>
    <p class="lead">Ehrlich erklärt: Was passiert bei einer Kartenlegung, welche Fragen du stellen kannst und was Kartenlegen leisten kann – und was nicht.</p>
  </div>
</header>

<section class="section">
  <div class="container">
    <div class="card-grid three">
%s
    </div>
  </div>
</section>
""" % cards

# ----------------------------------------------------------------------------
# IMPRESSUM / DATENSCHUTZ / 404
# ----------------------------------------------------------------------------
def impressum_body():
    return """
<section class="section">
  <div class="container prose">
    <h1>Impressum</h1>
    <h2>Angaben gemäß § 5 DDG</h2>
    <p>Thomas Lude<br>Hindenburgstr. 1<br>88045 Friedrichshafen</p>
    <h2>Kontakt</h2>
    <p>Telefon: %s %s<br>E-Mail: %s</p>
    <h2>Umsatzsteuer</h2>
    <p>Kleinunternehmer im Sinne von § 19 Abs. 1 UStG. Es wird daher keine Umsatzsteuer berechnet und nicht gesondert ausgewiesen.</p>
    <h2>Verantwortlich für den Inhalt (§ 18 Abs. 2 MStV)</h2>
    <p>Thomas Lude, Anschrift wie oben.</p>
    <h2>Urheberrecht</h2>
    <p>Die durch den Seitenbetreiber erstellten Inhalte, Bilder und Werke auf dieser Website unterliegen dem deutschen Urheberrecht. Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung des jeweiligen Erstellers.</p>
    <h2>Haftungshinweis</h2>
    <p>Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.</p>
  </div>
</section>
""" % (PHONE, PHONE_HINT, EMAIL)

def datenschutz_body():
    return """
<section class="section">
  <div class="container prose">
    <h1>Datenschutzerklärung</h1>
    <h2>1. Verantwortlicher</h2>
    <p>Thomas Lude, Hindenburgstr. 1, 88045 Friedrichshafen, E-Mail: %s</p>
    <h2>2. Hosting</h2>
    <p>Diese Website wird über GitHub Pages (GitHub Inc.) bereitgestellt. Beim Aufruf werden technisch bedingt Verbindungsdaten (z. B. IP-Adresse) verarbeitet. Details siehe die Datenschutzhinweise von GitHub.</p>
    <h2>3. Kontaktformular</h2>
    <p>Das Kontaktformular wird über den Dienst Formspree (Formspree, Inc.) technisch abgewickelt, damit deine Anfrage per E-Mail bei Thomas ankommt. Es werden nur die von dir eingegebenen Daten übertragen. Details siehe die Datenschutzhinweise von Formspree.</p>
    <h2>4. Kontaktaufnahme</h2>
    <p>Bei Kontaktaufnahme per E-Mail, Telefon oder WhatsApp werden die angegebenen Daten ausschließlich zur Bearbeitung der Anfrage verarbeitet und nicht an Dritte weitergegeben.</p>
    <h2>5. Reichweitenmessung</h2>
    <p>Diese Website nutzt den datenschutzfreundlichen Analysedienst GoatCounter zur anonymen Auswertung von Seitenaufrufen. GoatCounter setzt keine Cookies, verwendet keine geräteübergreifende Wiedererkennung und speichert keine personenbezogenen Profile. IP-Adressen werden nicht gespeichert. Details siehe die Datenschutzhinweise von GoatCounter (goatcounter.com).</p>
  </div>
</section>
""" % EMAIL

def notfound_body():
    return """
<section class="section">
  <div class="container center">
    <p class="eyebrow">Fehler 404</p>
    <h1>Diese Seite gibt es nicht (mehr).</h1>
    <p class="lead" style="margin:0 auto;">Vielleicht hat sich die Adresse geändert. Hier geht es weiter:</p>
    <div class="cta-row center">
      <a class="btn btn-gold" href="/">Zur Startseite</a>
      <a class="btn btn-outline-dark" href="/kartenlegen-friedrichshafen/">Kartenlegen in Friedrichshafen</a>
      <a class="btn btn-ghost" href="/kontakt-termin/">Kontakt</a>
    </div>
  </div>
</section>
"""

# ----------------------------------------------------------------------------
# BUILD
# ----------------------------------------------------------------------------
def main():
    # Startseite
    write_page("", "Thomas Lude – Kartenlegen am Bodensee | Friedrichshafen",
               "Persönliche Kartenberatung mit Thomas Lude in Friedrichshafen am Bodensee. Direkt, diskret, ohne großes Theater – auch telefonisch und als Kartenabend für JGA & Events.",
               home_body(),
               hero_preload="/assets/img/thomas-lude-kartenleger-friedrichshafen-bodensee-768w.webp",
               extra_schema=[faq_schema(FAQ_MAIN)])

    # Landingpages
    for p in LANDING_PAGES:
        schema = [faq_schema(p["faq"])] if p.get("faq") else None
        write_page(p["slug"], p["title"], p["desc"],
                   landing_body(p["eyebrow"], p["h1"], p["lead"], p["image"], p["alt"],
                                p["prose"], p.get("faq"),
                                p.get("wa", "Hallo Thomas, ich interessiere mich für eine Beratung."),
                                p.get("cta_title", "Manchmal beginnt Klarheit mit einem Gespräch."),
                                p.get("cta_text", "Schreib kurz, worum es geht – Thomas meldet sich persönlich.")),
                   extra_schema=schema)

    # Sondersseiten
    write_page("events", "Kartenlegen für Events am Bodensee | Thomas Lude",
               "Kartenlegen für JGA, Mädelsabend, Geburtstag und private Feiern am Bodensee. Thomas Lude kommt mit den Karten zu euch – Anfrage hier.",
               events_body())
    write_page("kartenlegen-junggesellinnenabschied-bodensee",
               "Kartenlegen für JGA am Bodensee | Thomas Lude",
               "Kartenlegen für euren Junggesellinnenabschied am Bodensee: Ihr habt den Prosecco, Thomas bringt die Karten. Jetzt Kartenabend anfragen.",
               jga_body())
    write_page("tier-mensch", "Energetische Tierbegleitung am Bodensee | Thomas Lude",
               "Energetische Begleitung für Tiere und ihre Menschen am Bodensee – ruhig und achtsam. Ergänzend zur tierärztlichen Versorgung.",
               tier_body())
    write_page("ergaenzende-impulse", "Wenn ein zweiter Blick hilft | Ergänzende Impulse | Thomas Lude",
               "Thomas' Kartenlegung steht für sich. Für einzelne Themen verweist er ergänzend auf ausgewählte andere Systeme wie VortexKey sowie auf behutsame Impulse zu beruflichen und finanziellen Entscheidungen.",
               ergaenzende_impulse_body())
    write_page("vortexkey-kompass", "Der VortexKey Kompass | Thomas Lude",
               "Eine Erklärung von Thomas' Kooperationspartner VortexKey, in dessen eigenen Worten: warum die Kombination aus Kristinas Human-Design-Perspektive und Thomas' Kartenlegung Sinn ergibt.",
               kompass_body())
    write_page("ueber-thomas-lude", "Thomas Lude – Kartenleger am Bodensee | Über mich",
               "Thomas Lude ist Kartenleger aus Friedrichshafen: bodenständig, direkt und diskret. Erfahre, wie er arbeitet und was dich erwartet.",
               ueber_body())
    write_page("erfahrungen", "Erfahrungen mit Thomas Lude | Kartenlegen am Bodensee",
               "Was Menschen nach einer Beratung mit Thomas Lude sagen: Erfahrungen zu Kartenlegen, Events und Tierbegleitung am Bodensee.",
               erfahrungen_body())
    write_page("faq-kartenlegen", "Häufige Fragen zum Kartenlegen (FAQ) | Thomas Lude",
               "Antworten auf häufige Fragen: Ablauf, Dauer, Kosten, Telefonberatung und Kartenabende – ehrlich beantwortet von Thomas Lude.",
               faq_body(), extra_schema=[faq_schema(FAQ_MAIN)])
    write_page("ratgeber", "Ratgeber rund ums Kartenlegen | Thomas Lude",
               "Ehrlich erklärt: Was passiert bei einer Kartenlegung, welche Fragen kann man stellen, was kostet Kartenlegen – Ratgeber von Thomas Lude.",
               ratgeber_body())
    write_page("blog", "Blog: Hellfühligkeit, Raumklärung & Sinnfragen | Thomas Lude",
               "Persönliche Blogbeiträge von Thomas Lude über Hellfühligkeit, energetische Raumklärung, Verlust, Wiedergeburt, karmische Aufgaben und mediale Grenzen.",
               blog_body(),
               hero_preload="/assets/img/%s-768w.webp" % BLOG_POSTS[0]["image"],
               extra_schema=[blog_overview_schema()])
    for post in BLOG_POSTS:
        write_page("blog/" + post["slug"], post["meta_title"], post["desc"],
                   article_body(post),
                   hero_preload="/assets/img/%s-768w.webp" % post["image"],
                   extra_schema=[blog_schema(post)])
    write_page("kontakt-termin", "Kontakt & Termin | Thomas Lude – Kartenlegen am Bodensee",
               "Termin bei Thomas Lude anfragen: per WhatsApp, Telefon oder Formular. Persönliche Beratung in Friedrichshafen, telefonisch überall.",
               kontakt_body())
    write_page("impressum", "Impressum | Thomas Lude",
               "Impressum von Thomas Lude – Kartenlegen am Bodensee, Friedrichshafen.",
               impressum_body())
    write_page("datenschutz", "Datenschutzerklärung | Thomas Lude",
               "Datenschutzerklärung von Thomas Lude – Kartenlegen am Bodensee, Friedrichshafen.",
               datenschutz_body())

    # 404.html (Wurzel – GitHub Pages nutzt sie automatisch)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(layout("404", "Seite nicht gefunden | Thomas Lude",
                       "Diese Seite gibt es nicht. Zur Startseite von Thomas Lude – Kartenlegen am Bodensee.",
                       notfound_body()).replace('href="/assets', 'href="/assets').replace(
                           'rel="canonical" href="' + SITE_URL + '/404/"',
                           'rel="canonical" href="' + SITE_URL + '/404.html"'))
    print("gebaut: /404.html")

    # robots.txt
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)

    # sitemap.xml
    slugs = [""] + [p["slug"] for p in LANDING_PAGES] + [
        "events", "kartenlegen-junggesellinnenabschied-bodensee", "tier-mensch", "ergaenzende-impulse",
        "vortexkey-kompass",
        "ueber-thomas-lude", "erfahrungen", "faq-kartenlegen", "ratgeber",
        "blog", "kontakt-termin", "impressum", "datenschutz",
    ] + ["blog/" + p["slug"] for p in BLOG_POSTS]
    urls = "\n".join(
        "  <url><loc>%s/%s</loc></url>" % (SITE_URL, (s + "/") if s else "")
        for s in slugs
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % urls)

    # llms.txt (optional, kein Rankingfaktor – hilft Antwortsystemen beim Einordnen)
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("""# Thomas Lude – Kartenlegen am Bodensee

Thomas Lude ist Kartenleger aus Friedrichshafen am Bodensee.
Er bietet an: persönliche Kartenberatung in Friedrichshafen, telefonische
Kartenberatung (bundesweit und in der Schweiz erreichbar), Kartenabende für
Events (JGA, Mädelsabend, Geburtstage) rund um den Bodensee sowie energetische
Tierbegleitung (kein Ersatz für tierärztliche Behandlung).

Einzugsgebiet: Bodenseeregion (Friedrichshafen, Meersburg, Überlingen,
Konstanz, Lindau, Ravensburg) persönlich; telefonisch auch für Kundinnen und
Kunden aus München, Augsburg, Ulm, Memmingen sowie Zürich und der Schweiz.

Kernbotschaft: Manchmal braucht es einen anderen Blick.
Haltung: Keine Heils- oder Zukunftsversprechen, keine Angstmache, Diskretion.
Kontakt: {phone}, {email}

## Wichtige Seiten
- Startseite: {u}/
- Kartenlegen Friedrichshafen: {u}/kartenlegen-friedrichshafen/
- Kartenlegen München: {u}/kartenlegen-muenchen/
- Kartenlegen Augsburg: {u}/kartenlegen-augsburg/
- Kartenlegen Ulm: {u}/kartenlegen-ulm/
- Kartenlegen Memmingen: {u}/kartenlegen-memmingen/
- Kartenlegen Zürich & Schweiz: {u}/kartenlegen-zuerich/
- Telefonische Beratung: {u}/kartenlegen-telefonisch/
- JGA am Bodensee: {u}/kartenlegen-junggesellinnenabschied-bodensee/
- Hausbesuch & Raumklärung: {u}/hausbesuch-raumklaerung/
- Tier & Mensch: {u}/tier-mensch/
- Ergänzende Impulse (u.a. VortexKey, berufliche/finanzielle Entscheidungen): {u}/ergaenzende-impulse/
- Blog: {u}/blog/
- Kontakt: {u}/kontakt-termin/

## Blog-Beiträge
{blog_lines}
""".format(
            phone=PHONE, email=EMAIL, u=SITE_URL,
            blog_lines="\n".join("- %s: %s/blog/%s/" % (p["title"], SITE_URL, p["slug"]) for p in BLOG_POSTS),
        ))

    # .nojekyll (GitHub Pages: Jekyll-Verarbeitung abschalten)
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    print("\nFertig. %d Seiten + 404 gebaut." % (len(slugs)))

if __name__ == "__main__":
    main()
