import os
import re
from datetime import datetime

def update_documentation_images():
    """Atualiza as referências de imagens na documentação para apontar para os screenshots mais recentes"""
    
    # Diretório de screenshots
    screenshots_dir = "screenshots"
    
    # Diretórios de documentação
    docs_dirs = ["docs/user"]
    
    # Padrão para identificar referências de imagens
    image_pattern = r'!\[([^\]]*)\]\(([^)]*)\)'
    
    # Para cada diretório de documentação
    for doc_dir in docs_dirs:
        if not os.path.exists(doc_dir):
            continue
            
        # Para cada arquivo markdown no diretório
        for filename in os.listdir(doc_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(doc_dir, filename)
                
                # Ler o conteúdo do arquivo
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Encontrar todas as referências de imagens
                matches = re.findall(image_pattern, content)
                
                # Atualizar as referências
                updated_content = content
                for alt_text, image_path in matches:
                    # Verificar se é um screenshot
                    if "screenshots/" in image_path and not image_path.startswith("http"):
                        # Obter o nome base do arquivo (sem extensão e timestamp)
                        base_name = os.path.basename(image_path)
                        if '.' in base_name:
                            base_name = '.'.join(base_name.split('.')[:-1])
                        
                        # Remover timestamp se existir
                        if '_' in base_name:
                            base_name = '_'.join(base_name.split('_')[:-2])
                        
                        # Procurar o screenshot mais recente com esse nome base
                        if os.path.exists(screenshots_dir):
                            screenshots = [f for f in os.listdir(screenshots_dir) if f.startswith(base_name)]
                            if screenshots:
                                # Ordenar por data (do mais recente para o mais antigo)
                                screenshots.sort(reverse=True)
                                latest_screenshot = screenshots[0]
                                
                                # Atualizar a referência
                                old_ref = f'![{alt_text}]({image_path})'
                                new_ref = f'![{alt_text}](../screenshots/{latest_screenshot})'
                                updated_content = updated_content.replace(old_ref, new_ref)
                                print(f"Atualizado: {old_ref} -> {new_ref}")
                
                # Salvar o conteúdo atualizado
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"Arquivo atualizado: {filepath}")

if __name__ == "__main__":
    update_documentation_images()
    print("Atualização de imagens concluída!")