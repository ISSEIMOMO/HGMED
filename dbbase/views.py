from django.shortcuts import render
from django.urls import reverse

from functions.sql.pado import chamada
import pandas as pd
from django.http import HttpResponse
import urllib.parse

# Create your views here.



def pes(request, chm=""):
    chm = urllib.parse.unquote(chm) if chm else ""
    cargo = chamada(chm) if chm else [True, "", ""]
    err = ""
    if not cargo[0]:
        err = cargo[1]
        cargo = [True, "", ""]
    url=str(request.build_absolute_uri(reverse('excel',args=[str(urllib.parse.quote(chm))]))) if chm else ""
    contex = {"re": cargo[1], "ch": cargo[2], "ve": chm,
              "url": url,"urlpes":request.build_absolute_uri(reverse('pes')),"err":err}
    return render(request, "db/terminal.html", contex)

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




def adicionar(request):
    return render(request, "db/terminal.html", {})
