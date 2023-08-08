"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import home,delete,update,add,sub
from product.views import product,login_page,register,logout_page
from cart.views import cart
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    
urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login_page,name='login_page'),
    path('logout/',logout_page,name='logout_page'),
    path('delete/<id>/',delete,name='delete'),
    path('update/<id>/',update,name='update'),
    path('', home , name = "home"),
    path('product/', product ,name = 'product'),
    path('cart/', cart , name='cart'),
    path('admin/', admin.site.urls),
    path('add/<id>/',add,name='add'),
    path('sub/<id>/',sub,name='sub'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)
    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   
urlpatterns += staticfiles_urlpatterns()







    
