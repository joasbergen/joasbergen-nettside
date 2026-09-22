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
MAP_W, MAP_H = 1623, 2000
BYDELER = [
    dict(navn="Ytre Sandviken", points="412.0,562.5 416.0,563.5 430.0,580.5 438.5,580.0 447.5,591.0 448.5,607.0 454.5,614.0 454.5,621.0 460.5,632.0 479.0,650.5 492.0,656.5 495.5,662.0 496.5,674.0 501.5,686.0 500.5,698.0 504.5,709.0 504.5,715.0 494.0,722.5 490.0,728.5 481.0,726.5 473.0,718.5 469.5,724.0 468.5,733.0 464.0,733.5 460.5,730.0 460.5,722.0 457.5,716.0 457.5,711.0 460.5,708.0 458.5,696.0 455.0,694.5 452.5,700.0 449.0,701.5 441.5,692.0 441.5,684.0 443.5,680.0 434.5,670.0 432.5,662.0 433.5,659.0 428.5,647.0 429.5,643.0 426.0,639.5 420.0,637.5 417.5,634.0 405.5,606.0 405.5,601.0 410.0,601.5 411.5,597.0 417.5,594.0 411.5,568.0 412.0,562.5", cx=455.5, cy=655.9),
    dict(navn="Sandviken", points="503.0,714.5 506.0,714.5 513.5,723.0 519.5,741.0 529.5,753.0 534.5,777.0 541.5,795.0 541.0,799.5 505.0,796.5 503.5,795.0 504.5,791.0 499.5,781.0 492.5,776.0 493.0,770.5 503.0,772.5 504.0,775.5 528.5,775.0 528.0,773.5 521.0,772.5 504.5,773.0 508.5,767.0 508.5,759.0 504.0,753.5 502.5,754.0 502.0,758.5 497.5,756.0 497.5,754.0 501.5,752.0 498.5,750.0 499.5,744.0 497.5,741.0 497.5,736.0 489.5,730.0 490.5,724.0 503.0,714.5", cx=514.6, cy=762.3),
    dict(navn="Ladegården", points="502.0,796.5 541.0,799.5 540.5,825.0 537.0,825.5 525.0,821.5 510.0,827.5 509.5,821.0 503.5,817.0 498.5,805.0 498.5,798.0 502.0,796.5", cx=521.1, cy=810.4),
    dict(navn="Nordnes", points="439.0,816.5 452.0,817.5 461.0,825.5 468.0,824.5 472.5,829.0 472.5,833.0 468.5,834.0 471.5,841.0 465.0,847.5 463.0,847.5 459.0,842.5 454.0,841.5 450.0,836.5 446.0,837.5 438.5,826.0 437.5,818.0 439.0,816.5", cx=455.2, cy=830.5),
    dict(navn="Verftet", points="449.0,837.5 452.0,837.5 455.0,841.5 459.0,841.5 473.5,854.0 473.5,857.0 467.0,864.5 459.5,865.0 461.5,862.0 458.5,859.0 459.5,855.0 455.0,852.5 454.5,850.0 459.0,850.5 466.0,857.5 467.5,856.0 456.0,845.5 451.0,844.5 448.5,841.0 449.0,837.5", cx=461.9, cy=852.5),
    dict(navn="Strandsiden", points="472.0,839.5 474.5,840.0 472.5,845.0 489.5,858.0 485.0,864.5 482.0,864.5 464.5,850.0 464.5,847.0 472.0,839.5", cx=476.5, cy=853.2),
    dict(navn="Bergenhus", points="480.0,811.5 487.0,811.5 489.0,816.5 495.0,817.5 501.5,823.0 500.0,832.5 494.0,832.5 492.0,837.5 488.0,837.5 484.5,835.0 481.5,828.0 473.5,820.0 474.0,817.5 482.5,817.0 479.5,815.0 480.0,811.5", cx=488.5, cy=824.4),
    dict(navn="Bryggen", points="500.0,827.5 502.0,827.5 504.5,831.0 505.5,842.0 509.5,846.0 509.5,849.0 514.5,853.0 514.5,855.0 511.0,857.5 506.0,857.5 490.5,838.0 491.5,832.0 493.0,830.5 497.0,831.5 500.0,827.5", cx=501.8, cy=842.7),
    dict(navn="Fjellet", points="523.0,820.5 528.5,821.0 532.5,843.0 518.0,846.5 515.5,835.0 511.5,831.0 510.5,826.0 517.0,823.5 520.0,830.5 518.5,823.0 523.0,820.5", cx=522.4, cy=833.3),
    dict(navn="Vågsbunnen", points="519.0,868.5 522.0,868.5 526.0,873.5 530.0,873.5 536.5,885.0 533.0,885.5 529.5,883.0 526.0,876.5 520.0,875.5 517.5,872.0 519.0,868.5", cx=527.1, cy=876.6),
    dict(navn="Nøstet", points="472.0,856.5 477.0,857.5 477.5,861.0 472.0,868.5 469.0,868.5 466.5,866.0 466.5,862.0 472.0,856.5", cx=471.9, cy=862.4),
    dict(navn="Engen", points="478.0,867.5 490.5,872.0 491.5,882.0 490.0,883.5 485.0,882.5 474.5,874.0 474.5,871.0 478.0,867.5", cx=483.8, cy=875.2),
    dict(navn="Sentrum", points="488.0,860.5 492.0,860.5 499.5,868.0 497.5,871.0 499.0,872.5 500.5,869.0 506.0,865.5 515.5,877.0 514.5,881.0 505.5,888.0 505.5,891.0 495.0,897.5 492.0,897.5 486.5,893.0 486.5,890.0 491.5,884.0 491.5,873.0 493.0,870.5 496.5,870.0 492.0,867.5 490.0,870.5 482.5,869.0 482.5,866.0 488.0,860.5", cx=498.6, cy=879.0),
    dict(navn="Marken og Skansen", points="521.0,845.5 534.0,845.5 547.5,866.0 548.0,871.5 540.0,870.5 530.0,865.5 530.0,868.5 551.0,873.5 558.5,882.0 557.5,888.0 547.0,899.5 545.0,899.5 537.5,890.0 526.5,871.0 518.5,850.0 521.0,845.5", cx=538.6, cy=871.3),
    dict(navn="Sydnes", points="449.0,871.5 452.0,871.5 459.0,877.5 465.0,877.5 469.0,881.5 475.0,882.5 489.5,896.0 489.5,903.0 484.0,907.5 467.0,908.5 461.0,910.5 451.5,896.0 452.0,892.5 456.0,892.5 458.0,895.5 460.5,893.0 446.5,876.0 449.0,871.5", cx=467.8, cy=893.6),
    dict(navn="Møhlenpris", points="480.0,908.5 485.0,908.5 489.5,916.0 501.5,927.0 501.5,931.0 497.0,932.5 479.0,914.5 477.5,918.0 481.5,923.0 487.0,925.5 496.5,935.0 497.0,937.5 500.0,937.5 505.0,942.5 517.0,942.5 518.5,945.0 518.0,951.5 506.0,952.5 497.0,947.5 492.5,944.0 492.0,940.5 486.0,938.5 466.5,919.0 462.5,914.0 465.0,909.5 480.0,908.5", cx=489.5, cy=929.3),
    dict(navn="Gyldenpris", points="459.0,922.5 463.0,922.5 469.0,927.5 490.5,949.0 485.0,956.5 481.0,956.5 475.0,963.5 463.0,959.5 454.0,950.5 452.0,950.5 449.0,954.5 442.5,953.0 444.5,941.0 454.5,932.0 454.5,926.0 459.0,922.5", cx=465.6, cy=944.3),
    dict(navn="Nygård", points="503.0,890.5 509.0,893.5 516.0,893.5 519.0,896.5 531.0,896.5 538.5,905.0 545.5,918.0 546.5,927.0 539.0,929.5 533.5,939.0 526.0,943.5 521.0,943.5 519.0,941.5 512.0,942.5 502.0,937.5 500.5,936.0 501.5,928.0 491.5,919.0 485.5,909.0 485.5,906.0 489.5,903.0 490.5,898.0 503.0,890.5", cx=516.3, cy=916.5),
    dict(navn="Kalfaret", points="558.0,887.5 561.0,887.5 567.0,894.5 577.0,895.5 588.5,908.0 588.5,910.0 586.0,912.5 570.0,912.5 568.0,910.5 564.0,910.5 562.0,912.5 558.0,912.5 557.0,914.5 554.5,914.0 554.0,910.5 551.0,910.5 551.0,916.5 588.0,916.5 588.5,913.0 593.0,911.5 604.5,919.0 603.5,929.0 589.0,939.5 585.0,939.5 577.0,933.5 564.0,938.5 556.0,932.5 547.0,930.5 544.5,925.0 544.5,919.0 538.5,908.0 530.5,900.0 530.5,896.0 532.0,894.5 536.0,895.5 544.0,903.5 558.0,887.5", cx=568.6, cy=915.8),
    dict(navn="Damsgård", points="412.0,879.5 416.5,880.0 416.5,890.0 424.0,898.5 426.0,895.5 432.0,896.5 439.0,904.5 449.0,907.5 460.5,920.0 454.5,928.0 454.5,933.0 444.5,942.0 442.0,957.5 432.0,956.5 430.0,952.5 426.0,953.5 418.0,947.5 414.0,948.5 409.5,934.0 401.5,922.0 400.5,910.0 392.5,898.0 393.5,888.0 398.0,887.5 401.0,891.5 405.5,888.0 405.5,882.0 412.0,879.5", cx=425.1, cy=919.5),
    dict(navn="Kringsjå", points="364.0,847.5 372.0,848.5 377.5,853.0 377.5,862.0 380.0,864.5 387.0,861.5 390.0,857.5 394.0,857.5 400.0,860.5 414.5,874.0 414.5,876.0 408.0,877.5 403.0,875.5 405.5,881.0 405.5,888.0 400.0,890.5 395.0,886.5 392.5,889.0 392.0,896.5 383.0,897.5 370.0,886.5 362.5,877.0 360.5,861.0 364.0,847.5", cx=383.6, cy=873.2),
    dict(navn="Solheim", points="489.0,951.5 492.0,951.5 509.0,965.5 512.5,965.0 512.5,959.0 516.0,955.5 521.0,955.5 521.5,961.0 529.5,981.0 529.5,995.0 534.0,995.5 539.0,989.5 541.0,989.5 547.5,1000.0 547.5,1009.0 549.5,1013.0 542.5,1020.0 540.5,1025.0 542.5,1036.0 537.5,1040.0 537.5,1049.0 535.5,1051.0 537.0,1066.5 513.0,1062.5 508.5,1060.0 507.5,1037.0 494.5,984.0 474.5,965.0 474.5,962.0 480.0,955.5 484.0,956.5 489.0,951.5", cx=516.5, cy=1006.2),
    dict(navn="Kronstad", points="522.0,955.5 531.0,957.5 531.5,961.0 536.0,964.5 548.0,966.5 552.5,974.0 564.5,983.0 564.5,991.0 562.5,994.0 564.5,1000.0 569.0,1000.5 575.0,1004.5 587.5,1019.0 588.5,1030.0 590.5,1032.0 589.0,1042.5 585.0,1039.5 581.0,1039.5 577.0,1032.5 558.0,1032.5 556.5,1028.0 552.5,1026.0 547.5,1008.0 548.5,1001.0 543.5,996.0 540.5,989.0 535.0,995.5 529.5,995.0 529.5,981.0 521.5,961.0 522.0,955.5", cx=556.3, cy=1000.1),
    dict(navn="Årstad", points="598.0,931.5 602.0,931.5 604.5,934.0 605.5,937.0 613.5,944.0 617.5,950.0 617.5,953.0 614.5,967.0 605.5,977.0 603.5,997.0 604.5,1003.0 592.5,1010.0 592.5,1019.0 588.0,1020.5 578.5,1012.0 574.0,1004.5 566.0,1001.5 561.5,996.0 564.5,985.0 556.0,978.5 545.0,965.5 537.0,965.5 532.0,963.5 530.5,958.0 533.0,957.5 542.0,962.5 550.0,958.5 564.0,961.5 571.5,957.0 569.5,945.0 566.5,941.0 571.0,934.5 578.0,933.5 588.0,939.5 598.0,931.5", cx=584.4, cy=971.2),
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
.kart-layout{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:28px;align-items:start}
.kart-wrap{border-radius:12px;overflow:hidden;background:var(--surface);border:1.5px solid var(--line)}
.kart-wrap svg{width:100%;height:auto;display:block}
.bydel{cursor:pointer}
.bydel .hit{fill:transparent;stroke:transparent;stroke-width:7}
.bydel .fill{fill:rgba(255,255,255,0);stroke:rgba(255,255,255,.85);stroke-width:1;pointer-events:none;transition:fill .15s,stroke-width .15s}
.bydel:hover .fill,.bydel:focus-visible .fill{fill:rgba(255,255,255,.45);stroke-width:2.5}
.bydel.active .fill{fill:rgba(168,55,42,.4);stroke:#A8372A;stroke-width:2.5}
.bydel:focus-visible{outline:none}
.kart-info{position:sticky;top:40px;background:var(--surface);border:1.5px solid var(--line);border-radius:12px;padding:20px 22px;min-height:220px}
.kart-info h3{margin:0 0 14px;font:700 1.25rem var(--display);letter-spacing:-.01em}
.kart-info .ph{color:var(--muted);font-size:.92rem}
.kart-info dl{margin:0;display:grid;gap:10px}
.kart-info dt{font:600 .74rem var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:2px}
.kart-info dd{margin:0;font-size:.95rem}
.kart-info dd.empty{color:var(--muted);font-style:italic}
@media(max-width:820px){
 .kart-layout{grid-template-columns:minmax(0,1fr)}
 .kart-info{position:static}
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

def kart_svg():
    groups = []
    for b in BYDELER:
        navn = html.escape(b["navn"])
        groups.append(
            f'<g class="bydel" data-navn="{navn}" tabindex="0" role="button" aria-label="{navn}">'
            f'<polygon class="hit" points="{b["points"]}"/>'
            f'<polygon class="fill" points="{b["points"]}"/></g>'
        )
    return (
        f'<svg viewBox="0 0 {MAP_W} {MAP_H}" role="group" aria-label="Kart over bydeler i sentrum av Bergen">'
        f'<image href="bilder/bergenskart.webp" x="0" y="0" width="{MAP_W}" height="{MAP_H}"/>'
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
<p class="kart-intro">Kartet viser hele Bergen som referanse. Bydelene i sentrum er interaktive: hold musen over eller trykk på en bydel for å se mer.</p>
<div class="kart-layout">
<div class="kart-wrap">{kart_svg()}</div>
<div class="kart-info" id="kart-info" aria-live="polite"><p class="ph">Velg en bydel i kartet for å se informasjon om den.</p></div>
</div>
</section>
{FOOT}</main></div>
<script>
var BYDEL_DATA={kart_data_js()};
var FELT=[["nabolag","Faller ofte under nabolaget:"],["innbyggere","Innbyggertall:"],["kjent","Kjent for:"],["mangler","Mangler/lite av:"],["tilbud","Andre tilbud:"],["hoyde","Gjennomsnittlig høyde over havet:"]];
var kartInfo=document.getElementById("kart-info"),bydeler=[].slice.call(document.querySelectorAll(".bydel"));
function visBydel(navn){{
  bydeler.forEach(function(g){{g.classList.toggle("active",g.dataset.navn===navn)}});
  var d=BYDEL_DATA[navn]||{{}},html="<h3>"+navn+"</h3><dl>";
  FELT.forEach(function(f){{var v=d[f[0]]||"";html+="<dt>"+f[1]+"</dt><dd"+(v?"":" class=\\"empty\\"")+">"+(v||"Fylles inn senere")+"</dd>"}});
  kartInfo.innerHTML=html+"</dl>";
}}
bydeler.forEach(function(g){{
  g.addEventListener("mouseenter",function(){{visBydel(g.dataset.navn)}});
  g.addEventListener("click",function(){{visBydel(g.dataset.navn)}});
  g.addEventListener("keydown",function(e){{if(e.key==="Enter"||e.key===" "){{e.preventDefault();visBydel(g.dataset.navn)}}}});
  g.addEventListener("focus",function(){{visBydel(g.dataset.navn)}});
}});
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
