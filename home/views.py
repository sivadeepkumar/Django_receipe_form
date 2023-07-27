from django.shortcuts import render,redirect

from django.http import HttpResponse 

from home.models import *

def home(request):
    if request.method == 'POST':

        data = request.POST
        receipe_name = data.get('receipe-name')
        receipe_description = data.get('receipe-description')
        receipe_image = request.FILES.get('receipe-image')

        # print(receipe_name,receipe_description,receipe_image)   


        # Receipe.objects.create(receipe_name = receipe_name,receipe_description = receipe_description,receipe_image = receipe_image)
        Receipe.objects.create(receipe_name = receipe_name,receipe_description = receipe_description,receipe_image = receipe_image)
        # Receipe.objects.all().delete()

        return redirect('/')
    
    queryset = Receipe.objects.all()
    
    if request.GET.get('search'):
        # print(request.GET.get('search'))

        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))

    context = {'receipes' : queryset}
    return render(request,'home.html',context)


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
    





def delete(request,id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    # Receipe.objects.get(id = id).delete()
    return redirect('/')

