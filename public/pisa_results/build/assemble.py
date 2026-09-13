"""Inject the extracted PISA dataset into template.html -> ../index.html"""
import json, pathlib
from validate_data import validate
validate(include_html=False)
here = pathlib.Path(__file__).parent
data = json.loads((here / 'pisa_data.json').read_text())
tpl = (here / 'template.html').read_text()
assert tpl.count('__PISA_DATA__') == 1
out = tpl.replace('__PISA_DATA__', json.dumps(data, separators=(',', ':')))
(here.parent / 'index.html').write_text(out)
print('index.html', len(out), 'bytes')
