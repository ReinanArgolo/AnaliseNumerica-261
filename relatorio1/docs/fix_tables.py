import os
import glob
import re

tex_files = glob.glob('/home/reinanlinux/Documentos/UESC/semIV/AnNum20261/relatorio1/docs/secoes/*.tex')

for fpath in tex_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace [h] with [ht] in table/figure
    content = re.sub(r'\\begin\{(table|figure)\}\[h\]', r'\\begin{\1}[ht]', content)
    
    # Optional: wrap tabular in resizebox if not already wrapped
    if 'graphicx' not in content:
        # We'll just replace \begin{table}[h] to [ht] for now
        pass

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

