from django.contrib import admin

from dbbase.models import (Funcionario,Cargo,Departamento,Venda,VProduto,Fornecedor,Carregamento,Desconto,
                           Perda, Estoque, Despesa, Atividade, Ponto,TipoProduto,Marca, PVenda, Cliente)

# Register your models here.


admin.site.register(Funcionario)
admin.site.register(Cliente)
admin.site.register(Cargo)
admin.site.register(Departamento)
admin.site.register(Venda)
admin.site.register(PVenda)
admin.site.register(VProduto)
admin.site.register(Fornecedor)
admin.site.register(Carregamento)
admin.site.register(Desconto)
admin.site.register(Perda)
admin.site.register(Estoque)
admin.site.register(Despesa)
admin.site.register(Atividade)
admin.site.register(Ponto)
admin.site.register(TipoProduto)
admin.site.register(Marca)