from urllib import response
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from myproject.forms import CreateUserForm,LoginForm



from home.models import NoticeBoard
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
            
            user = authenticate(request,username = user_name , password = password)
            
            if user is not None:
                login(request, user)

                if hasattr(user, 'profile') and hasattr(user.profile, 'user_type'):
                    user_type = user.profile.user_type
                    request.session['user_type'] = user_type
               
                return redirect('/group/')
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
        username = request.POST.get('username')
        user_type = request.POST.get('user_type')
        user = f'{username}@{user_type}'

        print(user)
        form = CreateUserForm(request.POST)

        request.session['username'] = user
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
   



def email_verification(request,uidb64,token):
    #unique id
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Success wen to user clicked on link 
    if user and user_tokenizer_generate.check_token(user,token):
        user.is_active = True 
        user.save()
        return redirect('/group/')
    
    # Failed
    else:
        return redirect('/email-verification-fail/')



def email_verification_fail(request):
    return render(request,'accounts/email-verification-fail.html')




@login_required(login_url='/login/')
def group(request):
    user = request.user.username
    # user_type = request.user.user_type
    # print(user_type)
    print(user)
    users = User.objects.all()
    values = {'users' : users}
    return render(request,'group.html',values)
    # i need to access user.user_type here but i am getting an error
    




@login_required(login_url='/login/')
def add_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        #why i am not able to send user_type to CreateUserForm
        if form.is_valid():
            user = form.save()  # This will create and save the user
            return redirect('/group/')
    
    # ---------------------/
    return render(request, 'addUser.html')


@login_required(login_url='/login/')
def add_notice(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        notice = request.POST.get('notice')
        description = request.POST.get('description')
        remarks = request.POST.get('remarks')


        NoticeBoard.objects.create(user = user ,
                                    notice = notice ,
                                    description = description ,
                                    remarks = remarks )
        return redirect('/group')
    
    return render(request, 'add_notice.html')


