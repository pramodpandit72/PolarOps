from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


def index(request):
    """Landing page — authenticated users go to dashboard."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'landing.html')


def signup(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to PolarOps, {user.username}!')
            return redirect('core:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


from operations.views import dashboard_view as dashboard

