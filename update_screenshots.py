import subprocess
import sys
import os

def run_command(command, description):
    \"\"\"Executa um comando e mostra sua saída em tempo real\"\"\"
    print(f\"\\n🔍 {description}\")
    print(f\"📋 Comando: {command}\\n\")
    
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f\"❌ Erro ao executar o comando: {e}\")
        print(f\"stderr: {e.stderr}\")
        return False

def main():
    print(\"🔄 Atualização Automática de Screenshots e Documentação\")
    print(\"=\" * 50)
    
    # 1. Executar Playwright para gerar novos screenshots
    print(\"\\n📸 Etapa 1: Gerando novos screenshots com Playwright\")
    if not run_command(\"python playwright_tests.py\", \"Executando Playwright para capturar screenshots\"):
        print(\"❌ Falha ao gerar screenshots\")
        return
    
    # 2. Atualizar referências de imagens na documentação
    print(\"\\n📝 Etapa 2: Atualizando referências de imagens na documentação\")
    if not run_command(\"python update_doc_images.py\", \"Atualizando referências de imagens na documentação\"):
        print(\"❌ Falha ao atualizar referências de imagens\")
        return
    
    print(\"\\n✅ Processo concluído com sucesso!\")
    print(\"\\n📋 Próximos passos:\")
    print(\"1. Verifique os novos screenshots na pasta 'screenshots/'\")
    print(\"2. Revise a documentação atualizada em 'docs/user/'\")
    print(\"3. Faça commit das mudanças se estiverem corretas\")

if __name__ == \"__main__\":
    main()