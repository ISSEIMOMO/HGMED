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
    import random
    from dbbase.models import Funcionario as fn
    from dbbase.models import Cargo as cg
    from dbbase.models import Departamento as dp
    from dbbase.models import VProduto as vp
    from dbbase.models import Venda as vde
    """from dbbase.models import VProduto as mm
    from dbbase.models import Marca as ma
    from dbbase.models import TipoProduto as tp
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
    primeiros_nomes = [
        "Ana", "Bruno", "Carlos", "Daniel", "Elena", "Fernando", "Gabriela", "Hugo",
        "Isabela", "João", "Karina", "Lucas", "Mariana", "Nicolas", "Olivia", "Paulo",
        "Quiteria", "Rafael", "Sofia", "Tiago", "Vanessa", "Walter", "Yasmin", "Zoe"
    ]

    sobrenomes = [
        "Almeida", "Barbosa", "Costa", "Dias", "Fernandes", "Gomes", "Henrique",
        "Lima", "Melo", "Oliveira", "Pereira", "Queiroz", "Ramos", "Santos",
        "Silva", "Souza", "Teixeira", "Valente", "Xavier", "Zanetti"
    ]
    enderecos = [
        "Rua das Flores, 123, Centro, São Paulo, SP",
        "Avenida Brasil, 987, Vila Mariana, Rio de Janeiro, RJ",
        "Rua Oliveira, 456, Jardim das Acácias, Belo Horizonte, MG",
        "Travessa dos Pássaros, 32, Boa Vista, Recife, PE",
        "Praça da Liberdade, 1020, Centro, Salvador, BA",
        "Rua São João, 55, Tijuca, Rio de Janeiro, RJ",
        "Avenida Paulista, 1500, Bela Vista, São Paulo, SP",
        "Alameda Santos, 800, Jardim Paulista, São Paulo, SP",
        "Rua dos Pioneiros, 321, Cidade Nova, Curitiba, PR",
        "Rua Castro Alves, 18, Centro, Florianópolis, SC",
        "Rua XV de Novembro, 200, Centro Histórico, Porto Alegre, RS",
        "Avenida Sete de Setembro, 445, Comércio, Salvador, BA",
        "Rua Santos Dumont, 1234, Boa Viagem, Recife, PE",
        "Rua Amazonas, 678, Eldorado, Contagem, MG",
        "Rua dos Jacarandás, 890, Parque Verde, Goiânia, GO",
        "Avenida Independência, 543, Vila Progresso, Fortaleza, CE",
        "Rua da Paz, 78, Vila Nova, Brasília, DF",
        "Rua Coronel Faria, 12, Alto da Glória, Curitiba, PR",
        "Avenida Rio Branco, 999, Centro, Rio de Janeiro, RJ",
        "Rua da Aurora, 567, Boa Vista, Recife, PE",
        "Rua Pedro Álvares Cabral, 23, Cidade Baixa, Porto Alegre, RS",
        "Avenida das Nações, 654, Jardim América, São Paulo, SP",
        "Rua Professor Antônio, 120, Cidade Universitária, Campinas, SP",
        "Rua Dr. Pedroso, 44, Centro, São José dos Campos, SP",
        "Rua Visconde de Mauá, 89, Centro, Santos, SP",
        "Avenida Governador, 333, Centro, São Luís, MA",
        "Rua da Liberdade, 22, Liberdade, São Paulo, SP",
        "Rua Esperança, 400, Jardim Europa, São Paulo, SP",
        "Rua Vitória, 99, Alto do Ipiranga, Belo Horizonte, MG",
        "Rua Paraná, 13, Vila Velha, Vitória, ES",
        "Avenida Ceará, 202, Estação, Porto Velho, RO",
        "Rua Marechal Deodoro, 9, Centro, Maceió, AL",
        "Avenida Ipiranga, 251, Bela Vista, São Paulo, SP",
        "Rua Pedro de Toledo, 415, Paraíso, São Paulo, SP",
        "Rua Aurora, 101, Barra Funda, São Paulo, SP",
        "Avenida Sapopemba, 777, Jardim Santa Clara, São Paulo, SP",
        "Rua da Saudade, 300, Cambuí, Campinas, SP",
        "Rua Carijós, 89, Eldorado, Contagem, MG",
        "Rua Estrela Dalva, 75, Planalto, Belo Horizonte, MG",
        "Avenida João Dias, 987, Santo Amaro, São Paulo, SP",
        "Rua Amazonas, 135, Vila Leopoldina, São Paulo, SP",
        "Rua Francisco Sá, 65, Santa Efigênia, Belo Horizonte, MG",
        "Avenida Dr. Enéas, 43, Jardim Europa, São Paulo, SP",
        "Rua dos Inconfidentes, 987, Lourdes, Belo Horizonte, MG",
        "Rua das Palmeiras, 222, Flamengo, Rio de Janeiro, RJ",
        "Rua dos Guararapes, 13, Boa Viagem, Recife, PE",
        "Avenida Santos Dumont, 765, Aeroporto, Fortaleza, CE",
        "Rua do Comércio, 50, Centro, Florianópolis, SC",
        "Rua Dom Pedro I, 890, Alto da Mooca, São Paulo, SP",
        "Rua México, 45, Vila Buarque, São Paulo, SP",
        "Rua Bandeirantes, 123, Jardim América, Curitiba, PR",
        "Avenida Presidente Vargas, 1001, Centro, Rio de Janeiro, RJ",
        "Rua dos Limoeiros, 65, Vila Clementino, São Paulo, SP",
        "Rua Ceará, 456, Santa Tereza, Belo Horizonte, MG",
        "Rua Senador Dantas, 17, Centro, Rio de Janeiro, RJ",
        "Rua do Sol, 234, Centro, São Luís, MA",
        "Rua Álvaro Alvim, 320, Flamengo, Rio de Janeiro, RJ",
        "Avenida Dom Pedro II, 789, Nova Petrópolis, São Paulo, SP",
        "Rua Professor Moraes, 911, Savassi, Belo Horizonte, MG",
        "Rua dos Patriotas, 555, Ipiranga, São Paulo, SP",
        "Avenida do Estado, 44, Cambuci, São Paulo, SP",
        "Rua Lauro Müller, 23, Praia de Iracema, Fortaleza, CE",
        "Rua República do Líbano, 50, Centro, Brasília, DF",
        "Rua Tupiniquins, 12, Pinheiros, São Paulo, SP",
        "Rua Campos Sales, 800, Vila Romana, São Paulo, SP"
    ]
    from django.utils import timezone
    vp = list(vp.objects.values_list('codpro', flat=True))
    caixa = cg.objects.filter(nome="CAIXA").first()  # Obtém o primeiro objeto correspondente
    fn = list(fn.objects.filter(codcarg=caixa).values_list('codf', flat=True))  # Filtra por este objeto e pega os `codf`
    print(fn)
    x=0
    while x<10000:
        numpd=random.randint(1, 100)
        data_gerada = f'{random.randint(2020, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d} {random.randint(7, 18):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}'

        # Converter a string para um objeto datetime e adicionar o fuso horário
        data_com_fuso = timezone.make_aware(timezone.datetime.strptime(data_gerada, '%Y-%m-%d %H:%M:%S'))

        vende=random.choice(fn)
        for i in range(1,numpd):
            videl = vde(codf_id=vende,codpro_id=random.choice(vp),data_hora=data_com_fuso)
            videl.save()
            x=x+1
        print(x)
    """
    x=0
    for i in range(0,len(nomes)-1):
        dia=random.randint(1, 28)
        funcionario = fn(
            username=f'{nomes[i][0]}_{nomes[i][1]}',
            first_name=nomes[i][0],
            last_name=nomes[i][1],
            email=f'{nomes[i][0]}{nomes[i][1]}@gmail.com',
            cpf=cpf[i],
            data_nasc=f'{random.randint(2024-50, 2024-18)}-{random.randint(1, 12)}-{dia}',
            telefone=tele[i],
            endereco=random.choice(enderecos),
            salario=round(random.uniform(200.00, 500.00), 2),
            tipo=random.choice(['Contrato', 'Efetivo']),
            data_entrada=f'{random.randint(2024-30, 2024)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
            codcarg_id=random.choice(cg),
            coddep_id=random.choice(dp),

        )
        funcionario.set_password(f"{str(tele[i])[-4:]}{dia}{str(cpf[i])[:3]}")  # Use set_password para criptografar a senha
        funcionario.save()
        print(x)
        x=x+1"""
    print("terminou")
    return render(request, "db/terminal.html", {})