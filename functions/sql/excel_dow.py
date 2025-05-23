import pandas as pd
from django.http import HttpResponse
from django.db import connection

from functions.sql.pado import chamada


def exportar_para_excel(request):
    resultados, colunas = chamada('SELECT * FROM Cargo AS c\nWHERE c.nome = c.nome')

    # Convertendo os resultados para um DataFrame do pandas
    df = pd.DataFrame(resultados, columns=colunas)

    # Criando uma resposta HTTP para o arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=produtos.xlsx'

    # Exportando o DataFrame para Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Produtos')

    return response
