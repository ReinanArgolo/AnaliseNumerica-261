import re
import glob

tex_files = glob.glob(r'/home/reinanlinux/Documentos/UESC/semIV/AnNum20261/relatorio1/docs/secoes/*.tex')

for path in tex_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert \resizebox{\linewidth}{!}{ ... }
    # Note: we used exactly this format in the previous script 
    # r'\resizebox{\linewidth}{!}{' + '\n' + full_match + '\n}'
    
    new_content = re.sub(r'\\resizebox\{\\linewidth\}\{!}\{\n(\\begin\{tabular\}[\s\S]*?\\end\{tabular\})\n\}', r'\1', content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Reverted in {path}")

