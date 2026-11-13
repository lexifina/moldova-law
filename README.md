# Moldova: istoria dreptului în git

**Română** · [English](README.en.md)

<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/ro/effort-dark.svg">
<img alt="Legislația Republicii Moldova în acest depozit: ce conține, modificările pe anul intrării în vigoare, completitudinea față de sursele oficiale și corectitudinea conținutului" src="data/ro/effort-light.svg" width="880">
</picture>

Face parte din [lexifina/global-law](https://github.com/lexifina/global-law), o singură istorie git pentru dreptul tuturor țărilor: acesta este dreptul național al Republicii Moldova, pe care global-law îl citește la `moldova/national/acts/`.

Dreptul Republicii Moldova ca istorie git: un fișier pentru fiecare dispoziție, un commit pentru fiecare modificare, la data intrării ei în vigoare, iar legea sau hotărârea judecătorească care a făcut fiecare modificare este autorul commitului. `git blame` indică actul din spatele unui alineat acolo unde sursele arată care a fost acel act; `git log` enumeră fiecare modificare a unui articol; alegând o dată, se obține textul în vigoare în acea zi.

Depozitul urmează structura comună a [lexifina/global-law](https://github.com/lexifina/global-law), care îl plasează la `md/`. Textele sunt în limba română, limba oficială, așa cum le tipăresc Registrul de stat al actelor juridice și ediția oficială Moldpres.

**Ce conține acum**

| Dosar | Act | Versiuni | Istoric |
| --- | --- | ---: | --- |
| `constitutia/` | Constituția Republicii Moldova (Constituția din 29 iulie 1994) | 3 | Textul consolidat cu modificările până în 2006 (cea mai veche versiune disponibilă); Hotărârea Curții Constituționale HCC7/2016 (4 martie 2016); ediția oficială cu modificările până la 20 octombrie 2024 |

Acest depozit a fost construit din ceea ce poate fi citit:

- fosta adresă a registrului, **lex.justice.md** (Ministerul Justiției), prin capturile din Internet Archive (2008-2024). Pagina sa cu Constituția conține textul consolidat, cu note care indică legile de modificare, până în 2006, precum și notele adăugate pentru HCC7/2016;
- **Hotărârea Curții Constituționale HCC7/2016** de pe același site, al cărei punct 8 lit. b) stabilește noul text al articolelor 78 și 89;
- **ediția Moldpres** „Constituția Republicii Moldova. Cu modificări și completări la data de 20 octombrie 2024” (Moldpres este agenția de stat care publică Monitorul Oficial), găzduită ca PDF de Președinție (presedinte.md).

## Întrebările unui jurist, ca comenzi git

| Întrebare | Comandă |
| --- | --- |
| Ce prevedea articolul 78 la 1 ianuarie 2010? | `python tools/on.py 2010-01-01 constitutia art-078` |
| Același lucru, doar cu git (bash) | `git show $(git rev-list -1 --before="2010-01-01T23:59:59Z" main -- constitutia/art-078.md):constitutia/art-078.md` |
| Același lucru, în PowerShell | `$r = git rev-list -1 --before="2010-01-01T23:59:59Z" main -- constitutia/art-078.md; git show "$($r):constitutia/art-078.md"` |
| Cine a scris fiecare alineat al articolului 89? | `git blame constitutia/art-089.md` |
| Fiecare modificare a articolului 13 (limba), cuvânt cu cuvânt | `git log -p --word-diff constitutia/art-013.md` |
| Toate modificările, în ordine | `git log --reverse --format="%ad %an" --date=short main` |
| Tot ce a modificat HCC7/2016 | `git log --author="HCC7" --stat` |
| Întreaga Constituție la o anumită dată | `python tools/on.py 2020-01-01 constitutia` |

După o reconstrucție, actualizați etichetele cu `git fetch --force --tags`: un fetch simplu păstrează etichetele vechi.

## Datare

- Fiecare commit este datat la **ora 12:00, ora Europe/Chisinau, în ziua în care modificarea a intrat în vigoare**. Datele adoptării și publicării sunt trailere; ziua intrării în vigoare se află în `In-force:`, pe care îl citește `tools/on.py`.
- **Constituția** a fost adoptată la 29 iulie 1994, publicată în Monitorul Oficial nr. 1 la 12 august 1994 și a intrat în vigoare la 27 august 1994 (art. I al ei). Textul ei, așa cum a fost adoptat inițial, nu se află în nicio sursă pe care această construcție a putut-o citi, astfel că istoria începe la 14 iulie 2006.
- **14 iulie 2006**: cea mai veche versiune disponibilă, textul consolidat al registrului, care consemnează toate modificările până la Legea nr. 185-XVI din 29 iunie 2006, publicată la 14 iulie 2006. Această lege nu stabilește o dată proprie, așa că, potrivit art. 76 din Constituție, a intrat în vigoare la data publicării.
- **4 martie 2016**: HCC7/2016 a intrat în vigoare la data adoptării (punctul 9 al ei), înainte de publicarea din 18 martie 2016.
- **20 octombrie 2024**: data pe care și-o atribuie ediția Moldpres („la data de 20 octombrie 2024”), ziua referendumului prin care a fost adoptată Legea nr. 244/2024.
- `--before="YYYY-MM-DD"` fără oră folosește ora curentă a ceasului dumneavoastră; folosiți `T23:59:59Z`, ca mai sus, sau instrumentul.

## Cum este verificat

- **Cele două pagini ale registrului concordă.** Pagina registrului din 2016 este comparată cu cea din 2013, folosită pentru textul din 2006: poate diferi doar prin notele privind HCC7, în trei unități în care HTML-ul ei este corupt (art. 35, 75, 129) și prin corecturile de greșeli de tipar enumerate; orice altă diferență oprește construcția.
- **Hotărârea este aplicată așa cum este scrisă.** Articolele 78 și 89 primesc textul stabilit la punctul 8 lit. b) din HCC7/2016, iar sintagma de la punctul 3 este eliminată din art. 85 alin. (4). Articolul 89, așa cum este construit, este identic cuvânt cu cuvânt cu ediția din 2024. Articolul 78 diferă de aceasta doar prin înlocuirea sintagmei „limba de stat” cu „limba română” (Legea nr. 52/2023), iar articolul 85 doar printr-o corectură ortografică.
- **Textul din 2024 este cel al ediției**, citit din stratul de text al PDF-ului: fiecare articol, titlu, capitol și secțiune, în ordine. Construcția verifică faptul că ediția numește cele șapte acte de modificare pe care le enumeră.
- Fiecare versiune este citită înapoi din git în ziua în care a intrat în vigoare și în ziua precedentă (`tools/check_repo.py`); ambele trebuie să corespundă cu `corpus.json`. Rezultatele se află în `REPRODUCE.md`.
- Verificări de integritate: niciun commit de îmbinare (merge) pe `main`, datele commiturilor nu merg niciodată înapoi, nimic nu este datat în viitor, iar trailerele fiecărui commit pot fi analizate cu `git interpret-trailers --parse`.
- Depozitul este reconstruit a doua oară din aceleași date și trebuie să dea hashuri identice.

## Ce înseamnă „autor”

Autorul unui commit este legea sau hotărârea care a făcut modificarea, cu o adresă de e-mail care nu poate exista (`hcc-7-2016@legis.invalid`), astfel încât `git blame` și `git log --author` o numesc. Cel care face commitul (committer) este întotdeauna Lexifina.

- **Primul commit** este cea mai veche versiune disponibilă, atribuită Registrului de stat (editorul). Mesajul său numește actele care modificaseră deja textul: cele două corecturi din 1994 și Legile nr. 957/1996, 1115/2000, 351/2001, 1469, 1470 și 1471/2002, 344/2003 și 185/2006.
- **Atribuirile provin numai din surse.** Hotărârii HCC7/2016 îi sunt atribuite articolele 78, 85 și 89, dispozițiile numite în dispozitivul ei.
- **Modificările din 2024 nu sunt atribuite una câte una.** Între 2016 și 2024, ediția Moldpres enumeră șapte acte de modificare: Legile nr. 256/2016, 70/2017, 255/2018 și 120/2021, Legea nr. 52/2023 (privind denumirea limbii), Hotărârea Curții Constituționale HCC8/2024 și Legea nr. 244/2024 (modificarea privind integrarea europeană, adoptată prin referendum). Ediția nu conține note care să arate ce articol a modificat fiecare act, iar textele acestora nu au putut fi citite, așa că cele 111 unități care diferă formează un singur commit, cu editorul drept autor, marcat ca neexplicat. În plus, textul republicat folosește peste tot ortografia actuală („â”, „sunt”), astfel că aproape fiecare articol diferă față de 2016.
- Blame atribuie rânduri întregi (un alineat sau o literă pe rând); folosiți `git log -p --word-diff` pentru cuvinte.

## Ce nu arată

- **Textul din 1994 așa cum a fost adoptat și fiecare modificare din perioada 1994-2006 la data ei.** Registrul arată doar textul consolidat, cu note precum „[Art.78 în redacția LP1115-XIV din 05.07.00]”, dar nu și formulările anterioare.
- **Fiecare modificare din perioada 2016-2024 la data ei** (vezi mai sus) și **orice modificare ulterioară ediției din 2024**. Pentru acestea este nevoie de legis.md.
- **Ce a tipărit pagina registrului din 2016 pentru art. 78, 85 și 89**: aceasta a păstrat formulările din 2000 și a adăugat note. Această istorie aplică, în schimb, hotărârea de la data intrării ei în vigoare.
- **Legile ordinare.** Legea nr. 133/2011 privind protecția datelor cu caracter personal (abrogată de la 23 august 2026 prin Legea nr. 195/2024), Legea nr. 195/2024 însăși și Codul penal (985/2002) nu sunt construite. Textele lor actuale se află doar pe legis.md, iar arhivele conțin doar pagini ale registrului de dinainte de 2019.
- **Textul în limba rusă.** Aici se află doar textul oficial, în limba română.

## Cum este construit

Lexifina citește sursele enumerate aici și înregistrează versiunile datate ale fiecărui act, precum și legile care au făcut fiecare modificare, într-un singur fișier de corpus. `tools/build.py` scrie acest depozit din acel fișier, iar același corpus dă întotdeauna aceleași hashuri de commit; `REPRODUCE.md` oferă detaliile și verificările. Un model (Claude) a scris codul Lexifina; nu a scris niciun text juridic, iar la construirea istoriei nu rulează niciun model.

Nu s-a folosit OCR și niciun model AI nu a scris sau modificat text juridic. Claude Opus 5.5 a scris scripturile și a ales sursele; vezi `REPRODUCE.md`.

## Surse

| Sursă | Tip | Versiuni anterioare, pe date | Numește actul de modificare | API sau descărcare în bloc | Note |
| --- | --- | --- | --- | --- | --- |
| [Registrul de stat al actelor juridice](https://www.legis.md) | Legislație oficială | da (versiuni datate pentru fiecare act) | da | nu | – |
| [lex.justice.md](http://lex.justice.md/md/311496/) prin [Internet Archive](https://web.archive.org/) | Fosta adresă a registrului (Ministerul Justiției) | doar textul consolidat | în note, pe articole | nu | Capturi 2008-2024; pagina Constituției nu s-a mai schimbat după 2016 |
| [Președinția: Constituția](https://presedinte.md/rom/constitutia-republicii-moldova) | Ediția Moldpres din 2024 (PDF, strat de text) | nu | enumeră actele de modificare, nu pe articole | nu | ISBN 978-9975-3618-2-8 |
| [Monitorul Oficial](https://monitorul.gov.md) | Publicația oficială (Moldpres) | fiecare număr | da | nu | Numerele din 2009 încoace pot fi consultate online; descărcarea lor necesită un abonament plătit, de aceea nu este folosit |

Ghiduri de cercetare: [GlobaLex](https://www.nyulawglobal.org/globalex/) și [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licență

Textele oficiale, precum legile și hotărârile judecătorești, nu sunt protejate de dreptul de autor în Republica Moldova (Legea nr. 139/2010 privind dreptul de autor și drepturile conexe). Textele provin din Registrul de stat al actelor juridice (lex.justice.md, citit prin Internet Archive) și din ediția Moldpres a Constituției (2024). Contribuțiile proprii ale Lexifina sunt dedicate domeniului public prin CC0 1.0; vezi `LICENSE`.

Acest depozit nu constituie consultanță juridică și nu este o publicație oficială.

Aceasta este o traducere a versiunii în engleză ([README.en.md](README.en.md)); dacă diferă, prevalează versiunea în engleză.

## Mai multe

Din depozitul [lexifina/global-law](https://github.com/lexifina/global-law) (pagini în engleză):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): toate funcțiile și ce trebuie să suporte fiecare corpus (`git blame`, `law.py`, instrumente MCP)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): întrebări și răspunsuri · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): propunerea de modificări · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): serverul MCP · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): cum a fost construit · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): cât de actualizat este fiecare corpus · [Monitorizare](https://github.com/lexifina/global-law/tree/main/monitoring): dacă actualizările funcționează · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): cum este urmărită fiecare sursă oficială pentru modificări
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): cât de rapide sunt instrumentele, măsurat
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): grafice și legături în dreptul întregii lumi
- [Vulnerabilități](https://github.com/lexifina/global-law/tree/main/vulnerabilities): erori în actele normative așa cum au fost publicate
