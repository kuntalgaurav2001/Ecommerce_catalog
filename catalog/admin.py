from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .models import (
    Category, Product, ProductImage, ProductVariant, Cart, CartItem,
    Order, OrderItem, ProductReview, Wishlist, WishlistItem, Coupon, UserProfile
)
from .customer_views import (
    customer_catalog, product_detail_customer, customer_cart,
    add_to_cart, update_cart_item, remove_cart_item,
    category_products
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    ordering = ['-is_primary', 'created_at']
    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'sku', 'final_price', 'inventory_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'sku']
    ordering = ['product', 'name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'variant', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__user__username', 'variant__name']

# Additional Admin Models
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username']
    readonly_fields = ['order_number', 'created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'variant', 'quantity', 'price', 'total_price']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'variant__name']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['product__name', 'user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['wishlist__user__username', 'product__name']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'is_active', 'used_count', 'valid_until']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    readonly_fields = ['used_count', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']

# Customer-facing admin views
class CustomerAdminSite(admin.AdminSite):
    site_header = "E-commerce Customer Portal"
    site_title = "Customer Portal"
    index_title = "Welcome to E-commerce Store"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('catalog/', customer_catalog, name='customer_catalog'),
            path('catalog/product/<int:product_id>/', product_detail_customer, name='product_detail_customer'),
            path('catalog/category/<int:category_id>/', category_products, name='category_products_admin'),
            path('cart/', customer_cart, name='customer_cart'),
            path('cart/add/', add_to_cart, name='add_to_cart_admin'),
            path('cart/items/<int:item_id>/update/', update_cart_item, name='update_cart_item_admin'),
            path('cart/items/<int:item_id>/remove/', remove_cart_item, name='remove_cart_item_admin'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        """Custom index page with customer portal links"""
        extra_context = extra_context or {}
        extra_context.update({
            'customer_links': [
                {'name': 'Browse Products', 'url': 'catalog/', 'description': 'Browse all available products'},
                {'name': 'Shopping Cart', 'url': 'cart/', 'description': 'View your shopping cart'},
                {'name': 'Admin Panel', 'url': '../admin/', 'description': 'Manage products and categories'},
            ]
        })
        return super().index(request, extra_context)

# Create custom admin site instance
customer_admin = CustomerAdminSite(name='customer_admin')