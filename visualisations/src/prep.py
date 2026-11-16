"""Compute every number of the 20 charts into .build/data.json (run by make.py).

    python prep.py <.build folder>

Reads only what make.py extracted from git: commits.jsonl, records.jsonl, texts.jsonl, constitution.json and
repo/data/. Every classification below is a rule on the repository's own words (titles, operative parts,
case numbers); whatever no rule recognises is counted as "other" and shown as such.
"""
import collections, csv, datetime, difflib, json, os, re, statistics, sys

B = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '.build')
OUT = {}
PF = {}


def jl(name):
    with open(os.path.join(B, name), encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)


def D(s):
    return datetime.date.fromisoformat(s[:10])


def norm_cedilla(s):
    return s.replace('ş', 'ș').replace('ţ', 'ț').replace('Ş', 'Ș').replace('Ţ', 'Ț')


def lev(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def med(a):
    return statistics.median(a) if a else None


# ====================================================================== I. the Constitution
CONST = json.load(open(os.path.join(B, 'constitution.json'), encoding='utf-8'))
assert len(CONST) >= 3, 'expected three versions of the Constitution'
VD = [v['date'] for v in CONST]
U = {v['date']: v['units'] for v in CONST}
V0, V1, V2 = VD[0], VD[1], VD[-1]
last = U[V2]


def caption(units, u):
    lines = units[u].split('\n')
    return lines[1].lstrip('# ').strip() if len(lines) > 1 else ''


# the titles' article ranges, checked against the captions and words the repository holds (fails loudly if they move)
CHECK = [('art-014', 'Capitala'), ('art-015', 'Universalitatea'), ('art-059-1', 'Avocatului Poporului'), ('art-060', 'Parlamentul'),
         ('art-125-1', 'Consiliul Superior al Procurorilor'), ('art-126', 'Economia'), ('art-133', 'Curtea de Conturi'),
         ('art-140', 'Hotărârile Curții Constituționale'), ('art-141', 'Inițiativa revizuirii'), ('art-143', 'Legea privind modificarea Constituției')]
for u, w in CHECK:
    assert w in caption(last, u), (u, caption(last, u))
assert 'Curtea Constituțională' in last['art-134'] and 'Uniunii Europene' in last['art-140-1'] and 'INTEGRAREA ÎN UNIUNEA EUROPEANĂ' in last['titlul-05-1']
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}


def title_of(u):
    if u == 'preambul':
        return 'P'
    m = re.match(r'art-(\d{3})(?:-(\d))?$', u)
    if m:
        n, s = int(m.group(1)), int(m.group(2) or 0)
        if n <= 14: return 'I'
        if n <= 59: return 'II'
        if n <= 125: return 'III'
        if n <= 133: return 'IV'
        if n < 140 or (n == 140 and s == 0): return 'V'
        if n == 140: return 'V1'
        return 'VI'
    if u.startswith('tranz-'):
        return 'VII'
    m = re.match(r'titlul-(\d{2})(-1)?$', u)
    if m:
        return ROMAN[int(m.group(1))] + ('1' if m.group(2) else '')
    m = re.match(r'capitolul-(\d{2})', u)
    if m:   # chapters I to III^1 are the rights, IV to IX the public authorities (their headings say so)
        return 'II' if int(m.group(1)) <= 3 else 'III'
    raise ValueError(u)


TORDER = ['P', 'I', 'II', 'III', 'IV', 'V', 'V1', 'VI', 'VII']
for u in last:
    if u.startswith('capitolul'):
        head = last[u].upper()
        if title_of(u) == 'II':
            assert any(k in head for k in ('DISPOZIȚII GENERALE', 'DREPTURILE', 'ÎNDATORIRILE', 'AVOCATUL POPORULUI')), u
        elif not u.endswith(('sectiunea-1', 'sectiunea-2', 'sectiunea-3')):
            assert any(k in head for k in ('PARLAMENTUL', 'PREȘEDINTELE', 'GUVERNUL', 'RAPORTURILE', 'ADMINISTRAȚIA', 'AUTORITATEA JUDECĂTOREASCĂ')), u


def ukey(u):
    if u == 'preambul': return (0, 0, 0)
    m = re.match(r'titlul-(\d{2})(-1)?$', u)
    if m: return (1, int(m.group(1)), 1 if m.group(2) else 0)
    m = re.match(r'capitolul-(\d{2})(?:-(\d))?(?:-sectiunea-(\d))?$', u)
    if m: return (2, int(m.group(1)) * 100 + int(m.group(2) or 0) * 10 + int(m.group(3) or 0), 0)
    m = re.match(r'art-(\d{3})(?:-(\d))?$', u)
    if m: return (3, int(m.group(1)), int(m.group(2) or 0))
    m = re.match(r'tranz-(\d{2})$', u)
    if m: return (4, int(m.group(1)), 0)
    return (9, 0, 0)


def ulabel(u):
    """Art. 59^1, Titlul V^1, Capitolul III^1, Secțiunea 2 (Cap. IV), Art. II (tranz.), Preambul"""
    if u == 'preambul': return 'Preambul'
    m = re.match(r'art-(\d{3})(?:-(\d))?$', u)
    if m: return f"Art. {int(m.group(1))}" + (f"^{m.group(2)}" if m.group(2) else '')
    m = re.match(r'tranz-(\d{2})$', u)
    if m: return f"Art. {ROMAN.get(int(m.group(1)), str(int(m.group(1))))}" if int(m.group(1)) <= 7 else 'Art. VIII'
    return last.get(u, U[V1].get(u, '')).split('\n')[0].lstrip('# ').strip()


def kind_of(u):
    return 'art' if u.startswith('art-') else 'tranz' if u.startswith('tranz-') else 'pre' if u == 'preambul' else 'head'


def words(s):
    return re.findall(r'\w+', s.replace('^', ''))


def spell(s):
    """the 2024 edition's spelling brought back to the 1994-2016 one: â -> î, sunt -> sînt (and suntem, sunteți)"""
    s = s.replace('â', 'î').replace('Â', 'Î')
    for a, b in (('sunt', 'sînt'), ('Sunt', 'Sînt'), ('suntem', 'sîntem'), ('sunteți', 'sînteți')):
        s = re.sub(rf'\b{a}\b', b, s)
    return s


def toks(s):
    return re.findall(r'\S+', s)


def op_kind(a, b):
    ja, jb = ' '.join(a), ' '.join(b)
    if 'moldovene' in ja or ('stat' in ja and 'romîn' in jb):
        return 'language'
    if 'handicap' in ja:
        return 'disability'
    sq = lambda x: re.sub(r'[\W_#]', '', x.lower())
    if sq(ja) == sq(jb):
        return 'editorial'                        # joined/split words, hyphens, quotes, headings, number spacing
    if len(a) == 1 and len(b) == 1:
        x, y = sq(a[0]), sq(b[0])
        if lev(x, y) <= 2 or (len(os.path.commonprefix([x, y])) >= 6 and lev(x, y) <= 4):
            return 'editorial'                    # a letter or an ending: typos, numbering, grammar
    if (not a and sq(jb) in ('de', '')) or (not b and sq(ja) in ('de', '')):
        return 'editorial'
    return 'substantive'


def change_kind(old, new):
    if old is None:
        return 'new', 0, len(words(new))
    if old == new:
        return 'same', 0, 0
    a, b = toks(spell(old)), toks(spell(new))
    if a == b:
        return 'spelling', 0, 0
    kinds, rem, add = set(), 0, 0
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        k = op_kind(a[i1:i2], b[j1:j2])
        kinds.add(k)
        if k == 'substantive':
            rem += len(words(' '.join(a[i1:i2])))
            add += len(words(' '.join(b[j1:j2])))
    for k in ('substantive', 'language', 'disability', 'editorial'):
        if k in kinds:
            return k, rem, add
    return 'editorial', rem, add


units = sorted(set(last) | set(U[V1]), key=ukey)
grid = []
cnt = collections.Counter()
for u in units:
    k24, rem, add = change_kind(U[V1].get(u), last.get(u))
    k16 = change_kind(U[V0].get(u), U[V1].get(u))[0] if u in U[V1] else None
    cnt[k24] += 1
    grid.append({'u': u, 'l': ulabel(u), 'cap': caption(last, u) if kind_of(u) in ('art', 'tranz') else '', 't': title_of(u), 'k': kind_of(u),
                 'c24': k24, 'c16': k16, 'w': len(words(last.get(u, ''))), 'rem': rem, 'add': add})
changed = sum(v for k, v in cnt.items() if k != 'same')
print('constitution 2016->2024:', dict(cnt), 'changed', changed)
for g in grid:
    if g['c24'] not in ('same', 'spelling'):
        print('   ', g['u'], g['c24'], g['rem'], g['add'])
titles = {}
for u in last:
    if u.startswith('titlul-'):
        nm = last[u].split('\n')
        titles[title_of(u)] = (nm[1] if len(nm) > 1 else '').strip()
# words per title and version; words removed and added (outside spelling and editorial changes)
wpt = []
for t in TORDER:
    row = {'t': t, 'name': titles.get(t, 'Preambul' if t == 'P' else t)}
    for d in VD:
        row['w' + d[:4]] = sum(len(words(s)) for u, s in U[d].items() if title_of(u) == t)
    row['rem'] = sum(g['rem'] for g in grid if g['t'] == t)
    row['add'] = sum(g['add'] for g in grid if g['t'] == t)
    row['n_sub'] = sum(1 for g in grid if g['t'] == t and g['c24'] in ('substantive', 'new'))
    row['lang'] = sum(1 for g in grid if g['t'] == t and g['c24'] == 'language')
    row['dis'] = sum(1 for g in grid if g['t'] == t and g['c24'] == 'disability')
    row['units'] = [g['l'] for g in grid if g['t'] == t and g['c24'] in ('substantive', 'new')]
    wpt.append(row)
OUT['c01'] = {'grid': grid, 'versions': VD, 'titles': titles, 'counts': dict(cnt), 'changed': changed,
              'hcc7': [g['l'] for g in grid if g['c16'] not in (None, 'same')], 'units_v': {d: len(U[d]) for d in VD}}
OUT['c04'] = {'rows': wpt, 'total': {d: sum(len(words(s)) for s in U[d].values()) for d in VD}}
print('words per version', OUT['c04']['total'])
for r in wpt:
    print('   ', r['t'], r['name'][:30], r['w' + V1[:4]], '->', r['w' + V2[:4]], '-', r['rem'], '+', r['add'], r['units'])


# the President: Articles 78, 85 and 89 in each version, as word diffs against the version before, paragraph by
# paragraph ("(1)", "(2)"...); punctuation at the end of a word does not count as a change
def wdiff(a, b):
    ta, tb = a.split(), b.split()
    key = lambda w: re.sub(r'[.,;:]+$', '', w).lower()
    sm = difflib.SequenceMatcher(None, [key(w) for w in ta], [key(w) for w in tb], autojunk=False)
    if ta and tb and sm.ratio() < 0.5:   # rewritten rather than edited: show the old words, then the new
        return [['-', a], ['+', b]]
    segs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            segs.append(['=', ' '.join(tb[j1:j2])])
        else:
            if i2 > i1: segs.append(['-', ' '.join(ta[i1:i2])])
            if j2 > j1: segs.append(['+', ' '.join(tb[j1:j2])])
    return segs


def paras(s):
    out = []
    for line in s.split('\n'):
        line = line.strip()
        if line:
            m = re.match(r'\((\d+)(?:\^(\d))?\)\s*', line)
            out.append(((int(m.group(1)), int(m.group(2) or 0)) if m else (len(out) + 1, 0), m.group(0).strip() if m else '', line[m.end():] if m else line))
    return out


def pdiff(old, new):
    A, Bn = {k: (n, t) for k, n, t in paras(old)}, {k: (n, t) for k, n, t in paras(new)}
    out = []
    for k in sorted(set(A) | set(Bn)):
        num = (Bn.get(k) or A.get(k))[0]
        if k in A and k in Bn:
            segs = wdiff(A[k][1], Bn[k][1])
        elif k in A:
            segs = [['-', A[k][1]]]
        else:
            segs = [['+', Bn[k][1]]]
        out.append({'p': num, 'gone': k not in Bn, 'new': k not in A, 'segs': segs})
    return out


def body(s):
    return '\n'.join(s.split('\n')[2:]).strip()


pres = {}
for u in ('art-078', 'art-085', 'art-089'):
    pres[u] = {'cap': {d: caption(U[d], u) for d in VD}, 'w': {d: len(words(body(U[d][u]))) for d in VD},
               'd16': pdiff(body(U[V0][u]), body(U[V1][u])), 'd24': pdiff(spell(body(U[V1][u])), spell(body(last[u]))),
               'text': {d: body(U[d][u]) for d in VD}}
OUT['c02'] = {'arts': pres, 'hcc7_law': CONST[1]['author'], 'v': VD}

# words that came and went
PHR = [
    ('lang', 'moldoveneasca', r'\blimb(?:a|ii) moldovene(?:ască|ști)\b'),
    ('lang', 'romana', r'\blimb(?:a|ii) rom[âî]n(?:ă|e)\b'),
    ('lang', 'de_stat', r'\blimb(?:a|ii) de stat\b'),
    ('pres', 'ales_parlament', r'\bales de Parlament\b'),
    ('pres', 'vot_universal', r'\bvot universal\b'),
    ('eu', 'ue', r'\bUniun(?:ea|ii)\s+Europe(?:ană|ne)\b'),
    ('inst', 'avocat', r'\bAvocat(?:ul|ului) Poporului\b'),
    ('inst', 'csp', r'\bConsiliu(?:l|lui) Superior al Procurorilor\b'),
    ('inst', 'csm', r'\bConsiliu(?:l|lui) Superior al Magistraturii\b'),
    ('spell', 'sint', r'\bs[îi]nt(?:em|eți)?\b'),
    ('spell', 'sunt', r'\bsunt(?:em|eți)?\b'),
    ('spell', 'nici_o', r'\bnici (?:o|un|unui|unei|una)\b'),
    ('spell', 'nicio', r'\bnici(?:o|un|unui|unei|una)\b'),
    ('spell', 'i_mid', r'\b\w+î\w+\b'),
    ('spell', 'a_hat', r'\b\w*â\w*\b'),
]
phr = []
for g, k, rx in PHR:
    row = {'g': g, 'k': k, 'n': []}
    for d in VD:
        txt = '\n'.join(U[d].values())
        row['n'].append(len(re.findall(rx, txt, flags=0 if k in ('i_mid', 'a_hat') else re.I)))
    phr.append(row)
OUT['c03'] = {'rows': phr, 'v': VD}
print('phrases', [(r['k'], r['n']) for r in phr])

# the acts that amended the Constitution: adoption and publication in the Monitorul Oficial
acts = []
with open(os.path.join(B, 'repo', 'data', 'laws.csv'), encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['kind'] not in ('law', 'court') or not r['enacted'] or not r['published']:
            continue
        m = re.match(r'(LP|HCC)\s?(\d+)(?:-([IVX]+))?', r['label'])
        name = f"Legea nr. {m.group(2)}-{m.group(3)}/{r['enacted'][:4]}" if m.group(1) == 'LP' else f"HCC nr. {m.group(2)}/{r['enacted'][:4]}"
        acts.append({'id': r['key'], 'name': name, 'kind': 'court' if r['kind'] == 'court' else 'law', 'enacted': r['enacted'], 'published': r['published'],
                     'mo': re.search(r'MO\s?([\d-]+)', r['title']).group(1) if re.search(r'MO\s?([\d-]+)', r['title']) else '', 'src': 'data/laws.csv'})
msg = re.sub(r'\s+', ' ', CONST[-1]['message'])
for m in re.finditer(r'(LP|HCC|Legea nr\.)\s?(\d+) din (\d{2})\.(\d{2})\.(\d{2}) \(MO([\d-]+)/(\d{2})\.(\d{2})\.(\d{2}) art\.\d+\)', msg):
    en = f"20{m.group(5)}-{m.group(4)}-{m.group(3)}"
    pub = f"20{m.group(9)}-{m.group(8)}-{m.group(7)}"
    court = m.group(1) == 'HCC'
    acts.append({'id': f"{m.group(1)}{m.group(2)}-{en[:4]}", 'name': (f"HCC nr. {m.group(2)}/{en[:4]}" if court else f"Legea nr. {m.group(2)}/{en[:4]}"),
                 'kind': 'court' if court else 'law', 'enacted': en, 'published': pub, 'mo': m.group(6), 'src': 'git log (' + CONST[-1]['commit'][:8] + ')'})
seen = set()
acts = [a_ for a_ in sorted(acts, key=lambda x: (x['enacted'], x['name'])) if not (a_['name'] in seen or seen.add(a_['name']))]
for a_ in acts:
    a_['days'] = (D(a_['published']) - D(a_['enacted'])).days
OUT['c05'] = {'acts': acts, 'median': med([a_['days'] for a_ in acts]), 'rect': [r for r in csv.DictReader(open(os.path.join(B, 'repo', 'data', 'laws.csv'), encoding='utf-8')) if r['kind'] == 'publisher']}
print('acts', len(acts), 'median days', OUT['c05']['median'], [(a_['name'], a_['days']) for a_ in acts])
PF['const_units'] = len(last)
PF['const_versions'] = VD
PF['const_words'] = OUT['c04']['total']



# ====================================================================== II. the Supreme Court of Justice (jurisprudenta.csj.md)
REC = list(jl('records.jsonl'))
TXT = {t['path'].rsplit('/', 1)[0]: norm_cedilla(t['text']) for t in jl('texts.jsonl')}
CSJP = 'caselaw/curtea-suprema-de-justitie/'
DBS = ['col_civil', 'plen_penal', 'col_penal', 'cont_csm', 'case_lawc', 'case_lawp', 'hot_expl', 'avize_csj', 'plen_csj', 'rec_csj', 'interes_lege']
PRIO = {k: i for i, k in enumerate(['hot_expl', 'interes_lege', 'avize_csj', 'rec_csj', 'case_lawc', 'case_lawp', 'plen_csj', 'plen_penal', 'col_civil', 'col_penal', 'cont_csm'])}
raw = [dict(x['r'], _path=x['path'], _dir=x['path'].rsplit('/', 1)[0]) for x in REC if x['path'].startswith(CSJP)]
raw.sort(key=lambda r: (PRIO[r['database']], r['source_id']))
seen, csj, dups = set(), [], collections.Counter()
for r in raw:
    if r['source_sha256'] in seen:
        dups[r['database']] += 1
        continue
    seen.add(r['source_sha256'])
    csj.append(r)
print('CSJ records', len(raw), 'distinct PDFs', len(csj), 'repeats', dict(dups))
assert all(r['database'] in DBS for r in csj)
LABEL = {r['database']: r['database_label'] for r in raw}
for r in csj:
    r['d'] = D(r['decision_date'])
years = sorted({r['d'].year for r in csj})
mat = {db: collections.Counter(r['d'].year for r in csj if r['database'] == db) for db in DBS}
OUT['c06'] = {'dbs': [{'db': db, 'label': LABEL[db], 'n': sum(mat[db].values()), 'y': {str(y): mat[db][y] for y in mat[db]},
                       'first': min(r['decision_date'] for r in csj if r['database'] == db), 'last': max(r['decision_date'] for r in csj if r['database'] == db),
                       'ids': [min(r['source_id'] for r in raw if r['database'] == db), max(r['source_id'] for r in raw if r['database'] == db)],
                       'records': sum(1 for r in raw if r['database'] == db)} for db in DBS],
              'years': list(range(years[0], years[-1] + 1)), 'n': len(csj), 'records': len(raw), 'repeats': sum(dups.values())}
PF['csj'] = len(csj)
PF['csj_text'] = sum(1 for r in csj if r['_dir'] in TXT)
PF['civ'] = sum(1 for r in csj if r['database'] == 'col_civil')
PF['csj_records'] = len(raw)

# the day of the week each body's decisions carry, and how many per sitting day
wk = []
for db in DBS:
    rs = [r for r in csj if r['database'] == db]
    c = collections.Counter(r['d'].weekday() for r in rs)
    per = collections.Counter(r['decision_date'] for r in rs)
    wk.append({'db': db, 'n': len(rs), 'wd': [c[i] for i in range(7)], 'days': len(per), 'med': med(list(per.values())), 'max': max(per.values()),
               'maxday': max(per.items(), key=lambda kv: (kv[1], kv[0]))[0]})
OUT['c07'] = {'rows': wk}
print('weekdays', [(w['db'], w['wd'], w['days'], w['med'], w['max']) for w in wk])

# the civil college day by day; where its numbering has long runs of missing ids, the repository lacks those weeks
cc = [r for r in raw if r['database'] == 'col_civil']
ids = sorted(r['source_id'] for r in cc)
byid = {r['source_id']: r['decision_date'] for r in cc}
holes = []
for i_, (a_, b_) in enumerate(zip(ids, ids[1:])):
    if b_ - a_ > 100:   # the typical date of the 20 ids on each side (single ids can carry stray dates)
        before = sorted(byid[x] for x in ids[max(0, i_ - 19):i_ + 1])
        after = sorted(byid[x] for x in ids[i_ + 1:i_ + 21])
        holes.append({'from_id': a_ + 1, 'to_id': b_ - 1, 'after': before[len(before) // 2], 'before': after[len(after) // 2]})
civ = [r for r in csj if r['database'] == 'col_civil']
days = collections.Counter(r['decision_date'] for r in civ)
main = sorted(d for d in days if '2013-04-01' <= d <= '2014-02-28')
gap = [holes[0]['after'], holes[-1]['before']] if holes else None
OUT['c08'] = {'days': {d: days[d] for d in main}, 'outside': sorted((d, days[d]) for d in days if d not in main), 'holes': holes, 'gap': gap,
              'ids': [ids[0], ids[-1]], 'records': len(cc), 'n': len(civ), 'max': max(days.items(), key=lambda kv: kv[1]),
              'months': {m: sum(v for d, v in days.items() if d[:7] == m) for m in sorted({d[:7] for d in main})}}
print('civil days', len(main), 'max', OUT['c08']['max'], 'holes', holes, 'outside', OUT['c08']['outside'])


# the civil college's case numbers: 2... civil and commercial, 3... administrative litigation; the letters name the procedure
def fam(num):
    m = re.match(r'\s*([23])\s*([a-z]+)', num or '')
    if not m:
        return None, 'other'
    br, lt = m.group(1), m.group(2)
    if lt in ('ra', 'rac', 'rae'): f_ = 'ra'
    elif lt in ('r', 'rc'): f_ = 'r'
    elif lt in ('rh', 'rhc'): f_ = 'rh'
    elif lt == 'ri': f_ = 'ri'
    else: f_ = 'other'
    return br, f_


pc = collections.Counter()
codes = collections.defaultdict(collections.Counter)
for r in civ:
    br, f_ = fam(r.get('number'))
    pc[(br or '-', f_)] += 1
    m = re.match(r'\s*([23]\s*[a-z]+)', r.get('number') or '')
    codes[f_][re.sub(r'\s', '', m.group(1)) if m else '–'] += 1
# what the text of each kind of case says it is against (verifies the letters): share of texts with each phrase
evid = collections.defaultdict(collections.Counter)
EVID = {'decizie': r'împotriva (?:deciziei|hotăr[îâ]rii)', 'incheiere': r'împotriva încheierii', 'revizuire': r'revizuir', 'insolv': r'insolvab',
        'admin': r'act\w* administrativ|anular\w* (?:a )?(?:actului|deciziei|hotăr[îâ]rii|ordinului|dispoziției)|contenciosului administrativ'}
for r in civ:
    t = TXT.get(r['_dir'])
    if not t:
        continue
    br, f_ = fam(r.get('number'))
    head = re.sub(r'\s+', ' ', t)
    evid[(br, f_)]['n'] += 1
    for k, rx in EVID.items():
        if re.search(rx, head[:3000] if k in ('decizie', 'incheiere') else head):
            evid[(br, f_)][k] += 1
OUT['c09'] = {'rows': [{'br': k[0], 'f': k[1], 'n': v} for k, v in sorted(pc.items(), key=lambda kv: -kv[1])], 'n': len(civ),
              'codes': {k: v.most_common() for k, v in codes.items()}, 'evid': [{'br': k[0], 'f': k[1], **v} for k, v in evid.items()]}
print('families', sorted(pc.items(), key=lambda kv: -kv[1]))
print('evidence', {f'{k[0]}{k[1]}': dict(v) for k, v in evid.items()})

# length in pages, per body
BINS = [(1, 2), (3, 4), (5, 7), (8, 12), (13, 10 ** 6)]
pg = []
for db in DBS:
    p_ = [r['pdf_pages'] for r in csj if r['database'] == db and r.get('pdf_pages')]
    pg.append({'db': db, 'n': len(p_), 'b': [sum(1 for x in p_ if a_ <= x <= b_) for a_, b_ in BINS], 'med': med(p_), 'max': max(p_),
               'words': med([r['text_check']['pymupdf_words'] for r in csj if r['database'] == db and r.get('text_check')])})
OUT['c10'] = {'rows': pg, 'all_med': med([r['pdf_pages'] for r in csj]), 'all_words': med([r['text_check']['pymupdf_words'] for r in csj if r.get('text_check')])}
print('pages', [(x['db'], x['b'], x['med'], x['words']) for x in pg], OUT['c10']['all_med'])

# the outcome, read from the operative part ("d e c i d e:", "d i s p u n e:") of the civil college's published texts
LT = r'A-Za-zăîâșțĂÎÂȘȚ'
sp_ = lambda w: rf'(?<![{LT}])' + r'\s*'.join(map(re.escape, w)) + rf'(?![{LT}])\s*:?'
MARK = re.compile('|'.join(sp_(w) for w in ['decide', 'dispune', 'hotărăște', 'hotărîște', 'hotărește']), re.I)


def outcome(flat):
    ms = [m for m in MARK.finditer(flat) if re.match(r'\s*(?:\d+\s+)?(?:Se\b|Recurs|Cerer|Respinge|Admite|Pricina|Procedura|Încet|Restitui)', flat[m.end():m.end() + 40])]
    if ms:
        d = flat[ms[-1].end():ms[-1].end() + 400]
    else:
        mm = re.search(r'(Se (?:admit|admite|respinge|resping)\b.{0,300}|Recursul.{0,120}inadmisibil.{0,100})', flat[-2500:])
        if not mm:
            return 'other', ''
        d = mm.group(0)
    d = re.sub(r'^\s*\d+\s+', '', d).strip()
    x = d.lower()[:260]
    if re.search(r'retrager|renunț', x[:140]): k = 'other'
    elif 'inadmisibil' in x[:220]: k = 'inadmissible'
    elif re.match(r'(se )?(admite|admit)\b', x) or re.match(r'(recursul|recursurile|cererea)\b[^.]{0,160}\bse admit', x): k = 'admitted'
    elif re.match(r'(se )?(respinge|resping)\b', x) or re.match(r'(recursul|recursurile|cererea)\b[^.]{0,160}\bse resping', x): k = 'rejected'
    else: k = 'other'
    return k, d[:160]


oc = []
for r in civ:
    t = TXT.get(r['_dir'])
    if not t:
        continue
    flat = re.sub(r'\s+', ' ', t)
    k, d = outcome(flat)
    br, f_ = fam(r.get('number'))
    oc.append({'id': r['source_id'], 'num': r.get('number') or '', 'date': r['decision_date'], 'br': br or '-', 'f': f_, 'o': k, 'op': d[:120]})
OUT['c11'] = {'rows': oc, 'n': len(oc)}
print('outcomes', collections.Counter(o['o'] for o in oc), collections.Counter((o['br'], o['f'], o['o']) for o in oc).most_common(30))

# what the texts cite
CITE = [
    ('cpc', r'\bCPC\b|Codul(?:ui)? de procedură civilă'),
    ('cc', r'\bCodul(?:ui)? civil\b|\bCod(?:ul|ului)? Civil\b|\bart\.\s?\d+[^.;]{0,30}\bCC\b'),
    ('lca', r'contenciosului administrativ'),
    ('insolv', r'insolvabilit'),
    ('cf', r'\bCodul(?:ui)? fiscal\b|\bCF\b'),
    ('const', r'\bConstituți(?:a|ei|e)\b'),
    ('echr', r'Convenți(?:a|ei) (?:Europeană|europeană|pentru apărarea drepturilor omului)|\bCEDO\b|Curț(?:ii|ile|i) Europene a Drepturilor Omului|Curtea Europeană a Drepturilor Omului|\bCtEDO\b'),
    ('cm', r'\bCodul(?:ui)? muncii\b'),
    ('cv', r'\bCodul(?:ui)? vamal\b'),
    ('cex', r'\bCodul(?:ui)? de executare\b'),
]
cite = collections.Counter()
for r in civ:
    t = TXT.get(r['_dir'])
    if not t:
        continue
    flat = re.sub(r'\s+', ' ', t)
    for k, rx in CITE:
        if re.search(rx, flat):
            cite[k] += 1
OUT['c12'] = {'n': len(oc), 'rows': [{'k': k, 'n': cite[k]} for k, _ in CITE]}
print('cites', cite)

# the Plenum's explanatory decisions: new, amending an earlier one (with its date), repealing
MONTHS = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie']


def pdate(s):
    s = s.strip().rstrip('.,;')
    m = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{2}|\d{4})$', s)
    if m:
        y = int(m.group(3)) if len(m.group(3)) == 4 else 2000 + int(m.group(3)) if int(m.group(3)) < 30 else 1900 + int(m.group(3))
        return f"{y}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    m = re.match(r'(\d{1,2}) ([a-zăîâșț]+) (\d{4})$', s.lower())
    if m and m.group(2) in MONTHS: return f"{m.group(3)}-{MONTHS.index(m.group(2)) + 1:02d}-{int(m.group(1)):02d}"
    return None


he = []
for r in sorted((r for r in csj if r['database'] == 'hot_expl'), key=lambda r: r['decision_date']):
    t = re.sub(r'\s+', ' ', TXT.get(r['_dir'], ''))
    head = t[:900]
    m = re.search(r'(?:De modificare (?:și|şi) completare|Pentru modificarea (?:și|şi) completarea|privind modificarea (?:și|şi) completarea|Cu privire la actualizarea|privind introducerea unor modificări (?:și|şi) completări)', head, re.I)
    seg = head[m.end():m.end() + 500] if m else ''
    mm = re.search(r'nr\.?\s*(\d+)\s*,?\s*din\s*(\d{1,2} [a-zăîâșț]+ \d{4}|\d{1,2}\.\d{1,2}\.\d{2,4})', seg)
    if re.search(r'Cu privire la abrogarea', head, re.I):
        kind, on, od = 'repeal', None, None
    elif m:
        kind, on, od = 'amend', mm.group(1) if mm else None, pdate(mm.group(2)) if mm else None
    else:
        kind, on, od = 'new', None, None
    q = re.search(r'[„"“]([^”"“]{8,220})[”"]', seg or head)
    subj = q.group(1) if q else ''
    if kind == 'new':
        mm = re.search(r'((?:Cu privire la|Privind|privind|Despre|despre)\s.{8,200}?)(?:\s(?:nr\.|În|Plenul|Ținând|Avînd|Având)\b|\[)', head)
        subj = mm.group(1) if mm else ''
    he.append({'date': r['decision_date'], 'num': r.get('number') or '', 'kind': kind, 'on': on, 'od': od, 'subj': subj.strip(), 'pages': r['pdf_pages']})
OUT['c13'] = {'rows': he}
print('explanatory', collections.Counter(h['kind'] for h in he), collections.Counter((h['date'][:4], h['kind']) for h in he))
for h in he:
    if h['kind'] == 'amend' or h['date'] >= '2017': print('   ', h['date'], h['kind'], h['on'], h['od'], h['subj'][:90])


# ====================================================================== III. the courts' judgments of 12-13 November 2026 (instante.justice.md)
low = [dict(x['r'], _path=x['path']) for x in REC if x['path'].startswith('caselaw/') and not x['path'].startswith(CSJP)
       and not x['path'].startswith('caselaw/curtea-constitutionala/')]
TYPE = {'Civil': 'civ', 'Penal': 'pen', 'Contravenţional': 'con', 'Contravențional': 'con'}
NUMRX = re.compile(r'^(\d)-(\d{2})(\d+)-(\d{2})-([0-9a-zA-Z /]+?)-(\d{2})(\d{2})(\d{4})(?:-\d+)?$')
courts = collections.Counter()
ages, unparsed = [], []
for r in low:
    r['ty'] = TYPE[r['case_type']]
    r['court'] = norm_cedilla(r['court'])
    r['lvl'] = 'apel' if r['court'].startswith('Curtea de Apel') else 'fond'
    courts[(r['court'], r['ty'])] += 1
    m = NUMRX.match(r['number'].strip())
    if not m:
        unparsed.append(r['number'])
        continue
    reg = datetime.date(int(m.group(8)), int(m.group(7)), int(m.group(6)))
    r['age'] = (D(r['decision_date']) - reg).days
    ages.append({'ty': r['ty'], 'lvl': r['lvl'], 'age': r['age']})
dd = collections.Counter(r['decision_date'] for r in low)
pubs = collections.Counter((D(r['publication_date_source']) - D(r['decision_date'])).days for r in low)
COURTS = sorted({r['court'] for r in low}, key=lambda c: -sum(v for (c2, _), v in courts.items() if c2 == c))
OUT['c14'] = {'courts': [{'c': c, 'lvl': 'apel' if c.startswith('Curtea de Apel') else 'fond', 'civ': courts[(c, 'civ')], 'pen': courts[(c, 'pen')], 'con': courts[(c, 'con')]} for c in COURTS],
              'n': len(low), 'days': dict(dd), 'pub': dict(pubs)}
print('lower courts', len(low), dict(dd), [(c['c'], c['civ'] + c['pen'] + c['con']) for c in OUT['c14']['courts']])
ABINS = [(0, 30), (31, 90), (91, 180), (181, 365), (366, 10 ** 6)]
arows = []
for lvl in ('fond', 'apel'):
    for ty in ('civ', 'con', 'pen'):
        a_ = [x['age'] for x in ages if x['ty'] == ty and x['lvl'] == lvl]
        if a_:
            arows.append({'lvl': lvl, 'ty': ty, 'n': len(a_), 'b': [sum(1 for v in a_ if lo <= v <= hi) for lo, hi in ABINS], 'med': med(a_), 'max': max(a_)})
OUT['c15'] = {'rows': arows, 'unparsed': len(unparsed), 'all_med': {ty: med([x['age'] for x in ages if x['ty'] == ty]) for ty in ('civ', 'con', 'pen')}, 'n': len(ages)}
print('ages', [(r['lvl'], r['ty'], r['n'], r['b'], r['med']) for r in arows], 'unparsed', unparsed)
SUBJ = {
    'civ': [('debt', r'\bîncas\w*\s+(?:a\s+)?datori'), ('family', r'\bdesfacer\w*\s+(?:a\s+)?căsători|\bpensi\w*\s+(?:de\s+întreținere|alimentar)|\bcopil|\bpărintești'),
            ('admin', r'\bact\w*\s+administrativ'), ('damage', r'\bprejudici'), ('contract', r'\bcontract|\bbancar|\bleasing'),
            ('insolv', r'\binsolvab|\brăspundere\s+subsidiară')],
    'con': [('electoral', r'\b47\s*(?:/|\[|\^)\s*1\b|\bcorupe\w*\s+electoral'), ('family_v', r'\bviolenț\w*\s+în\s+familie|\bordinului\s+de\s+restricție|\b78\s*(?:/|\[|\^)\s*1\b'),
            ('traffic', r'\brutier|\bvehicul|\bcenturii|\bebrietate'), ('order', r'\bsamavolnic|\bnesubordon|\bhuligan'), ('child', r'\bcopil')],
    'pen': [('drunk', r'\b264\s*(?:/|\[|\^)\s*1\b|\bebrietate'), ('family_v', r'\bviolenț\w*\s+în\s+familie|\b201\s*(?:/|\[|\^)\s*1\b'),
            ('corrupt', r'\bcorupe|\btrafic\w*\s+de\s+influență'), ('property', r'\bfurt|\bjaf\w*|\bescrocher|\bdelapid'), ('injury', r'\bvătămar')],
}
subj = {}
for ty, rules in SUBJ.items():
    c = collections.Counter()
    for r in low:
        if r['ty'] != ty:
            continue
        t = norm_cedilla(r['title'])
        s = t.rsplit(' - ', 1)[1].strip() if ' - ' in t else ''
        if not s:
            c['none'] += 1
            continue
        for k, rx in rules:
            if re.search(rx, s, re.I):
                c[k] += 1
                break
        else:
            c['other'] += 1
    subj[ty] = {'n': sum(c.values()), 'c': dict(c)}
OUT['c16'] = subj
print('subjects', subj)
PF['low'] = len(low)

# ====================================================================== IV. the Competition Council (competition.md)
comp = [dict(x['r'], _path=x['path'], _dir=x['path'].rsplit('/', 1)[0]) for x in REC if x['path'].startswith('decision/competition-council/')]
MARKC = re.compile('|'.join(sp_(w) for w in ['decide', 'dispune', 'hotărăște', 'decid']), re.I)
OPSTART = re.compile(r'\s*:?\s*(?:[1lL]\s*[.)]?\s*|a\)\s*|I\.\s*)?(?:A\s|Se\s|Încetarea|Măsur|Recurs)')


def ccode(num):
    c = re.sub(r'[^A-Z]', '', (num or '').upper().replace('NR', ''))
    for k in ('EMAS', 'ASER', 'ASR', 'ASS', 'ASO', 'AAP', 'APD', 'APR', 'CEP', 'CNP', 'CCE', 'DCE', 'OTC', 'CN', 'DA'):
        if c.startswith(k):
            return k
    return c[:4] or '?'


def cdomain(op):
    o = op[:700]
    if re.search(r'ajutor\w*\s+de\s+stat|schem\w*\s+de\s+ajutor|măsur\w*\s+de\s+sprijin', o, re.I): return 'aid'
    if re.search(r'concentrar\w*\s+economic', o, re.I): return 'merger'
    if re.search(r'art\.\s*68\b|neprezentarea\s+informați|nefurnizar\w*|refuz\w*\s+(?:de\s+)?a\s+se\s+supune\s+inspecți|răspunsurilor\s+inexacte|prezentarea\s+incompletă', o, re.I): return 'procedure'
    if re.search(r'concurenț\w*\s+neloial|art\.\s*(?:1[5-9])\b', o, re.I): return 'unfair'
    if re.search(r'art\.\s*11\b|art\.\s*6\s+lit|poziți\w*\s+dominant', o, re.I): return 'dominance'
    if re.search(r'art\.\s*5\b|art\.\s*7\s+alin|acord\w*\s+anticoncurențial|înțelegere\s+secretă|oferte\s+trucate', o, re.I): return 'cartel'
    if re.search(r'art\.\s*12\b|acțiunile\s+(?:Consiliului|Primăriei|Ministerului)', o, re.I): return 'authority'
    return 'other'


def coutcome(op, dom):
    o = op[:400].lower()
    if dom == 'aid':
        if re.search(r'nu\s+constituie\s+ajutor', op[:2000].lower()): return 'noaid'
        if re.search(r'încălcar|incompatibil', op[:600].lower()): return 'violation'
        if re.search(r'autoriz|compatibil', op[:3000].lower()): return 'cleared'
        return 'other'
    if dom == 'merger':
        if re.search(r'încălcar', o[:200]): return 'violation'
        if re.search(r'compatibil', op[:800].lower()): return 'cleared'
        return 'other'
    if re.search(r'a\s+respinge\s+plângerea', o): return 'complaint'
    if re.search(r'a\s+accepta\s+(?:angajamentele|propunerile)|soluționare\s+pe\s+cale\s+amiabilă', o): return 'commitments'
    if re.search(r'a\s+înceta|încetarea\s+investigației|lipsa\s+încălcării', o[:160]): return 'closed'
    if re.search(r'a\s+constata\s+(?:încălcarea|încălcare|săvârșirea|acțiunea)|a\s+califica|ca\s+încălcare|drept\s+încălcare', o): return 'violation'
    return 'other'


crow = []
for r in comp:
    t = TXT.get(r['_dir'])
    code = ccode(r['number'])
    row = {'date': r['decision_date'], 'code': code, 'num': r['number'], 'text': bool(t)}
    if t:
        flat = re.sub(r'\s+', ' ', t)
        ms = [m for m in MARKC.finditer(flat) if OPSTART.match(flat, m.end())]   # "dispune de" (= has) is not one
        op = flat[ms[0].end():] if ms else flat
        row['dom'], row['op'] = cdomain(op), op[:1200]
        row['words'] = len(flat.split())
        if row['dom'] == 'aid':
            g = re.search(r'notificat\w*[^.;]{0,200}?\bde\s+către\s+(.{3,160}?)(?:,|\s+având|\s+privind|\s+sub\s|\s+cu\s+privire|\s+care|\s+constând|\s+și\s+acordat|\s+în\s+temeiul|\s+prin\s+intermediul|\s+ce\s|\s+referitor|\s+în\s+cadrul|\s+în\s+legătură|\s+instituit)', op[:900])
            row['grantor'] = g.group(1).strip() if g else ''
            o = op[:900]
            row['water'] = bool(re.search(r'Apă\s*[-–]?\s*Canal|apeduct|alimentare\s+cu\s+apă|canalizare', o, re.I))
            row['muni'] = bool(re.search(r'Î\.\s?M\.|[îi]ntreprinder\w*\s+municipal', o))
            row['measure'] = ('assets' if re.search(r'transmiter\w*\s+(?:în\s+gestiune|cu\s+titlu\s+gratuit)|\bbunuri\b|mijloace\s+fixe', o) else
                              'scheme' if re.search(r'modific\w*\s+(?:a\s+)?schemei|majorarea\s+bugetului|prelungirea', o) else
                              'tax' if re.search(r'scutir|\bT\.V\.A\b|dividende', o) else
                              'loan' if re.search(r'împrumut|garanți|credit', o) else
                              'grant' if re.search(r'subvenți|alocați\w*\s+bugetar|finanțar\w*|compensar|granturi|indemnizați', o) else 'other')
    crow.append(row)
# the code of each decision, read where the text says what was decided, gives its field to the decisions without text
code_dom = collections.defaultdict(collections.Counter)
for r in crow:
    if r['text']:
        code_dom[r['code']][r['dom']] += 1
for r in crow:   # a decision whose text does not name its field (or that has no text) takes the field its code has in the others
    known = sorted(((n_, d_) for d_, n_ in code_dom[r['code']].items() if d_ not in ('other', 'procedure')), reverse=True)
    proc = r['text'] and r['dom'] == 'procedure'
    if (not r['text'] or r['dom'] in ('other', 'procedure')) and known:
        r['dom'] = known[0][1]
    elif r['dom'] == 'procedure':
        r['dom'] = 'other'
    r['out'] = 'notext' if not r['text'] else 'procedural' if proc else coutcome(r['op'], r['dom'])
    r.pop('op', None)


def grant_level(g):
    if re.search(r'Primări|Consiliu\w*\s+(?:municipal|raional|local|orășenesc|comunal|sătesc)|UTA\s+Găgăuzia', g, re.I): return 'local'
    if g: return 'central'
    return 'unknown'


aid = [r for r in crow if r.get('dom') == 'aid' and r['text']]
for r in aid:
    r['lvl'] = grant_level(r.get('grantor', ''))
OUT['c17'] = {'rows': [{'y': r['date'][:4], 'dom': r['dom'], 'out': r['out'], 'code': r['code'], 'text': r['text']} for r in crow],
              'code_dom': {k: dict(v) for k, v in code_dom.items()}, 'n': len(crow)}
OUT['c19'] = {'rows': [{'y': r['date'][:4], 'lvl': r['lvl'], 'm': r['measure'], 'g': r['grantor'][:90], 'water': r['water'], 'muni': r['muni']} for r in aid], 'n': len(aid)}
print('competition', len(crow), collections.Counter(r['dom'] for r in crow), collections.Counter((r['dom'], r['out']) for r in crow).most_common())
print('code->domain', {k: dict(v) for k, v in code_dom.items()})
print('aid', len(aid), collections.Counter((r['lvl'], r['measure']) for r in aid))
for r in aid:
    if r['lvl'] == 'unknown' or r['measure'] == 'other': print('   ?', r['date'], r['code'], r['lvl'], r['measure'], r['grantor'][:80])
PF['comp'] = len(crow)
PF['comp_text'] = sum(1 for r in crow if r['text'])

# ====================================================================== V. the repository over time
cc_ = [dict(x['r'], _path=x['path']) for x in REC if x['path'].startswith('caselaw/curtea-constitutionala/')]
ccl = []
for t in jl('texts.jsonl'):
    if t['path'].startswith('caselaw/curtea-constitutionala/') and t['path'].endswith('README.md'):
        m = re.search(r'- Date: (\d{4}-\d{2}-\d{2})', t['text'])
        ccl.append({'date': m.group(1) if m else None, 'title': t['text'].split('\n')[0].lstrip('# ').strip(), 'path': t['path'].rsplit('/', 1)[0]})
other = [dict(x['r'], _path=x['path']) for x in REC if x['path'].split('/')[0] in ('law', 'norm', 'treaty')]
lanes = {
    'const': [d for d in VD],
    'csj': [r['decision_date'] for r in csj],
    'cc': [c['date'] for c in ccl if c['date']],
    'low': [r['decision_date'] for r in low],
    'comp': [r['date'] for r in crow],
    'law': [r['in_force'] for r in other if r['_path'].startswith('law/')],
    'bnm': [r['in_force'] for r in other if r['_path'].startswith('norm/')],
    'treaty': [r['in_force'] for r in other if r['_path'].startswith('treaty/')],
}
OUT['c20'] = {'lanes': {k: dict(collections.Counter(d[:4] for d in v)) for k, v in lanes.items()}, 'n': {k: len(v) for k, v in lanes.items()},
              'span': {k: [min(v), max(v)] for k, v in lanes.items() if v}}
OUT['cc'] = ccl
OUT['other'] = [{'path': r['_path'].rsplit('/', 1)[0], 'title': r['title'], 'in_force': r.get('in_force')} for r in other]
print('lanes', OUT['c20']['n'], OUT['c20']['span'])

# ====================================================================== the data profile
commits = list(jl('commits.jsonl'))
kinds = collections.Counter(c['t'].get('Kind', '-') for c in commits)
PF.update({'commits': len(commits), 'kinds': dict(kinds), 'head': os.environ.get('HEAD_SHA', ''), 'ref': os.environ.get('HEAD_REF', ''),
           'built': max(c['ad'][:10] for c in commits if c['an'] == 'Lexifina'),
           'last_record': max(c['t'].get('In-force', '0000') for c in commits),
           'cc': len(ccl), 'laws': len(lanes['law']), 'bnm': len(lanes['bnm']), 'treaty': len(lanes['treaty'])})
print('profile', {k: v for k, v in PF.items() if k not in ('kinds',)})
json.dump({'charts': OUT, 'profile': PF}, open(os.path.join(B, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('data.json', os.path.getsize(os.path.join(B, 'data.json')))
