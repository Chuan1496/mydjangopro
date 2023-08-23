from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_init, name='productInit'),
    path('doSearch/', views.doSearch, name='doSearch'),
    path('newProd/', views.newProd, name='newProd'),
    path('newProd/doSave/', views.doSave, name='doSave'),
    path('editProd/<int:pk>/', views.editProd, name='editProd'),
    path('deleteProd/<int:pk>/', views.deleteProd, name='deleteProd'),
]