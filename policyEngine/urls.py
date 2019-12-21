"""policyEngine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, register_converter
import webapp.views as views
from . import converters

register_converter(converters.boolConverter, 'bool')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_rules', views.get_rules),
    path('add_rule/<int:maxAmount>/<str:destinations>', views.add_rule),
    path('add_rule/<int:maxAmount>/<str:destinations>/<bool:amountInUsd>', views.add_rule),
    path('del_rule/<int:uid>', views.del_rule),
    path('update_rule/<int:uid>/<int:maxAmount>/<str:destinations>', views.update_rule),
    path('update_rule/<int:uid>/<int:maxAmount>/<str:destinations>/<bool:amountInUsd>', views.update_rule),
    path('get_transactions', views.get_transactions),
    path('get_transactions/<bool:outgoing>', views.get_transactions),
    path('add_transaction/<int:amount>/<str:destination>', views.add_transaction),
]
