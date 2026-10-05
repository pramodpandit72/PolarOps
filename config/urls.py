from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # fallback auth paths
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', include('core.urls')),
    path('', include('operations.urls')),
]
