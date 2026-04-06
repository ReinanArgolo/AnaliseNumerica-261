import re
import glob

# 1. Update utils.py to add configurar_ambiente
utils_path = 'relatorio1/src/metodos/utils.py'
with open(utils_path, 'r', encoding='utf-8') as f:
    utils_code = f.read()

if 'def configurar_ambiente(' not in utils_code:
    utils_code += "\n\ndef configurar_ambiente(nome_script, linhas_padrao=None):\n"
    utils_code += '    """Garante a estrutura de pastas e ler arquivo txt.\n'
    utils_code += '    Substitui as funcoes `inicializar_ambiente` redundantes."""\n'
    utils_code += "    if linhas_padrao is None:\n"
    utils_code += "        linhas_padrao = ['tol:1e-4\\n', 'max_iter:100\\n']\n\n"
    utils_code += "    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))\n"
    utils_code += "    entradas_dir = os.path.join(base_dir, 'dados', 'entradas')\n"
    utils_code += "    saidas_dir = os.path.join(base_dir, 'dados', 'saida', nome_script)\n\n"
    utils_code += "    os.makedirs(entradas_dir, exist_ok=True)\n"
    utils_code += "    os.makedirs(saidas_dir, exist_ok=True)\n\n"
    utils_code += "    arquivo_entrada = os.path.join(entradas_dir, f\"{nome_script}.txt\")\n\n"
    utils_code += "    if not os.path.exists(arquivo_entrada):\n"
    utils_code += "        print(f\"[{nome_script}] Arquivo '{nome_script}.txt' ausente. Criando template...\")\n"
    utils_code += "        with open(arquivo_entrada, 'w') as file:\n"
    utils_code += "            file.writelines(linhas_padrao)\n"
    utils_code += "        return None, saidas_dir\n\n"
    utils_code += "    parametros = {}\n"
    utils_code += "    with open(arquivo_entrada, 'r') as file:\n"
    utils_code += "        for linha in file:\n"
    utils_code += "            linha = linha.strip()\n"
    utils_code += "            if linha and not linha.startswith('#') and ':' in linha:\n"
    utils_code += "                chave, valor = linha.split(':')\n"
    utils_code += "                parametros[chave.strip()] = float(valor.strip())\n\n"
    utils_code += "    return parametros, saidas_dir\n"
    with open(utils_path, 'w', encoding='utf-8') as f:
        f.write(utils_code)

# 2. Refactor all script files
for script_file in glob.glob('relatorio1/src/scripts_questoes/*.py'):
    with open(script_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # regex extract file.write(...) contents
    inicia_match = re.search(r'def inicializar_ambiente\(.*?\):(.*?)return\s+parametros,\s+saidas_dir', code, re.DOTALL)
    if inicia_match:
        writes = re.findall(r'file\.write\((.*?)\)', inicia_match.group(1))
        linhas_lista = "[" + ", ".join(writes) + "]"
        
        # Remove the function definition
        code = code[:inicia_match.start()] + code[inicia_match.end():]
        
        # Replace the call
        code = code.replace("inicializar_ambiente(nome_script)", f"utils.configurar_ambiente(nome_script, {linhas_lista})")
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"Refactored {script_file}")

