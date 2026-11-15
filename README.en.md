# Moldova: law history in git

**English** · **[Sau citiți în română](README.md)**

<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/effort-dark.svg">
<img alt="Moldovan law in this repository: what it holds, changes by the year they took effect, completeness against the official sources, and the correctness of what is held" src="data/effort-light.svg" width="880">
</picture>

The law of Moldova as a git history: one file per article, one commit per version on the day it took effect, and the act that made each change as the commit's author. `git blame` names the act behind every paragraph where the sources say which act it was; `git log` lists every change to an article; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Moldova's national law, which global-law reads at `moldova/national/acts/`.

**What is in it now:** the Constitution of 29 July 1994, in 3 versions (14 July 2006, 4 March 2016 and 20 October 2024), with 180 provisions in the latest. No other act is here yet: no laws or codes, local acts, court decisions or bills. [`constitutia/README.md`](constitutia/README.md) lists every provision and how often it changed.

The Constitution is in `constitutia/`, one file per article (`constitutia/art-078.md` is Article 78, the election of the President); the preamble, titles, chapters and sections have their own files, and the transitional Articles I to VIII are `tranz-01.md` to `tranz-08.md`.

The text is in Romanian, the official language, as the State Register of Legal Acts and the official Moldpres edition print it. The Russian text and an English translation are not part of this record.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to Article 78 of the Constitution | `git log -p --word-diff -- constitutia/art-078.md` |
| Which act wrote each line of Article 78? | `git blame constitutia/art-078.md` |
| Every version of the Constitution, with the day each took effect | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- constitutia ':!constitutia/README.md'` |
| Article 78 as in force on 1 January 2010 | `python tools/on.py 2010-01-01 constitutia art-078` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Moldovan law](https://global-law.lexifina.com/v1/try_claude?country=moldova)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=moldova)**: the same question in ChatGPT.
- **[Search Moldovan law on our site](https://lexifina.com/law?country=moldova&q=concediul+de+odihn%C4%83)**: a search for "concediul de odihnă", with each provision's text and its versions, no account needed.
- **[Developer REST API](https://global-law.lexifina.com/v1/search_law?query=concediul+de+odihn%C4%83&jurisdiction=moldova)**: the same search as JSON, with no key. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in Romanian or in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add moldova/national/acts
python3 tools/law.py show 2026-01-01 moldova/national/acts/constitutia/art-078.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, Europe/Chisinau, on the day the version took effect, and carries it in its `In-force:` trailer:

- a law takes effect on the day it sets, or else on its publication in the Monitorul Oficial (Art. 76 of the Constitution); a Constitutional Court judgment on the day its own text sets (HCC7/2016: on its adoption, 4 March 2016, two weeks before it was published);
- the first version is dated 14 July 2006, the day Law 185-XVI, the last amendment in the register's consolidated text, was published; it sets no day of its own;
- the 2024 version takes the date the Moldpres edition gives itself, 20 October 2024, the day of the referendum that adopted Law 244/2024.

The first version is the "oldest version available", credited to the State Register (the publisher), and its message names the two 1994 corrections and eight laws of 1996 to 2006 it already includes. HCC7/2016 is credited with Articles 78, 85 and 89. The 2024 edition lists seven amending acts since 2016 but not which article each changed, so its 111 changed provisions are one commit credited to the publisher and marked as not explained.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`), and must match the corpus; results are in [`REPRODUCE.md`](REPRODUCE.md).
- The register's 2016 page is compared with the 2013 page that gives the 2006 text: they may differ only in the HCC7 notes, three units whose HTML is corrupted (Arts. 35, 75 and 129) and listed typo corrections.
- HCC7/2016 is applied as written: Articles 78 and 89 take the text its point 8 b) sets out, and the phrase its point 3 strikes leaves Art. 85(4); Article 89 as built equals the 2024 edition word for word. The 2024 text is read from the edition's PDF text layer, with no OCR.
- History is append-only: no merge commits, no commit dates going backwards, nothing dated in the future, and every commit's trailers parse.

## What it does not show

- **The text as adopted in 1994, and each amendment from 1994 to 2006 on its own day.** The register showed only the consolidated text, with notes naming the amending laws but not the earlier words.
- **Each amendment from 2016 to 2024 on its own day, and any change after the 2024 edition.** These need the current register, legis.md, which this build could not read.
- **What the 2016 register page printed for Arts. 78, 85 and 89.** It kept the words of 2000, with notes; this history applies the judgment from the day it took effect.
- **Any other law.** Laws and codes (the Labour Code, the Criminal Code and the rest), local acts, court decisions and bills are not built yet.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [lex.justice.md](https://web.archive.org/web/20130527162646/http://lex.justice.md:80/index.php?action=view&view=doc&lang=1&id=311496), through the Internet Archive | The State Register of Legal Acts' earlier home (Ministry of Justice) | consolidated text only, with notes naming the amending laws | The 2006 text (2013 capture) and [HCC7/2016](https://web.archive.org/web/20160831022417/http://lex.justice.md/md/363742/) (2016 capture) |
| [Moldpres edition of the Constitution](https://presedinte.md/app/webroot/Constitutia_RM/Constitutia_2024_ro.pdf), hosted by the Presidency | Official edition, as amended to 20 October 2024 | no | Lists the amending acts, not which article each changed |

## Licence

See [`LICENSE`](LICENSE). Laws and court decisions are not objects of copyright in Moldova (Law 139/2010 on copyright and related rights); Lexifina's own contributions (the arrangement of the history, the commit messages, the tables and the tools) are CC0 1.0.

No AI model wrote, translated or corrected legal text, and none runs when the history is built; the scripts were written by an AI model (see [`REPRODUCE.md`](REPRODUCE.md)).

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
