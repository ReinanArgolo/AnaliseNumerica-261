import re
import glob

tex_files = glob.glob(r'/home/reinanlinux/Documentos/UESC/semIV/AnNum20261/relatorio1/docs/secoes/*.tex')

for path in tex_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # To avoid double-wrapping, skip if \resizebox is already there
    # It's safer to just do a simple sub where we find \begin{tabular}{something} ... \end{tabular}
    # and only wrap if it's not preceded by \resizebox

    def replace_tabular(match):
        full_match = match.group(0)
        return r'\resizebox{\linewidth}{!}{' + '\n' + full_match + '\n}'

    # Regex matches \begin{tabular}{...} content \end{tabular}
    # We use negative lookbehind but Python's re engine has limits for variable length.
    # So let's just do a naive regex, but skip if the file already has \resizebox
    if r'\resizebox' not in content:
        new_content = re.sub(r'\\begin\{tabular\}[\s\S]*?\\end\{tabular\}', replace_tabular, content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

