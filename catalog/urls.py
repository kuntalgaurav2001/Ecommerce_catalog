from django.urls import path
from . import views

urlpatterns = [
    # API Info
    path('', views.api_info, name='api-info'),
    
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/products/', views.category_products, name='category-products'),
    
    # Products
    path('products/', views.ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/search/', views.search_products, name='search-products'),
    
    # Product Variants
    path('variants/', views.ProductVariantListCreateView.as_view(), name='variant-list'),
    path('variants/<int:pk>/', views.ProductVariantDetailView.as_view(), name='variant-detail'),
    
    # Cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('cart/items/<int:item_id>/', views.update_cart_item, name='update-cart-item'),
    path('cart/items/<int:item_id>/remove/', views.remove_from_cart, name='remove-from-cart'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Product Reviews
    path('products/<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('reviews/<int:pk>/', views.ProductReviewDetailView.as_view(), name='review-detail'),
    
    # Orders
    path('orders/', views.OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Wishlist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    
    # Coupons
    path('coupons/', views.CouponListView.as_view(), name='coupon-list'),
    path('coupons/validate/', views.validate_coupon, name='validate-coupon'),
    
    # Admin Statistics
    path('admin/stats/', views.admin_stats, name='admin-stats'),
]
