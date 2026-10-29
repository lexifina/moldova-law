# How this repository was made (Moldova)

This file is written by the build on 2026-10-29, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| Registrul de stat al actelor juridice, lex.justice.md (via the Internet Archive) | <http://lex.justice.md/md/311496/> | 2026-10-29 | 46 | Official texts, not objects of copyright (Law 139/2010); Internet Archive Wayback Machine captures (id_ raw form), pinned by timestamp |
| Moldpres: Constituția Republicii Moldova, cu modificări și completări la data de 20 octombrie 2024 (PDF, hosted by the Presidency) | <https://presedinte.md/app/webroot/Constitutia_RM/Constitutia_2024_ro.pdf> | 2026-10-29 | 1 | Official text, not an object of copyright (Law 139/2010) |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitutia` | Constituția Republicii Moldova | 3 | 2006-07-14 to 2024-10-20 |

The build made 3 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 1 | one law on its in-force day |
| 1 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `viitor`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 11 laws in the record.
- 4 tags.

## Dates

Each commit is dated at noon (Europe/Chisinau) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Constituția Republicii Moldova art. 76: a law is published in the Monitorul Oficial and takes effect on the day of publication or on the day its text sets. A Constitutional Court judgment takes effect on the day its own text sets (HCC7/2016: on adoption). https://www.legis.md/cautare/getResults?doc_id=145723&lang=ro

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-29
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-29 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/moldova-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `600ef3b171cb68303f4947c2d1dbb7f693fd880ac87ef58ffd09d95e57622d20` (306635 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `2bfc4ac9df193a7be844556d7f69cdb9d93ec3f2` |
| check.py | `cd346c7ff9996d450240e3bab52bcae03b2bc865` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `7771d377b9a6a4ef4652859403a2b70e7fe9c4e2` |
| parse.py | `c33505f0e43a74b7b37f5336558a3309f5895ac1` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

Not yet run for this build.

A second build from the same corpus into an empty folder gave identical hashes for all 3 history commits and 4 tags (history tip `03888561d5e28fbed36026bd939fd056e082d3bf`).

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- No dated versions before 2006 are available: the register shows only the consolidated text, with notes ('[Art.78 în redacția LP1115-XIV ...]') but not the earlier wording. The first version is the register's text as amended by LP185-XVI/2006 ('oldest version available', first_law null), dated 14 July 2006, the day LP185-XVI was published: it has no in-force clause, so Constitution art. 76 (in force on publication) applies. The register lists no amending act between LP185-XVI and HCC7/2016.
- The 2013-05-27 capture is used for that text: from 2015 the register page carries markup corruption inside art. 35, 75 and 129 (escaped tags in the middle of words). The 2016 capture is checked against it: it differs only in those units, in the HCC7 notes, and in typo corrections (art. 24, 26, 34, 72, 88, 93, 136, Art. IV), which reach this history with the 2024 edition.
- HCC7/2016: the register kept the 2000 words and added notes; this build applies the judgment itself. Articles 78 and 89 take the text its point 8 b) sets out ('vor avea următorul cuprins'), and the phrase point 3 strikes is removed from art. 85 (4) with its commas as the 2024 edition reads it. The judgment took effect on adoption, 4 March 2016 (its point 9).
- The 2024 version is the Moldpres edition dated 20 October 2024 (the day of the referendum that adopted Law 244/2024), the date the edition gives itself. The sources give no per-article attribution for the seven acts it lists after 2016 (LP256/2016, LP70/2017, LP255/2018, LP120/2021, LP52/2023, HCC8/2024, Law 244/2024), so those changes are one uncredited commit on that day rather than guessed credits. Any change after that edition is not shown, because legis.md cannot be read.
- Typesetting normalised the same way in every source: cedilla ş/ţ and comma-below ș/ț are one letter (written ș, ț); spaced dashes are '–'; runs of spaces collapse; thousands set with a space ('200 000') are joined; letter-spaced headings ('G U V E R N U L') are joined; line-end hyphens of the PDF are removed unless the hyphenated word is printed elsewhere with its hyphen. Spelling is kept as each source prints it, including the 2024 edition's 'nou- ales' (art. 80) and its misprint 'Artcolul 52' (the heading line is rewritten from the article number).
- Units: the preamble; titles, chapters and sections as heading files (titlul-NN, capitolul-NN, capitolul-NN-sectiunea-N); articles art-NNN with art-NNN-N for superscript numbers (106^1); Title VII's Articles I-VIII as tranz-NN. An article file's first line is '# Articolul N', its second its caption.
- Left out as not law: the register's bracketed notes and 'Notă:' lines (used only to check credits), the 1961 footnote to Art. IV, a stray 'Originalul art.24' line, and the 2024 edition's 'Articolul 82 - abrogat.' / 'Articolul 83 - abrogat.' lines (a repealed article is a removed file; the register omits them too).
- Not built (Phase 1 core acts): Law 133/2011 on personal data protection, repealed from 23 August 2026 by Law 195/2024; the Criminal Code (985/2002), amended by well over a hundred acts; and Law 195/2024 itself. Their current texts are only on legis.md, and archives hold only pre-2019 register pages for the older two, so no build of them could end at today's official text (over the 45-minute budget per act).

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) chose the sources and wrote the fetch and parse scripts. No model wrote or edited legal text; the HCC7 wording is read from the judgment by code. No model runs at parse or git-build time.
