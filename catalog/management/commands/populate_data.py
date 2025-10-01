from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import (
    Category, Product, ProductVariant, ProductImage, Order, OrderItem,
    ProductReview, Wishlist, WishlistItem, Coupon, UserProfile
)
from decimal import Decimal
import os
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate database with comprehensive test data for e-commerce catalog'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate database with test data...')
        
        # Create categories
        self.stdout.write('Creating categories...')
        electronics = Category.objects.create(
            name='Electronics', 
            description='Electronic devices and accessories',
            is_active=True
        )
        clothing = Category.objects.create(
            name='Clothing', 
            description='Fashion and apparel',
            is_active=True
        )
        home = Category.objects.create(
            name='Home & Garden', 
            description='Home improvement and garden supplies',
            is_active=True
        )
        
        # Create subcategories
        phones = Category.objects.create(
            name='Phones', 
            parent=electronics, 
            description='Mobile phones and accessories',
            is_active=True
        )
        laptops = Category.objects.create(
            name='Laptops', 
            parent=electronics, 
            description='Laptop computers and accessories',
            is_active=True
        )
        shirts = Category.objects.create(
            name='Shirts', 
            parent=clothing, 
            description='Men\'s and women\'s shirts',
            is_active=True
        )
        shoes = Category.objects.create(
            name='Shoes', 
            parent=clothing, 
            description='Footwear for all occasions',
            is_active=True
        )
        furniture = Category.objects.create(
            name='Furniture', 
            parent=home, 
            description='Home furniture and decor',
            is_active=True
        )
        
        # Create products
        self.stdout.write('Creating products...')
        
        # iPhone products
        iphone = Product.objects.create(
            name='iPhone 15 Pro',
            description='Latest iPhone with titanium design, A17 Pro chip, and advanced camera system',
            category=phones,
            base_price=Decimal('999.00'),
            is_active=True
        )
        
        iphone_regular = Product.objects.create(
            name='iPhone 15',
            description='Latest iPhone with aluminum design, A16 Bionic chip, and dual camera system',
            category=phones,
            base_price=Decimal('799.00'),
            is_active=True
        )
        
        # MacBook products
        macbook_pro = Product.objects.create(
            name='MacBook Pro 16-inch',
            description='Professional laptop with M3 Pro chip, 16GB RAM, and 512GB SSD',
            category=laptops,
            base_price=Decimal('2499.00'),
            is_active=True
        )
        
        macbook_air = Product.objects.create(
            name='MacBook Air 13-inch',
            description='Ultra-thin laptop with M2 chip, 8GB RAM, and 256GB SSD',
            category=laptops,
            base_price=Decimal('1199.00'),
            is_active=True
        )
        
        # Clothing products
        cotton_tshirt = Product.objects.create(
            name='Premium Cotton T-Shirt',
            description='100% organic cotton t-shirt, comfortable and breathable',
            category=shirts,
            base_price=Decimal('29.99'),
            is_active=True
        )
        
        polo_shirt = Product.objects.create(
            name='Classic Polo Shirt',
            description='Classic polo shirt with collar, perfect for casual and semi-formal occasions',
            category=shirts,
            base_price=Decimal('49.99'),
            is_active=True
        )
        
        running_shoes = Product.objects.create(
            name='Running Shoes',
            description='High-performance running shoes with advanced cushioning technology',
            category=shoes,
            base_price=Decimal('129.99'),
            is_active=True
        )
        
        # Furniture products
        office_chair = Product.objects.create(
            name='Ergonomic Office Chair',
            description='Comfortable ergonomic office chair with lumbar support and adjustable height',
            category=furniture,
            base_price=Decimal('299.99'),
            is_active=True
        )
        
        # Create product variants
        self.stdout.write('Creating product variants...')
        
        # iPhone 15 Pro variants
        ProductVariant.objects.create(
            product=iphone,
            name='128GB Natural Titanium',
            sku='IPH15P-128-NT',
            inventory_count=50
        )
        
        ProductVariant.objects.create(
            product=iphone,
            name='256GB Natural Titanium',
            sku='IPH15P-256-NT',
            price_modifier=Decimal('100.00'),
            inventory_count=30
        )
        
        ProductVariant.objects.create(
            product=iphone,
            name='512GB Natural Titanium',
            sku='IPH15P-512-NT',
            price_modifier=Decimal('300.00'),
            inventory_count=20
        )
        
        ProductVariant.objects.create(
            product=iphone,
            name='128GB Blue Titanium',
            sku='IPH15P-128-BT',
            inventory_count=40
        )
        
        # iPhone 15 variants
        ProductVariant.objects.create(
            product=iphone_regular,
            name='128GB Pink',
            sku='IPH15-128-PK',
            inventory_count=60
        )
        
        ProductVariant.objects.create(
            product=iphone_regular,
            name='256GB Pink',
            sku='IPH15-256-PK',
            price_modifier=Decimal('100.00'),
            inventory_count=40
        )
        
        ProductVariant.objects.create(
            product=iphone_regular,
            name='128GB Blue',
            sku='IPH15-128-BL',
            inventory_count=55
        )
        
        # MacBook Pro variants
        ProductVariant.objects.create(
            product=macbook_pro,
            name='M3 Pro 18GB/512GB',
            sku='MBP16-M3P-18-512',
            inventory_count=25
        )
        
        ProductVariant.objects.create(
            product=macbook_pro,
            name='M3 Pro 18GB/1TB',
            sku='MBP16-M3P-18-1TB',
            price_modifier=Decimal('200.00'),
            inventory_count=15
        )
        
        ProductVariant.objects.create(
            product=macbook_pro,
            name='M3 Max 36GB/1TB',
            sku='MBP16-M3M-36-1TB',
            price_modifier=Decimal('500.00'),
            inventory_count=10
        )
        
        # MacBook Air variants
        ProductVariant.objects.create(
            product=macbook_air,
            name='M2 8GB/256GB',
            sku='MBA13-M2-8-256',
            inventory_count=40
        )
        
        ProductVariant.objects.create(
            product=macbook_air,
            name='M2 8GB/512GB',
            sku='MBA13-M2-8-512',
            price_modifier=Decimal('200.00'),
            inventory_count=30
        )
        
        # T-Shirt variants
        ProductVariant.objects.create(
            product=cotton_tshirt,
            name='Small',
            sku='TSH-COT-S',
            inventory_count=100
        )
        
        ProductVariant.objects.create(
            product=cotton_tshirt,
            name='Medium',
            sku='TSH-COT-M',
            inventory_count=100
        )
        
        ProductVariant.objects.create(
            product=cotton_tshirt,
            name='Large',
            sku='TSH-COT-L',
            inventory_count=100
        )
        
        ProductVariant.objects.create(
            product=cotton_tshirt,
            name='X-Large',
            sku='TSH-COT-XL',
            inventory_count=80
        )
        
        # Polo shirt variants
        ProductVariant.objects.create(
            product=polo_shirt,
            name='Small',
            sku='POLO-S',
            inventory_count=50
        )
        
        ProductVariant.objects.create(
            product=polo_shirt,
            name='Medium',
            sku='POLO-M',
            inventory_count=50
        )
        
        ProductVariant.objects.create(
            product=polo_shirt,
            name='Large',
            sku='POLO-L',
            inventory_count=50
        )
        
        # Running shoes variants
        ProductVariant.objects.create(
            product=running_shoes,
            name='Size 8',
            sku='SHOE-RUN-8',
            inventory_count=25
        )
        
        ProductVariant.objects.create(
            product=running_shoes,
            name='Size 9',
            sku='SHOE-RUN-9',
            inventory_count=30
        )
        
        ProductVariant.objects.create(
            product=running_shoes,
            name='Size 10',
            sku='SHOE-RUN-10',
            inventory_count=35
        )
        
        ProductVariant.objects.create(
            product=running_shoes,
            name='Size 11',
            sku='SHOE-RUN-11',
            inventory_count=20
        )
        
        # Office chair variants
        ProductVariant.objects.create(
            product=office_chair,
            name='Black',
            sku='CHAIR-OFF-BLK',
            inventory_count=15
        )
        
        ProductVariant.objects.create(
            product=office_chair,
            name='Gray',
            sku='CHAIR-OFF-GRY',
            inventory_count=12
        )
        
        ProductVariant.objects.create(
            product=office_chair,
            name='White',
            sku='CHAIR-OFF-WHT',
            inventory_count=8
        )
        
        # Create a test user
        self.stdout.write('Creating test user...')
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
            self.stdout.write('Test user created: testuser / testpass123')
        else:
            self.stdout.write('Test user already exists')
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('Admin user created: admin / admin123')
        else:
            admin_user = User.objects.get(username='admin')
            self.stdout.write('Admin user already exists')
        
        # Create user profiles
        self.stdout.write('Creating user profiles...')
        for user in User.objects.all():
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': f'+1-555-{user.id:04d}',
                    'address': f'{user.id} Main Street',
                    'city': 'New York',
                    'state': 'NY',
                    'zip_code': '10001',
                    'country': 'USA'
                }
            )
        
        # Create coupons
        self.stdout.write('Creating coupons...')
        now = timezone.now()
        Coupon.objects.get_or_create(
            code='WELCOME10',
            defaults={
                'description': '10% off for new customers',
                'discount_type': 'percentage',
                'discount_value': Decimal('10.00'),
                'min_order_amount': Decimal('50.00'),
                'max_uses': 100,
                'is_active': True,
                'valid_from': now,
                'valid_until': now + timedelta(days=30)
            }
        )
        
        Coupon.objects.get_or_create(
            code='SAVE20',
            defaults={
                'description': '$20 off orders over $100',
                'discount_type': 'fixed',
                'discount_value': Decimal('20.00'),
                'min_order_amount': Decimal('100.00'),
                'max_uses': 50,
                'is_active': True,
                'valid_from': now,
                'valid_until': now + timedelta(days=60)
            }
        )
        
        Coupon.objects.get_or_create(
            code='FLASH50',
            defaults={
                'description': '50% off flash sale',
                'discount_type': 'percentage',
                'discount_value': Decimal('50.00'),
                'min_order_amount': Decimal('0.00'),
                'max_uses': 20,
                'is_active': True,
                'valid_from': now,
                'valid_until': now + timedelta(days=7)
            }
        )
        
        # Create sample orders
        self.stdout.write('Creating sample orders...')
        test_user = User.objects.get(username='testuser')
        
        # Create order 1
        order1 = Order.objects.create(
            user=test_user,
            order_number='ORD-001',
            status='delivered',
            total_amount=Decimal('999.00'),
            shipping_address='123 Test Street, New York, NY 10001',
            billing_address='123 Test Street, New York, NY 10001',
            payment_method='credit_card',
            payment_status='paid'
        )
        
        # Add items to order 1
        iphone_variant = ProductVariant.objects.filter(product__name='iPhone 15 Pro').first()
        if iphone_variant:
            OrderItem.objects.create(
                order=order1,
                variant=iphone_variant,
                quantity=1,
                price=iphone_variant.final_price
            )
        
        # Create order 2
        order2 = Order.objects.create(
            user=test_user,
            order_number='ORD-002',
            status='shipped',
            total_amount=Decimal('129.99'),
            shipping_address='123 Test Street, New York, NY 10001',
            billing_address='123 Test Street, New York, NY 10001',
            payment_method='paypal',
            payment_status='paid'
        )
        
        # Add items to order 2
        shoes_variant = ProductVariant.objects.filter(product__name='Running Shoes').first()
        if shoes_variant:
            OrderItem.objects.create(
                order=order2,
                variant=shoes_variant,
                quantity=1,
                price=shoes_variant.final_price
            )
        
        # Create product reviews
        self.stdout.write('Creating product reviews...')
        products = Product.objects.all()[:5]  # Review first 5 products
        
        review_data = [
            {'rating': 5, 'title': 'Amazing product!', 'comment': 'Great quality and fast delivery. Highly recommended!'},
            {'rating': 4, 'title': 'Very good', 'comment': 'Good value for money. Would buy again.'},
            {'rating': 5, 'title': 'Perfect!', 'comment': 'Exceeded my expectations. Excellent product.'},
            {'rating': 3, 'title': 'Average', 'comment': 'It\'s okay, nothing special but does the job.'},
            {'rating': 5, 'title': 'Love it!', 'comment': 'Best purchase I\'ve made in a while. Great quality!'},
        ]
        
        for i, product in enumerate(products):
            ProductReview.objects.get_or_create(
                product=product,
                user=test_user,
                defaults={
                    'rating': review_data[i]['rating'],
                    'title': review_data[i]['title'],
                    'comment': review_data[i]['comment'],
                    'is_verified_purchase': True,
                    'helpful_votes': i * 2
                }
            )
        
        # Create wishlist items
        self.stdout.write('Creating wishlist items...')
        wishlist, created = Wishlist.objects.get_or_create(user=test_user)
        
        # Add some products to wishlist
        wishlist_products = Product.objects.all()[:3]
        for product in wishlist_products:
            WishlistItem.objects.get_or_create(
                wishlist=wishlist,
                product=product
            )
        
        # Summary
        self.stdout.write('\nTest data created successfully!')
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Products: {Product.objects.count()}')
        self.stdout.write(f'Variants: {ProductVariant.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Orders: {Order.objects.count()}')
        self.stdout.write(f'Reviews: {ProductReview.objects.count()}')
        self.stdout.write(f'Coupons: {Coupon.objects.count()}')
        self.stdout.write(f'Wishlist Items: {WishlistItem.objects.count()}')
        
        self.stdout.write('\nAvailable endpoints:')
        self.stdout.write('  Home: http://localhost:8000/')
        self.stdout.write('  Customer Portal: http://localhost:8000/customer/')
        self.stdout.write('  Admin Panel: http://localhost:8000/admin/')
        self.stdout.write('  API Info: http://localhost:8000/api/')
        self.stdout.write('  Products: http://localhost:8000/api/products/')
        self.stdout.write('  Orders: http://localhost:8000/api/orders/')
        self.stdout.write('  Reviews: http://localhost:8000/api/products/1/reviews/')
        self.stdout.write('  Wishlist: http://localhost:8000/api/wishlist/')
        self.stdout.write('  Coupons: http://localhost:8000/api/coupons/')
        self.stdout.write('  Admin Stats: http://localhost:8000/api/admin/stats/')
        
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  User: testuser / testpass123')
        
        self.stdout.write('\nTest coupons:')
        self.stdout.write('  WELCOME10 - 10% off (min $50)')
        self.stdout.write('  SAVE20 - $20 off (min $100)')
        self.stdout.write('  FLASH50 - 50% off (no minimum)')
