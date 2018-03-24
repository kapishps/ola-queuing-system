"""DocsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from core.views import driver_view,customer_view,dashboard_view,pick_req,home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home ,name ='home'),
    path('driver/<int:id>', driver_view, name='driver'),
    path('customer/', customer_view, name='customer'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # path('create_req/', create_req, name='create_req'),
    path('pick_req/', pick_req, name='pick_req'),
]
