from django.urls import path
from . import views

urlpatterns = [
    #path('main', views.index, name='main'),
    #path('index',views.index, name='index'),
    path('tables',views.tables, name='tables'),
    path('crawler',views.sendTag, name='crawler'),
    path('generate',views.generate, name='generate'),
    path('savedata',views.savedata, name='savedata'),
]