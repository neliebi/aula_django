"""proteins URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from website.views import *
from website.api import *


#handlerXXX = 'app_name.views_file.view_function'
handler400 = 'website.views.error400'
handler403 = 'website.views.error403'
handler404 = 'website.views.error404'
handler500 = 'website.views.error500'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', hello),
    path('filters/', test_filters),

    path('proteins/', proteins, name="proteins"),
    path('clades/', clades, name="clades"),
    path('genes/', genes, name="genes"),
    path('gos/', gos, name="gos"),
    path('families/', families, name="families"),
    path('structures/', structures, name="structures"),


    path('protein/<accession>/', protein, name="protein"),
    path('taxonomy/<ncbi_id>/', taxonomy, name="taxonomy"),
    path('gene/<gene_name>/', gene, name="gene"),
    path('go/<go_id>/', go, name="go"),
    path('pfam/<pfam_id>/', pfam, name="pfam"),
    path('pdb/<accession>/', pdb, name="pdb"),

    path('api/protein/<accession>/', protein_api),
    path('api/proteins/', protein_list_api),    
]


