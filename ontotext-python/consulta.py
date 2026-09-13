import requests 

url = "http://localhost:7200/repositories/tcc_pessoas"

consulta = """
PREFIX ex: <http://example.com/base/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?nome ?idade
WHERE {
    ?pessoa a ex:Pessoa ;
            ex:nome ?nome ;
            ex:idade ?idade .
    FILTER(xsd:integer(STR(?idade)) > 25)
}
"""

resposta = requests.post(
    url,
    data=consulta,
    headers={ "Content-Type": "application/sparql-query",
        "Accept": "application/sparql-results+json"}
    
)

print("Status:", resposta.status_code)
print(resposta.text)