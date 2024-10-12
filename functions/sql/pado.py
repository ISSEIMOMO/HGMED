from django.db import connection
from dbbase.md import mod
def pdr(t):
    for i in mod:
        t=t.replace(i,f"dbbase_{i}")
    return t


def chamada(str):
    with connection.cursor() as cursor:
        try:
            cursor.execute(pdr(str))
        except:
            return False, "erro na chamada"
        resultados = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]
    return True, resultados, colunas