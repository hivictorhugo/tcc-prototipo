import subprocess
import re 
import requests

CLI = r"C:\Users\vhque\AppData\Local\Ontotext Refine\app\bin\ontorefine-cli.cmd"
URL = "http://localhost:7333"

CSV = r"C:\Users\vhque\OneDrive\Área de Trabalho\TCC\ontotext-python\pessoas - Página1.csv"

def criar_projeto():
    comando = [
        CLI,
        "create",
        CSV,
        "-u",
        URL      
    ]
    
    resultado = subprocess.run(
    comando,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
    )

    
    print(resultado.stdout)
    print(resultado.stderr)
    
    #Procura o idenficador retornado pelo Ontotext Refine
    
    correspondencia = re.search(r"identifier:\s*(\d+)", resultado.stdout)
    
    if not correspondencia: 
        raise RuntimeError("Não foi possível encontrar o ID do projeto.")
    
    return correspondencia.group(1)

def gerar_rdf(projeto_id):
    comando = [
        CLI,
        "rdf",
        projeto_id,
        "-u",
        URL,
        "-m",
        r"C:\Users\vhque\Downloads\mapping.json"    
    ]
    
    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    
    print(resultado.stderr)
    
    caminho_saida = r"C:\Users\vhque\OneDrive\Área de Trabalho\TCC\ontotext-python\resultado.ttl"
    
    with open(caminho_saida, "w", encoding="utf-8-sig", newline="\n") as arquivo:
        arquivo.write(resultado.stdout)

    print(f"RDF gerado com sucesso! Caminho do arquivo: {caminho_saida}")
    
def ingerir_no_graphdb(caminho_ttl):
    url_graphdb = "http://localhost:7200/repositories/tcc_pessoas/statements"
    
    with open(caminho_ttl, "rb") as arquivo:
        resposta = requests.post(
            url_graphdb,
            data=arquivo,
            headers={
                "Content-Type": "application/x-turtle"
            }
        )
        
    print("Status GraphDB:", resposta.status_code)
    print("Resposta GraphDB:", resposta.text)
    
    if resposta.status_code not in [200, 204]:
        raise RuntimeError("Não foi possível ingerir o RDF no GraphDB.") 


projeto_id = criar_projeto()

print(f"Projeto criado com sucesso! ID do projeto: {projeto_id}")

gerar_rdf(projeto_id)

ingerir_no_graphdb("resultado.ttl")

print("Processo completo!")
