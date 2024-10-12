from django.db import models

# Create your models here.
class Funcionario(models.Model):
    codf = models.AutoField(primary_key=True)
    codcarg = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    coddep = models.ForeignKey('Departamento', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    data_nasc = models.DateField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    email = models.EmailField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=[('Contrato', 'Contrato'), ('Efetivo', 'Efetivo')])
    data_entrada = models.DateField()
    senha = models.CharField(max_length=128)

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
    codf = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    codpro = models.ForeignKey('Produto', on_delete=models.CASCADE)
    data_hora = models.DateTimeField()

    def __str__(self):
        return str(self.codpro.codcarg.nome)

# Produtos

class TipoProduto(models.Model):
    codtpro = models.CharField(primary_key=True)
    nome = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    codpro = models.CharField(primary_key=True, max_length=100)  # Código de barras
    codcarg = models.ForeignKey('TipoProduto', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nome}-{self.codcarg.nome}"

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
    codpro = models.ForeignKey(Produto, on_delete=models.CASCADE)
    df = models.DateField()  # Data de fabricação
    dv = models.DateField()  # Data de validade
    lote = models.CharField(max_length=50)

    def __str__(self):
        return self.lote

# Desconto
class Desconto(models.Model):
    coddes = models.AutoField(primary_key=True)
    codpro = models.ForeignKey(Produto, on_delete=models.CASCADE)
    di = models.DateField()  # Data de início
    dt = models.DateField()  # Data de término

    def __str__(self):
        return str(self.codpro)

# Perdas
class Perda(models.Model):
    codper = models.AutoField(primary_key=True)
    codpro = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    dt = models.DateField()

# Estoque
class Estoque(models.Model):
    codpro = models.OneToOneField(Produto, on_delete=models.CASCADE, primary_key=True)  # Relaciona com Produto
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
