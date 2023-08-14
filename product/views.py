from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from myproject.forms import CreateUserForm,LoginForm



from django.contrib.sites.shortcuts import get_current_site
from myproject.token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
import pdb


@login_required(login_url='/login/')
def product(request):
    return render(request,'product.html')

def user_not_authenticated(user):
    return not user.is_authenticated



@user_passes_test(user_not_authenticated, login_url='home')
def login_page(request):
    
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request,data = request.POST)
    
        if form.is_valid():

            user_name = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request,username = user_name , password=password)
            
            
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.warning(request, "Invalid Username or Password")
          
    context = {'form':form}  
    return render(request, 'login.html',context)






@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return redirect('/login/')

 
def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            user.is_active = False

            user.save()

            # Email verification setup (template)
            
            current_site = get_current_site(request)
            subject = 'Account verification email'

            message = render_to_string('accounts/email-verification.html',{
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : user_tokenizer_generate.make_token(user),
            })

             # Sending message to email        
            
            user.email_user(subject = subject,message = message)
            return redirect('/login')
        
    
    context = {'form':form}

    return render(request,'accounts/register.html',context)
    # if request.method == "POST":
    #     user_name = request.POST.get('username')
    #     first_name = request.POST.get('first_name')
    #     last_name = request.POST.get('last_name')
    #     password = request.POST.get('password')
    #     is_user_available = User.objects.filter(username=user_name)
    #     if is_user_available.exists():
    #         messages.error(request, "Please Try with Different Username. Bcz it was already Taken")
    #         return redirect('/register/')
    #     user = User.objects.create(username=user_name,first_name=first_name,last_name=last_name)  
    #     user.set_password(password)
    #     user.save()
    #     messages.success(request, "User Created Successfully")
    #     print(user_name,password,first_name,last_name)
    #     return redirect('/login/')




def email_verification(request,uidb64,token):
    #unique id
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Success when to user clicked on link 
    if user and user_tokenizer_generate.check_token(user,token):
        user.is_active = True 
        user.save()
        return redirect('/login/')
    
    # Failed
    else:
        return redirect('/email-verification-fail/')



def email_verification_fail(request):
    return render(request,'accounts/email-verification-fail.html')