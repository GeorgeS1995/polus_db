from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/result/', views.ESearchView.as_view(), name='result'),
    path('search/product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('search/product/char/<int:pk>/', views.product_2_chardetailview, name='product_2_characteristic-detail'),
    path('add/type-product/', views.type_product_add_form, name='type_product_add_form'),
    path('add/operation/', views.operation_menu, name='operation_menu'),
    path('add/operation/assembly/', views.operation_assembly_main, name='operation_assembly_main'),
    path('add/operation/assembly/form/<int:quantity_of_fields>/', views.operation_assembly_form, name='operation_assembly_form'),
    path('add/operation/tech/', views.operation_add_main, name='operation_add_main'),
    path('add/operation/tech/form/<int:type_of_product>/', views.operation_add_form, name='operation_add_form')
]