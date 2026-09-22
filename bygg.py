"""Genererer bloggens filer. Kjør: python bygg.py
Innlegg legges til i POSTS nederst, så kjører du skriptet på nytt."""
import os, html

BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{BASE}/innlegg", exist_ok=True)
os.makedirs(f"{BASE}/bilder", exist_ok=True)

def w(path, text):
    with open(f"{BASE}/{path}", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

# ---------- Innlegg (nyeste først). Bytt ut med egne. ----------
# Mal for nytt innlegg (kopier inn i listen):
# dict(slug="url-navn", img="bildefil", cats=["Fotturer"], rain=False, date="2026-09-14", label="14. september 2026",
#      title="Tittel", lead="Kort ingress.", body="<p>Tekst</p><h2>Mellomtittel</h2><p>Mer tekst</p>"),
POSTS = []
POSTS.sort(key=lambda p: p["date"], reverse=True)

# ---------- Bilder (plassholdere: bytt ut med egne .jpg og endre img-navn) ----------
def scene(name, bg, sun, c1, c2, hill):
    w(f"bilder/{name}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450"><rect width="800" height="450" fill="{bg}"/><circle cx="640" cy="90" r="46" fill="{sun}" opacity=".9"/><path d="M0 330 Q200 270 400 320 T800 300 V450 H0Z" fill="{hill}" opacity=".55"/><polygon points="120,380 120,230 190,170 260,230 260,380" fill="{c1}"/><polygon points="270,380 270,250 340,190 410,250 410,380" fill="{c2}"/><polygon points="420,380 420,220 495,155 570,220 570,380" fill="{sun}"/><rect x="175" y="250" width="30" height="30" fill="{bg}"/><rect x="325" y="270" width="30" height="30" fill="{bg}"/><rect x="480" y="245" width="30" height="30" fill="{bg}"/><rect y="380" width="800" height="70" fill="#1B2932" opacity=".85"/></svg>''')
w("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#EAEEED"/><polygon points="12,52 12,30 32,12 52,30 52,52" fill="#A8372A"/><rect x="26" y="34" width="12" height="12" fill="#EAEEED"/></svg>')

# ---------- Stil ----------
w("style.css", r'''
:root{color-scheme:light;--bg:#FAF8F2;--surface:#FFFFFF;--mint:#CDEBDD;--ink:#1B2932;--muted:#55666F;--line:#C3CDCC;--accent:#A8372A;--focus:#2F6F8F;--ok:#4C7A5A;
--display:"Bricolage Grotesque","Trebuchet MS",system-ui,sans-serif;--body:"Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:20px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 var(--body)}
img{max-width:100%;display:block}
a{color:inherit}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px;border-radius:6px}
button,input,textarea{font:inherit;color:inherit}

.layout{display:grid;grid-template-columns:240px minmax(0,1fr);column-gap:56px;row-gap:56px;max-width:1080px;margin:0 auto;padding:40px clamp(16px,4vw,32px) 48px}
.layout.has-hero{row-gap:22px}
.hero-banner{grid-column:1/-1;border-radius:16px;overflow:hidden;height:clamp(200px,28vw,360px);background:var(--line)}
.hero-banner img{width:100%;height:100%;object-fit:cover;object-position:center 38%}
.side{position:sticky;top:40px;align-self:start}
.has-hero .side{margin-top:-78px;z-index:2}
.brand{position:relative;background:var(--mint);border-radius:16px;padding:22px 20px 24px;font-family:var(--display);font-weight:700;font-size:2.3rem;line-height:1;letter-spacing:-.03em;text-decoration:none;display:block;text-wrap:balance;box-shadow:0 10px 26px rgba(27,41,50,.16)}
.street{width:100%;height:auto;display:block;margin-bottom:18px}
.street .g{stroke:var(--ink);stroke-width:2}.street .w{fill:var(--mint)}
.nav{margin-top:28px;display:grid;gap:4px;font:.82rem var(--mono);letter-spacing:.06em;text-transform:uppercase}
.nav a{color:var(--muted);text-decoration:none;padding:6px 0;border-bottom:1.5px solid transparent;width:max-content}
.nav a:hover{color:var(--ink);border-bottom-color:var(--ink)}

.filters{margin:0 0 36px;display:grid;gap:12px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:transparent;border:1.5px solid var(--line);border-radius:999px;padding:6px 16px;font-size:.9rem;font-weight:500;color:var(--muted);cursor:pointer}
.chip:hover{border-color:var(--muted)}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.chip.rain[aria-pressed="true"]{background:var(--focus);border-color:var(--focus)}
.fmeta{display:flex;gap:14px;align-items:center;font-size:.9rem;color:var(--muted)}
.fmeta button{background:none;border:0;text-decoration:underline;cursor:pointer;color:var(--muted);padding:0}
.none{color:var(--muted)}
[hidden]{display:none!important}
.cats{display:block;font:.75rem var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-top:14px}
.cats+.date{margin-top:4px}
.posts{display:grid;gap:56px}
.card{display:block;text-decoration:none}
.card .img{border-radius:12px;overflow:hidden;background:var(--line);aspect-ratio:16/9}
.card img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.card:hover img{transform:scale(1.03)}
.date{display:block;font:.8rem var(--mono);color:var(--muted);letter-spacing:.04em;margin-top:16px}
.card h2{font:700 clamp(1.5rem,3vw,2rem)/1.15 var(--display);letter-spacing:-.015em;margin:6px 0 0;text-wrap:balance}
.card:hover h2{color:var(--accent)}
.card p{margin:8px 0 0;color:var(--muted);max-width:60ch}

.section{margin-top:72px;padding-top:44px;border-top:1px dashed var(--line)}
.section h2.h{font:700 1.8rem/1.1 var(--display);letter-spacing:-.015em;margin:0 0 20px}
.section p{max-width:60ch}
.lead{font-size:1.2rem;line-height:1.5}

.article .hero{border-radius:12px;overflow:hidden;aspect-ratio:16/9;background:var(--line)}
.article .hero img{width:100%;height:100%;object-fit:cover}
.article h1{font:700 clamp(2rem,5vw,3.2rem)/1.05 var(--display);letter-spacing:-.025em;margin:8px 0 0;text-wrap:balance}
.article .body{margin-top:24px;max-width:62ch;font-size:1.08rem}
.article .body p{margin:0 0 1.1em}
.article .body h2{font:700 1.4rem/1.2 var(--display);margin:1.6em 0 .5em}
.back{display:inline-block;margin-top:40px;font:.85rem var(--mono);letter-spacing:.04em;color:var(--muted)}

form{display:grid;gap:18px;max-width:560px}
.field{display:grid;gap:6px}
.field label{font-weight:600;font-size:.95rem}
.field input,.field textarea{width:100%;background:var(--surface);border:1.5px solid var(--line);border-radius:10px;padding:11px 14px}
.field textarea{min-height:150px;resize:vertical}
.field [aria-invalid="true"]{border-color:var(--accent)}
.err{margin:0;color:var(--accent);font-size:.85rem}.err:empty{display:none}
.btn{background:var(--ink);color:var(--bg);border:0;border-radius:999px;padding:12px 26px;font-weight:600;cursor:pointer}
.btn:hover{background:var(--focus)}
.status{margin:12px 0 0;font-size:.92rem}.status.ok{color:var(--ok);font-weight:500}
.hint{font-size:.85rem;color:var(--muted);margin:0}
footer{margin-top:64px;padding-top:20px;border-top:1px dashed var(--line);font:.8rem var(--mono);color:var(--muted)}

@media(max-width:820px){
 .brand{font-size:1.8rem;padding:16px 16px 18px}.street{max-width:220px;margin-bottom:12px}
 .layout{grid-template-columns:minmax(0,1fr);gap:28px;padding-top:20px}
 .layout.has-hero{row-gap:16px}
 .hero-banner{height:clamp(160px,52vw,220px)}
 .has-hero .side{margin-top:-40px}
 .side{position:static}
 .nav{margin-top:14px;display:flex;gap:18px}
 .posts{gap:44px}.section{margin-top:56px}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
''')

# ---------- Felles hode ----------
def head(title, desc, pre, img, hero=None):
    t, d = html.escape(title), html.escape(desc)
    og = f'<meta property="og:image" content="{pre}bilder/{img}.svg">' if img else (f'<meta property="og:image" content="{pre}bilder/{hero}">' if hero else '')
    hero_html = f'<div class="hero-banner"><img src="{pre}bilder/{hero}" alt="Historisk kobberstikk av Bergen, sett fra sjøsiden" loading="eager"></div>' if hero else ''
    return f'''<!doctype html>
<html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{d}">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">{og}
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Mono:wght@400&family=Instrument+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{pre}style.css"></head><body><div class="layout{' has-hero' if hero else ''}">
{hero_html}<header class="side"><a class="brand" href="{pre}index.html"><svg class="street" viewBox="0 0 300 74" role="img" aria-label="Trehusene på Bryggen"><polygon fill="#C08A1E" points="0,72 0,34 23,10 46,34 46,72"/><rect class="w" x="19" y="26" width="8" height="8"/><rect class="w" x="17" y="46" width="12" height="12"/><polygon fill="#B23A2B" points="50,72 50,36 73,14 96,36 96,72"/><rect class="w" x="69" y="28" width="8" height="8"/><rect class="w" x="67" y="48" width="12" height="12"/><polygon fill="#F7F5EE" stroke="#A9BDB3" points="100,72 100,32 123,8 146,32 146,72"/><rect class="w" x="119" y="24" width="8" height="8"/><rect class="w" x="117" y="44" width="12" height="12"/><polygon fill="#2F6F8F" points="150,72 150,35 173,12 196,35 196,72"/><rect class="w" x="169" y="27" width="8" height="8"/><rect class="w" x="167" y="47" width="12" height="12"/><polygon fill="#C08A1E" points="200,72 200,34 223,10 246,34 246,72"/><rect class="w" x="219" y="26" width="8" height="8"/><rect class="w" x="217" y="46" width="12" height="12"/><polygon fill="#4C7A5A" points="250,72 250,37 273,15 296,37 296,72"/><rect class="w" x="269" y="29" width="8" height="8"/><rect class="w" x="267" y="49" width="12" height="12"/><line class="g" x1="0" y1="73" x2="300" y2="73"/></svg>Joa's Bergen</a>
<nav class="nav" aria-label="Meny"><a href="{pre}index.html#om">Om meg</a><a href="{pre}index.html#kontakt">Kontakt</a></nav></header>
'''

FOOT = '<footer>&copy; 2026 Joa &middot; Laget i Bergen</footer>'

import glob
for old in glob.glob(f"{BASE}/innlegg/*.html"):
    os.remove(old)
for p in POSTS:
    w(f"innlegg/{p['slug']}.html", head(f"{p['title']} – Joa's Bergen", p["lead"], "../", p["img"]) + f'''<main><article class="article"><div class="hero"><img src="../bilder/{p['img']}.svg" alt=""></div>
<span class="cats">{' · '.join(p['cats'])}{' · Regnværsdag' if p['rain'] else ''}</span><time class="date" datetime="{p['date']}">{p['label']}</time><h1>{html.escape(p['title'])}</h1>
<div class="body"><p><strong>{html.escape(p['lead'])}</strong></p>{p['body']}</div>
<a class="back" href="../index.html">&larr; Alle innlegg</a></article>
{FOOT}</main></div></body></html>
''')

cards = "\n".join(
    f'''<a class="card" href="innlegg/{p['slug']}.html" data-cats="{'|'.join(p['cats'])}" data-rain="{int(p['rain'])}"><div class="img"><img src="bilder/{p['img']}.svg" alt="" loading="lazy"></div><span class="cats">{' · '.join(p['cats'])}{' · Regnværsdag' if p['rain'] else ''}</span><time class="date" datetime="{p['date']}">{p['label']}</time><h2>{html.escape(p['title'])}</h2><p>{html.escape(p['lead'])}</p></a>'''
    for p in POSTS)

empty = "" if POSTS else '<p class="none">Innleggene kommer snart.</p>'
CATS = sorted(["Byvandring", "Fotturer", "Historie", "Leserinnlegg", "Mat og drikke", "Solforhold"], key=str.casefold)
chips = "".join(f'<button type="button" class="chip" aria-pressed="false" data-cat="{c}">{c}</button>' for c in CATS) + '<button type="button" class="chip rain" aria-pressed="false">☔ Regnværsdag</button>'

w("index.html", head("Joa's Bergen – blogg", "Blogg om Bergen: mat, turer og historie.", "", "", hero="forside.webp") + f'''<main>
<div class="filters" role="group" aria-label="Filtrer innlegg"{" hidden" if not POSTS else ""}>
<div class="chips">{chips}</div>
<div class="fmeta"><span id="count" aria-live="polite"></span><button type="button" id="reset" hidden>Nullstill filter</button></div></div>
<div class="posts">
{cards}
</div>{empty}<p class="none" id="none" hidden>Ingen innlegg passer med filtrene dine.</p>
<section class="section" id="om"><h2 class="h">Om meg</h2>
<p>4de generasjons bergenser. Oppvokst ved foten av fjellsiden, nedenfor Skansen brannstasjon. Nabolaget heter Fjellet, men de færreste kaller det for, eller i det hele tatt vet at det heter det.</p>
<p>Eg er en drømmer, bergensnostalgiker, for ikke å si: en urban melankoliker. Noen kunne til og med sagt: en kontrafaktisk historiker, men eg er ingen historiker. Eg tenker mye på hvordan byen ville ha sett ut hvis det ikke hadde for alle bybrannene (er det derfor forballaget heter Brann?). Hvordan hadde det vært her, hvis den kalde arkitekturen fra 60-tallet ikke hadde fått herje? Men for all del, det kunne vært mye verre, ta Oslo for eksempel. Men nok om det.</p>
<p>Eg tenker på gamle hotell Norge. Bygget i 1885, som overlevde både bybrannen i 1916 og andre verdenskrig, da det hovedsakelig huset tyske offiserer. Revet i 1961 til fordel for dagens koordinatsystem i betong. Nei, gamle hotell Norge lå der nye hotell Norge ligger i dag, eg blandet med annet, like flott bygg som lå der Gulatinget ligger, nemlig Hotel Metropol, et hotell eg også tenker på. En (ukjent) bergensavis sa det kanskje best da dets på en gang imponerende og tiltrekkende ytre, lyser og liver opp i en av vårs by vakreste kvartaler med marmorets dans og fargevirkningens harmoni. Det var også 60 værelser.</p>
<p>Takk</p>
<p>J</p></section>
<section class="section" id="kontakt"><h2 class="h">Kontakt</h2>
<p>Fortell kort hva du lurer på, så svarer jeg så snart jeg kan.</p>
<form id="contact" name="kontakt" method="POST" data-netlify="true" netlify-honeypot="bot" novalidate>
<input type="hidden" name="form-name" value="kontakt"><p hidden><label>Ikke fyll ut: <input name="bot"></label></p>
<div class="field"><label for="n">Navn</label><input id="n" name="navn" type="text" autocomplete="name" required><p class="err" id="en" role="alert"></p></div>
<div class="field"><label for="e">E-post</label><input id="e" name="epost" type="email" autocomplete="email" required><p class="err" id="ee" role="alert"></p></div>
<div class="field"><label for="m">Melding</label><textarea id="m" name="melding" required></textarea><p class="err" id="em" role="alert"></p></div>
<div><button class="btn" type="submit">Send melding</button><p class="status" id="st" aria-live="polite"></p></div>
</form></section>
{FOOT}</main></div>
<script>
var chips=[].slice.call(document.querySelectorAll(".chip")),cards=[].slice.call(document.querySelectorAll(".card")),cnt=document.getElementById("count"),none=document.getElementById("none"),rs=document.getElementById("reset");
function filt(){{var cats=chips.filter(function(c){{return c.dataset.cat&&c.getAttribute("aria-pressed")==="true"}}).map(function(c){{return c.dataset.cat}}),rain=document.querySelector(".chip.rain").getAttribute("aria-pressed")==="true",n=0;
cards.forEach(function(k){{var ok=(!cats.length||cats.some(function(c){{return k.dataset.cats.split("|").indexOf(c)>-1}}))&&(!rain||k.dataset.rain==="1");k.hidden=!ok;if(ok)n++}});
cnt.textContent=n+" innlegg";none.hidden=n>0;rs.hidden=!(cats.length||rain)}}
if(cards.length){{chips.forEach(function(c){{c.addEventListener("click",function(){{c.setAttribute("aria-pressed",c.getAttribute("aria-pressed")==="true"?"false":"true");filt()}})}});
rs.addEventListener("click",function(){{chips.forEach(function(c){{c.setAttribute("aria-pressed","false")}});filt()}});filt()}}
var f=document.getElementById("contact"),st=document.getElementById("st");
function chk(id,eid,ok,msg){{var i=document.getElementById(id),v=i.value.trim(),r=ok(v);document.getElementById(eid).textContent=r?"":msg;if(r)i.removeAttribute("aria-invalid");else i.setAttribute("aria-invalid","true");return r}}
f.addEventListener("submit",function(x){{x.preventDefault();st.textContent="";st.className="status";
var a=chk("n","en",function(v){{return v}},"Skriv inn navnet ditt."),b=chk("e","ee",function(v){{return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v)}},"Skriv inn en gyldig e-postadresse."),c=chk("m","em",function(v){{return v.length>=5}},"Skriv en kort melding.");
if(!(a&&b&&c))return;
var btn=f.querySelector("button");btn.disabled=true;
fetch("/",{{method:"POST",headers:{{"Content-Type":"application/x-www-form-urlencoded"}},body:new URLSearchParams(new FormData(f)).toString()}}).then(function(r){{if(!r.ok)throw 0;st.className="status ok";st.textContent="Takk! Meldingen er sendt.";f.reset()}}).catch(function(){{st.textContent="Noe gikk galt. Prøv igjen, eller send e-post direkte."}}).then(function(){{btn.disabled=false}})}});
</script></body></html>
''')
print("Ferdig")
