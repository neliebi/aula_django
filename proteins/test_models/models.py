from django.db import models
from decimal import Decimal
from datetime import datetime, date

# Create your models here.

class Temas(models.Model):
    desc_tema = models.CharField(max_length=150, null=False, verbose_name= "Nome do Tema")
    
    def __str__(self):
        return "{}".format(self.desc_tema)

class Acoes(models.Model):
    desc_acao = models.CharField(max_length=150, null=True, verbose_name= "Nome da Ação")

    def __str__(self):
        return "{}".format(self.desc_acao)

class Responsaveis(models.Model):
    nome_responsavel = models.CharField(max_length=150, blank=False, null=False, verbose_name= "Nome")
    contato_responsavel = models.EmailField(max_length=150, blank=False, null=False, verbose_name= "E-mail")

    def __str__(self):
        return "{}".format(self.nome_responsavel)
    
class Projetos(models.Model):
    acess_temas_projeto = models.ForeignKey(Temas, default=True, on_delete=models.CASCADE, verbose_name= "Nome do Tema")
    acess_acoes_projeto = models.ForeignKey(Acoes, on_delete=models.CASCADE, verbose_name= "Nome da Ação")
    acess_responsaveis_projeto = models.ForeignKey(Responsaveis, on_delete=models.CASCADE, null=True, verbose_name= "Responsável")
    desc_projeto = models.CharField(max_length=150, blank=False, null=False, verbose_name= "Nome do Projeto")
    valor_financeiro_projeto = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00), verbose_name= "Valor (Ex.: 100000)")
    data_inicio_projeto = models.DateField(auto_now_add=False, auto_now=False, blank=False, null=True, verbose_name= "Data de Inicio (Ex.: dd/mm/yyyy)")
    data_fim_projeto = models.DateField(auto_now_add=False, auto_now=False, blank=False, null=True, verbose_name= "Data de Fim (Ex.: dd/mm/yyyy)")

    def __str__(self):  
        return "{} {} {} {} {} {} {}".format(self.acess_temas_projeto, self.acess_acoes_projeto, self.acess_responsaveis_projeto, self.desc_projeto, self.valor_financeiro_projeto, self.data_inicio_projeto, self.data_fim_projeto)

class Objetivos(models.Model):
    acess_projeto_objetivo = models.ForeignKey(Projetos, on_delete=models.CASCADE, null=True, verbose_name= "Projeto")
    desc_objetivo = models.CharField(max_length=350, blank=False, null=False, verbose_name=False)
    
    def __str__(self):
        return "{}".format(self.desc_objetivo,self.acess_projeto_objetivo)
    
class Tarefas(models.Model):
    acess_objetivo_tarefa = models.ForeignKey(Objetivos, on_delete=models.CASCADE, verbose_name=False)
    realizado_tarefa = models.BooleanField(default=False, verbose_name="Concluída")
    valor_financeiro_tarefa = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00), verbose_name=False)
    desc_tarefa = models.CharField(max_length=350, blank=False, null=True, verbose_name=False)

    def __str__(self):
        return "{}{}{}{}".format(self.acess_objetivo_tarefa,self.realizado_tarefa,self.valor_financeiro_tarefa,self.desc_tarefa)
    
class SubTarefas(models.Model):
    acess_tarefas = models.ForeignKey(Tarefas, on_delete=models.CASCADE)
    acess_responsaveis = models.ForeignKey(Responsaveis, on_delete=models.CASCADE)
    desc_subTarefa = models.CharField(max_length=150, blank=False, null=False, verbose_name= "Nome da SubTarefa")
    realizado_subTarefa = models.BooleanField(default=False, verbose_name= "Sub Tarefa realizada")
    data_inicio_subtarefa = models.DateField(auto_now_add=False, auto_now=False, blank=False, null=True, verbose_name= "Data de Inicio")
    data_fim_subtarefa = models.DateField(auto_now_add=False, auto_now=False, blank=False, null=True, verbose_name= "Data de Fim")
    

    def __str__(self):
        return "{}".format(self.desc_subTarefa)