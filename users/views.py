from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
#  resseting passwprd 
from django.contrib.auth.tokens import default_token_generator

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully Created for {username} Login In Now!!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request,'users/profile.html')

@login_required
def profile_update(request):
    user = request.user
    try:
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            profile.profile_picture ='default.jpg'  # Set the default profile picture path
            profile.save()
        # profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated successful !')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'users/profile_update.html', context)

#  forgeting and reseting   password 

def generate_reset_token(user):
    return default_token_generator.make_token(user)


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

User = get_user_model()

def reset_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        password = request.POST.get('password')

        user = get_object_or_404(User, email=request.POST.get('email'))
        
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return JsonResponse({'message': 'Password reset successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid token'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
        

