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
        cargo = [True, "", ""]
        err = "Erro na chamada, chamada errada"
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
    """from dbbase.models import VProduto as mm
    from dbbase.models import Marca as ma
    from dbbase.models import TipoProduto as tp
    import random
    marcas = []
    while len(marcas)<3000:
        numero = random.randint(10 ** 12, 10 ** 13 - 1)
        if not numero in marcas:
            marcas.append(numero)
    print(marcas)
    x=0
    tp=list(tp.objects.values_list('codtip', flat=True))
    ma=list(ma.objects.values_list('codtmarc', flat=True))
    for i in range(1,300):
        it = random.randint(0, len(tp)-1)
        for ii in range(1,10):
            ipo = random.randint(0, len(ma) - 1)
            marc = mm(codpro=marcas[x],codtip_id=tp[it],codmarc_id=ma[ipo],valor=round(random.uniform(0.01, 300.00), 2))
            marc.save()
            print(x)
            x=x+1
        del tp[0]
    print("terminou")"""
    return render(request, "db/terminal.html", {})