"""Inject the extracted PISA dataset into template.html -> ../index.html"""
import json, pathlib
from validate_data import validate
validate(include_html=False)
here = pathlib.Path(__file__).parent
data = json.loads((here / 'pisa_data.json').read_text())
tpl = (here / 'template.html').read_text()
assert tpl.count('__PISA_DATA__') == 1
# template.html is published too, so it is noindex; the assembled page is the
# one meant for search. Everything else in <head> is shared.
TEMPLATE_ROBOTS = '<meta name="robots" content="noindex, follow">'
PAGE_ROBOTS = '<meta name="robots" content="index, follow, max-image-preview:large">'
assert tpl.count(TEMPLATE_ROBOTS) == 1
out = tpl.replace('__PISA_DATA__', json.dumps(data, separators=(',', ':')))
out = out.replace(TEMPLATE_ROBOTS, PAGE_ROBOTS)
(here.parent / 'index.html').write_text(out)
print('index.html', len(out), 'bytes')
