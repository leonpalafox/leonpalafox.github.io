"""Build from pinned OECD sources; fail on changed inputs or inconsistent tables."""
import hashlib
import json
import math
from pathlib import Path
import re
import openpyxl

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'sources'
manifest = json.loads((SOURCE / 'manifest.json').read_text())
for filename, metadata in manifest.items():
    if hashlib.sha256((SOURCE / filename).read_bytes()).hexdigest() != metadata['sha256']:
        raise ValueError(f'Source checksum mismatch: {filename}; review any replacement before rebuilding')
wb = openpyxl.load_workbook(SOURCE / 'annex.xlsx', data_only=True)
chapter = openpyxl.load_workbook(SOURCE / 'ch2.xlsx', data_only=True)
DOMAINS = {'sci': (1, 36, 26, 28), 'read': (2, 37, 34, 36), 'math': (3, 38, 30, 32), 'cps': (4, None, None, None)}
def number(v):
    return type(v) in (int, float) and math.isfinite(v)
def entities(sheet):
    return {row[0].value: row[0].row for row in sheet if isinstance(row[0].value, str) and (number(row[1].value) or row[1].value == 'm')}
# The report snapshot independently establishes the participating systems and suppression codes.
report = (SOURCE / 'pisa.txt').read_text()
start = report.index('Table I.1. Snapshot of performance', report.index('Table I.1. Snapshot of performance') + 1)
segment = report[start:report.index('* Caution is required', start)]
pattern = re.compile(r'^\s*(\S.*?)\s{2,}(\d{3}|m)\s+(\d{3}|m)\s+(\d{3}|m)\s+(\d{3}|m)\s', re.M)
snapshot = {m[1].strip(): [None if x == 'm' else int(x) for x in m.groups()[1:]] for m in pattern.finditer(segment)}
assert len(snapshot) == 92 and 'OECD average' in snapshot
order = [n for n in snapshot if n != 'OECD average']
GEO = {
 'Canada*':'Canada','United States*':'United States of America','Netherlands*':'Netherlands',
 'New Zealand*':'New Zealand','Norway*':'Norway','Albania*':'Albania','Viet Nam':'Vietnam',
 'Türkiye':'Turkey','Slovak Republic':'Slovakia','Korea':'South Korea',
 'North Macedonia':'Macedonia','Dominican Republic':'Dominican Rep.',
 'Hong Kong (China)':'Hong Kong','Macao (China)':'Macao','Chinese Taipei':'Taiwan',
 'B-S-J-Z (China)':'China','Ukrainian regions (17 of 27)':'Ukraine',
 'Dushanbe (Tajikistan)':'Tajikistan','Kurdistan Region (Iraq)':'Iraq',
 'Palestinian Authority':'Palestine','Brunei Darussalam':'Brunei',
}
PARTIAL = {
 'B-S-J-Z (China)':'Covers Beijing, Shanghai, Jiangsu and Zhejiang only — not all of China.',
 'Ukrainian regions (17 of 27)':'Covers 17 of Ukraine’s 27 regions (wartime sample).',
 'Dushanbe (Tajikistan)':'Covers the city of Dushanbe only.',
 'Kurdistan Region (Iraq)':'Covers the Kurdistan Region only.',
}
CAUTION = 'One or more PISA sampling standards were not met (OECD Reader’s Guide).'


rows = []
for name in order + ['OECD average']:
    label = name.rstrip('*')
    rec = {'name': label, 'geo': GEO.get(name, label), 'm': {}, 's': {}, 'd': {}, 'evidence': {}}
    for dom, (mean_id, trend_id, short_col, decade_col) in DOMAINS.items():
        sheet = wb[f'Table I.B1.2a.{mean_id}']
        i = entities(sheet)[name]
        value, se = sheet.cell(i, 2).value, sheet.cell(i, 3).value
        rec['m'][dom] = round(value, 1) if number(value) else None
        snap = snapshot[name][list(DOMAINS).index(dom)]
        assert (snap is None and not number(value)) or (number(value) and abs(value - snap) <= .50001), (name, dom, value, snap)
        evidence = {'mean': {'sheet': sheet.title, 'cell': f'B{i}', 'value': value if number(value) else None, 'missing_code': value if not number(value) else None, 'se': se if number(se) else None}}
        if trend_id:
            sheet = wb[f'Table I.B1.2a.{trend_id}']
            i = entities(sheet)['OECD average-35' if name == 'OECD average' else name]
            for period, col in [('s', short_col), ('d', decade_col)]:
                value, se = sheet.cell(i, col).value, sheet.cell(i, col + 1).value
                if name == 'Albania*':
                    evidence[period] = {'suppressed': 'No trend reporting: OECD Reader’s Guide, p. 18.'}
                    continue
                if not number(value):
                    evidence[period] = {'sheet': sheet.title, 'cell': sheet.cell(i,col).coordinate, 'missing_code': value}
                    continue
                assert number(se) and se > 0
                p = sheet.cell(i, col + 2).value if period == 'd' else math.erfc(abs(value / se) / math.sqrt(2))
                assert number(p) and 0 <= p <= 1
                rec[period][dom] = [round(value, 1), p < .05]
                evidence[period] = {'sheet': sheet.title, 'cell': sheet.cell(i,col).coordinate, 'value': value, 'se': se, 'p': p, 'p_method': 'published' if period == 'd' else 'two-sided normal test using published difference SE'}
        rec['evidence'][dom] = evidence
    if name.endswith('*'): rec['caution'] = CAUTION
    if name in PARTIAL: rec['partial'] = PARTIAL[name]
    if label in ['Albania', 'United States']: rec['caution'] += ' Limited reporting; potential non-response bias. See the Reader’s Guide.'
    if label in ['Guatemala', 'Paraguay']: rec['note'] = 'Changed from paper to computer testing. Trend uncertainty extends beyond the reported linking errors.'
    if label == 'Uzbekistan': rec['note'] = 'Reading and mathematics withheld by OECD because of response-data inconsistencies; science is reportable.'
    if label == 'Viet Nam': rec['note'] = 'Trend comparisons excluded by OECD following a change in test mode and instruments.'
    if label == 'Albania': rec['note'] = 'OECD prohibits trend reporting because of school non-response and structural coverage gaps.'
    if name == 'OECD average': oecd = rec
    else: rows.append(rec)
# Cross-check every published chapter comparison and its significance split against the annex.
lookup = {r['name']: r for r in rows}
lookup['OECD average-35'] = oecd
for period, title, first in [('s','Table I.2.6',104),('d','Table I.2.9',102)]:
    sheet = chapter[title]
    for i in range(first, sheet.max_row + 1):
        name = sheet.cell(i,1).value
        if not isinstance(name,str): continue
        rec = lookup[name.rstrip('*')]
        for dom, col in [('sci',2),('read',4),('math',6)]:
            a,b = sheet.cell(i,col).value, sheet.cell(i,col+1).value
            assert number(a) != number(b), (title,i,dom)
            assert rec[period][dom] == [round(a if number(a) else b,1), number(a)], (title,name,dom)
assert len(rows) == 91 and len({r['name'] for r in rows}) == 91
# ---------- 5. topojson -> geojson-ish rings, only what we need ----------
topo = json.loads((SOURCE / 'w50.json').read_text())
tr = topo['transform']; sx, sy = tr['scale']; tx, ty = tr['translate']
arcs_raw = topo['arcs']
arcs = []
for arc in arcs_raw:
    x = y = 0; pts = []
    for dx, dy in arc:
        x += dx; y += dy
        p = [round(x * sx + tx, 2), round(y * sy + ty, 2)]
        if not pts or p != pts[-1]: pts.append(p)
    if len(pts) < 2: pts = [[round(x * sx + tx, 2), round(y * sy + ty, 2)]] * 2
    arcs.append(pts)

def ring(idxs):
    out = []
    for i in idxs:
        a = arcs[~i][::-1] if i < 0 else arcs[i]
        out.extend(a if not out else a[1:])
    # unwrap longitudes so antimeridian-crossing rings (Russia, Fiji) stay contiguous
    # under a naive planar projection; the map viewport clips whatever runs past the edge
    out = [list(p) for p in out]
    for k in range(1, len(out)):
        d = out[k][0] - out[k-1][0]
        if d > 180: out[k][0] -= 360
        elif d < -180: out[k][0] += 360
    xs = [p[0] for p in out]
    if min(xs) >= 180: 
        for p in out: p[0] -= 360
    elif max(xs) <= -180:
        for p in out: p[0] += 360
    return [[round(p[0], 2), round(p[1], 2)] for p in out]

wanted = {r['geo'] for r in rows}
feats = {}
for g in topo['objects']['countries']['geometries']:
    nm = g['properties']['name']
    if nm not in wanted: 
        polys = None
    if g['type'] == 'Polygon':
        polys = [[ring(r) for r in g['arcs']]]
    elif g['type'] == 'MultiPolygon':
        polys = [[ring(r) for r in poly] for poly in g['arcs']]
    else:
        continue
    feats[nm] = polys
base = {nm: p for nm, p in feats.items() if nm != 'Antarctica'}
print('geometries:', len(base), 'wanted matched:', len(wanted & set(base)), 'unmatched:', sorted(wanted - set(base)))


assert all(r['geo'] in base for r in rows)
output = {'rows': rows, 'oecd': oecd, 'geo': base, 'sources': manifest, 'verified': '2026-09-08', 'oecd_trend_population': 'OECD average-35'}
(HERE / 'pisa_data.json').write_text(json.dumps(output, separators=(',', ':'), allow_nan=False))
print('Built 91 systems; all snapshot means and chapter comparisons cross-checked against the annex.')
