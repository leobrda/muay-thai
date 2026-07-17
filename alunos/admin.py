from django.contrib import admin
from .models import Aluno


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'professor', 'telefone', 'dia_vencimento', 'valor_mensalidade', 'ultimo_pagamento')
    list_filter = ('professor', 'ultimo_pagamento')
    search_fields = ('nome', 'telefone')