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
# dict(slug="url-navn", img="bildefil.webp/.jpg/.svg", cats=["Fotturer"], rain=False, date="2026-09-14", label="14. september 2026",
#      title="Tittel", lead="Kort ingress.", body="<p>Tekst</p><h2>Mellomtittel</h2><p>Mer tekst</p>"),
# Legg til kart=True for å sette inn det interaktive bydelskartet i innlegget.
# enkel=True: ingen stort bilde øverst i innlegget, og kortet på forsiden viser kun overskrift.
POSTS = [
    dict(slug="strok-eller-nabolag", img="strok-kart.webp", cats=["Historie"], rain=False,
         date="2026-09-22", label="22. september 2026",
         title="Strøk eller nabolag i Bergen",
         lead="Et interaktivt kart over strøkene i sentrum av Bergen.",
         body="<p>Bergen sentrum er delt opp i en mengde små strøk og nabolag, og de færreste vet nøyaktig hvor grensene mellom dem går. Under er et forsøk på å tegne dem opp.</p>",
         kart=True, enkel=True),
]
POSTS.sort(key=lambda p: p["date"], reverse=True)

# ---------- Interaktivt kart (bydeler i sentrum). Formene er trukket ut fra bergenskart.webp.
# nøkkel = bydelsnavn (må matche "navn" i BYDELER under).
BYDEL_INFO = {
    "Nordnes":     dict(nabolag="Nordnes", gate="Strandgaten & C. Sundts gate"),
    "Verftet":     dict(nabolag="Nordnes", gate="Galgebakken"),
    "Nøstet":      dict(nabolag="Sentrum", gate="Nøstegaten"),
    "Engen":       dict(nabolag="Sentrum", gate="Håkonsgaten"),
    "Strandsiden": dict(nabolag="Nordnes", gate="Strandkaien"),
    "Sydnes":      dict(nabolag="Sentrum eller (Nygårds)Høyden", gate="Christies gate"),
    "Møhlenpris":  dict(nabolag="Møhlenpris", gate="Welhavens gate"),
    "Nygård":      dict(nabolag="Nygård", gate="Nygårdsgaten, Lars Hilles gate"),
    "Sentrum":     dict(nabolag="Sentrum", gate="Torgallmenningen"),
    "Kalfaret":    dict(nabolag="Kalfaret/Haukeland", gate="Kalfarveien"),
    "Skansen":     dict(nabolag="Skansen/Fjellsiden", gate="Fjellveien"),
    "Marken":      dict(nabolag="Marken", gate="Kong Oscars gate"),
    "Vågsbunnen":  dict(nabolag="Sentrum", gate="Skostredet, Lille Øvregaten"),
    "Fjellet":     dict(nabolag="Sentrum", gate="Vetrlidsallmenningen"),
    "Bryggen":     dict(nabolag="Bryggen", gate="Øvregaten"),
    "Bergenhus":   dict(nabolag="Bryggen / Skuteviken", gate="Bontelabo"),
    "Skuteviken":  dict(nabolag="Sandviken", gate="Sjøgaten"),
    "Stølen":      dict(nabolag="Sandviken", gate="Steinkjellergaten"),
    "Eidemarken":  dict(nabolag="Sandviken/Skansen", gate="Henrik Wergelandsgate"),
    "Ladegården":  dict(nabolag="Sandviken", gate="Ladegårdsgaten/Nye Sandviksvei"),
    "Sandviken":   dict(nabolag="Sandviken", gate="Sandviksveien"),
}
MAP_W, MAP_H = 505, 330
BYDELER = [
    dict(navn="Ytre Sandviken", points="19.7,26.1 23.2,24.0 45.1,26.1 50.8,19.8 64.9,21.2 76.9,31.8 86.1,32.5 91.1,37.4 103.1,41.0 129.3,41.0 142.7,36.0 149.1,37.4 158.2,45.2 170.3,50.2 178.0,59.4 188.7,64.3 192.9,68.6 190.8,81.3 192.2,88.4 184.4,93.3 173.1,93.3 174.5,99.7 180.2,106.7 177.3,110.3 172.4,110.3 166.7,104.6 160.4,102.5 156.8,99.0 156.8,94.7 146.9,87.6 143.4,89.1 145.5,94.7 144.1,98.3 132.1,96.8 126.4,91.2 125.0,86.9 111.6,86.2 104.5,82.0 103.1,79.2 91.1,74.2 88.9,70.7 84.0,70.7 78.3,73.5 74.1,72.8 45.8,61.5 42.3,57.9 45.8,55.1 43.7,50.9 45.8,44.5 23.2,30.4 19.7,26.1", cx=116.1, cy=67.2),
    dict(navn="Sandviken", points="191.5,69.3 193.6,67.1 204.9,67.8 221.9,76.3 237.4,77.7 257.9,91.2 275.6,99.0 278.5,102.5 250.9,125.8 248.8,125.8 246.6,122.3 236.0,118.8 227.5,120.2 224.0,115.9 232.5,110.3 235.3,111.7 252.3,94.0 250.9,93.3 245.2,97.5 233.9,109.6 232.5,102.5 226.8,96.8 219.8,96.1 219.1,97.5 221.9,101.1 216.9,102.5 215.5,101.1 216.9,96.8 213.4,97.5 209.9,92.6 206.3,91.9 202.8,88.4 192.9,89.8 189.4,84.8 191.5,69.3", cx=226.3, cy=97.3),
    dict(navn="Sydnes", points="265.7,223.4 287.6,225.5 287.6,229.1 284.1,228.4 281.3,231.2 283.4,234.0 300.4,237.6 303.2,231.9 314.5,219.2 315.2,212.1 310.3,207.1 290.5,207.9 285.5,211.4 279.9,211.4 275.6,215.6 266.4,216.3 264.3,218.5", cx=288.0, cy=221.2),
    dict(navn="Møhlenpris", points="312.4,222.7 315.9,219.2 324.4,221.3 340.7,220.6 343.5,223.4 341.4,227.7 315.9,227.7 317.3,231.2 323.7,231.9 329.4,229.8 342.8,229.8 344.9,231.2 347.0,229.1 354.1,229.1 362.6,220.6 365.4,221.3 369.7,226.2 361.9,235.4 352.0,238.3 346.3,239.0 343.5,236.8 337.8,239.7 310.3,239.7 303.9,239.0 302.5,234.0 312.4,222.7", cx=335.5, cy=229.5),
    dict(navn="Gyldenpris", points="307.4,247.5 310.3,244.6 318.1,243.9 348.5,243.9 349.9,253.1 347.0,255.9 347.7,265.1 336.4,270.8 323.7,270.8 322.3,272.2 323.0,277.2 317.3,280.7 310.3,270.8 311.0,257.4 306.7,253.1 307.4,247.5", cx=324.2, cy=259.7),
    dict(navn="Nygård", points="322.3,191.6 317.2,193.3 318.1,194.4 315.9,203.6 312.7,206.8 312.4,207.9 315.2,212.1 314.5,217.0 316.6,219.2 328.0,222.0 341.4,221.3 346.3,227.7 348.5,227.7 359.1,224.1 363.3,218.5 366.1,218.5 369.7,214.9 371.8,206.4 369.0,195.8 372.1,189.7 369.7,188.8 365.4,184.5 353.4,181.0 342.1,181.0 339.6,178.5 330.8,187.4 327.2,187.4 326.8,187.0", cx=340.5, cy=203.1),
    dict(navn="Kalfaret", points="354.1,173.9 342.8,173.9 339.3,176.0 339.3,178.2 342.1,181.0 353.4,181.0 365.4,184.5 369.7,188.8 375.3,190.9 383.1,185.9 393.0,184.5 398.7,171.8 408.6,170.4 411.4,167.6 414.2,149.9 407.9,142.1 394.4,144.9 392.3,149.2 394.4,152.0 390.2,150.6 390.2,147.0 388.8,145.6 371.8,144.9 364.0,151.3 354.8,150.6 352.7,152.7", cx=376.6, cy=165.0),
    dict(navn="Damsgård", points="243.8,250.3 247.3,247.5 254.4,254.5 265.7,255.2 265.0,251.7 270.0,248.2 280.6,248.9 289.8,243.9 306.7,244.6 308.2,254.5 311.7,258.1 311.0,271.5 320.2,284.2 312.4,290.6 308.2,289.2 306.0,292.7 296.1,294.1 294.0,297.7 280.6,290.6 266.4,287.8 257.2,280.0 243.1,277.2 236.7,269.4 239.6,265.8 244.5,266.5 245.2,260.9 241.0,256.6 243.8,250.3", cx=274.6, cy=267.2),
    dict(navn="Kringsjå", points="187.2,261.6 193.6,256.6 200.7,255.9 207.0,262.3 210.6,262.3 213.4,255.2 212.7,250.3 215.5,247.5 221.9,245.3 241.7,244.6 243.1,246.0 239.6,251.7 234.6,253.8 240.3,255.9 245.2,260.9 243.1,266.5 236.7,267.3 236.7,270.8 241.7,276.4 236.0,283.5 219.1,284.9 207.0,283.5 194.3,273.6 187.2,261.6", cx=221.2, cy=261.6),
    dict(navn="Solheim", points="349.2,246.7 351.3,244.6 373.2,242.5 375.3,239.7 371.1,235.4 371.1,230.5 374.6,226.9 378.9,230.5 398.7,239.0 408.6,248.9 412.1,246.0 411.4,238.3 412.8,236.8 424.8,239.7 431.2,246.0 435.4,247.5 435.4,257.4 437.6,262.3 446.7,268.7 446.0,275.0 452.4,281.4 452.4,284.2 464.4,294.1 444.6,308.3 439.7,309.7 422.7,294.1 376.0,265.8 348.5,266.5 346.3,264.4 345.6,255.9 349.2,253.8 349.2,246.7", cx=401.1, cy=257.1),
    dict(navn="Kronstad", points="378.9,230.5 398.7,239.0 408.6,248.9 412.8,245.3 412.1,236.8 419.2,239.7 426.2,239.7 430.5,245.3 446.7,254.5 451.0,253.1 455.2,255.2 468.7,241.8 476.4,243.9 479.3,241.1 484.2,240.4 477.9,231.9 475.0,231.9 466.5,224.8 447.5,223.4 440.4,224.8 436.8,227.7 431.2,224.8 430.5,221.3 424.8,215.6 410.0,217.8 401.5,215.6 391.6,222.7 385.9,223.4 383.1,221.3 375.3,226.2", cx=430.9, cy=233.6),
    dict(navn="Årstad", points="412.1,155.5 414.9,152.7 418.5,152.7 421.3,154.1 431.9,153.4 439.0,154.8 441.1,156.9 448.9,169.0 449.6,182.4 462.3,198.0 467.3,201.5 463.7,214.9 470.1,221.3 468.0,225.5 455.2,226.2 446.7,224.1 439.0,227.7 431.9,226.9 426.2,217.0 415.6,218.5 398.7,217.0 393.0,222.7 388.1,224.8 383.1,222.0 384.5,219.9 394.4,217.0 397.2,208.6 409.3,200.8 411.4,192.3 401.5,185.2 396.5,184.5 395.1,176.7 399.4,171.1 410.7,168.3 412.1,155.5", cx=422.8, cy=194.3),
    dict(navn="Ladegården", points="258.7,140.0 260.8,139.3 264.3,142.1 271.4,140.0 276.3,144.2 282.7,129.4 286.9,126.5 289.1,127.2 296.8,120.2 277.7,101.8 247.3,130.8 252.3,136.4", cx=272.0, cy=131.5),
    dict(navn="Skuteviken", points="253.7,144.2 256.5,151.8 263.6,152.5 267.0,148.3 265.0,142.8 266.1,141.9 265.8,141.6 264.3,142.1 262.0,140.3 260.1,140.0", cx=262.4, cy=144.5),
    dict(navn="Eidemarken", points="300.1,136.8 293.9,138.6 280.1,135.5 276.6,143.4 276.9,144.0 277.1,144.2 279.8,144.6 282.0,142.8 284.8,143.5 286.9,145.6 290.7,146.1 295.0,150.3 304.9,141.1 304.3,140.0", cx=288.1, cy=142.6),
    dict(navn="Vågsbunnen", points="293.3,174.3 298.3,176.0 316.5,175.0 313.8,171.5 310.3,164.7 306.3,163.0 304.6,163.5 298.3,161.3 298.3,164.7 294.7,168.3 293.7,168.2 291.2,172.9", cx=301.6, cy=168.6),
    dict(navn="Fjellet", points="299.0,152.0 294.0,152.0 291.8,153.6 290.5,156.9 290.0,157.4 291.2,159.8 292.8,159.9 294.0,158.4 296.8,160.2 300.4,160.5 310.3,164.7 313.8,171.5 330.0,175.0 342.8,173.9 354.1,173.9 342.1,173.0 330.0,169.0 325.7,167.1 315.6,164.7 313.6,160.5 311.5,158.0", cx=311.0, cy=163.0),
    dict(navn="Stølen", points="267.1,148.5 281.3,159.8 286.9,160.5 290.5,156.9 292.6,151.3 284.8,143.5 282.0,142.8 278.5,145.6 276.5,143.7 276.3,144.2 271.4,140.0 266.6,141.4 265.0,142.8", cx=278.4, cy=147.8),
    dict(navn="Bergenhus", points="248.5,152.0 241.0,164.0 243.1,166.1 247.3,163.3 254.4,164.0 256.5,166.1 265.7,167.6 269.1,164.2 265.7,159.8 270.7,155.5 270.0,153.4 263.6,152.5 256.5,151.8 256.4,151.5", cx=257.8, cy=159.4),
    dict(navn="Bryggen", points="269.3,151.3 270.7,155.5 265.7,159.8 270.0,165.4 294.7,168.3 298.3,164.7 298.3,161.2 294.0,158.4 291.2,161.9 280.6,161.9 281.1,159.6 270.4,151.1", cx=282.0, cy=159.9),
    dict(navn="Nordnes", points="221.9,192.3 233.9,195.8 237.4,195.8 241.0,192.3 247.3,194.4 250.9,190.9 255.8,191.6 258.7,188.8 257.9,181.7 248.8,175.3 248.0,171.8 244.5,171.8 240.3,177.5 236.0,177.5 234.6,181.0 236.7,183.1 243.8,181.7 253.7,185.2 233.9,184.5 231.1,183.1 232.5,180.3 229.7,178.2 219.8,185.2 218.3,188.8", cx=239.9, cy=184.5),
    dict(navn="Verftet", points="252.0,196.8 262.6,206.2 260.1,210.7 261.5,212.1 269.5,204.8 270.2,194.0 267.3,191.1 262.7,191.5 263.8,194.4", cx=263.3, cy=200.2),
    dict(navn="Strandsiden", points="259.6,191.8 281.7,189.7 290.8,185.8 290.4,184.7 291.6,184.2 292.0,180.0 284.8,177.5 256.6,180.8 257.9,181.7 258.7,188.8 257.6,189.9", cx=274.7, cy=185.0),
    dict(navn="Nøstet", points="270.2,194.0 269.5,204.5 276.1,211.1 285.2,206.1 279.7,192.9 280.8,190.4 280.2,189.8 271.9,190.6 269.1,192.9", cx=275.9, cy=196.9),
    dict(navn="Engen", points="282.0,196.5 282.0,198.4 283.2,201.3 284.1,202.2 297.5,200.8 300.8,198.6 292.0,189.8 291.2,187.4 290.5,186.5 281.5,190.0", cx=288.5, cy=195.2),
    dict(navn="Sentrum", points="301.3,199.1 300.0,207.5 310.3,207.1 311.3,208.1 315.9,203.6 318.1,194.4 315.9,191.6 317.3,177.5 315.2,175.3 313.7,175.2 304.2,175.7 303.3,176.0 296.1,176.5 294.6,177.3 299.2,181.2 290.4,184.7 292.0,189.8", cx=305.8, cy=188.3),
    dict(navn="Marken", points="323.7,183.8 327.2,187.4 330.8,187.4 338.6,179.6 338.6,177.5 337.1,176.0 322.3,176.0 316.2,174.6 316.5,175.0 315.8,175.0 316.5,175.5", cx=325.8, cy=178.9),
    dict(navn="Skansen", points="349.2,145.6 346.3,147.0 337.1,145.6 304.5,140.4 304.9,141.1 300.8,144.9 313.6,160.5 315.6,164.7 342.1,171.1 352.0,171.8 353.8,170.0 352.7,152.7 353.9,151.5 353.4,149.9", cx=334.3, cy=154.1),
]

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
.card-enkel{padding:20px 0;border-top:1px dashed var(--line);border-bottom:1px dashed var(--line)}
.card-enkel h2{margin:0}

.kommentar-liste{list-style:none;margin:0 0 28px;padding:0;display:grid;gap:18px}
.kommentar{border-top:1px dashed var(--line);padding-top:14px}
.kommentar-meta{margin:0 0 4px;font-size:.85rem;color:var(--muted)}
.kommentar p:last-child{margin:0}
.ingen-kommentarer{color:var(--muted);margin:0 0 28px}

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

.kart-figure{margin:32px 0 0}
.kart-figure figcaption{max-width:60ch;color:var(--muted);font-size:.92rem;margin:0 0 14px}
.kart-wrap{position:relative;border-radius:12px;overflow:hidden;background:var(--surface);border:1.5px solid var(--line);touch-action:none}
.kart-wrap svg{width:100%;height:auto;display:block;cursor:grab;user-select:none}
.kart-wrap svg.panning{cursor:grabbing}
.bydel{cursor:pointer}
.bydel .hit{fill:transparent;stroke:transparent;stroke-width:7}
.bydel .fill{fill:rgba(255,255,255,0);stroke:rgba(255,255,255,.85);stroke-width:1;pointer-events:none;transition:fill .15s,stroke-width .15s}
.bydel:hover .fill,.bydel:focus-visible .fill{fill:rgba(255,255,255,.45);stroke-width:2.5}
.bydel.active .fill{fill:rgba(168,55,42,.4);stroke:#A8372A;stroke-width:2.5}
.bydel:focus-visible{outline:none}
.bydel-label{font-family:var(--body);font-size:4.5px;font-weight:600;fill:#1B2932;paint-order:stroke;stroke:#fff;stroke-width:1.3px;stroke-linejoin:round;text-anchor:middle;pointer-events:none;letter-spacing:-.005em}
.bydel-label.sm{opacity:0;transition:opacity .15s}
.kart-wrap.show-sm .bydel-label.sm{opacity:1}
.kart-zoom{position:absolute;right:12px;bottom:12px;display:grid;gap:6px;z-index:5}
.kart-zoom button{width:34px;height:34px;border-radius:8px;border:1.5px solid var(--line);background:var(--surface);color:var(--ink);font-size:1.2rem;line-height:1;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.12)}
.kart-zoom button:hover{background:var(--bg)}
.kart-zoom button.reset{font-size:.7rem;font-family:var(--mono)}
.kart-hint{position:absolute;left:12px;bottom:12px;background:rgba(255,255,255,.85);color:var(--muted);font-size:.72rem;padding:4px 10px;border-radius:999px;pointer-events:none;z-index:5}
@media(max-width:820px){ .kart-hint{display:none} }
.kart-tip{position:fixed;z-index:60;background:var(--ink);color:var(--bg);border-radius:12px;padding:14px 18px;max-width:280px;font-size:.85rem;box-shadow:0 12px 30px rgba(0,0,0,.28);pointer-events:none;opacity:0;transform:translateY(4px);transition:opacity .12s,transform .12s}
.kart-tip.show{opacity:1;transform:translateY(0)}
.kart-tip h3{margin:0 0 10px;font:700 1.05rem var(--display);color:#fff}
.kart-tip dl{margin:0;display:grid;gap:6px}
.kart-tip dt{font:600 .68rem var(--mono);text-transform:uppercase;letter-spacing:.04em;color:#A9BDB3;margin-bottom:1px}
.kart-tip dd{margin:0;font-size:.85rem}
.kart-tip dd.empty{color:#9FB0AA;font-style:italic}
.kart-tip-tekst{margin:0;font-size:.95rem}
@media(max-width:820px){
 .kart-tip{max-width:calc(100vw - 32px)}
}
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

FIELDS = [
    ("nabolag", "Faller ofte under nabolaget:"),
    ("gate", "Mest kjente gate:"),
]

# Disse bydelene har ingen infoboks i det hele tatt (verken felt eller spesialtekst).
INGEN_BOKS = {"Solheim", "Gyldenpris", "Damsgård", "Ytre Sandviken"}
# Disse har en egen, enkel tekst i stedet for de vanlige feltene.
SPESIALTEKST = {"Kringsjå": "Overraskende navn!"}

SMA_BYDELER = {"Bergenhus", "Bryggen", "Fjellet", "Vågsbunnen", "Nordnes", "Verftet",
               "Strandsiden", "Nøstet", "Engen", "Sentrum", "Ladegården",
               "Skuteviken", "Stølen", "Marken", "Skansen", "Eidemarken"}

def kart_svg(pre=""):
    groups = []
    labels = []
    for b in BYDELER:
        navn = html.escape(b["navn"])
        groups.append(
            f'<g class="bydel" data-navn="{navn}" tabindex="0" role="button" aria-label="{navn}">'
            f'<polygon class="hit" points="{b["points"]}"/>'
            f'<polygon class="fill" points="{b["points"]}"/></g>'
        )
        # de tette, små bydelene i sentrumsklyngen får en skjult tekst som først vises
        # når man zoomer inn (klasse "sm") - ellers lå navnene oppå hverandre.
        lbl_cls = "bydel-label sm" if b["navn"] in SMA_BYDELER else "bydel-label"
        labels.append(f'<text class="{lbl_cls}" x="{b["cx"]}" y="{b["cy"]}">{navn}</text>')
    return (
        f'<svg viewBox="0 0 {MAP_W} {MAP_H}" id="kart-svg" role="group" aria-label="Kart over bydeler i sentrum av Bergen">'
        f'<image href="{pre}bilder/bergenskart-sentrum.webp" x="0" y="0" width="{MAP_W}" height="{MAP_H}"/>'
        + "".join(groups)
        # eget lag for tekst HELT til slutt, slik at navnene alltid tegnes foran
        # bydelsgrensene og over andre felters fyll/hover, uansett rekkefølge.
        + '<g class="kart-labels" style="pointer-events:none">' + "".join(labels) + "</g>"
        + "</svg>"
    )

def kart_section_html(pre=""):
    return f'''<div class="kart-wrap" id="kart-wrap">{kart_svg(pre)}
<span class="kart-hint">Rull for å zoome · dra for å flytte</span>
<div class="kart-zoom">
<button type="button" id="kart-in" aria-label="Zoom inn">+</button>
<button type="button" id="kart-out" aria-label="Zoom ut">−</button>
<button type="button" class="reset" id="kart-reset" aria-label="Nullstill zoom">100%</button>
</div>
</div>'''

def kart_script():
    return f'''<div class="kart-tip" id="kart-tip" role="status" aria-live="polite"></div>
<script>
var BYDEL_DATA={kart_data_js()};
var INGEN_BOKS={kart_ingen_boks_js()};
var SPESIALTEKST={kart_spesialtekst_js()};
var FELT=[["nabolag","Faller ofte under nabolaget:"],["gate","Mest kjente gate:"]];
var tip=document.getElementById("kart-tip"),bydeler=[].slice.call(document.querySelectorAll(".bydel")),pinned=false;
function harBoks(navn){{ return INGEN_BOKS.indexOf(navn)===-1; }}
function tipHtml(navn){{
  if(SPESIALTEKST[navn]){{ return "<h3>"+navn+"</h3><p class=\\"kart-tip-tekst\\">"+SPESIALTEKST[navn]+"</p>"; }}
  var d=BYDEL_DATA[navn]||{{}},h="<h3>"+navn+"</h3><dl>";
  FELT.forEach(function(f){{var v=d[f[0]]||"";h+="<dt>"+f[1]+"</dt><dd"+(v?"":" class=\\"empty\\"")+">"+(v||"Fylles inn senere")+"</dd>"}});
  return h+"</dl>";
}}
function placeTip(x,y){{
  var pad=14,w=tip.offsetWidth,h=tip.offsetHeight,left=x+18,top=y+18;
  if(left+w+pad>innerWidth) left=x-w-18;
  if(top+h+pad>innerHeight) top=y-h-18;
  if(left<pad) left=pad; if(top<pad) top=pad;
  tip.style.left=left+"px"; tip.style.top=top+"px";
}}
function showTip(navn,x,y){{
  if(!harBoks(navn)) return;
  bydeler.forEach(function(g){{g.classList.toggle("active",g.dataset.navn===navn)}});
  tip.innerHTML=tipHtml(navn); tip.classList.add("show"); placeTip(x,y);
}}
function hideTip(){{ if(pinned) return; tip.classList.remove("show"); bydeler.forEach(function(g){{g.classList.remove("active")}}); }}
var justDragged=false;
bydeler.forEach(function(g){{
  g.addEventListener("mousemove",function(e){{ if(!pinned && !justDragged) showTip(g.dataset.navn,e.clientX,e.clientY) }});
  g.addEventListener("mouseleave",function(){{ if(!pinned) hideTip() }});
  g.addEventListener("keydown",function(e){{if(e.key==="Enter"||e.key===" "){{e.preventDefault();if(!harBoks(g.dataset.navn))return;var r=g.getBoundingClientRect();pinned=true;showTip(g.dataset.navn,r.left+r.width/2,r.top+r.height/2)}}}});
  g.addEventListener("blur",function(){{ pinned=false; hideTip() }});
}});
// Lukk boksen når man klikker utenfor hele kartet (ikke mens man trykker inni det - se pointerup lenger ned).
document.addEventListener("click",function(e){{ if(!e.target.closest("#kart-wrap")){{ pinned=false; hideTip() }} }});

// ---------- Zoom og panorering ----------
(function(){{
  var svg=document.getElementById("kart-svg"), wrap=document.getElementById("kart-wrap");
  var MAPW={MAP_W}, MAPH={MAP_H};
  var MIN_W=MAPW/4.2, MAX_W=MAPW, SM_T=MAPW/2.1;
  var START_W=MAPW/2.3, START_H=START_W*(MAPH/MAPW);
  var START_CX=303.6, START_CY=188.1; // "Sentrum" - kartet åpner sentrert her
  var DEFAULT_VB={{x:START_CX-START_W/2, y:START_CY-START_H/2, w:START_W, h:START_H}};
  if(DEFAULT_VB.x<0) DEFAULT_VB.x=0; if(DEFAULT_VB.y<0) DEFAULT_VB.y=0;
  if(DEFAULT_VB.x+DEFAULT_VB.w>MAPW) DEFAULT_VB.x=MAPW-DEFAULT_VB.w;
  if(DEFAULT_VB.y+DEFAULT_VB.h>MAPH) DEFAULT_VB.y=MAPH-DEFAULT_VB.h;
  var vb={{x:DEFAULT_VB.x,y:DEFAULT_VB.y,w:DEFAULT_VB.w,h:DEFAULT_VB.h}};
  var resetBtn=document.getElementById("kart-reset");
  function clampVB(){{
    if(vb.w>MAX_W) vb.w=MAX_W;
    if(vb.w<MIN_W) vb.w=MIN_W;
    vb.h=vb.w*(MAPH/MAPW);
    if(vb.x<0) vb.x=0;
    if(vb.y<0) vb.y=0;
    if(vb.x+vb.w>MAPW) vb.x=MAPW-vb.w;
    if(vb.y+vb.h>MAPH) vb.y=MAPH-vb.h;
  }}
  function apply(){{
    svg.setAttribute("viewBox", vb.x.toFixed(1)+" "+vb.y.toFixed(1)+" "+vb.w.toFixed(1)+" "+vb.h.toFixed(1));
    wrap.classList.toggle("show-sm", vb.w<SM_T);
    resetBtn.textContent=Math.round(MAPW/vb.w*100)+"%";
  }}
  function zoomToward(clientX,clientY,newW,baseVB){{
    var r=svg.getBoundingClientRect();
    var fx=(clientX-r.left)/r.width, fy=(clientY-r.top)/r.height;
    var px=baseVB.x+fx*baseVB.w, py=baseVB.y+fy*baseVB.h;
    vb.w=newW; vb.h=newW*(MAPH/MAPW);
    if(vb.w>MAX_W) vb.w=MAX_W, vb.h=vb.w*(MAPH/MAPW);
    if(vb.w<MIN_W) vb.w=MIN_W, vb.h=vb.w*(MAPH/MAPW);
    vb.x=px-fx*vb.w; vb.y=py-fy*vb.h;
    clampVB(); apply();
  }}
  svg.addEventListener("wheel",function(e){{
    e.preventDefault();
    var factor=e.deltaY<0?1.08:1/1.08;
    zoomToward(e.clientX,e.clientY,vb.w/factor,vb);
  }},{{passive:false}});
  document.getElementById("kart-in").addEventListener("click",function(){{
    var r=svg.getBoundingClientRect();
    zoomToward(r.left+r.width/2,r.top+r.height/2,vb.w/1.4,vb);
  }});
  document.getElementById("kart-out").addEventListener("click",function(){{
    var r=svg.getBoundingClientRect();
    zoomToward(r.left+r.width/2,r.top+r.height/2,vb.w*1.4,vb);
  }});
  resetBtn.addEventListener("click",function(){{ vb={{x:DEFAULT_VB.x,y:DEFAULT_VB.y,w:DEFAULT_VB.w,h:DEFAULT_VB.h}}; apply(); }});

  var pointers={{}}, dragMoved=0, lastX=0, lastY=0, pinchStartDist=0, pinchVB=null, pinchClient=null;
  svg.addEventListener("pointerdown",function(e){{
    try{{ svg.setPointerCapture(e.pointerId); }}catch(err){{}}
    pointers[e.pointerId]={{x:e.clientX,y:e.clientY}};
    var ids=Object.keys(pointers);
    if(ids.length===1){{ dragMoved=0; lastX=e.clientX; lastY=e.clientY; svg.classList.add("panning"); }}
    else if(ids.length===2){{
      var pts=ids.map(function(k){{return pointers[k]}});
      pinchStartDist=Math.hypot(pts[0].x-pts[1].x,pts[0].y-pts[1].y);
      pinchVB={{x:vb.x,y:vb.y,w:vb.w,h:vb.h}};
      pinchClient={{x:(pts[0].x+pts[1].x)/2,y:(pts[0].y+pts[1].y)/2}};
    }}
  }});
  svg.addEventListener("pointermove",function(e){{
    if(!(e.pointerId in pointers)) return;
    pointers[e.pointerId]={{x:e.clientX,y:e.clientY}};
    var ids=Object.keys(pointers);
    if(ids.length===2 && pinchVB){{
      var pts=ids.map(function(k){{return pointers[k]}});
      var dist=Math.hypot(pts[0].x-pts[1].x,pts[0].y-pts[1].y);
      var factor=dist/(pinchStartDist||1);
      zoomToward(pinchClient.x,pinchClient.y,pinchVB.w/factor,pinchVB);
    }} else if(ids.length===1){{
      var dx=e.clientX-lastX, dy=e.clientY-lastY;
      dragMoved+=Math.abs(dx)+Math.abs(dy);
      var r=svg.getBoundingClientRect();
      vb.x-=dx*(vb.w/r.width); vb.y-=dy*(vb.h/r.height);
      clampVB(); apply();
      lastX=e.clientX; lastY=e.clientY;
    }}
  }});
  function endPointer(e){{
    delete pointers[e.pointerId];
    if(Object.keys(pointers).length<2){{ pinchVB=null; }}
    if(Object.keys(pointers).length===0){{
      svg.classList.remove("panning");
      justDragged = dragMoved>6;
      if(justDragged){{ setTimeout(function(){{ justDragged=false }},50); }}
      else{{
        // ikke en dra-bevegelse: velg bydelen man trykket på, eller lukk boksen
        // hvis man trykket på vannet/fjellet/et parti uten nabolagsgrense.
        var el=e.target.closest(".bydel");
        if(el && harBoks(el.dataset.navn)){{ pinned=true; showTip(el.dataset.navn,e.clientX,e.clientY); }}
        else{{ pinned=false; hideTip(); }}
      }}
    }}
  }}
  svg.addEventListener("pointerup",endPointer);
  svg.addEventListener("pointercancel",endPointer);
  apply();
}})();
</script>'''

def kart_data_js():
    import json as _json
    data = {}
    for b in BYDELER:
        info = BYDEL_INFO.get(b["navn"], {})
        data[b["navn"]] = {key: info.get(key, "") for key, _ in FIELDS}
    return _json.dumps(data, ensure_ascii=False)

def kart_ingen_boks_js():
    import json as _json
    return _json.dumps(sorted(INGEN_BOKS), ensure_ascii=False)

def kart_spesialtekst_js():
    import json as _json
    return _json.dumps(SPESIALTEKST, ensure_ascii=False)

import glob
for old in glob.glob(f"{BASE}/innlegg/*.html"):
    os.remove(old)
def kommentar_html(p):
    liste = p.get("kommentarer") or []
    if liste:
        items = "".join(
            f'<li class="kommentar"><p class="kommentar-meta"><strong>{html.escape(k["navn"])}</strong> · {k["dato"]}</p><p>{html.escape(k["tekst"])}</p></li>'
            for k in liste
        )
        liste_html = f'<ul class="kommentar-liste">{items}</ul>'
    else:
        liste_html = '<p class="ingen-kommentarer">Ingen kommentarer ennå. Bli den første!</p>'
    navn = f"kommentar-{p['slug']}"
    return f'''<section class="section" id="kommentarer"><h2 class="h">Kommentarer</h2>
{liste_html}
<form id="kommentar-form" name="{navn}" method="POST" data-netlify="true" netlify-honeypot="kbot" novalidate>
<input type="hidden" name="form-name" value="{navn}"><p hidden><label>Ikke fyll ut: <input name="kbot"></label></p>
<div class="field"><label for="kn">Navn</label><input id="kn" name="navn" type="text" autocomplete="name" required><p class="err" id="ken" role="alert"></p></div>
<div class="field"><label for="kk">Kommentar</label><textarea id="kk" name="kommentar" required></textarea><p class="err" id="kek" role="alert"></p></div>
<div><button class="btn" type="submit">Send kommentar</button><p class="status" id="kst" aria-live="polite"></p></div>
<p class="hint">Kommentarer blir lest gjennom før de eventuelt legges ut.</p>
</form></section>'''

def kommentar_script():
    return '''<script>
var kf=document.getElementById("kommentar-form"),kst=document.getElementById("kst");
function kchk(id,eid,ok,msg){var i=document.getElementById(id),v=i.value.trim(),r=ok(v);document.getElementById(eid).textContent=r?"":msg;if(r)i.removeAttribute("aria-invalid");else i.setAttribute("aria-invalid","true");return r}
kf.addEventListener("submit",function(x){x.preventDefault();kst.textContent="";kst.className="status";
var a=kchk("kn","ken",function(v){return v},"Skriv inn navnet ditt."),b=kchk("kk","kek",function(v){return v.length>=2},"Skriv en kommentar.");
if(!(a&&b))return;
var btn=kf.querySelector("button");btn.disabled=true;
fetch("/",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:new URLSearchParams(new FormData(kf)).toString()}).then(function(r){if(!r.ok)throw 0;kst.className="status ok";kst.textContent="Takk! Kommentaren er sendt inn.";kf.reset()}).catch(function(){kst.textContent="Noe gikk galt. Prøv igjen litt senere."}).then(function(){btn.disabled=false})});
</script>'''

for p in POSTS:
    kart_del = ""
    if p.get("kart"):
        kart_del = f'''<figure class="kart-figure">
<figcaption>Interaktivt kart over Bergens strøk. Zoom inn og ut. Det er noe cirka laget, og noen hull og glipper i mellom strøkene, da mine datakunnskaper er begrenset.</figcaption>
{kart_section_html("../")}
</figure>'''
    slutt_script = (kart_script() if p.get("kart") else "") + kommentar_script()
    hero_html = "" if p.get("enkel") else f'<div class="hero"><img src="../bilder/{p["img"]}" alt=""></div>'
    lead_html = "" if p.get("enkel") else f'<p><strong>{html.escape(p["lead"])}</strong></p>'
    w(f"innlegg/{p['slug']}.html", head(f"{p['title']} – Joa's Bergen", p["lead"], "../", p["img"]) + f'''<main><article class="article">{hero_html}
<span class="cats">{' · '.join(p['cats'])}{' · Regnværsdag' if p['rain'] else ''}</span><time class="date" datetime="{p['date']}">{p['label']}</time><h1>{html.escape(p['title'])}</h1>
<div class="body">{lead_html}{p['body']}</div>
{kart_del}
<a class="back" href="../index.html">&larr; Alle innlegg</a></article>
{kommentar_html(p)}
{FOOT}</main></div>{slutt_script}</body></html>
''')

def card_html(p):
    if p.get("enkel"):
        return f'''<a class="card card-enkel" href="innlegg/{p['slug']}.html" data-cats="{'|'.join(p['cats'])}" data-rain="{int(p['rain'])}"><h2>{html.escape(p['title'])}</h2></a>'''
    return f'''<a class="card" href="innlegg/{p['slug']}.html" data-cats="{'|'.join(p['cats'])}" data-rain="{int(p['rain'])}"><div class="img"><img src="bilder/{p['img']}" alt="" loading="lazy"></div><span class="cats">{' · '.join(p['cats'])}{' · Regnværsdag' if p['rain'] else ''}</span><time class="date" datetime="{p['date']}">{p['label']}</time><h2>{html.escape(p['title'])}</h2><p>{html.escape(p['lead'])}</p></a>'''

cards = "\n".join(card_html(p) for p in POSTS)

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
<p>Eg er en drømmer, bergensnostalgiker, for ikke å si: en urban melankoliker. Noen kunne til og med sagt: en kontrafaktisk historiker, men eg er ingen historiker. Eg tenker mye på hvordan byen ville ha sett ut hvis det ikke hadde for alle bybrannene (er det derfor forballaget heter Brann?). Hvordan hadde det vært her, hvis den kalde arkitekturen fra 60-tallet ikke hadde fått herje? Men for all del, det kunne vært mye verre, ta Oslo for eksempel, men nok om det.</p>
<p>Eg tenker på gamle Hotell Norge. Bygget i 1885, som overlevde både bybrannen i 1916 og andre verdenskrig, da det hovedsakelig huset tyske offiserer. Revet i 1961 til fordel for dagens koordinatsystem i betong. Nei, gamle Hotell Norge lå der nye Hotell Norge ligger i dag, eg blandet med annet, like flott bygg som lå der Gulatinget ligger, nemlig Hotel Metropol, et hotell eg også tenker på. En (ukjent) bergensavis sa det kanskje best da dets på en gang imponerende og tiltrekkende ytre, lyser og liver opp i en av vårs by vakreste kvartaler med marmorets dans og fargevirkningens harmoni. Det var også 60 værelser.</p>
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
