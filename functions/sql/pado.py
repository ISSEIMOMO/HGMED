from django.db import connection
from dbbase.md import mod
def pdr(t):
    mdd=mod[:]
    x=0
    for i in mdd:
        t=t.replace(i,str(x))
    for i in mdd:
        if str(x) in t:
            t = t.replace(i, f"dbbase_{mdd[x]}")
        x=x+1
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