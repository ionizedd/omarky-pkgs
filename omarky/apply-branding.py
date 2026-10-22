#!/usr/bin/env python3
"""Omarky: make /etc/os-release say Omarky in the omarchy-settings recipes (stable and -dev).
Repeatable on purpose -- upstream edits these lines. ID stays `omarchy` (other code keys on it).
Run from the repo root after every upstream merge; idempotent."""
import os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
NEW = {
 'NAME': '"Omarky"', 'PRETTY_NAME': '"Omarky"',
 'HOME_URL': '"https://github.com/ionizedd/omarky"',
 'DOCUMENTATION_URL': '"https://github.com/ionizedd/omarky"',
 'BUG_REPORT_URL': '"https://github.com/ionizedd/omarky/issues"',
}
n = 0
for p in ('pkgbuilds/omarchy-settings/PKGBUILD', 'pkgbuilds/omarchy-settings-dev/PKGBUILD'):
    s = open(p).read()
    a = s.find('NAME="Omarchy"\nPRETTY_NAME'); a = a if a >= 0 else s.find('NAME="Omarky"\nPRETTY_NAME')
    if a < 0: print('no os-release block in', p); continue
    b = s.index('EOF', a); block = s[a:b]; out = []
    for line in block.split('\n'):
        k = line.split('=', 1)[0]
        if k == 'SUPPORT_URL': continue            # upstream's Discord
        out.append(f'{k}={NEW[k]}' if k in NEW else line)
    new = s[:a] + '\n'.join(out) + s[b:]
    if new != s: open(p, 'w').write(new); n += 1
print(f'apply-branding: {n} file(s) changed')
