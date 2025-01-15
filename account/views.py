from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User
from django.urls import reverse
from .forms import UserForm,PasswordResetEmail
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .utils import send_activiton_email,send_reset_email
from django.contrib.auth import authenticate,login , logout
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'account/home.html', )


def registration(request):
    if request.method == 'POST':
        fm = UserForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit = False)
            user.set_password(fm.cleaned_data['password'])
            user.is_active = False
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activition_link = reverse('activate',kwargs={'uidb64': uidb64, 'token': token})
            activition_url = f'{settings.SITE_DOMAIN}{activition_link}'
            send_activiton_email(user.email, activition_url)
            messages.success(request, 'Registration successful')
            return redirect('login')
    else:
        fm = UserForm()
    return render(request, 'account/registration.html',{'form' : fm} )
# Replace with your actual User model path

def activision_check(request, uidb64, token):
    try:
        # Decode the user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # Check if the user is already active
        if user.is_active:
            messages.warning(request, 'Your account is already activated.')
            return redirect('login')
        
        # Validate the token
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid activation link.')
            return redirect('signup')  # Redirect to a relevant page like signup or home
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid activation link.')
        return redirect('signup')  # Redirect to a relevant page like signup or home

  # Replace `account.models` with your app name

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if user is already logged in

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "All fields are required!")
            return render(request, 'account/login.html')  # Re-render form

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")
            return render(request, 'account/login.html')

        if not user.is_active:
            messages.error(request, "Your account is not active! Please check your email for the activation link.")
            return render(request, 'account/login.html')

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password!")

    return render(request, 'account/login.html')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been updated successfully!')
            logout(request)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/password_change.html', {'form': form})
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('home') 
    
    
    
     # Redirect to a page where you want to redirect after logout.
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetEmail(request.POST)
        if form.is_valid():
            email = request.POST['email']
            user = User.objects.get(email=email)
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                password_reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                password_reset_url = f'{settings.SITE_DOMAIN}{password_reset_link}'
                send_reset_email(user.email, password_reset_url)
                messages.success(request, 'We have sent a password reset link to your email address.')
                return redirect('login')
        
       
    else:
        form = PasswordResetEmail()
    return render(request, 'account/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # Check if the user exists
        if not user:
            messages.error(request, 'User does not exist.')
            return redirect('home')
        
        # Validate the token
        if not default_token_generator.check_token(user, token):
            messages.error(request, 'Invalid password reset link.')
            return redirect('home')
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid password reset link.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
            form = SetPasswordForm(user) 

    return render(request, 'account/password_reset_confirm.html',{'form': form})  
    