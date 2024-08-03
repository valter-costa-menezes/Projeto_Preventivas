from django.shortcuts import render
from .models import UltimaPreventiva, Patrimonio
from .forms import PrevForm, CompForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# página principal do projeto
def index(request):
    maq = UltimaPreventiva.objects.all()
    context = {'maquinas': maq}
    return render(request, 'maquinas/index.html', context)

# formulário para adicionar novas preventivas
def nova_prev(request):
    if request.method != 'POST':
        form = PrevForm()
    else:
        form = PrevForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('addPrev'))
        
    context = {'form': form}
    return render(request, 'maquinas/addPrev.html', context)    



# formulário de comparação de horim
def CompPrev(request):
    
    mensagem_info = None
    mensagem_prev = None
    if request.method != 'POST':
        form = CompForm()
    else: 
        form = CompForm(request.POST)
        if form.is_valid():

            numero = form.cleaned_data['frota']
            horimetro = form.cleaned_data['horimetro']
            
            # salva o ultimo horimetro
            request.session['ultimo_horimetro'] = horimetro
            
            try:
                ultima_preventiva = UltimaPreventiva.objects.get(frota=numero)
                proxima_preventiva = ultima_preventiva.proximaPrev
                
                if horimetro >= proxima_preventiva:
                    mensagem_prev = 'É necessário fazer a manutenção preventiva'
                else:
                    diferenca_preventiva = proxima_preventiva - horimetro
                    mensagem_info = f'Não é necessário a manutenção preventiva faltam:{diferenca_preventiva}'
            except UltimaPreventiva.DoesNotExist:
                mensagem_prev = 'Número de máquina não encontrado no banco de dados por favo cadastre'               

            form.save()

    context = {'form': form, 'mensagem_prev': mensagem_prev, 'mensagem_info': mensagem_info}
    return render(request, 'maquinas/CompPrev.html', context)

def pecas(request, pecas_id):

    Id_pecas = UltimaPreventiva.objects.get(id = pecas_id) 
    pecas_usadas = Id_pecas.pecas.all()
    prox_prev = Id_pecas.proximaPrev

    try:
        ultimo_lance = Patrimonio.objects.filter(frota = Id_pecas.frota).latest('id')
        ultimo_horimetro = ultimo_lance.horimetro
    except Patrimonio.DoesNotExist:
        ultimo_horimetro = None

    context = {'Id_pecas': Id_pecas, 'pecas_usadas': pecas_usadas, 'ultimo_horimetro': ultimo_horimetro, 'prox_prev': prox_prev}

    return render(request, 'maquinas/pecas.html', context)

def pendentes(request):
    ultimo_horimetro = request.session.get('ultimo_horimetro', None)
    maq_manutencao = []
    
    maquinas = UltimaPreventiva.objects.all()
    for maquina in maquinas:
        try:
            ultimo_horimetro = Patrimonio.objects.filter(frota=maquina.frota).latest('id').horimetro
            if ultimo_horimetro >= maquina.proximaPrev:
                maq_manutencao.append({'maquina': maquina, 'ultimo_horimetro': ultimo_horimetro})
        except Patrimonio.DoesNotExist:
            continue
    
    context = {'maq_manutencao': maq_manutencao, 'ultimo_horimetro': ultimo_horimetro}
    return render(request, 'maquinas/pendentes.html', context)