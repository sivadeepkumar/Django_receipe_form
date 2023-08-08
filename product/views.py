from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test


@login_required(login_url='/login/')
def product(request):
    return render(request,'product.html')

def user_not_authenticated(user):
    return not user.is_authenticated


@user_passes_test(user_not_authenticated, login_url='home')
def login_page(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username = user_name).exists():
           messages.warning(request,"Invalid Username")
           return redirect('/login/')
        
        user_and_password_is_matched = authenticate(username = user_name,password =  password)
        # if user.exists():
        print(user_and_password_is_matched)
        if user_and_password_is_matched is None:
            messages.warning(request,"Password In-valid")
            return redirect('/login/')
        else:
            login(request,user_and_password_is_matched)
            return redirect('/')
            

    return render(request,'login.html')

@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return redirect('/login/')

 
def register(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        is_user_available = User.objects.filter(username=user_name)
        if is_user_available.exists():
            messages.error(request, "Please Try with Different Username. Bcz it was already Taken")
            return redirect('/register/')
        user = User.objects.create(username=user_name,first_name=first_name,last_name=last_name)  
        user.set_password(password)
        user.save()
        messages.success(request, "User Created Successfully")
        print(user_name,password,first_name,last_name)
        return redirect('/login/')

    return render(request,'register.html')

