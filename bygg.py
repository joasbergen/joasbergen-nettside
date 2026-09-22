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

# ---------- Interaktivt kart (bydeler i sentrum). Formene er trukket ut fra bergenskart.webp.
# Legg inn innhold etter hvert: nøkkel = bydelsnavn (må matche "navn" i BYDELER under).
BYDEL_INFO = {
    # "Sentrum": dict(nabolag="", innbyggere="", kjent="", mangler="", tilbud="", hoyde=""),
}
MAP_W, MAP_H = 1100, 1050
BYDELER = [
    dict(navn="Ytre Sandviken", points="254.0,-75.0 262.0,-73.0 290.0,-39.0 307.0,-40.0 325.0,-18.0 327.0,14.0 339.0,28.0 339.0,42.0 351.0,64.0 388.0,101.0 414.0,113.0 421.0,124.0 423.0,148.0 433.0,172.0 431.0,196.0 439.0,218.0 439.0,230.0 418.0,245.0 410.0,257.0 392.0,253.0 376.0,237.0 369.0,248.0 367.0,266.0 358.0,267.0 351.0,260.0 351.0,244.0 345.0,232.0 345.0,222.0 351.0,216.0 347.0,192.0 340.0,189.0 335.0,200.0 328.0,203.0 313.0,184.0 313.0,168.0 317.0,160.0 299.0,140.0 295.0,124.0 297.0,118.0 287.0,94.0 289.0,86.0 282.0,79.0 270.0,75.0 265.0,68.0 241.0,12.0 241.0,2.0 250.0,3.0 253.0,-6.0 265.0,-12.0 253.0,-64.0 254.0,-75.0", cx=341.0, cy=111.8),
    dict(navn="Sandviken", points="436.0,229.0 442.0,229.0 457.0,246.0 469.0,282.0 489.0,306.0 499.0,354.0 513.0,390.0 512.0,399.0 440.0,393.0 437.0,390.0 439.0,382.0 429.0,362.0 415.0,352.0 416.0,341.0 436.0,345.0 438.0,351.0 487.0,350.0 486.0,347.0 472.0,345.0 439.0,346.0 447.0,334.0 447.0,318.0 438.0,307.0 435.0,308.0 434.0,317.0 425.0,312.0 425.0,308.0 433.0,304.0 427.0,300.0 429.0,288.0 425.0,282.0 425.0,272.0 409.0,260.0 411.0,248.0 436.0,229.0", cx=459.2, cy=324.6),
    dict(navn="Ladegården", points="434.0,393.0 512.0,399.0 511.0,450.0 504.0,451.0 480.0,443.0 450.0,455.0 449.0,442.0 437.0,434.0 427.0,410.0 427.0,396.0 434.0,393.0", cx=472.2, cy=420.8),
    dict(navn="Nordnes", points="308.0,433.0 334.0,435.0 352.0,451.0 366.0,449.0 375.0,458.0 375.0,466.0 367.0,468.0 373.0,482.0 360.0,495.0 356.0,495.0 348.0,485.0 338.0,483.0 330.0,473.0 322.0,475.0 307.0,452.0 305.0,436.0 308.0,433.0", cx=340.4, cy=461.0),
    dict(navn="Verftet", points="328.0,475.0 334.0,475.0 340.0,483.0 348.0,483.0 377.0,508.0 377.0,514.0 364.0,529.0 349.0,530.0 353.0,524.0 347.0,518.0 349.0,510.0 340.0,505.0 339.0,500.0 348.0,501.0 362.0,515.0 365.0,512.0 342.0,491.0 332.0,489.0 327.0,482.0 328.0,475.0", cx=353.8, cy=505.0),
    dict(navn="Strandsiden", points="374.0,479.0 379.0,480.0 375.0,490.0 409.0,516.0 400.0,529.0 394.0,529.0 359.0,500.0 359.0,494.0 374.0,479.0", cx=383.0, cy=506.4),
    dict(navn="Bergenhus", points="390.0,423.0 404.0,423.0 408.0,433.0 420.0,435.0 433.0,446.0 430.0,465.0 418.0,465.0 414.0,475.0 406.0,475.0 399.0,470.0 393.0,456.0 377.0,440.0 378.0,435.0 395.0,434.0 389.0,430.0 390.0,423.0", cx=407.0, cy=448.8),
    dict(navn="Bryggen", points="430.0,455.0 434.0,455.0 439.0,462.0 441.0,484.0 449.0,492.0 449.0,498.0 459.0,506.0 459.0,510.0 452.0,515.0 442.0,515.0 411.0,476.0 413.0,464.0 416.0,461.0 424.0,463.0 430.0,455.0", cx=433.6, cy=485.4),
    dict(navn="Fjellet", points="476.0,441.0 487.0,442.0 495.0,486.0 466.0,493.0 461.0,470.0 453.0,462.0 451.0,452.0 464.0,447.0 470.0,461.0 467.0,446.0 476.0,441.0", cx=474.8, cy=466.6),
    dict(navn="Vågsbunnen", points="468.0,537.0 474.0,537.0 482.0,547.0 490.0,547.0 503.0,570.0 496.0,571.0 489.0,566.0 482.0,553.0 470.0,551.0 465.0,544.0 468.0,537.0", cx=484.2, cy=553.2),
    dict(navn="Nøstet", points="374.0,513.0 384.0,515.0 385.0,522.0 374.0,537.0 368.0,537.0 363.0,532.0 363.0,524.0 374.0,513.0", cx=373.8, cy=524.8),
    dict(navn="Engen", points="386.0,535.0 411.0,544.0 413.0,564.0 410.0,567.0 400.0,565.0 379.0,548.0 379.0,542.0 386.0,535.0", cx=397.6, cy=550.4),
    dict(navn="Sentrum", points="406.0,521.0 414.0,521.0 429.0,536.0 425.0,542.0 428.0,545.0 431.0,538.0 442.0,531.0 461.0,554.0 459.0,562.0 441.0,576.0 441.0,582.0 420.0,595.0 414.0,595.0 403.0,586.0 403.0,580.0 413.0,568.0 413.0,546.0 416.0,541.0 423.0,540.0 414.0,535.0 410.0,541.0 395.0,538.0 395.0,532.0 406.0,521.0", cx=427.2, cy=558.0),
    dict(navn="Marken og Skansen", points="472.0,491.0 498.0,491.0 525.0,532.0 526.0,543.0 510.0,541.0 490.0,531.0 490.0,537.0 532.0,547.0 547.0,564.0 545.0,576.0 524.0,599.0 520.0,599.0 505.0,580.0 483.0,542.0 467.0,500.0 472.0,491.0", cx=507.2, cy=542.6),
    dict(navn="Sydnes", points="328.0,543.0 334.0,543.0 348.0,555.0 360.0,555.0 368.0,563.0 380.0,565.0 409.0,592.0 409.0,606.0 398.0,615.0 364.0,617.0 352.0,621.0 333.0,592.0 334.0,585.0 342.0,585.0 346.0,591.0 351.0,586.0 323.0,552.0 328.0,543.0", cx=365.6, cy=587.2),
    dict(navn="Møhlenpris", points="390.0,617.0 400.0,617.0 409.0,632.0 433.0,654.0 433.0,662.0 424.0,665.0 388.0,629.0 385.0,636.0 393.0,646.0 404.0,651.0 423.0,670.0 424.0,675.0 430.0,675.0 440.0,685.0 464.0,685.0 467.0,690.0 466.0,703.0 442.0,705.0 424.0,695.0 415.0,688.0 414.0,681.0 402.0,677.0 363.0,638.0 355.0,628.0 360.0,619.0 390.0,617.0", cx=409.0, cy=658.6),
    dict(navn="Gyldenpris", points="348.0,645.0 356.0,645.0 368.0,655.0 411.0,698.0 400.0,713.0 392.0,713.0 380.0,727.0 356.0,719.0 338.0,701.0 334.0,701.0 328.0,709.0 315.0,706.0 319.0,682.0 339.0,664.0 339.0,652.0 348.0,645.0", cx=361.2, cy=688.6),
    dict(navn="Nygård", points="436.0,581.0 448.0,587.0 462.0,587.0 468.0,593.0 492.0,593.0 507.0,610.0 521.0,636.0 523.0,654.0 508.0,659.0 497.0,678.0 482.0,687.0 472.0,687.0 468.0,683.0 454.0,685.0 434.0,675.0 431.0,672.0 433.0,656.0 413.0,638.0 401.0,618.0 401.0,612.0 409.0,606.0 411.0,596.0 436.0,581.0", cx=462.6, cy=633.0),
    dict(navn="Kalfaret", points="546.0,575.0 552.0,575.0 564.0,589.0 584.0,591.0 607.0,616.0 607.0,620.0 602.0,625.0 570.0,625.0 566.0,621.0 558.0,621.0 554.0,625.0 546.0,625.0 544.0,629.0 539.0,628.0 538.0,621.0 532.0,621.0 532.0,633.0 606.0,633.0 607.0,626.0 616.0,623.0 639.0,638.0 637.0,658.0 608.0,679.0 600.0,679.0 584.0,667.0 558.0,677.0 542.0,665.0 524.0,661.0 519.0,650.0 519.0,638.0 507.0,616.0 491.0,600.0 491.0,592.0 494.0,589.0 502.0,591.0 518.0,607.0 546.0,575.0", cx=567.2, cy=631.6),
    dict(navn="Damsgård", points="254.0,559.0 263.0,560.0 263.0,580.0 278.0,597.0 282.0,591.0 294.0,593.0 308.0,609.0 328.0,615.0 351.0,640.0 339.0,656.0 339.0,666.0 319.0,684.0 314.0,715.0 294.0,713.0 290.0,705.0 282.0,707.0 266.0,695.0 258.0,697.0 249.0,668.0 233.0,644.0 231.0,620.0 215.0,596.0 217.0,576.0 226.0,575.0 232.0,583.0 241.0,576.0 241.0,564.0 254.0,559.0", cx=280.2, cy=639.0),
    dict(navn="Kringsjå", points="158.0,495.0 174.0,497.0 185.0,506.0 185.0,524.0 190.0,529.0 204.0,523.0 210.0,515.0 218.0,515.0 230.0,521.0 259.0,548.0 259.0,552.0 246.0,555.0 236.0,551.0 241.0,562.0 241.0,576.0 230.0,581.0 220.0,573.0 215.0,578.0 214.0,593.0 196.0,595.0 170.0,573.0 155.0,554.0 151.0,522.0 158.0,495.0", cx=197.2, cy=546.4),
    dict(navn="Solheim", points="408.0,703.0 414.0,703.0 448.0,731.0 455.0,730.0 455.0,718.0 462.0,711.0 472.0,711.0 473.0,722.0 489.0,762.0 489.0,790.0 498.0,791.0 508.0,779.0 512.0,779.0 525.0,800.0 525.0,818.0 529.0,826.0 515.0,840.0 511.0,850.0 515.0,872.0 505.0,880.0 505.0,898.0 501.0,902.0 504.0,933.0 456.0,925.0 447.0,920.0 445.0,874.0 419.0,768.0 379.0,730.0 379.0,724.0 390.0,711.0 398.0,713.0 408.0,703.0", cx=463.0, cy=812.4),
    dict(navn="Kronstad", points="474.0,711.0 492.0,715.0 493.0,722.0 502.0,729.0 526.0,733.0 535.0,748.0 559.0,766.0 559.0,782.0 555.0,788.0 559.0,800.0 568.0,801.0 580.0,809.0 605.0,838.0 607.0,860.0 611.0,864.0 608.0,885.0 600.0,879.0 592.0,879.0 584.0,865.0 546.0,865.0 543.0,856.0 535.0,852.0 525.0,816.0 527.0,802.0 517.0,792.0 511.0,778.0 500.0,791.0 489.0,790.0 489.0,762.0 473.0,722.0 474.0,711.0", cx=542.6, cy=800.2),
    dict(navn="Årstad", points="626.0,663.0 634.0,663.0 639.0,668.0 641.0,674.0 657.0,688.0 665.0,700.0 665.0,706.0 659.0,734.0 641.0,754.0 637.0,794.0 639.0,806.0 615.0,820.0 615.0,838.0 606.0,841.0 587.0,824.0 578.0,809.0 562.0,803.0 553.0,792.0 559.0,770.0 542.0,757.0 520.0,731.0 504.0,731.0 494.0,727.0 491.0,716.0 496.0,715.0 514.0,725.0 530.0,717.0 558.0,723.0 573.0,714.0 569.0,690.0 563.0,682.0 572.0,669.0 586.0,667.0 606.0,679.0 626.0,663.0", cx=598.8, cy=742.4),
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

.kart-intro{max-width:60ch;color:var(--muted);margin:0 0 20px}
.kart-wrap{position:relative;border-radius:12px;overflow:hidden;background:var(--surface);border:1.5px solid var(--line)}
.kart-wrap svg{width:100%;height:auto;display:block}
.bydel{cursor:pointer}
.bydel .hit{fill:transparent;stroke:transparent;stroke-width:7}
.bydel .fill{fill:rgba(255,255,255,0);stroke:rgba(255,255,255,.85);stroke-width:1;pointer-events:none;transition:fill .15s,stroke-width .15s}
.bydel:hover .fill,.bydel:focus-visible .fill{fill:rgba(255,255,255,.45);stroke-width:2.5}
.bydel.active .fill{fill:rgba(168,55,42,.4);stroke:#A8372A;stroke-width:2.5}
.bydel:focus-visible{outline:none}
.bydel-label{font-family:var(--body);font-size:15px;font-weight:700;fill:#1B2932;paint-order:stroke;stroke:#fff;stroke-width:3.5px;stroke-linejoin:round;text-anchor:middle;pointer-events:none;letter-spacing:-.01em}
.bydel-label.sm{font-size:11px;font-weight:600;stroke-width:2.5px}
.kart-tip{position:fixed;z-index:60;background:var(--ink);color:var(--bg);border-radius:12px;padding:14px 18px;max-width:280px;font-size:.85rem;box-shadow:0 12px 30px rgba(0,0,0,.28);pointer-events:none;opacity:0;transform:translateY(4px);transition:opacity .12s,transform .12s}
.kart-tip.show{opacity:1;transform:translateY(0)}
.kart-tip h3{margin:0 0 10px;font:700 1.05rem var(--display);color:#fff}
.kart-tip dl{margin:0;display:grid;gap:6px}
.kart-tip dt{font:600 .68rem var(--mono);text-transform:uppercase;letter-spacing:.04em;color:#A9BDB3;margin-bottom:1px}
.kart-tip dd{margin:0;font-size:.85rem}
.kart-tip dd.empty{color:#9FB0AA;font-style:italic}
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
    ("innbyggere", "Innbyggertall:"),
    ("kjent", "Kjent for:"),
    ("mangler", "Mangler/lite av:"),
    ("tilbud", "Andre tilbud:"),
    ("hoyde", "Gjennomsnittlig høyde over havet:"),
]

SMA_BYDELER = {"Bergenhus", "Bryggen", "Fjellet", "Vågsbunnen", "Nordnes", "Verftet",
               "Strandsiden", "Nøstet", "Engen", "Sentrum", "Ladegården"}

def kart_svg():
    groups = []
    for b in BYDELER:
        navn = html.escape(b["navn"])
        lbl_cls = "bydel-label sm" if b["navn"] in SMA_BYDELER else "bydel-label"
        groups.append(
            f'<g class="bydel" data-navn="{navn}" tabindex="0" role="button" aria-label="{navn}">'
            f'<polygon class="hit" points="{b["points"]}"/>'
            f'<polygon class="fill" points="{b["points"]}"/>'
            f'<text class="{lbl_cls}" x="{b["cx"]}" y="{b["cy"]}">{navn}</text></g>'
        )
    return (
        f'<svg viewBox="0 0 {MAP_W} {MAP_H}" role="group" aria-label="Kart over bydeler i sentrum av Bergen">'
        f'<image href="bilder/bergenskart-sentrum.webp" x="0" y="0" width="{MAP_W}" height="{MAP_H}"/>'
        + "".join(groups) + "</svg>"
    )

def kart_data_js():
    import json as _json
    data = {}
    for b in BYDELER:
        info = BYDEL_INFO.get(b["navn"], {})
        data[b["navn"]] = {key: info.get(key, "") for key, _ in FIELDS}
    return _json.dumps(data, ensure_ascii=False)

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
<section class="section" id="kart"><h2 class="h">Bydeler i Bergen</h2>
<p class="kart-intro">Nærbilde av de sentrale bydelene. Hold musen over eller trykk på en bydel for å se mer.</p>
<div class="kart-wrap">{kart_svg()}</div>
</section>
{FOOT}</main></div>
<div class="kart-tip" id="kart-tip" role="status" aria-live="polite"></div>
<script>
var BYDEL_DATA={kart_data_js()};
var FELT=[["nabolag","Faller ofte under nabolaget:"],["innbyggere","Innbyggertall:"],["kjent","Kjent for:"],["mangler","Mangler/lite av:"],["tilbud","Andre tilbud:"],["hoyde","Gjennomsnittlig høyde over havet:"]];
var tip=document.getElementById("kart-tip"),bydeler=[].slice.call(document.querySelectorAll(".bydel")),pinned=false;
function tipHtml(navn){{
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
  bydeler.forEach(function(g){{g.classList.toggle("active",g.dataset.navn===navn)}});
  tip.innerHTML=tipHtml(navn); tip.classList.add("show"); placeTip(x,y);
}}
function hideTip(){{ if(pinned) return; tip.classList.remove("show"); bydeler.forEach(function(g){{g.classList.remove("active")}}); }}
bydeler.forEach(function(g){{
  g.addEventListener("mousemove",function(e){{ if(!pinned) showTip(g.dataset.navn,e.clientX,e.clientY) }});
  g.addEventListener("mouseleave",function(){{ if(!pinned) hideTip() }});
  g.addEventListener("click",function(e){{ pinned=(pinned&&g.classList.contains("active"))?false:true; showTip(g.dataset.navn,e.clientX,e.clientY) }});
  g.addEventListener("keydown",function(e){{if(e.key==="Enter"||e.key===" "){{e.preventDefault();var r=g.getBoundingClientRect();pinned=true;showTip(g.dataset.navn,r.left+r.width/2,r.top+r.height/2)}}}});
  g.addEventListener("blur",function(){{ pinned=false; hideTip() }});
}});
document.addEventListener("click",function(e){{ if(!e.target.closest(".bydel")){{ pinned=false; hideTip() }} }});
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
