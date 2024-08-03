from django.db import models
from django import forms

# será lançado as novos registros para serem comparados com as ultimas preventivas

class Patrimonio(models.Model):
    frota = models.IntegerField(verbose_name='Número de frota')
    horimetro = models.IntegerField(verbose_name='Horimetro de máquina')

    def __str__(self):  
        return f"frota{self.frota} hor: {self.horimetro}"
    

# será registrado as preventiva de máquinas 

class Pecas(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class UltimaPreventiva(models.Model):

    frota = models.IntegerField(default = '', verbose_name='Número de frota')
    horimetro = models.IntegerField(default = '', verbose_name='Horimetro de máquina')
    modelo = models.CharField(default= '',max_length=100, verbose_name='Modelo de máquina')
    HoradePreventiva = models.IntegerField(default = '',verbose_name='Preventiva de quantas horas')
    OS = models.IntegerField(default = '',verbose_name='Ordem de serviço')
    pecas = models.ManyToManyField(Pecas, verbose_name='Peças usadas')

    @property
    def proximaPrev(self): 
        return self.horimetro + self.HoradePreventiva
    
    def __str__(self):
        return f"Frota: {self.frota} OS: {self.OS}"
 
