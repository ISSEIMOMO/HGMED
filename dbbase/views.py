from django.shortcuts import render
from django.db import connection

from functions.sql.pado import pdr


# Create your views here.


def terminal(request):
    from dbbase.models import Cargo
    with connection.cursor() as cursor:
        cursor.execute(pdr(f'SELECT * FROM Cargo WHERE nome = nome'))
        resultados = cursor.fetchall()
    contex={"re":resultados}
    print(resultados)
    return render(request,"db/terminal.html", contex)