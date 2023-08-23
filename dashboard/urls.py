from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchaseInit, name='invenInit'),
    path('purchaseInit/', views.purchaseInit, name='purchaseInit'),
    path('purchaseHis/', views.purchaseHis, name='purchaseHis'),
    path('doPurchase/<int:pk>/', views.doPurchase, name='doPurchase'),
    path('purchase/orderList/', views.orderList, name='orderList'),
    path('purchase/doOrder/', views.doOrder, name='doOrder'),
    path('order/doDelete/', views.doDelete, name='doDelete'),
    path('purchase/editStatus/<int:pk>/', views.editStatus, name='editStatus'),
    #path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    #path('add_record/', views.add_record, name='add_record'),
    #path('update_record/<int:pk>', views.update_record, name='update_record'),

]