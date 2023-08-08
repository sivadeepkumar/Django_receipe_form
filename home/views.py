from django.shortcuts import render,redirect

from django.http import HttpResponse 

from home.models import *

from django.contrib.auth.decorators import login_required

import pdb

@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        
        data = request.POST
        receipe_name = data.get('receipe-name')
        receipe_description = data.get('receipe-description')
        receipe_image = request.FILES.get('receipe-image')
        rating = 5
        receipe_cost = data.get('receipe-cost')
        count = 1
        # print(receipe_name,receipe_description,receipe_image)   
        # Receipe.objects.create(receipe_name = receipe_name,receipe_description = receipe_description,receipe_image = receipe_image)
        Receipe.objects.create(receipe_name = receipe_name,receipe_description = receipe_description,receipe_image = receipe_image,rating=rating,price=receipe_cost,count=count)
        # Receipe.objects.all().delete()
        return redirect('/')
    
    queryset = Receipe.objects.all()
    
    if request.GET.get('search'):
        # print(request.GET.get('search'))

        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
    count = Receipe.objects.all()
    count = count.count()
    
    cart_value = 0

    for each in queryset:
        each.total = each.price * each.count
        cart_value += each.total


    if request.GET.get('search'):
        # print(request.GET.get('search'))

        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
        
    context = {'receipes' : queryset,'count' :count,'cart_value':cart_value}
    return render(request,'home.html',context)

@login_required(login_url='/login/')
def update(request,id):
    queryset = Receipe.objects.get(id = id)
    context = {'receipe' : queryset}
    
    if request.method == 'POST':
        data = request.POST

        receipe_name = data.get('receipe-name')
        receipe_description = data.get('receipe-description')
        receipe_image = request.FILES.get('receipe-image')

        queryset.receipe_name= receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        
    
        return redirect('/')
    
    return render(request,'update.html',context)
    
@login_required(login_url='/login/')
def delete(request,id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    # Receipe.objects.get(id = id).delete()
    return redirect('/')


@login_required(login_url='/login/')
def add(request,id):

    r = Receipe.objects.get(id = id)
    # pdb.set_trace()
    r.count += 1
    r.save()
    # pdb.set_trace()
    return redirect('/')



@login_required(login_url='/login/')
def sub(request,id):
    r = Receipe.objects.get(id = id)
    r.count -= 1
    r.save()
    if r.count == 0:
        r.delete()
    return redirect('/')
