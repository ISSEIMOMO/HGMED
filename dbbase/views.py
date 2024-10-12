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
    from dbbase.models import TipoProduto as mm
    marcas = [
    "Arroz", "Feijão", "Açúcar", "Sal", "Óleo de soja", "Milho", "Macarrão", "Farinha de trigo", "Biscoito", "Café",
    "Leite", "Iogurte", "Manteiga", "Queijo", "Presunto", "Salsicha", "Frango", "Carne bovina", "Peixe", "Ovos",
    "Maçã", "Banana", "Laranja", "Uva", "Pera", "Abacaxi", "Manga", "Morango", "Limão", "Cenoura",
    "Batata", "Cebola", "Alho", "Tomate", "Pepino", "Repolho", "Brócolis", "Alface", "Espinafre", "Pimentão",
    "Salsa", "Cebolinha", "Pimenta", "Rúcula", "Beterraba", "Abóbora", "Berinjela", "Batata-doce", "Nabo",
    "Radicchio", "Quiabo", "Jiló", "Couve-flor", "Ervilha", "Grão-de-bico", "Lentilha", "Feijão-preto", "Feijão-branco",
    "Feijão-verde", "Macarrão instantâneo", "Caldo de galinha", "Caldo de carne", "Molho de tomate", "Ketchup",
    "Mostarda", "Maionese", "Azeite de oliva", "Vinagre", "Pasta de dente", "Sabonete", "Shampoo", "Condicionador",
    "Desodorante", "Detergente", "Lava-roupas", "Amaciante", "Esponja", "Papel toalha", "Papel higiênico", "Guardanapo",
    "Saquinho de lixo", "Saco de arroz", "Saco de feijão", "Saco de açúcar", "Saco de sal", "Saco de farinha",
    "Saco de macarrão", "Saco de batata", "Saco de cebola", "Saco de alho", "Saco de cenoura", "Saco de tomate",
    "Saco de pimentão", "Saco de uva", "Saco de maçã", "Saco de banana", "Saco de laranja", "Saco de abacaxi",
    "Saco de manga", "Saco de morango", "Saco de pera", "Saco de limão", "Saco de ervilha", "Saco de grão-de-bico",
    "Saco de lentilha", "Saco de feijão-preto", "Saco de feijão-branco", "Saco de feijão-verde", "Saco de macarrão instantâneo",
    "Saco de caldo de galinha", "Saco de caldo de carne", "Saco de molho de tomate", "Saco de ketchup", "Saco de mostarda",
    "Saco de maionese", "Saco de azeite de oliva", "Saco de vinagre", "Pão", "Pão de forma", "Pão francês",
    "Pão integral", "Pão de queijo", "Bolo", "Biscoito recheado", "Bolacha", "Granola", "Cereal", "Pasta",
    "Leite condensado", "Creme de leite", "Leite em pó", "Achocolatado", "Suco de fruta", "Refrigerante",
    "Cerveja", "Vinho", "Destilado", "Água mineral", "Chá", "Cachaça", "Adoçante", "Bebida láctea", "Mix de nuts",
    "Barra de cereal", "Bolo de cenoura", "Bolo de chocolate", "Bolo de frutas", "Pudim", "Gelatina", "Doce de leite",
    "Açai", "Sorvete", "Picolé", "Chiclete", "Balas", "Pirulito", "Torrada", "Cracker", "Biscoito de água e sal",
    "Biscoito de polvilho", "Biscoito de chocolate", "Biscoito integral", "Biscoito sem glúten", "Chips", "Batata frita",
    "Salgadinho", "Amendoim", "Castanha de caju", "Noz", "Azeitona", "Palmito", "Coco ralado", "Farinha de mandioca",
    "Farinha de milho", "Farinha de rosca", "Bacon", "Linguiça", "Presunto cozido", "Presunto cru", "Queijo minas",
    "Queijo parmesão", "Queijo prato", "Queijo gorgonzola", "Queijo feta", "Queijo cottage", "Ricota", "Queijo coalho",
    "Chester", "Peru", "Cordeiro", "Camarão", "Salmão", "Atum", "Bacalhau", "Linguado", "Merluza", "Robalo",
    "Polvo", "Lula", "Sardinha", "Ceviche", "Bolinho de bacalhau", "Sushi", "Ceviche", "Sanduíche", "Wrap",
    "Salada pronta", "Pasta de amendoim", "Patê", "Sopa instantânea", "Mistura para bolo", "Mistura para pão",
    "Mistura para panqueca", "Mistura para pizza", "Cachaça", "Bebida energizante", "Refrigerante light", "Refrigerante zero",
    "Leite de coco", "Leite de amêndoa", "Leite de soja", "Leite de aveia", "Leite de arroz", "Nectar", "Mistura para drink",
    "Vinho tinto", "Vinho branco", "Espumante", "Aperitivo", "Bebida isotônica", "Cerveja artesanal", "Chá gelado",
    "Café solúvel", "Café torrado", "Chá de ervas", "Chá mate", "Chá preto", "Chá verde", "Chá de frutas",
    "Chá de hibisco", "Chá de camomila", "Chá de limão", "Chá de menta", "Chá de gengibre", "Chá de maracujá", "Chá de laranja",
    "Chá de maçã", "Chá de morango", "Chá de pêssego", "Chá de abacaxi", "Chá de framboesa", "Chá de cranberry",
    "Chá de erva-doce", "Chá de capim-limão", "Chá de hibisco", "Chá de rooibos", "Café gelado", "Café descafeinado",
    "Café em grão", "Café moído", "Bebida de amêndoa", "Bebida de aveia", "Bebida de soja", "Bebida de arroz", "Pão sírio",
    "Tortilha", "Wrap de frango", "Wrap de atum", "Wrap vegetariano", "Hambúrguer", "Cachorro-quente", "Salsicha",
    "Mussarela", "Requeijão", "Cream cheese", "Queijo cheddar", "Queijo brie", "Queijo camembert", "Queijo provolone",
    "Sopa em pó", "Caldo em pó", "Mistura para molho", "Mistura para tempero", "Mistura para arroz", "Mistura para feijão",
    "Mistura para salada", "Mistura para legumes", "Mistura para carnes", "Mistura para grelhados", "Mistura para sopas",
    "Mistura para tortas", "Mistura para frituras", "Mistura para pães", "Mistura para pizzas", "Mistura para bolos",
    "Mistura para panquecas", "Mistura para sobremesas", "Mistura para drinks", "Mistura para coquetéis", "Mistura para batidas",
    "Mistura para lanches", "Mistura para petiscos", "Mistura para saladas", "Mistura para acompanhamentos", "Mistura para sobremesas",
    "Biscoito de maizena", "Biscoito de chocolate branco", "Biscoito de castanha", "Biscoito de amendoim", "Biscoito de aveia",
    "Biscoito de limão", "Biscoito de baunilha", "Biscoito de canela", "Biscoito de mel", "Biscoito de frutas", "Biscoito de iogurte",
    "Biscoito de coco", "Biscoito de cacau", "Biscoito de castanha-do-pará", "Biscoito de queijo", "Biscoito de chocolate amargo",
    "Biscoito de frutas secas", "Biscoito de chia", "Biscoito de linhaça", "Biscoito de goiabada", "Biscoito de maçã",
    "Biscoito de cenoura", "Biscoito de abóbora", "Biscoito de pimenta", "Biscoito de erva-doce", "Biscoito de açafrão",
    "Biscoito de curry", "Biscoito de tomate seco", "Biscoito de azeitona", "Biscoito de semente de girassol", "Biscoito de quinoa",
    "Biscoito de amêndoa", "Biscoito de nozes", "Biscoito de amendoim", "Biscoito de pistache", "Biscoito de castanha de caju",
    "Biscoito de castanha de baru", "Biscoito de castanha do Brasil", "Biscoito de nozes pecan", "Biscoito de semente de abóbora",
    "Biscoito de semente de linhaça", "Biscoito de semente de chia", "Biscoito de semente de gergelim", "Biscoito de semente de melancia",
    "Biscoito de semente de girassol", "Biscoito de semente de pinhão", "Biscoito de semente de cânhamo", "Biscoito de semente de quinoa",
    "Biscoito de semente de chia", "Biscoito de semente de linhaça", "Biscoito de semente de abóbora", "Biscoito de semente de gergelim",
    "Biscoito de semente de melancia", "Biscoito de semente de girassol", "Biscoito de semente de pinhão", "Biscoito de semente de cânhamo",
    "Biscoito de semente de quinoa", "Biscoito de semente de chia", "Biscoito de semente de linhaça", "Biscoito de semente de abóbora",
    "Biscoito de semente de gergelim", "Biscoito de semente de melancia", "Biscoito de semente de girassol", "Biscoito de semente de pinhão",
    "Biscoito de semente de cânhamo", "Biscoito de semente de quinoa", "Biscoito de semente de chia", "Biscoito de semente de linhaça",
    "Biscoito de semente de abóbora", "Biscoito de semente de gergelim", "Biscoito de semente de melancia", "Biscoito de semente de girassol",
    "Biscoito de semente de pinhão", "Biscoito de semente de cânhamo", "Biscoito de semente de quinoa", "Biscoito de semente de chia",
    "Biscoito de semente de linhaça", "Biscoito de semente de abóbora", "Biscoito de semente de gergelim", "Biscoito de semente de melancia",
    "Biscoito de semente de girassol", "Biscoito de semente de pinhão", "Biscoito de semente de cânhamo", "Biscoito de semente de quinoa",
]
    x=0
    for i in marcas:
        marc = mm(nome=i)
        marc.save()
        print(x)
        x=x+1
    print("terminou")
    return render(request, "db/terminal.html", {})