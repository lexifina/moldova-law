"""Moldova: the Constitution (Constituția Republicii Moldova, 29.07.1994) parsed into units.

Two official expressions are read:
- the State Register of Legal Acts in its earlier home, lex.justice.md (Ministry of Justice), as archived by the
  Internet Archive (HTML, one page per act, consolidated, with "[Art.N în redacția ...]" notes);
- the Moldpres edition "Constituția Republicii Moldova. Cu modificări și completări la data de 20 octombrie 2024"
  (Moldpres, the state agency that publishes the Monitorul Oficial; PDF with a text layer, hosted by the Presidency).

Both are reduced to the same unit keys: preambul, titlul-NN[-capitolul-NN[-sectiunea-N]] headings, art-NNN[-N]
articles and tranz-NN (Titlul VII, Articolul I-VIII). Typesetting is normalised the same way for both
(norm()); words, spelling and punctuation are kept.
"""
import html as _html
import re
import subprocess

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


def norm(s):
    s = s.replace(" ", " ").replace("­", "")
    s = s.translate(str.maketrans("şŞţŢ", "șȘțȚ"))   # cedilla and comma-below forms are one letter
    s = s.replace("‐", "-").replace("‑", "-")
    s = re.sub(r"\s+[-–—]\s+", " – ", s)            # a spaced dash is one dash
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,;.:)])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    return s


def roman(n):
    return ROMAN.index(n) + 1


# ------------------------------------------------------------------ structure from a flat list of lines

ART = re.compile(r"^Articolul\s+(\d+)(?:\^(\d+))?(?:\s*[-–]\s*(abrogat|exclus)\.?)?$")
TART = re.compile(r"^Articolul\s+([IVX]+)$")
TITLU = re.compile(r"^Titlul\s+([IVX]+)(?:\^(\d))?$")
CAP = re.compile(r"^Capitolul\s+([IVX]+)(?:\^(\d))?$", re.I)
SECT = re.compile(r"^Secțiunea\s+(?:a\s+)?(\d)(?:-a)?$")


def art_key(n, sup):
    return f"art-{int(n):03d}" + (f"-{sup}" if sup else "")


def build_units(items):
    """items: list of ("head", text) | ("para", text) in reading order. Returns {key: unit}."""
    units = {}
    order = []
    cur = None        # key of the unit being filled
    title = chapter = None
    pending_caption = None  # key of a heading/article whose caption comes next

    def start(key, label, kind, heading):
        nonlocal cur
        assert key not in units, key
        units[key] = {"label": label, "kind": kind, "lines": [heading]}
        order.append(key)
        cur = key

    for kind, text in items:
        if kind == "bold":
            kind = "head" if (pending_caption and pending_caption == cur) else "para"
        if kind == "head":
            m = ART.match(text)
            if m:
                n, sup, gone = m.groups()
                key = art_key(n, sup)
                lab = f"Art. {int(n)}" + (f"^{sup}" if sup else "")
                start(key, lab, "art", f"# Articolul {n}" + (f"^{sup}" if sup else ""))
                if gone:
                    units[key]["lines"][0] += f" – {gone}."
                    pending_caption = None
                else:
                    pending_caption = key
                continue
            m = TART.match(text)
            if m:
                key = f"tranz-{roman(m.group(1)):02d}"
                start(key, f"Art. {m.group(1)} (dispoziții tranzitorii)", "transitional", f"# Articolul {m.group(1)}")
                pending_caption = None
                continue
            m = TITLU.match(text)
            if m:
                title = f"titlul-{roman(m.group(1)):02d}" + (f"-{m.group(2)}" if m.group(2) else "")
                chapter = None
                start(title, f"Titlul {m.group(1)}" + (f"^{m.group(2)}" if m.group(2) else ""), "title",
                      f"# Titlul {m.group(1)}" + (f"^{m.group(2)}" if m.group(2) else ""))
                pending_caption = title
                continue
            m = CAP.match(text)
            if m:
                # chapters are numbered through the whole Constitution (I-IX), so the key does not need the title
                chapter = f"capitolul-{roman(m.group(1).upper()):02d}" + (f"-{m.group(2)}" if m.group(2) else "")
                start(chapter, f"Capitolul {m.group(1).upper()}" + (f"^{m.group(2)}" if m.group(2) else ""),
                      "chapter", f"# Capitolul {m.group(1).upper()}" + (f"^{m.group(2)}" if m.group(2) else ""))
                pending_caption = chapter
                continue
            m = SECT.match(text)
            if m:
                key = f"{chapter}-sectiunea-{m.group(1)}"
                start(key, f"Secțiunea {m.group(1)} ({chapter})", "section",
                      "# Secțiunea " + ("1" if m.group(1) == "1" else f"a {m.group(1)}-a"))
                pending_caption = key
                continue
            if pending_caption and pending_caption == cur:
                u = units[cur]
                if u["kind"] in ("title", "chapter", "section") and len(u["lines"]) > 1:
                    u["lines"][-1] += " " + text   # a caption set on two lines ("DREPTURILE, LIBERTĂȚILE ȘI / ...")
                else:
                    u["lines"].append(("## " if u["kind"] == "art" else "") + text)
                if u["kind"] == "art":
                    pending_caption = None
                continue
            raise ValueError(f"unplaced heading: {text!r} after {cur}")
        else:
            pending_caption = None
            if cur is None:
                cur = "preambul"
                units[cur] = {"label": "Preambul", "kind": "preamble", "lines": []}
                order.append(cur)
            units[cur]["lines"].append(text)
    out = {}
    for k in order:
        u = units[k]
        out[k] = {"label": u["label"], "kind": u["kind"], "text": "\n".join(u["lines"]) + "\n"}
    return out


# ------------------------------------------------------------------ lex.justice.md (archived HTML)

NOTE = re.compile(r"^\[(.+)\]$")


def register_items(raw):
    """Lines of the consolidated text from a lex.justice.md page, and the bracketed notes per unit."""
    s = raw.decode("utf-8")
    i = s.find("NOI,")
    j = s.rfind("Articolul VIII")
    assert i > 0 and j > i
    j = s.find("</div>", s.find("vigoare", j))
    body = s[s.rfind("<", 0, i):j]
    body = re.sub(r"<sup>\s*(\d+)\s*</sup>", r"^\1", body, flags=re.I)
    body = re.sub(r"<br\s*/?>|</div>|</p>|<div[^>]*>|<p[^>]*>", "\n", body, flags=re.I)
    # bold spans that open a heading become their own lines
    body = re.sub(r"<span[^>]*font-weight:\s*bold[^>]*>", "\n\x01", body, flags=re.I)
    body = re.sub(r"<[^>]+>", "", body)
    body = _html.unescape(body)
    items, notes = [], []
    for line in body.split("\n"):
        bold = "\x01" in line
        line = norm(line.replace("\x01", ""))
        if not line:
            continue
        line = re.sub(r"^T\s?i\s?t\s?l\s?u\s?l\b", "Titlul", line)
        line = re.sub(r"^Articolul\s+(\d+)\s+(\d)$", r"Articolul \1^\2", line)
        m = NOTE.match(line)
        if m:
            notes.append((len(items), m.group(1)))
            continue
        kind = "bold" if bold and not line.startswith("(") and len(line) < 140 else "para"
        if ART.match(line) or TART.match(line) or TITLU.match(line) or CAP.match(line) or SECT.match(line):
            kind = "head"
        items.append((kind, line))
    return items, notes


def from_register(raw):
    items, notes = register_items(raw)
    units = build_units(items)
    return units, [n for _, n in notes]


# ------------------------------------------------------------------ Moldpres 2024 edition (PDF)

def pdf_lines(path):
    out = subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", path, "-"], capture_output=True, check=True)
    return out.stdout.decode("utf-8").split("\n")


def moldpres_items(lines, known_words):
    """Paragraphs: a line indented 3-4 spaces starts one, a line at column 0 continues it, a line indented 5+
    is a heading. Page furniture (running head, page numbers) is dropped. A hyphen at a line end is a line-break
    hyphen unless the hyphenated form is a known word (known_words: words seen elsewhere with their hyphen)."""
    start = next(i for i, l in enumerate(lines) if l.strip().startswith("NOI, reprezentan"))
    end = next(i for i, l in enumerate(lines) if "intrarea ei în vigoare" in l) + 1
    paras = []   # [kind, [lines]]
    for raw in lines[start:end]:
        if not raw.strip():
            continue
        t = raw.rstrip()
        st = t.strip()
        if st in ("CONSTITUŢIA REPUBLICII MOLDOVA", "CONSTITUȚIA REPUBLICII MOLDOVA") or re.fullmatch(r"\d{1,2}", st):
            continue
        ind = len(t) - len(t.lstrip(" "))
        if ind >= 5:
            paras.append(["head", [st]])
        elif ind >= 1 or not paras or paras[-1][0] == "head":
            paras.append(["para", [st]])
        else:
            paras[-1][1].append(st)
    items = []
    for kind, ls in paras:
        if kind == "head":
            # superscripts are flattened in the text layer: "Articolul 1061", "Titlul V1", "Capitolul III1"
            items.append(("head", ls[0]))
            continue
        text = ls[0]
        for nxt in ls[1:]:
            if text.endswith("-") and not text.endswith(" -"):
                left = re.search(r"(\S+)-$", text).group(1)
                right = re.match(r"\S+", nxt).group(0)
                joined_h = (left + "-" + right).strip(",.;:()„”")
                if joined_h.lower() in known_words:
                    text = text + nxt
                else:
                    text = text[:-1] + nxt
            else:
                text = text + " " + nxt
        items.append(("para", norm(text)))
    return items


def fix_superscripts(items):
    """Turn the flattened 'Articolul 1061' / 'Titlul V1' / 'Capitolul III1' back into 106^1, V^1, III^1."""
    out, last = [], 0
    for kind, t in items:
        if kind == "head":
            t = norm(t)
            m = re.match(r"^Articolul (\d+)(.*)$", t)
            if m:
                n, rest = m.group(1), m.group(2)
                if int(n) > last + 1 and len(n) > len(str(last)) and n.startswith(str(last)):
                    t = f"Articolul {last}^{n[len(str(last)):]}{rest}"
                else:
                    last = int(n)
            t = re.sub(r"^(Titlul|Capitolul) ([IVX]+)1$", r"\1 \2^1", t)
        out.append((kind, t))
    return out


def from_moldpres(path, known_words):
    return build_units(fix_superscripts(moldpres_items(pdf_lines(path), known_words)))
