from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Funcionario(AbstractUser):
    codf = models.AutoField(primary_key=True)
    codcarg = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    coddep = models.ForeignKey('Departamento', on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    data_nasc = models.DateField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=[('Contrato', 'Contrato'), ('Efetivo', 'Efetivo')])
    data_entrada = models.DateField()

    class Meta:
        verbose_name = 'Funcionario'  # Nome singular
        verbose_name_plural = 'Funcionarios'  # Nome plural




class Cliente(models.Model):
    codcli = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    senha = models.CharField(max_length=128)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    data_cas = models.DateField()  # Data e hora



# Cargo
class Cargo(models.Model):
    codcargo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Departamento
class Departamento(models.Model):
    coddep = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
# Vendas
class Venda(models.Model):
    codvend = models.AutoField(primary_key=True)
    codf = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    codcli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=False)
    data_hora = models.DateTimeField()


    def __str__(self):
        return f"{self.codf.nome} - {self.data_hora}"

class PVenda(models.Model):
    codpv = models.AutoField(primary_key=True)
    codvend = models.ForeignKey(Venda, on_delete=models.CASCADE)
    codpro = models.ForeignKey('VProduto', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codpro.codtip.nome} - {self.codpro.codmarc.nome}"

# VProdutos

class TipoProduto(models.Model):
    codtip = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Marca(models.Model):
    codtmarc = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class VProduto(models.Model):
    codpro = models.CharField(primary_key=True, max_length=100)  # Código de barras
    codtip = models.ForeignKey('TipoProduto', on_delete=models.CASCADE)
    codmarc = models.ForeignKey('Marca', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.codpro} - {self.codtip.nome} - {self.codmarc.nome}"

# Fornecedor
class Fornecedor(models.Model):
    codfor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    ende = models.CharField(max_length=255)
    vpc = models.DecimalField(max_digits=10, decimal_places=2)  # Valor por carregamento
    ve = models.DecimalField(max_digits=10, decimal_places=2)   # Valor de entrega

    def __str__(self):
        return self.nome

# Carregamentos
class Carregamento(models.Model):
    codcar = models.AutoField(primary_key=True)
    codpro = models.ForeignKey(VProduto, on_delete=models.CASCADE)
    df = models.DateField()  # Data de fabricação
    dv = models.DateField()  # Data de validade
    lote = models.CharField(max_length=50)

    def __str__(self):
        return self.lote

# Desconto
class Desconto(models.Model):
    codf = models.ForeignKey(Funcionario, on_delete=models.CASCADE, default=55)
    coddes = models.AutoField(primary_key=True)
    codpro = models.ForeignKey(VProduto, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    di = models.DateField()  # Data de início
    dt = models.DateField()  # Data de término

    def __str__(self):
        return str(self.codpro)

# Perdas
class Perda(models.Model):
    codper = models.AutoField(primary_key=True)
    codpro = models.ForeignKey(VProduto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    dt = models.DateField()

# Estoque
class Estoque(models.Model):
    codpro = models.OneToOneField(VProduto, on_delete=models.CASCADE, primary_key=True)  # Relaciona com VProduto
    quantidade = models.PositiveIntegerField()

# Despesas
class Despesa(models.Model):
    coddesp = models.AutoField(primary_key=True)
    desp = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

# Atividade (ATV)
class Atividade(models.Model):
    codatv = models.AutoField(primary_key=True)
    codf_gerente = models.ForeignKey(Funcionario, related_name='gerente', on_delete=models.CASCADE)
    codf_funcionario = models.ForeignKey(Funcionario, related_name='funcionario', on_delete=models.CASCADE)
    tarefa = models.CharField(max_length=255)
    dia = models.DateField()

# Ponto
class Ponto(models.Model):
    codponto = models.AutoField(primary_key=True)
    codf = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    diah = models.DateTimeField()  # Data e hora