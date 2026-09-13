import requests
import re

def gerar_consulta(pergunta):

    pergunta = pergunta.lower()

    correspondencia_maior = re.search(r"mais\s+de\s+(\d+)", pergunta)

    correspondencia_idade = re.search(r"(\d+)\s+anos", pergunta)

    if correspondencia_maior:

        idade_minima = correspondencia_maior.group(1)

        consulta = f"""
        PREFIX ex: <http://example.com/base/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?nome ?idade
        WHERE {{
            ?pessoa a ex:Pessoa ;
                    ex:nome ?nome ;
                    ex:idade ?idade .
            FILTER(xsd:integer(STR(?idade)) > {idade_minima})
        }}
        """

        return consulta

    elif correspondencia_idade:

        idade = correspondencia_idade.group(1)

        consulta = f"""
        PREFIX ex: <http://example.com/base/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?nome ?idade
        WHERE {{
            ?pessoa a ex:Pessoa ;
                    ex:nome ?nome ;
                    ex:idade ?idade .
            FILTER(xsd:integer(STR(?idade)) = {idade})
        }}
        """

        return consulta

    return None


pergunta = input("Faça uma pergunta: ")

consulta = gerar_consulta(pergunta)

if consulta is None:
    print("Pergunta não reconhecida. Por favor, tente novamente.")
    exit()


url = "http://localhost:7200/repositories/tcc_pessoas"

resposta = requests.post(
    url,
    data=consulta,
    headers={
        "Content-Type": "application/sparql-query",
        "Accept": "application/sparql-results+json"
    }
)

print("Status:", resposta.status_code)

dados = resposta.json()

resultados = dados["results"]["bindings"]

if resultados:

    for resultado in resultados:

        nome = resultado["nome"]["value"]
        idade = resultado["idade"]["value"]

        print(f"Resposta: {nome} tem {idade} anos.")

else:
    print("Nenhuma pessoa encontrada.")
    