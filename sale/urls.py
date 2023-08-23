from django.urls import path
from . import views

urlpatterns = [
    path('', views.saleInit, name='saleInit'),
    path('init/', views.customer_init, name='customer_init'),
    path('newCust/', views.newCust, name='newCust'),
    path('editCust/<int:pk>/', views.editCust, name='editCust'),
    path('deleteCust/<int:pk>/', views.deleteCust, name='deleteCust'),
    path('saleHis/', views.saleHis, name='saleHis'),
    path('doSale/', views.doSale, name='doSale'),
    path('sale/searchCust/', views.searchCust, name='searchCust'),
    #path('register/', views.register_user, name='register'),
    #path('record/<int:pk>', views.customer_record, name='record'),
    #path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    #path('add_record/', views.add_record, name='add_record'),
    #path('update_record/<int:pk>', views.update_record, name='update_record'),

]