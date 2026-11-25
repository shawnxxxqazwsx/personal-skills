#!/usr/bin/env python3
"""Freeze the current UI into an offline, recording-only design laboratory."""
import argparse, datetime, hashlib, json, pathlib

root = pathlib.Path(__file__).resolve().parents[4]
skill = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=pathlib.Path, default=root)
parser.add_argument('--date', default=datetime.date.today().isoformat())
args = parser.parse_args()
src = args.repo / 'apps/host/ui'
dst = skill / 'assets/atlas/source-ui'
html = (src / 'host-surface.html').read_text()
ending = '})();\n</script>\n</body>'
assert ending in html, 'Production surface closure changed: inspect before exposing the laboratory.'
dst.mkdir(parents=True, exist_ok=True)
files = {}
for p in sorted(src.rglob('*')):
    if not p.is_file(): continue
    relative = p.relative_to(src)
    target = dst / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    data = p.read_bytes()
    target.write_bytes(data)
    files[str(relative)] = hashlib.sha256(data).hexdigest()
html = html.replace('<head>', '<head>\n<script src="../lab-init.js"></script>', 1)
expose = '''window.chloraUiLabSource={
 markup:graphNodeInnerMarkup,metrics:graphNodeMetrics,helpers:fileGraphUiHelpers,
 create:createGraphNodeElement,update:updateGraphNodeElement,
 setBrowser:setBrowserCollapsed,render:renderGraph,
 getState:function(){return state;},setState:function(s){state=Object.assign(state,s);},
 setThumb:setChannelThumb
};\n'''
html = html.replace(ending, expose + ending, 1)
html = html.replace('</body>', '<script src="../motion-specs.js"></script><script src="../lab-runtime.js"></script>\n</body>', 1)
(dst / 'lab.html').write_text(html)
manifest = {'date':args.date,'scope':'Strip and DraftRoom; Device Input, Device Output and Analyzer excluded as design references',
 'layer':'Frozen working-tree CSS/HTML/JS; authored fixture data; recording backend; no engine, files, audio or native changes',
 'sourceRoot':str(src),'files':files,'previousSnapshot':'history/20261029/provenance.json',
 'palettePolicy':'Existing approved palette retained; snapshot refresh is documentation, not a regenerated test expectation.',
 'labTransform':'Inject recording-only backend and expose source functions; no production file edits'}
(skill / 'assets/atlas/provenance.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'snapshot':str(dst),'files':len(files),'bytes':sum(p.stat().st_size for p in dst.rglob('*') if p.is_file())}))
