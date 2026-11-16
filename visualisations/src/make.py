"""Rebuild visualisations/dreptul-republicii-moldova-in-20-de-grafice.html from this repository.

    python visualisations/src/make.py [--repo PATH] [--ref REF]

Steps (all read-only on the repository; scratch output goes to visualisations/src/.build/):
  1. git log of REF, streamed: author date, author, subject and trailers of every commit -> .build/commits.jsonl
  2. the record files (record.json) of caselaw/, decision/, law/, norm/ and treaty/   -> .build/records.jsonl
  3. the texts (text.md) of the Supreme Court, the Constitutional Court and the
     Competition Council                                                               -> .build/texts.jsonl
  4. every version of the Constitution, one entry per unit file                       -> .build/constitution.json
  5. data/laws.csv and data/versions.json                                              -> .build/repo/data/
  6. prep.py turns those into .build/data.json; build.py fills page.tpl.html with it.
Works in a blobless or --no-checkout clone: everything is read from git objects. Blobs the clone lacks are
fetched in one request (the same `git fetch --stdin` a partial clone uses for a lazy fetch), never one by one.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--repo', default=os.path.abspath(os.path.join(HERE, '..', '..')))
ap.add_argument('--ref', default=None, help='default: origin/main if present, else HEAD')
ap.add_argument('--out', default=os.path.join(HERE, '..', 'dreptul-republicii-moldova-in-20-de-grafice.html'))
a = ap.parse_args()
B = os.path.join(HERE, '.build')
os.makedirs(os.path.join(B, 'repo', 'data'), exist_ok=True)
ENV = dict(os.environ, GIT_NO_LAZY_FETCH='1')   # never fetch a blob silently, one at a time


def git(*args, env=ENV):
    return subprocess.run(['git', '-C', a.repo, *args], check=True, capture_output=True, env=env).stdout


ref = a.ref
if not ref:
    ref = 'origin/main' if subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', '-q', 'origin/main'], capture_output=True).returncode == 0 else 'HEAD'
sha = git('rev-parse', ref).decode().strip()
print('ref', ref, sha)

# 1. commits, streamed (subject + trailers; bodies are not needed)
n = 0
fmt = '%x1e%H%x1f%ad%x1f%an%x1f%ae%x1f%s%x1f%(trailers:only,unfold)'
with open(os.path.join(B, 'commits.jsonl'), 'w', encoding='utf-8') as out:
    p = subprocess.Popen(['git', '-C', a.repo, 'log', ref, '--date=iso-strict', '--format=' + fmt], stdout=subprocess.PIPE, env=ENV, encoding='utf-8', errors='replace')
    buf = ''

    def emit(rec):
        global n
        f = rec.split('\x1f')
        if len(f) < 6:
            return
        t = {}
        for line in f[5].strip().split('\n'):
            if ': ' in line:
                k, v = line.split(': ', 1)
                t.setdefault(k, v)
        out.write(json.dumps({'h': f[0].strip(), 'ad': f[1], 'an': f[2], 'ae': f[3], 's': f[4], 't': t}, ensure_ascii=False) + '\n')
        n += 1
    for chunk in iter(lambda: p.stdout.read(1 << 16), ''):
        buf += chunk
        recs = buf.split('\x1e')
        buf = recs.pop()
        for r in recs:
            emit(r)
    emit(buf)
    p.wait()
print('commits', n)

# 2-4. which blobs: records, texts, constitution versions, data tables
tree = [l.split('\t', 1) for l in git('ls-tree', '-r', ref, '--', 'caselaw', 'decision', 'law', 'norm', 'treaty', 'data').decode('utf-8').splitlines()]
items = [(meta.split()[2], path) for meta, path in tree]
records = [(o, p) for o, p in items if p.endswith('/record.json')]
texts = [(o, p) for o, p in items if p.endswith('/text.md') and (p.startswith('caselaw/curtea-suprema-de-justitie/') or p.startswith('caselaw/curtea-constitutionala/') or p.startswith('decision/'))]
texts += [(o, p) for o, p in items if p.endswith('/README.md') and p.startswith('caselaw/curtea-constitutionala/')]
tables = [(o, p) for o, p in items if p in ('data/laws.csv', 'data/versions.json')]
# the versions of the Constitution: every commit that changed a unit file (not the README), oldest first
vers = []
for line in git('log', ref, '--reverse', '--format=%H %ad', '--date=short', '--', 'constitutia', ':(exclude)constitutia/README.md').decode().splitlines():
    h, d = line.split()
    units = [l.split('\t', 1) for l in git('ls-tree', '-r', h, '--', 'constitutia').decode('utf-8').splitlines()]
    vers.append((h, d, [(m.split()[2], p) for m, p in units if not p.endswith('README.md')]))
want = [o for o, _ in records + texts + tables] + [o for _, _, us in vers for o, _ in us]
chk = subprocess.run(['git', '-C', a.repo, 'cat-file', '--batch-check=%(objectname) %(objecttype)'], input='\n'.join(want) + '\n',
                     capture_output=True, encoding='utf-8', env=ENV).stdout.split('\n')
missing = sorted({l.split()[0] for l in chk if l.endswith(' missing')})
if missing:
    print('fetching', len(missing), 'blobs in one request')
    subprocess.run(['git', '-C', a.repo, '-c', 'fetch.negotiationAlgorithm=noop', 'fetch', 'origin', '--no-tags', '--no-write-fetch-head',
                    '--recurse-submodules=no', '--filter=blob:none', '--stdin'], input='\n'.join(missing) + '\n', encoding='utf-8', check=True)

cat = subprocess.Popen(['git', '-C', a.repo, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=ENV)


def blob(oid):
    cat.stdin.write((oid + '\n').encode())
    cat.stdin.flush()
    hdr = cat.stdout.readline().split()
    if len(hdr) < 3 or hdr[1] == b'missing':
        sys.exit(f'blob {oid} missing')
    data = cat.stdout.read(int(hdr[2]))
    cat.stdout.read(1)
    return data.decode('utf-8')


with open(os.path.join(B, 'records.jsonl'), 'w', encoding='utf-8') as out:
    for o, p in records:
        out.write(json.dumps({'path': p, 'r': json.loads(blob(o))}, ensure_ascii=False) + '\n')
with open(os.path.join(B, 'texts.jsonl'), 'w', encoding='utf-8') as out:
    for o, p in texts:
        out.write(json.dumps({'path': p, 'text': blob(o)}, ensure_ascii=False) + '\n')
const = []
for h, d, us in vers:
    const.append({'commit': h, 'date': d, 'message': git('log', '-1', '--format=%B', h).decode('utf-8'),
                  'author': git('log', '-1', '--format=%an', h).decode('utf-8').strip(),
                  'units': {p.split('/')[-1][:-3]: blob(o) for o, p in us}})
json.dump(const, open(os.path.join(B, 'constitution.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for o, p in tables:
    open(os.path.join(B, 'repo', p), 'w', encoding='utf-8', newline='').write(blob(o))
cat.stdin.close()
cat.wait()
print('records', len(records), 'texts', len(texts), 'constitution versions', [d for _, d, _ in vers])

# 6. prep + build
env = dict(os.environ, HEAD_SHA=sha, HEAD_REF=ref)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'prep.py'), B], check=True, env=env)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'build.py'), os.path.join(B, 'data.json'), os.path.abspath(a.out)], check=True)
