from django.contrib.auth import authenticate,login
from django.urls import path
from django.contrib import messages
from xpenseapp.forms import LoginForm, RegisterForm
from . import views
from django.shortcuts import redirect, render

def login_view(request):
    context={}
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,'username or password is incorrect')
            form = LoginForm()
            context = {'form':form}
    else:
        form = LoginForm()
        context = {'form':form}
    return render(request, 'auth/login.html',context)

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')
        # else:
        #     print(form.errors)
        #     form = RegisterForm()

    context = {'form':form}

    return render(request,'auth/register.html',context)

def dashboard(request):
    return render(request,'dashboard.html')
