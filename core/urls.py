from django.contrib import admin
from django.urls import path, include  # Não esqueça de importar o 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('alunos.urls')),  # Isso liga o seu app à página inicial do site
]