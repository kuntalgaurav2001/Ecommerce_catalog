from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product, ProductVariant, Cart, CartItem, Category
from django.db.models import Q

@login_required
def customer_catalog(request):
    """Customer product catalog with search and filters"""
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'variants')
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(base_price__gte=min_price)
    if max_price:
        products = products.filter(base_price__lte=max_price)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'title': 'Product Catalog'
    }
    
    return render(request, 'customer/catalog.html', context)

@login_required
def product_detail_customer(request, product_id):
    """Customer product detail view"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    variants = product.variants.filter(is_active=True)
    
    context = {
        'product': product,
        'variants': variants,
        'title': product.name
    }
    
    return render(request, 'customer/product_detail.html', context)

@login_required
def customer_cart(request):
    """Customer shopping cart view"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('variant__product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'title': 'Shopping Cart'
    }
    
    return render(request, 'customer/cart.html', context)

@login_required
@require_POST
def add_to_cart(request):
    """Add item to customer cart"""
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        variant = ProductVariant.objects.get(id=variant_id, is_active=True)
        
        if variant.inventory_count < quantity:
            messages.error(request, f'Only {variant.inventory_count} items available in stock.')
            return redirect('customer:product_detail', product_id=variant.product.id)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{variant.product.name} added to cart!')
        return redirect('customer:product_detail', product_id=variant.product.id)
        
    except ProductVariant.DoesNotExist:
        messages.error(request, 'Product variant not found.')
        return redirect('customer:catalog')

@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    else:
        if quantity > cart_item.variant.inventory_count:
            messages.error(request, f'Only {cart_item.variant.inventory_count} items available in stock.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    
    return redirect('customer:cart')

@login_required
@require_POST
def remove_cart_item(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.variant.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    
    return redirect('customer:cart')

@login_required
def category_products(request, category_id):
    """Products by category"""
    category = get_object_or_404(Category, id=category_id, is_active=True)
    products = Product.objects.filter(category=category, is_active=True).select_related('category').prefetch_related('images', 'variants')
    
    context = {
        'category': category,
        'products': products,
        'title': f'{category.name} Products'
    }
    
    return render(request, 'customer/category_products.html', context)


