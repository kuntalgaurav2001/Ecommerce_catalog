from django.urls import path
from . import customer_views

app_name = 'customer'

urlpatterns = [
    path('', customer_views.customer_catalog, name='catalog'),
    path('catalog/', customer_views.customer_catalog, name='catalog'),
    path('product/<int:product_id>/', customer_views.product_detail_customer, name='product_detail'),
    path('cart/', customer_views.customer_cart, name='cart'),
    path('cart/add/', customer_views.add_to_cart, name='add_to_cart'),
    path('cart/items/<int:item_id>/update/', customer_views.update_cart_item, name='update_cart_item'),
    path('cart/items/<int:item_id>/remove/', customer_views.remove_cart_item, name='remove_cart_item'),
    path('category/<int:category_id>/', customer_views.category_products, name='category_products'),
]


