# Tools

The scripts behind this Moldova-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/moldova-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only moldova-law and its commit.
`build_vulns.py`, `flags_chart.py`, `late_ext_select.py` and `late_ext_rebut.py` sit two folders above the scripts, next to
`config.json`.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `add_root.py` | Builds the history rows from this repository's own commits, so the history detectors read every change |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the strongest lapsed time limits in law texts, and the empty periods |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (there were none here) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Romanian and English, light and dark |
| `config.json` | The repository, the Romanian category names, the top-level folders that are not law, and the chart's labels |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(caselaw|decision|data|tools)/'`.

Changes made for this repository:

- `add_root.py` counts as law not only amendments but also an act's first text, which this repository marks `as-enacted`
  (the Competition Council's decisions) or `regulation` (the National Bank's regulations), the Constitutional Court's change
  to the Constitution (`court`) and the publisher's versions of the Constitution (`publisher`). No commit of this repository
  carries one of the kinds global-law's script reads as law, so without them the text and reference scans, which read only
  rows of kind `law`, would read nothing. Records without text (`metadata`) and case law (`case-law`) keep their own kind;
  `config.json` then counts the Competition Council's decisions as not law.
- `run.sh` takes `LE_WORKERS` and `LE_GREP_THREADS` from the environment (default 6), so that a run that runs out of memory
  on a shared machine can be repeated with fewer; it was run with 4 shards.
