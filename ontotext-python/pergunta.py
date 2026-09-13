import requests
import re


def gerar_consulta(pergunta):

    pergunta = pergunta.lower()

    # Mais de X anos
    
    correspondencia_maior = re.search(r"mais\s+de\s+(\d+)", pergunta)

    if correspondencia_maior:

        idade = correspondencia_maior.group(1)

        return f"""
        PREFIX ex: <http://example.com/base/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?nome ?idade
        WHERE {{
            ?pessoa a ex:Pessoa ;
                    ex:nome ?nome ;
                    ex:idade ?idade .
            FILTER(xsd:integer(STR(?idade)) > {idade})
        }}
        """


    # Menos de X anos
    
    correspondencia_menor = re.search(r"menos\s+de\s+(\d+)", pergunta)

    if correspondencia_menor:

        idade = correspondencia_menor.group(1)

        return f"""
        PREFIX ex: <http://example.com/base/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?nome ?idade
        WHERE {{
            ?pessoa a ex:Pessoa ;
                    ex:nome ?nome ;
                    ex:idade ?idade .
            FILTER(xsd:integer(STR(?idade)) < {idade})
        }}
        """


    # Idade exata
    
    correspondencia_idade = re.search(r"(\d+)\s+anos", pergunta)

    if correspondencia_idade:

        idade = correspondencia_idade.group(1)

        return f"""
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


    # Idade de uma pessoa
    
    nomes = ["joão", "maria", "pedro"]

    for nome in nomes:

        if nome in pergunta:

            return f"""
            PREFIX ex: <http://example.com/base/>

            SELECT ?nome ?idade
            WHERE {{
                ?pessoa a ex:Pessoa ;
                        ex:nome ?nome ;
                        ex:idade ?idade .
                FILTER(?nome = "{nome.capitalize()}")
            }}
            """


    # Listar todas as pessoas
    
    if "todas as pessoas" in pergunta or "liste as pessoas" in pergunta:

        return """
        PREFIX ex: <http://example.com/base/>

        SELECT ?nome ?idade
        WHERE {
            ?pessoa a ex:Pessoa ;
                    ex:nome ?nome ;
                    ex:idade ?idade .
        }
        """


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