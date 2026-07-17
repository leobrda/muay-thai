from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_professor, name='cadastro_professor'),
    path('login/', auth_views.LoginView.as_view(template_name='alunos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('aluno/novo/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('aluno/<int:aluno_id>/pagamento/', views.alternar_pagamento, name='alternar_pagamento'),
    path('', views.dashboard, name='dashboard'),

]