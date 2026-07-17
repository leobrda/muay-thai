from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    TURMAS_CHOICES = [
        # Turmas de Seg, Qua, Sex (R$ 120)
        ('MWF_17', 'Seg/Qua/Sex - 17:00 às 18:00 (R$ 120)'),
        ('MWF_18', 'Seg/Qua/Sex - 18:00 às 19:00 (R$ 120)'),
        ('MWF_19', 'Seg/Qua/Sex - 19:00 às 20:00 (R$ 120)'),
        ('MWF_20', 'Seg/Qua/Sex - 20:00 às 21:00 (R$ 120)'),

        # Turmas de Ter e Qui (R$ 100)
        ('TR_19', 'Ter/Qui - 19:00 às 20:00 (R$ 100)'),
        ('TR_20', 'Ter/Qui - 20:00 às 21:00 (R$ 100)'),
    ]

    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alunos')
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    turma = models.CharField(max_length=10, choices=TURMAS_CHOICES, default='MWF_19')
    foto = models.ImageField(upload_to='alunos_fotos/', blank=True, null=True)
    valor_mensalidade = models.DecimalField(max_digits=6, decimal_places=2)
    # Dia do mês combinado para o pagamento (Ex: todo dia 10)
    dia_vencimento = models.IntegerField()
    # Indica se o aluno já pagou a mensalidade do mês atual
    ultimo_pagamento = models.DateField(blank=True, null=True)
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome