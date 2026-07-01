#!/usr/bin/env python3
import sys
from pathlib import Path
import base64
html_file = Path('gemini-code-1782873122785.html')
out_file = Path('site_embedded.html')
if not html_file.exists():
    print('HTML not found', file=sys.stderr); sys.exit(1)
html = html_file.read_text(encoding='utf-8')
replacements = {
    'UDD.png': ('image/png', Path('UDD.png')),
    'UDDMED.jpg': ('image/jpeg', Path('UDDMED.jpg')),
    'LUCIANO.jpg': ('image/jpeg', Path('LUCIANO.jpg')),
    'EMILIANO.jpeg': ('image/jpeg', Path('EMILIANO.jpeg')),
    'NACHO.jpg': ('image/jpeg', Path('NACHO.jpg')),
}
for name,(mtype,p) in replacements.items():
    if p.exists():
        b64 = base64.b64encode(p.read_bytes()).decode('ascii')
        datauri = f"data:{mtype};base64,{b64}"
        html = html.replace(f'src="{name}"', f'src="{datauri}"')
    else:
        print(f'Warning: {name} not found', file=sys.stderr)
out_file.write_text(html, encoding='utf-8')
print('Wrote', out_file)
# Try upload to transfer.sh
import subprocess
try:
    cmd = ['curl','--progress-bar','--upload-file', str(out_file), 'https://transfer.sh/'+out_file.name]
    print('Uploading with:', ' '.join(cmd))
    res = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode==0:
        print(res.stdout.strip())
    else:
        print('Upload failed', res.stderr.strip(), file=sys.stderr)
except Exception as e:
    print('Upload error', e, file=sys.stderr)
