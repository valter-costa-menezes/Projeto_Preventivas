# FAZ IMPORAÇÕES NECESSÁRIAS PARA FUNCIONAR A LOGICA DO APP

from django.shortcuts import render
from .models import UltimaPreventiva, Patrimonio
from .forms import PrevForm, CompForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# FUNÇÃO QUE CRIA A PÁGINA INICAIAL
def index(request):
    # VARIAVEL QUE PEGA TODOS OS OBJETOS DENTRO DA MODELS UltimaPreventiva
    maq = UltimaPreventiva.objects.all()
    
    # CRIA UM DICIONÁRIO QUE DEFINE O VALOR DE maquinas PARA maq
    context = {'maquinas': maq}

    # RENDERIZA A PÁGINA DIRECIONANDO ELA PARA O CAMINHO maquinas/index.html E PASSA PARA O INDEX O CONTEXT PARA SER USADO NO INDEX
    return render(request, 'maquinas/index.html', context)



# CRIA A LÓGICA POR TRAS DO FORMULÁRIO DE CRIAÇÃO DE NOVAS PREVENITVAS
def nova_prev(request):
    # SE O METODO PASSA PARA O FORMULÁRIO FOR DIFERENTE DE POST ELE CARREGA A PAGINA NOVAMENTE COM UM FORMULÁRIO VAZIO.
    if request.method != 'POST':
        form = PrevForm()
    else:
        # SE O METODO FOR IGUAL A POST ENTÃO ELE PEGA AS INFORMÇÕES DO FORMULÁRIO VALIDA E SALVA
        form = PrevForm(request.POST)
        if form.is_valid():
            form.save()

            # QUANDO AS INFORMAÇÕES FOREM VÁLIDADAS ELE REDIRECIONA PARA A MESMA PÁGINA EM BRANCO 
            return HttpResponseRedirect(reverse('addPrev'))
    
    # CRIA UM DICIONÁRIO DEFININDO O VALOR DA CHAVE form PARA form
    context = {'form': form}

    # RENDERIZA A PÁGINA DIRECIONANDO PARA O CAMINHO maquinas/addPrev.html E PASSA O CONTEXT PARA SER USADO NO addPrev.html 
    return render(request, 'maquinas/addPrev.html', context)    



# LÓGICA PARA A COMPARAÇÃO DE HORIMETROS
def CompPrev(request):
    # CRIA VARIAVEIS NULAS QUE SERAM USADAS PARA PASSAR MENSAGENS AO USUÁRIO
    mensagem_info = None
    mensagem_prev = None

    # SE O METODO PASSADO PELO FORMULÁRIO FOR DIFERENTE DE POST RETORNA A PÁGINA COM UM FORMULÁRIO VAZIO
    if request.method != 'POST':
        form = CompForm()
    else: 

        # SE O METODO FOR IGUAL A POST ENTÃO ELE PEGA AS INFORMÇÕES DO FORMULÁRIO VALIDA
        form = CompForm(request.POST)
        if form.is_valid():

        # VALIDA SE AS INFORMAÇÕES PASSADAS NOS CAMPOS DO FORMULÁRIO SÃO VALIDAS E "LIMPAS"
            numero = form.cleaned_data['frota']
            horimetro = form.cleaned_data['horimetro']
            
            # salva o ultimo horimetro
            request.session['ultimo_horimetro'] = horimetro


            # TENTA PEGAR UM REGISTRO DE ULTIMA PREVENTIVA NA MÁQUINA
            try:
                ultima_preventiva = UltimaPreventiva.objects.get(frota=numero)
                proxima_preventiva = ultima_preventiva.proximaPrev
                
                # SE O HORIMETRO ATUAL INFORMADO FOR MAIOR OU IGUAL AO HORIMETRO REGISTRADO EM proxima_preventiva EXIBE MENSAGEM DE PREVENTIVA
                if horimetro >= proxima_preventiva:
                    mensagem_prev = 'É necessário fazer a manutenção preventiva'

                else:
                    #  CASO O HORIMETRO FOR MENOR FAZ O CALCULO DE QUANTAS HORAS FALTAM ATÉ A PROXIMA PREVENTIVA E EXIBE A MENSAGEM DE INFORMAÇÃO
                    diferenca_preventiva = proxima_preventiva - horimetro
                    mensagem_info = f'Não é necessário a manutenção preventiva faltam:{diferenca_preventiva}'

            #  CASO O NUMERO DA MÁQUINA NÃO EXISTIR NO REGISTRO, EXIBE MENSAGEM DE PREVENTIVA INFORMANDO QUE NÃO HÁ REGISTRO.
            except UltimaPreventiva.DoesNotExist:
                mensagem_prev = 'Número de máquina não encontrado no banco de dados por favo cadastre'               

            # SALVA OS DADOS DO FORMULÁRIO.
            form.save()

    # CRIA UM DICIONÁRIO PASSANDO OS VALORES DE form, mensagem_prev e mensagem_info
    context = {'form': form, 'mensagem_prev': mensagem_prev, 'mensagem_info': mensagem_info}

    # RENDERIZA A PÁGINA DIRECIONANDO PARA O CAMINHO maquinas/CompPrev.html E PASSA O CONTEXT PARA SER USADO NO CompPrev.html
    return render(request, 'maquinas/CompPrev.html', context)



# LÓGICA PARA A PÁGINA QUE EXIBE AS PEÇAS USADAS NA PREVENTIVA DA MÁQUINA.
def pecas(request, pecas_id):

    # PROCURA NO REGISTRO UltimaPreventiva ATRAVES Do metodo get() ALGO ESPECIFICO 
    Id_pecas = UltimaPreventiva.objects.get(id = pecas_id) 

    # PEGA TODOS OS OBJETOS DENTRO DE Id_pecas 
    pecas_usadas = Id_pecas.pecas.all()

    # PEGA O VALOR DO CAMPO proximaPrev dentro de Id_pecas
    prox_prev = Id_pecas.proximaPrev


    # TENTA FILTRAR O MAIS RECENTE frota QUE CORRESPONDE TAMBÉM AO Id_pecas
    try:
        ultimo_lance = Patrimonio.objects.filter(frota = Id_pecas.frota).latest('id')
        ultimo_horimetro = ultimo_lance.horimetro

    # CASO NÃO EXISTA UM ULTIMO HORIMETRO INFORMADO RETORNA NONE
    except Patrimonio.DoesNotExist:
        ultimo_horimetro = None

    # CRIA UM DICIONARIO QUE PASSA OS VALORES DE Id_pecas, pecas_usadas, ultimo_horimetro, prox_prev
    context = {'Id_pecas': Id_pecas, 'pecas_usadas': pecas_usadas, 'ultimo_horimetro': ultimo_horimetro, 'prox_prev': prox_prev}


    # RENDERIZA A PAGINA COM O CAMINHO maquinas/pecas.html E PASSA O CONTEXT PARA SER USADO NO pecas.html.
    return render(request, 'maquinas/pecas.html', context)



# LÓGICA PARA PAGINA DE PREVENTIVAS PENDENTES
def pendentes(request):

    # PEGA OS VALORES DE ultimo_horimetro DA session SE NÃO HOUVER DEFINE O VALOR COMO None
    ultimo_horimetro = request.session.get('ultimo_horimetro', None)

    # CRIA UMA LISTA VAZIA QUE SERAM ARMAZENADAS AS MÁQUINAS QUE PRECISAM DE PREVENTIVA
    maq_manutencao = []
    
    # CRIA UMA VARIAVEL QUE PEGA TODOS OS OBJETOS DENTRO DE Ultimapreventiva
    maquinas = UltimaPreventiva.objects.all()

    # PARA QUALQUER ITEM DENTRO DE maquinas
    for maquina in maquinas:

        # TENTA PEGAR O REGISTRO MAIS RECENTE DE Patrimonio QUE CORRESPONDE A FROTA
        try:
            ultimo_horimetro = Patrimonio.objects.filter(frota=maquina.frota).latest('id').horimetro

            # SE O ultimo_horimetro FOR IGUAL O MAIOR QUE A proximaPrev ENÃO É ADICIONADO DENTRO DA LISTA VAZIA 
            if ultimo_horimetro >= maquina.proximaPrev:
                maq_manutencao.append({'maquina': maquina, 'ultimo_horimetro': ultimo_horimetro})
        
        # CASO NÃO HAJA REGISTRO DENTRO DE Patrimonio ENTÃO CONTINUA PARA A PROXIMA MÁQUINA
        except Patrimonio.DoesNotExist:
            continue
    
    # CRIA UM DICIONARIO COM VALORES DE maq_manutencao, ultimo_horimetro 
    context = {'maq_manutencao': maq_manutencao, 'ultimo_horimetro': ultimo_horimetro}

    # RENDERIZA A PÁGINA PARA O CAMINHO maquinas/pendentes.html E O ADICIONA O CONTEXT PARA SER USADO NO pendentes.hrml
    return render(request, 'maquinas/pendentes.html', context)