"""Independent source-to-output validation. Run after either build step."""
import hashlib
import json
import math
from pathlib import Path
import re
import openpyxl

HERE = Path(__file__).resolve().parent

def validate(include_html=True):
    data = json.loads((HERE / 'pisa_data.json').read_text())
    manifest = json.loads((HERE / 'sources/manifest.json').read_text())
    assert data['sources'] == manifest
    for filename, source in manifest.items():
        assert hashlib.sha256((HERE / 'sources' / filename).read_bytes()).hexdigest() == source['sha256'], filename
    workbook = openpyxl.load_workbook(HERE / 'sources/annex.xlsx', data_only=True)
    assert len(data['rows']) == len({r['name'] for r in data['rows']}) == 91
    counts = {'means': 0, 'changes': 0, 'missing_means': 0}
    for row in data['rows'] + [data['oecd']]:
        if row is not data['oecd']: assert row['geo'] in data['geo']
        for domain, proof in row['evidence'].items():
            evidence = proof['mean']
            source = workbook[evidence['sheet']][evidence['cell']]
            assert source.parent.cell(source.row,1).value.rstrip('*') == row['name']
            assert source.value == (evidence['value'] if evidence['value'] is not None else evidence['missing_code'])
            if evidence['value'] is None:
                assert row['m'][domain] is None
                counts['missing_means'] += 1
            else:
                assert row['m'][domain] == round(source.value, 1)
                assert evidence['se'] == source.offset(column=1).value
                counts['means'] += 1
            for period in ['s', 'd']:
                if period not in proof: continue
                evidence = proof[period]
                if 'suppressed' in evidence:
                    assert row['name'] == 'Albania' and domain not in row[period]
                    continue
                source = workbook[evidence['sheet']][evidence['cell']]
                expected_name = 'OECD average-35' if row is data['oecd'] else row['name']
                assert source.parent.cell(source.row,1).value.rstrip('*') == expected_name
                if 'missing_code' in evidence:
                    assert source.value == evidence['missing_code'] and domain not in row[period]
                    continue
                assert evidence['value'] == source.value
                assert evidence['se'] == source.offset(column=1).value > 0
                p = source.offset(column=2).value if period == 'd' else math.erfc(abs(source.value / evidence['se']) / math.sqrt(2))
                assert p == evidence['p']
                assert row[period][domain] == [round(source.value, 1), p < .05]
                counts['changes'] += 1
    # Independent published chapter table values + conditional-format backing blocks.
    chapter = openpyxl.load_workbook(HERE / 'sources/ch2.xlsx', data_only=True)
    lookup = {r['name']:r for r in data['rows']}
    lookup['OECD average-35'] = data['oecd']
    for period, title, first, last in [('s','Table I.2.6',10,84),('d','Table I.2.9',11,82)]:
        sheet = chapter[title]
        for i in range(first,last+1):
            name = sheet.cell(i,1).value.rstrip('*')
            for col,dom in enumerate(['sci','read','math'],2):
                assert lookup[name][period][dom][0] == round(sheet.cell(i,col).value,1)
    # Release-specific regressions for corrections found in this audit.
    assert data['oecd']['s']['sci'] == [-2.8, False]
    assert [data['oecd']['d'][k][0] for k in ['sci','read','math']] == [-6.7,-27.0,-23.9]
    assert lookup['Uzbekistan']['s']['sci'] == [82.7,True]
    assert lookup['Uzbekistan']['m']['read'] is None
    assert lookup['Albania']['s'] == lookup['Albania']['d'] == {}
    assert lookup['Viet Nam']['s'] == lookup['Viet Nam']['d'] == {}
    assert lookup['Jordan']['d']['math'] == [-7.0,False]
    assert lookup['Cyprus']['d']['read'] == [-69.6,True]
    if include_html:
        html = (HERE.parent/'index.html').read_text()
        embedded = re.search(r'<script id="pisa-data" type="application/json">(.*?)</script>', html, re.S)
        assert embedded and json.loads(embedded[1]) == data, 'Stale embedded dataset; run assemble.py'
        assert html.startswith('<!doctype html>') and '__PISA_DATA__' not in html
    print(json.dumps({'status':'PASS', **counts}))

if __name__ == '__main__':
    validate()
