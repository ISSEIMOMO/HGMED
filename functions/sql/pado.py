from django.db import connection
from dbbase.md import mod, ER as er
import sqlglot
import difflib


def pdr(t):
    t = t[0:len(t)-1] if t[len(t)-1]==";" else t
    palavras = t.split()
    for i in mod:
        palavra_nova = f"dbbase_{i}"
        palavra_antiga = i
        palavras = [palavra_nova.lower() if palavra.lower() == palavra_antiga.lower() else palavra for palavra in palavras]
    palavras = ' '.join(palavras)
    return palavras


def nome_mais_proximo(palavra, opcoes):
    correspondencias = difflib.get_close_matches(palavra, opcoes, n=1)

    if correspondencias:
        return f" - Vc não quis dizer |{correspondencias[0]}|"
    else:
        return ""


def verifierros(query):
    txtre = [
        ["Required keyword: 'expression' missing for <class 'sqlglot.expressions.Mul'>.", ""],
        ["[4m", "|"],
        ["[0m", "|"]
    ]

    erros = []
    sugestoes = {
        "FRROM": "FROM",
        "SELCT": "SELECT",
        "INSRT": "INSERT",
        "UPDAE": "UPDATE",
        # Adicione mais correções comuns aqui, se necessário
    }

    try:
        parsed = sqlglot.parse_one(query)
    except Exception as e:
        e = str(e)
        for i in txtre:
            e = e.replace(i[0], i[1])
        for erro, correcao in sugestoes.items():
            if erro in query:
                e = f"você quis dizer |{correcao}| em vez de |{erro}|?"
        return [f"Erro de sintaxe na consulta SQL: {e}"]

    if not isinstance(parsed, sqlglot.exp.Select):
        erros.append(f"Ação do tipo |{parsed.__class__.__name__}| não autorizada")

    # Obtendo as tabelas da consulta
    tables = parsed.find_all(sqlglot.exp.Table)
    table_map = {table.alias or table.name: table.name for table in tables}

    # Obtendo as colunas selecionadas e associando-as às tabelas
    columns = parsed.find_all(sqlglot.exp.Column)
    column_info = [(col.name, col.table or col.alias) for col in columns]

    # Verifica se as tabelas existem
    for table_name in table_map.values():
        if not f"dbbase_{table_name}" in list(er.keys()):
            erros.append(f"A tabela |{table_name}| não existe{nome_mais_proximo(table_name, mod)}")

    # Verifica se as colunas existem nas respectivas tabelas
    for col_name, table_alias in column_info:
        real_table_name = table_map.get(table_alias, table_alias)
        if f"dbbase_{real_table_name}" in list(er.keys()):
            if not col_name in er[f"dbbase_{real_table_name}"]["cp"]:
                erros.append(f"A tabela |{real_table_name}| não tem o campo |{col_name}|{nome_mais_proximo(col_name,er[f'dbbase_{real_table_name}']['cp'])}")

    return erros


def chamada(str):
    with connection.cursor() as cursor:
        cc=verifierros(str)
        if not cc==[]:
           return False, cc
        try:
            print(pdr(str))
            cursor.execute(pdr(str))
        except Exception as e:
            print(e)
            return False, ["erro na chamada"]
        resultados = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]
    return True, resultados, colunas