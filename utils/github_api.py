from github import Github
import re
import os
import io

# Conecta ao GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPOSITORIO = os.getenv("REPOSITORIO")
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPOSITORIO)

def analisar_fontes(choice=None):
    match choice:
        case "NFe":
            files = repo.get_contents("src/Libs/nfephp/libs/NFe/MakeNFePHP.class.php")
        case "CTe":
            files = repo.get_contents("src/Libs/nfephp/libs/CTe/MakeCTeNFePHP.class.php")
        case "MDFe":
            files = repo.get_contents("src/Libs/nfephp/libs/MDFe/MakeMDFeNFePHP.class.php")
        case "NFCe":
            files = repo.get_contents("src/Libs/nfephp/libs/NFe/MakeNFePHP.class.php")
        case "NFSe":
            files = repo.get_contents("src/Libs/nfephp/libs/NFSe/NFSeSP.class.php")
    
    if files:
        extrair_e_salvar_fontes(files)

def extrair_e_salvar_fontes(conteudo_arquivo, pasta_destino=".temp"):
    """
    Extrai o conteúdo de um arquivo do GitHub usando geradores 
    e salva localmente como um arquivo .php.
    """
    
    # Obtém o conteúdo bruto do arquivo
    conteudo_bytes = conteudo_arquivo.decoded_content
    
    # Gerador para ler o conteúdo em pedaços (chunks)
    def gerador_de_leitura(dados, chunk_size=1024):
        stream = io.BytesIO(dados)
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            yield chunk.decode("utf-8")

    # Criando o arquivo localmente
    nome_arquivo_local = conteudo_arquivo.name

    # Garante que a pasta de destino existe
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Gera um nome único para evitar que um download sobrescreva o outro
    nome_unico = f"{uuid.uuid4()}_{nome_arquivo_local}.php"
    caminho_completo = os.path.join(pasta_destino, nome_unico)
    
    with open(caminho_completo, "w", encoding="utf-8") as f:
        for trecho in gerador_de_leitura(conteudo_bytes):
            f.write(trecho)
            
    return caminho_completo