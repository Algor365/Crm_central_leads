"""
URL configuration for lead_ecorp project.

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
from lead.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/leads/<int:pk>/mover/", mover_lead, name="mover_lead"),
    path("", kanban_funil, name="kanban-funil"),
    path('api/leads/<int:lead_id>/', get_lead_details, name='lead_details'),
    path("landing/", landing_lead, name="landing"),
    path("api/leads/", listar_leads, name="listar_leads"),
    path("api/leads/<int:pk>/editar/", editar_lead, name="editar_lead"),
    path("api/leads/<int:pk>/deletar/", deletar_lead, name="deletar_lead"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
