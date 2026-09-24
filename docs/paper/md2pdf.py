#!/usr/bin/env python3
# Usage: python3 docs/paper/md2pdf.py docs/paper/handover-2026-09-24.md /tmp/handover.tex && (cd /tmp && tectonic handover.tex)
# Needs XeLaTeX via tectonic, DejaVu fonts and Droid Sans Fallback (CJK).
"""Minimal Markdown -> XeLaTeX (xeCJK) converter for the handover document: headings, paragraphs,
bullet/numbered lists, pipe tables, **bold**, `code`."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
def esc(t):
    t = t.replace('\\', r'\textbackslash{}')
    for a, b in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'), ('~', r'\textasciitilde{}'), ('^', r'\textasciicircum{}')]:
        t = t.replace(a, b)
    return t
def inline(t):
    out = []; pos = 0
    for m in re.finditer(r'`([^`]*)`|\*\*(.+?)\*\*', t):
        out.append(esc(t[pos:m.start()]))
        if m.group(1) is not None:
            parts = re.split(r'([/_.\-])', m.group(1))
            out.append(r'\texttt{' + ''.join(esc(pt) + (r'\allowbreak{}' if re.fullmatch(r'[/_.\-]', pt) else '') for pt in parts) + '}')
        else: out.append(r'\textbf{' + inline(m.group(2)) + '}')
        pos = m.end()
    out.append(esc(t[pos:])); return ''.join(out)
lines = open(src, encoding='utf-8').read().splitlines()
body = []; i = 0; mode = None
def close():
    global mode
    if mode == 'ul': body.append(r'\end{itemize}')
    if mode == 'ol': body.append(r'\end{enumerate}')
    mode = None
title = None
while i < len(lines):
    l = lines[i]
    if l.startswith('# '):
        close(); title = inline(l[2:]); i += 1; continue
    if l.startswith('## '):
        close(); body.append(r'\section*{' + inline(l[3:]) + '}'); i += 1; continue
    if l.startswith('|'):
        close(); rows = []
        while i < len(lines) and lines[i].startswith('|'):
            rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
        rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c) for c in r)]
        n = max(len(r) for r in rows)
        size = r'\scriptsize' if n > 6 else r'\small'
        spec = ('p{4.2cm}' + 'l' * (n - 1)) if n > 6 else ('p{3.5cm}' + 'p{%.1fcm}' % (13.0 / max(n - 1, 1))) * 1 if n <= 3 else ('p{3.5cm}' + 'l' * (n - 1))
        if n == 2: spec = 'p{3.2cm}p{13.3cm}'
        body.append(r'\begin{center}' + size + r'\setlength{\tabcolsep}{3pt}' + '\n' + r'\begin{tabular}{' + spec + '}' + '\n' + r'\toprule')
        for k, r in enumerate(rows):
            r = r + [''] * (n - len(r))
            body.append(' & '.join(inline(c) for c in r) + r' \\')
            if k == 0: body.append(r'\midrule')
        body.append(r'\bottomrule' + '\n' + r'\end{tabular}\end{center}'); continue
    m = re.match(r'^(\s*)[-*] (.*)', l)
    if m:
        if mode != 'ul': close(); body.append(r'\begin{itemize}'); mode = 'ul'
        body.append(r'\item ' + inline(m.group(2))); i += 1; continue
    m = re.match(r'^(\d+)\. (.*)', l)
    if m:
        if mode != 'ol': close(); body.append(r'\begin{enumerate}'); mode = 'ol'
        body.append(r'\item ' + inline(m.group(2))); i += 1; continue
    if l.startswith('```'):
        close(); i += 1; code = []
        while i < len(lines) and not lines[i].startswith('```'): code.append(lines[i]); i += 1
        i += 1; body.append(r'\begin{verbatim}' + '\n' + '\n'.join(code) + '\n' + r'\end{verbatim}'); continue
    if not l.strip():
        close(); body.append(''); i += 1; continue
    if mode in ('ul', 'ol') and l.startswith('  '):
        body[-1] += ' ' + inline(l.strip()); i += 1; continue
    close(); body.append(inline(l)); i += 1
close()
head = r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=2cm]{geometry}
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont[Scale=0.9]{DejaVu Sans Mono}
\usepackage{xeCJK}
\xeCJKDeclareCharClass{Default}{"2010->"2027, "2030->"205E}
\setCJKmainfont{Droid Sans Fallback}
\setCJKsansfont{Droid Sans Fallback}
\setCJKmonofont{Droid Sans Fallback}
\usepackage{booktabs}
\usepackage[hidelinks]{hyperref}
\setlength{\parskip}{4pt}
\setlength{\parindent}{0pt}
\begin{document}
'''
doc = head + (r'\section*{' + title + '}' + '\n' if title else '') + '\n'.join(body) + '\n\\end{document}\n'
open(dst, 'w', encoding='utf-8').write(doc)
print('wrote', dst, len(body), 'lines')
