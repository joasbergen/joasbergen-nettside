# Joa's Bergen – blogg om Bergen

Statisk nettside på Netlify (joasbergen.no), repo: github.com/joasbergen/joasbergen-nettside. Netlify bygger ikke noe selv: all HTML/CSS genereres lokalt av `bygg.py` og committes. Kjør `python bygg.py` (på Mac: `python3 bygg.py`) etter hver endring.

## Regler for samarbeidet
- Push til GitHub KUN når brukeren sier "push det", "deretter push", "gjennomfør" eller lignende. Ellers: bygg, verifiser, og si fra.
- Bruker skriver på uformell bergensk bokmål ("eg", "ikkje" osv.). Gjengi tekst i innlegg ORDRETT, ikke rett opp stavemåte eller dialekt.
- Test gjerne lokalt (`python -m http.server 8123` i denne mappen) før push.
- Commit-meldinger avsluttes med Co-Authored-By-linjen fra systemet.

## Nytt innlegg
Legg et nytt `dict(...)` ØVERST i `POSTS` i `bygg.py`:

```python
dict(slug="url-navn", img="bildefil.jpg", cats=["Mat og drikke", "Leserinnlegg"], rain=False,
     date="2026-09-29", label="29. september 2026",
     title="Tittel", lead="Kort ingress (vises på forsiden og i fet skrift øverst).",
     body="""<p>Tekst</p><p>Mer tekst</p>"""),
```
- Bildet kopieres til `bilder/` (jpg/webp). Det vises på forsidekortet og som stort bilde øverst i innlegget.
- Kategorier som finnes (`CATS`): Byvandring, Fotturer, Historie, Leserinnlegg, Mat og drikke, Solforhold. `rain=True` gir "Regnværsdag"-merke.
- Avsnitt som `<p>`, lister som `<ul><li>`, mellomtitler som `<h2>`. Signatur (f.eks. HH, JAT, J) som eget `<p>`.
- Valgfritt: `kart=True` setter inn det interaktive bydelskartet, `body2` er tekst etter kartet, `enkel=True` fjerner toppbilde og ingress i selve innlegget (brukes bare av kart-innlegget).
- Forsidekortet viser alltid bilde, kategorier, dato, tittel og ingress.
- Etter `python bygg.py`: commit og push (når brukeren ber om det).

## Kommentarer og kontaktskjema
- Kontaktskjema: Netlify Forms (må være aktivert på siden).
- Kommentarer: publiseres umiddelbart via Netlify Function `netlify/functions/comments.js` (Netlify Blobs, avhenger av `package.json`). Eier sletter ved å trykke "administrer kommentarer" under kommentarfeltet og taste passordet fra miljøvariabelen `KOMMENTAR_PASSORD` (satt i Netlify). Fungerer ikke lokalt, bare på Netlify.

## Kartet
Interaktivt SVG-kart over Bergens strøk: data i `BYDELER` og `BYDEL_INFO` i `bygg.py`, bakgrunn `bilder/bergenskart-sentrum.webp`. Endring av grenser krever `pip install shapely` for overlappssjekk.
