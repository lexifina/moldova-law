# Cazuri-limită

**Română** · [English](EDGE-CASES.en.md)

Niciuna dintre cele 42 de semnalări examinate de model nu a rezistat. Iată-le, fiecare verificată manual și grupată după ceea ce s-a dovedit a fi, precum și ce sunt celelalte semnalări. Înapoi la [README-ul despre vulnerabilități](README.md).

## Norme cu efect epuizat (1)

| Dispoziție | Ce spune evidența | De ce nu mai are efect |
| --- | --- | --- |
| [Constituția, articolul IV](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/constitutia/tranz-04.md) (dispoziții tranzitorii) | prevederile articolului 25 alineatul (4), ce țin de termenul arestării, nu se răsfrâng, „până la 1 ianuarie 1995”, asupra persoanelor care au comis infracțiuni grave prevăzute de articolul 7^1 din Codul penal | O normă tranzitorie care și-a epuizat efectul la 1 ianuarie 1995. Singura ei modificare aici este grafia ediției din 2024 („răsfrâng, până” în loc de „răsfrîng, pînă” și „7^1” în loc de „71”, cum figura în registru). |

## Conforme legii (1)

| Act | Ce spune evidența | De ce este conform legii |
| --- | --- | --- |
| [Hotărârea HCC7/2016](https://github.com/lexifina/moldova-law/commit/009fddfa39d87241201b8f4e62297dca2438a1c9) a Curții Constituționale, care modifică articolele 78, 85 și 89 din Constituție | în vigoare de la 4 martie 2016, publicată la 18 martie 2016 | Legile sau unele părți ale acestora devin nule „din momentul adoptării hotărârii corespunzătoare a Curții Constituționale” (articolul 140 alineatul (1) din Constituție), iar hotărârile Curții prevăd că intră în vigoare la data adoptării, cum o face și [Hotărârea nr. 14 din 5 noiembrie 2026](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/caselaw/curtea-constitutionala/2026/hotariri-901/text.md), aflată în acest depozit, la punctul 5. |

## Nu sunt acte normative (40)

| Text | Ce spune evidența | De ce nu se socotește |
| --- | --- | --- |
| 40 de decizii ale Consiliului Concurenței, printre care [CN-36 din 21 iulie 2016](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2016/cn-36/text.md), [ASS-44 din 2 iulie 2015](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2015/ass-44/text.md) și [CN-28 din 29 iunie 2017](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2017/cn-28/text.md) | un certificat de conformitate din 29 aprilie 2015, „valabil până la 28 aprilie 2018”; planul de acțiuni al Î.S. „Calea Ferată din Moldova” din acordul de proiect încheiat cu BERD, cu termene de felul „Pînă pe 31.03.2016”; „Barrisol” SRL urma să înlăture două sintagme de pe eticheta sării de baie „până la data de 01 septembrie 2017” | Fapte ale cauzei: licențe, permise de activitate pe rută și certificate cu termenele lor, perioade contractuale, o obligație stabilită de Consiliu pentru o parte, primăria unui sat care trebuia să transmită informații privind ajutorul de stat „până la 31.03.2017” ([ASR-39 din 27 iulie 2016](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2016/asr-39/text.md)). O decizie într-o singură cauză, nu legislație; modelul nu a considerat niciuna dintre ele un defect. |

La prima rulare, modelul a considerat două dintre aceste semnalări posibile defecte, pe care a doua trecere le-a respins pe amândouă: certificatul din CN-36 este examinat și acum și este considerat un artefact; [DA-26 din 21 iunie 2017](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2017/da-26/text.md) (SRL „Transenca-Tur” urma să prezinte copiile unor acte „până la 31.03.2017”) și o perioadă din starea de fapt a unei cauze civile a Curții Supreme de Justiție (2rac-132/13 din 29 mai 2013) se află în continuare în `flags.csv`, dar nu mai sunt printre cele mai puternice, deoarece detectorul corectat a găsit mai multe semnalări cu punctajul maxim.

## Nesemnalate: urme ale HCC7/2016 în text

Observate la verificarea semnalării privind hotărârea; niciun detector nu le caută și niciuna nu schimbă conținutul vreunei norme.

- [Articolul 78](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/constitutia/art-078.md) trece de la alineatul (4) la alineatul (6). De la HCC7/2016 ([modificarea](https://github.com/lexifina/moldova-law/commit/009fddfa39d87241201b8f4e62297dca2438a1c9)), fostul alineat (5), potrivit căruia Președintele în exercițiu dizolva Parlamentul dacă nici după alegerile repetate Președintele nu era ales, a dispărut, iar alineatele nu au fost renumerotate. Ediția Moldpres din 2024 tipărește articolul la fel.
- [Articolul 85 alineatul (4)](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/constitutia/art-085.md) are textul „... mandatului Președintelui Republicii Moldova, și nici în timpul stării de urgență ...”: sintagma eliminată de HCC7/2016, „cu excepția cazului prevăzut la articolul 78 alineatul (5)”, a dispărut, dar virgula dinaintea ei a rămas. Ediția din 2024 tipărește și ea virgula.

## Celelalte semnalări

- **Termene expirate:** 206 din cele 207 se află în decizii, 171 ale Consiliului Concurenței și 35 ale Curții Supreme de Justiție; 25 sunt într-o singură decizie, [APD-18 din 21 aprilie 2016](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2016/apd-18/text.md), privind întreprinderile care nu au livrat medicamente instituțiilor medico-sanitare publice: 16 sunt contracte de livrare „valabil până la data de 31.12.2015”, iar 6 sunt termenele licențelor de activitate farmaceutică ale întreprinderilor. Dintre cele 41 examinate, 29 au fost considerate artefacte și 12 conforme legii; niciuna nu a fost un posibil defect. Detectorul citește acum „pînă” și „până la data de” înaintea unei date; îi scapă încă 23 de sintagme cu o dată trecută („până în anul”, „până la finele anului” și altele), 22 în decizii și una într-un aviz al Curții Constituționale.
- **Intrare în vigoare înainte de publicare:** singura semnalare, mai sus.
- **Numerotare dublă:** citite manual, nu de un model. Sunt rezultate fals pozitive. Cele 14 „numere duble”, 13 în decizii ale Consiliului Concurenței și 1 într-o decizie a Curții Supreme de Justiție, sunt același articol al unei legi citat la începutul a două rânduri (de exemplu „art. 19 alin. (1) lit. b) din Legea concurenţei nr. 183 din 11.07.2012” de două ori în [CN-62 din 8 octombrie 2015](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2015/cn-62/text.md)).
- **Monede ieșite din uz:** niciuna acum. Cele 3 de la prima rulare erau „inti”, fosta monedă a Perului, găsită în interiorul cuvintelor „intimatul” și „intimatului” în trei decizii ale Curții Supreme de Justiție; detectorul corectat recunoaște „inti” doar ca termen de sine stătător.
