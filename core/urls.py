from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('alunos.urls')),  # Isso liga o seu app à página inicial do site
]

try:
    # Digite aqui o username que você acabou de criar no site
    user = User.objects.get(username='leobrda')
    if not user.is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save()
except Exception:
    pass