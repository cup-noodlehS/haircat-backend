# Django REST Framework Generic ViewSet Documentation

## Overview
The `GenericView` is a versatile ViewSet class for Django REST Framework that provides a complete set of CRUD operations with built-in support for pagination, filtering, and caching. This ViewSet simplifies the creation of REST APIs by handling common patterns and reducing boilerplate code.

## Requirements
- Django REST Framework
- Django
- Python 3.x

## Installation
Include the `GenericView` class in your Django project's views.py file.

## Basic Usage

```python
from your_app.views import GenericView
from your_app.models import YourModel
from your_app.serializers import YourModelSerializer

class YourModelViewSet(GenericView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
```

## Configuration

### Required Attributes
- `queryset`: The base queryset for the model
- `serializer_class`: DRF serializer class for the model

### Optional Attributes
| Attribute | Description | Default |
|-----------|-------------|---------|
| `allowed_methods` | List of allowed HTTP methods | `['list', 'retrieve', 'create', 'update', 'delete']` |
| `allowed_filter_fields` | List of fields that can be filtered | `['*']` (all fields) |
| `allowed_update_fields` | List of fields that can be updated | `['*']` (all fields) |
| `size_per_request` | Number of objects per page | `20` |
| `permission_classes` | List of DRF permission classes | `[]` |
| `cache_key_prefix` | Prefix for cache keys | `None` |
| `cache_duration` | Cache duration in seconds | `3600` (1 hour) |

## API Endpoints

### GET / - List Objects
Retrieves a paginated list of objects with optional filtering.

**Query Parameters:**
- `page`: Page number for pagination
- `top`: Skip first N records
- `bottom`: Return records up to this position
- `order_by`: Field to sort by
- Any model field name for filtering
- `exclude__fieldname`: Exclude records matching criteria

**Response:**
```json
{
    "objects": [...],
    "total_count": 100,
    "num_pages": 5,
    "current_page": 1
}
```

### GET /<pk> - Retrieve Object
Retrieves a single object by primary key.

### POST / - Create Object
Creates a new object.

### PUT /<pk> - Update Object
Updates an existing object.

### DELETE /<pk> - Delete Object
Deletes an object or marks it as removed if the model has a `removed` field.

## Features

### Filtering
The ViewSet supports complex filtering operations:

```python
# Basic filtering
GET /api/your-model/?field=value

# Multiple values (OR condition)
GET /api/your-model/?field=value1,value2

# Exclusion filtering
GET /api/your-model/?exclude__field=value
```

### Pagination
Automatic pagination with customizable page size:

```python
class YourModelViewSet(GenericView):
    size_per_request = 50  # Override default page size
```

### Caching
Built-in caching support for both list and detail views:

```python
class YourModelViewSet(GenericView):
    cache_key_prefix = "your_model"
    cache_duration = 1800  # 30 minutes
```

### Middleware Methods
Customizable hooks for pre and post operations:

```python
class YourModelViewSet(GenericView):
    def pre_create(self, request):
        # Called before object creation
        pass

    def post_create(self, request, instance):
        # Called after successful creation
        pass

    def pre_update(self, request, instance):
        # Called before object update
        pass

    def post_update(self, request, instance):
        # Called after successful update
        pass

    def pre_destroy(self, instance):
        # Called before object deletion
        pass

    def post_destroy(self, instance):
        # Called after successful deletion
        pass
```

## Error Handling
The ViewSet provides standardized error responses:

- 400 Bad Request: Invalid data or validation errors
- 404 Not Found: Object not found
- 405 Method Not Allowed: Disabled HTTP method

## Security
- Field-level update restrictions via `allowed_update_fields`
- Filter field restrictions via `allowed_filter_fields`
- Customizable permission classes
- Automatic transaction management for write operations

## Performance
- Built-in caching support
- Efficient pagination
- Query optimization through select_related/prefetch_related (via queryset configuration)

## Best Practices
1. Always define explicit `allowed_filter_fields` in production
2. Configure appropriate cache duration based on data update frequency
3. Implement pre/post middleware methods for complex business logic
4. Set appropriate permission classes for security

## Examples

### Basic ViewSet
```python
class UserViewSet(GenericView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    allowed_filter_fields = ['username', 'email', 'is_active']
    allowed_update_fields = ['email', 'first_name', 'last_name']
```

### Cached ViewSet with Custom Page Size
```python
class ProductViewSet(GenericView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    size_per_request = 50
    cache_key_prefix = "product"
    cache_duration = 3600
```

### ViewSet with Custom Logic
```python
class OrderViewSet(GenericView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def pre_create(self, request):
        # Validate stock availability
        pass

    def post_create(self, request, instance):
        # Send order confirmation email
        pass
```