# E-commerce Product Catalog Backend System

A comprehensive Django REST API backend system for an e-commerce marketplace with product categories, variants, inventory management, and shopping cart functionality.

## Screenshots

### Admin Dashboard
![Admin Dashboard](./media/product_images/s1.png)

### Customer Portal
![Customer Portal](./media/product_images/s1.png)

## Project Structure

```
ecommerce_catalog/
├── catalog/                           # Main Django application
│   ├── __init__.py
│   ├── admin.py                      # Django admin configuration
│   ├── apps.py                       # App configuration
│   ├── customer_urls.py              # Customer-facing URL patterns
│   ├── customer_views.py             # Customer-facing views
│   ├── models.py                     # Database models
│   ├── serializers.py                # DRF serializers
│   ├── tests.py                      # Unit tests
│   ├── urls.py                       # API URL patterns
│   ├── views.py                      # API views
│   ├── management/                   # Custom management commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── populate_data.py      # Data population command
│   ├── migrations/                   # Database migrations
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_coupon_order_userprofile_wishlist_orderitem_and_more.py
│   └── templates/                    # HTML templates
│       ├── admin/
│       │   └── catalog/
│       │       └── customer_catalog.html
│       ├── customer_admin/
│       │   └── index.html
│       └── customer/
│           ├── cart.html
│           ├── catalog.html
│           └── product_detail.html
├── ecommerce_catalogg/               # Django project settings
│   ├── __init__.py
│   ├── asgi.py                      # ASGI configuration
│   ├── settings.py                  # Django settings
│   ├── urls.py                      # Main URL configuration
│   └── wsgi.py                      # WSGI configuration
├── media/                           # Media files
│   ├── avatars/                     # User avatar images
│   └── product_images/              # Product images (87 files)
├── manage.py                        # Django management script
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
└── postman_collection.json          # API testing collection
```

## Features

### Core Functionality
- **Product Management**: Create, read, update, and delete products with detailed information
- **Category System**: Hierarchical categories and subcategories for product organization
- **Product Variants**: Different sizes, colors, and configurations with separate inventory tracking
- **Shopping Cart**: Add, update, and remove items from cart
- **Search & Filtering**: Search products by name/description and filter by category, price range
- **Inventory Management**: Track stock levels and availability
- **Admin Panel**: Full Django admin interface for catalog management
- **Order Management**: Complete order processing with status tracking
- **User Reviews**: Product reviews and ratings system
- **Wishlist**: Save products for later purchase
- **Coupon System**: Discount codes with percentage/fixed amount support

### Technical Features
- **RESTful API**: Complete REST API with proper HTTP methods
- **Query Optimization**: Efficient database queries with select_related and prefetch_related
- **Error Handling**: Comprehensive error handling and validation
- **Pagination**: Built-in pagination for large datasets
- **Authentication**: Session-based authentication for cart functionality
- **CORS Support**: Cross-origin resource sharing enabled
- **Admin Customization**: Custom admin interface for customer portal

## Requirements

- Python 3.8+
- Django 5.2+
- PostgreSQL 12+ (or SQLite for development)
- Django REST Framework 3.14+
- Pillow (for image handling)
- Other dependencies listed in requirements.txt

## Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ecommerce_catalog
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# For PostgreSQL
createdb -U postgres ecommerce_catalog

# Or use SQLite (default in settings)
# No additional setup required
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Populate Test Data
```bash
python manage.py populate_data
```

### 8. Start Server
```bash
python manage.py runserver
```

## Access URLs

### Main Interfaces
- **Home Page**: http://localhost:8000/
- **Customer Portal**: http://localhost:8000/customer/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/

### Test Credentials
- **Admin**: `admin` / `admin123`
- **Customer**: `testuser` / `testpass123`

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### Available Endpoints

#### API Information
- `GET /api/` - API information and available endpoints

#### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Get category details
- `GET /api/categories/{id}/products/` - Get products in category
- `POST /api/categories/` - Create category (Admin only)

#### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/search/` - Search products
- `POST /api/products/` - Create product (Admin only)
- `PUT /api/products/{id}/` - Update product (Admin only)
- `DELETE /api/products/{id}/` - Delete product (Admin only)

#### Product Variants
- `GET /api/products/{id}/variants/` - Get product variants
- `POST /api/products/{id}/variants/` - Create variant (Admin only)

#### Shopping Cart
- `GET /api/cart/` - Get user's cart
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/` - Remove cart item

#### Orders
- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details

#### Reviews
- `GET /api/products/{id}/reviews/` - Get product reviews
- `POST /api/products/{id}/reviews/` - Create product review

#### Wishlist
- `GET /api/wishlist/` - Get user's wishlist
- `POST /api/wishlist/add/` - Add product to wishlist
- `DELETE /api/wishlist/remove/{id}/` - Remove from wishlist

#### Coupons
- `GET /api/coupons/` - List available coupons
- `POST /api/coupons/validate/` - Validate coupon code

## Database Models

### Core Models
- **Category** - Hierarchical product categories
- **Product** - Main product information
- **ProductImage** - Product images with primary image support
- **ProductVariant** - Product variations (size, color, storage)
- **Cart & CartItem** - Shopping cart functionality

### Extended Models
- **Order & OrderItem** - Order management system
- **ProductReview** - Customer reviews and ratings
- **Wishlist & WishlistItem** - Wishlist functionality
- **Coupon** - Discount code system
- **UserProfile** - Extended user information

## API Authentication
- Session-based authentication for cart operations
- Public access for browsing products and categories
- Admin-only access for create/update/delete operations

## Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure production database
3. Set up static file serving
4. Configure CORS for your frontend domain
5. Set up proper logging

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
ALLOWED_HOSTS=yourdomain.com
```

## Performance Optimizations

- **Query Optimization**: Uses `select_related` and `prefetch_related` for efficient queries
- **Pagination**: Built-in pagination to handle large datasets
- **Database Indexing**: Proper indexing on frequently queried fields
- **Caching**: Ready for Redis/Memcached integration

## Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
- Model validation
- API endpoint functionality
- Authentication and permissions
- Error handling

## API Documentation

### Response Format
All API responses follow this format:
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Handling
```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.