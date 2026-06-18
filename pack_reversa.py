import os
import base64

def pack_folder(folder_path, output_script):
    file_data = {}
    
    # Arquivos que não devem ser empacotados
    ignore_files = ['pack_reversa.py', 'unpack_reversa.py']
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file in ignore_files:
                continue
                
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, folder_path)
            
            with open(abs_path, 'rb') as f:
                content = f.read()
                file_data[rel_path] = base64.b64encode(content).decode('utf-8')
                
    with open(output_script, 'w', encoding='utf-8') as f:
        f.write('import os\n')
        f.write('import base64\n\n')
        f.write('file_data = {\n')
        for path, b64content in file_data.items():
            # Padroniza barras para evitar problemas entre SOs
            f.write(f'    "{path.replace(os.sep, "/")}": "{b64content}",\n')
        f.write('}\n\n')
        
        f.write('''def unpack(target_dir='reversa'):
    # Cria o diretório se não existir
    os.makedirs(target_dir, exist_ok=True)
    
    for rel_path, b64content in file_data.items():
        # Normaliza o caminho para o SO atual
        norm_path = os.path.normpath(rel_path)
        abs_path = os.path.join(target_dir, norm_path)
        
        # Cria as subpastas necessárias
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        
        # Escreve o arquivo
        with open(abs_path, 'wb') as f:
            f.write(base64.b64decode(b64content))
            
    print("Arquivos extraídos com sucesso na pasta:", os.path.abspath(target_dir))

if __name__ == "__main__":
    unpack()
''')

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, 'unpack_reversa.py')
    pack_folder(current_dir, output_file)
    print(f"Script de desempacotamento gerado com sucesso em: {output_file}")
    print("Copie o conteúdo de unpack_reversa.py para o seu GitHub pessoal.")
