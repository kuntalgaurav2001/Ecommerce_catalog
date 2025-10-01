from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Prefetch
from .models import (
    Category, Product, ProductVariant, Cart, CartItem,
    Order, OrderItem, ProductReview, Wishlist, WishlistItem, Coupon, UserProfile
)
from .serializers import (
    CategorySerializer, ProductSerializer, ProductListSerializer, ProductDetailSerializer,
    ProductVariantSerializer, CartSerializer, CartItemSerializer,
    UserSerializer, UserProfileSerializer, ProductReviewSerializer, ProductReviewCreateSerializer,
    OrderSerializer, OrderCreateSerializer, OrderItemSerializer,
    WishlistSerializer, WishlistItemSerializer, CouponSerializer, CouponValidationSerializer
)

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Allow public access for browsing

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # Only admin can modify

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'variants')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price', 'created_at']
    ordering = ['-created_at']
    permission_classes = [AllowAny]  # Allow public access for browsing

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if category:
            queryset = queryset.filter(category_id=category)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('images', 'variants', 'reviews__user')
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]  # Allow public access for viewing

# Product Variant Views
class ProductVariantListCreateView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.filter(is_active=True).select_related('product')
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing

class ProductVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.select_related('product')
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUser]  # Only admin can modify

# Cart Views
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    variant_id = request.data.get('variant_id')
    quantity = request.data.get('quantity', 1)

    try:
        variant = ProductVariant.objects.get(id=variant_id, is_active=True)
    except ProductVariant.DoesNotExist:
        return Response({'error': 'Product variant not found'}, status=status.HTTP_404_NOT_FOUND)

    if variant.inventory_count < quantity:
        return Response({'error': 'Insufficient inventory'}, status=status.HTTP_400_BAD_REQUEST)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

    if quantity <= 0:
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)

    if cart_item.variant.inventory_count < quantity:
        return Response({'error': 'Insufficient inventory'}, status=status.HTTP_400_BAD_REQUEST)

    cart_item.quantity = quantity
    cart_item.save()

    return Response(CartItemSerializer(cart_item).data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

# Home/API Info View
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information and available endpoints"""
    return Response({
        'message': 'E-commerce Product Catalog API',
        'version': '1.0.0',
        'endpoints': {
            'categories': '/api/categories/',
            'products': '/api/products/',
            'variants': '/api/variants/',
            'cart': '/api/cart/',
            'admin': '/admin/',
        },
        'features': [
            'Browse products by categories',
            'Search and filter products',
            'Add products to cart',
            'Manage inventory levels',
            'Admin panel for catalog management'
        ]
    })

# Category Products View
@api_view(['GET'])
@permission_classes([AllowAny])
def category_products(request, category_id):
    try:
        category = Category.objects.get(id=category_id, is_active=True)
        products = Product.objects.filter(category=category, is_active=True).select_related('category').prefetch_related('images', 'variants')
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'category': CategorySerializer(category).data,
            'products': serializer.data,
            'count': products.count()
        })
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

# Additional E-commerce API Views

# User Profile Views
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

# Product Reviews Views
class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(product_id=product_id).select_related('user')
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product)

class ProductReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProductReview.objects.filter(user=self.request.user)

# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__variant__product')
    
    def perform_create(self, serializer):
        # Create order from cart
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate order number
        import uuid
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate total
        total_amount = sum(item.total_price for item in cart_items)
        
        # Create order
        order = serializer.save(
            user=self.request.user,
            order_number=order_number,
            total_amount=total_amount
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                variant=cart_item.variant,
                quantity=cart_item.quantity,
                price=cart_item.variant.final_price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return order

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__variant__product')

# Wishlist Views
class WishlistView(generics.RetrieveAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        return wishlist

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    if created:
        return Response({'message': 'Product added to wishlist'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Product already in wishlist'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product_id=product_id)
    wishlist_item.delete()
    
    return Response({'message': 'Product removed from wishlist'}, status=status.HTTP_200_OK)

# Coupon Views
class CouponListView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        from django.utils import timezone
        now = timezone.now()
        return Coupon.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_coupon(request):
    serializer = CouponValidationSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        order_amount = serializer.validated_data['order_amount']
        
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_valid and order_amount >= coupon.min_order_amount:
                discount_amount = 0
                if coupon.discount_type == 'percentage':
                    discount_amount = (order_amount * coupon.discount_value) / 100
                else:
                    discount_amount = coupon.discount_value
                
                return Response({
                    'valid': True,
                    'discount_amount': discount_amount,
                    'discount_type': coupon.discount_type,
                    'discount_value': coupon.discount_value
                })
            else:
                return Response({
                    'valid': False,
                    'error': 'Coupon is not valid or minimum order amount not met'
                })
        except Coupon.DoesNotExist:
            return Response({
                'valid': False,
                'error': 'Invalid coupon code'
            })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Search and Filter Views
@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    rating = request.GET.get('rating', '')
    sort_by = request.GET.get('sort', '-created_at')
    
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'variants', 'reviews')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    if category:
        products = products.filter(category_id=category)
    
    if min_price:
        products = products.filter(base_price__gte=min_price)
    
    if max_price:
        products = products.filter(base_price__lte=max_price)
    
    if rating:
        products = products.filter(reviews__rating__gte=rating).distinct()
    
    products = products.order_by(sort_by)
    
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

# Statistics Views
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    from django.db.models import Count, Sum, Avg
    from django.utils import timezone
    from datetime import timedelta
    
    # Basic stats
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    
    # Recent orders (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Revenue stats
    total_revenue = Order.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    monthly_revenue = Order.objects.filter(
        created_at__gte=thirty_days_ago
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Top products
    top_products = Product.objects.annotate(
        order_count=Count('variants__orderitem__order')
    ).order_by('-order_count')[:5]
    
    return Response({
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'total_revenue': float(total_revenue),
        'monthly_revenue': float(monthly_revenue),
        'top_products': [
            {
                'id': product.id,
                'name': product.name,
                'order_count': product.order_count
            }
            for product in top_products
        ]
    })

# Import get_object_or_404
from django.shortcuts import get_object_or_404
