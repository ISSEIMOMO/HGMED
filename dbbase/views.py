from django.shortcuts import render
from functions.sql.pado import chamada
import pandas as pd
from django.http import HttpResponse
import urllib.parse

# Create your views here.


def terminal(request):
    ve='SELECT * FROM Cargo AS c\nWHERE c.nome = c.nome'
    cargo = chamada(ve)
    if not cargo[0]:
        cargo = [True, "", ""]
    contex={"re":cargo[1],"ch":cargo[2],"ve":ve,"url":f"{request.build_absolute_uri()}excel/{urllib.parse.quote(ve.replace('\n',' '))}"}
    return render(request,"db/terminal.html", contex)



def excel(request, chm):
    chm = urllib.parse.unquote(chm)
    est = chamada(chm)
    if est[0]:
        est, resultados, colunas = est
        # Convertendo os resultados para um DataFrame do pandas
        df = pd.DataFrame(resultados, columns=colunas)

        # Criando uma resposta HTTP para o arquivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=produtos.xlsx'

        # Exportando o DataFrame para Excel
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Produtos')

        return response
    return render(request, "db/terminal.html", {"ve":chm})
