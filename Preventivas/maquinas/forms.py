from django import forms
from .models import UltimaPreventiva, Pecas, Patrimonio

class PrevForm(forms.ModelForm):
    pecas = forms.ModelMultipleChoiceField(queryset=Pecas.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = UltimaPreventiva
        fields = ['frota', 'horimetro', 'modelo','HoradePreventiva','OS', 'pecas' ]
        labels = {'frota': 'Número de frota',
                  'horimetro': 'Horimetro de máquina',
                  'modelo': 'Modelo de máquina',
                  'HoradePreventiva': 'Preventiva de quantas horas',
                  'OS': 'Ordem de serviço',
                  'pecas': 'Peças usadas'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pecas'].queryset = Pecas.objects.all()
        
class CompForm(forms.ModelForm):
    frota = forms.IntegerField(label='Número de frota')
    horimetro = forms.IntegerField(label='Horimetro de máquina')
    class Meta:
        model = Patrimonio
        fields = ['frota', 'horimetro']
        label = {'frota', 'Número de frota',
                 'horimetro', 'Horimetro de máquina'}

