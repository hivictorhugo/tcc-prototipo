*Sobre o projeto*

Protótipo de Grafo de Conhecimento automatizado com Python, Ontotext Refine e GraphDB.

O sistema realiza:

CSV → Python → Ontotext Refine → RDF/Turtle → GraphDB → SPARQL

*Principais arquivos*

automacao.py — automatiza a criação do projeto no Ontotext Refine, geração do RDF e inserção no GraphDB.

pergunta.py — recebe perguntas em linguagem natural e gera consultas SPARQL.

consulta.py — testa consultas SPARQL diretamente.

mapping.json — define o mapeamento dos dados para RDF.

resultado.ttl — RDF gerado automaticamente.

pessoas - Página1.csv — dados utilizados no protótipo.

*Como executar*

1. Inicie
Ontotext Refine em http://localhost:7333
GraphDB em http://localhost:7200
Repositório tcc_pessoas
2. Instale a dependência
pip install requests
3. Gere e envie o Grafo

Na pasta do projeto:

python automacao.py

Se aparecer:

Status GraphDB: 204
Processo completo!

a automação funcionou.

4. Faça perguntas

Depois execute:

python pergunta.py

Exemplos:

quantos anos tem maria?
quem tem mais de 20 anos?
quem tem menos de 30 anos?
liste todas as pessoas

Funcionamento atual

O pergunta.py ainda utiliza regras fixas em Python para interpretar as perguntas.

A próxima etapa será substituir essas regras por um LLM, permitindo que perguntas mais variadas sejam convertidas automaticamente em SPARQL:

Usuário
 ↓
LLM
 ↓
SPARQL
 ↓
GraphDB
 ↓
Resultado
 ↓
Resposta em linguagem natural
