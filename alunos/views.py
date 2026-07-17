from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Aluno
from .forms import AlunoForm
from datetime import date


def cadastro_professor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz o login automático após cadastrar
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'alunos/cadastro.html', {'form': form})


from django.db.models import Sum


@login_required
def dashboard(request):
    meus_alunos = request.user.alunos.all()

    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    busca = request.GET.get('search')
    if busca:
        meus_alunos = meus_alunos.filter(nome__icontains=busca)

    for aluno in meus_alunos:
        aluno.pago_este_mes = (
                aluno.ultimo_pagamento is not None and
                aluno.ultimo_pagamento.month == mes_atual and
                aluno.ultimo_pagamento.year == ano_atual
        )

    # Cálculos baseados na checagem do mês atual
    total_recebido = 0
    total_a_receber = 0
    for aluno in request.user.alunos.all():
        pago = (aluno.ultimo_pagamento is not None and
                aluno.ultimo_pagamento.month == mes_atual and
                aluno.ultimo_pagamento.year == ano_atual)
        if pago:
            total_recebido += aluno.valor_mensalidade
        else:
            total_a_receber += aluno.valor_mensalidade

    turmas_agrupadas = []
    for codigo, nome_turma in Aluno.TURMAS_CHOICES:
        alunos_da_turma = [a for a in meus_alunos if a.turma == codigo]
        if alunos_da_turma:
            turmas_agrupadas.append({
                'nome': nome_turma,
                'alunos': alunos_da_turma
            })

    context = {
        'turmas_agrupadas': turmas_agrupadas,
        'total_recebido': total_recebido,
        'total_a_receber': total_a_receber,
        'busca': busca,
        'tem_alunos': request.user.alunos.exists()
    }
    return render(request, 'alunos/dashboard.html', context)

@login_required
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.professor = request.user
            aluno.save()
            return redirect('dashboard')
    else:
        form = AlunoForm

    return render(request, 'alunos/aluno_form.html', {'form': form})


@login_required
def alternar_pagamento(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, professor=request.user)
    hoje = date.today()

    # Verifica se ele já tinha pago este mês
    ja_pago_este_mes = (
            aluno.ultimo_pagamento is not None and
            aluno.ultimo_pagamento.month == hoje.month and
            aluno.ultimo_pagamento.year == hoje.year
    )

    if ja_pago_este_mes:
        # Se já estava pago e o professor clicou, cancela o pagamento (limpa a data)
        aluno.ultimo_pagamento = None
    else:
        # Se estava devendo, grava a data de hoje como último pagamento
        aluno.ultimo_pagamento = hoje

    aluno.save()
    return redirect('dashboard')


