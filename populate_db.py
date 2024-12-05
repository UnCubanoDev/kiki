import os
import django
import random
import time
from decimal import Decimal

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

from directorio.models import User, Address
from api.models import Restaurant, Product, Order, OrderDetail, Distributor, ProductCategory, Configuration

def get_timestamp():
    return int(time.time())

def create_configuration():
    config = Configuration.objects.first()
    if config:
        config.exchange_rate = 20.0
        config.distributor_gain = 0.1
        config.delivery_distance_price = 10
        config.delivery_fixed_price = 50
        config.save()
    else:
        Configuration.objects.create(
            exchange_rate=20.0,
            distributor_gain=0.1,
            delivery_distance_price=10,
            delivery_fixed_price=50
        )

def create_users(num_users=5):
    timestamp = get_timestamp()
    users = []
    for i in range(num_users):
        username = f'user{timestamp}{i}'
        user = User.objects.create_user(
            username=username,
            phone=f'+521{timestamp}555{i}',  # Teléfono único
            first_name=f'Usuario{timestamp}{i}',
            last_name=f'Apellido{i}',
            email=f'user{timestamp}{i}@example.com',
            password='password123',
            is_active=True
        )
        users.append(user)
    return users

def create_addresses(users):
    timestamp = get_timestamp()
    addresses = []
    for i, user in enumerate(users):
        address = Address.objects.create(
            user=user,
            name=f'Dirección {timestamp}{i}',
            details=f'Detalles de dirección {timestamp}{i}',
            long=str(-99.1332 + random.uniform(-0.1, 0.1)),
            lat=str(19.4326 + random.uniform(-0.1, 0.1)),
            receiver_name=f'Receptor {timestamp}{i}',
            phone=user.phone
        )
        addresses.append(address)
    return addresses

def create_restaurants(users, num_restaurants=3):
    timestamp = get_timestamp()
    restaurants = []
    for i in range(num_restaurants):
        restaurant = Restaurant.objects.create(
            user=random.choice(users),
            name=f'Restaurante {timestamp}{i}',
            description=f'Descripción del restaurante {timestamp}{i}',
            phone=f'+521{timestamp}666{i}',
            latitude=str(19.4326 + random.uniform(-0.1, 0.1)),
            longitude=str(-99.1332 + random.uniform(-0.1, 0.1)),
            is_active=True,
            funds=Decimal('1000.00')
        )
        restaurants.append(restaurant)
    return restaurants

def create_categories(restaurants):
    timestamp = get_timestamp()
    categories = []
    category_names = ['Comida', 'Bebidas', 'Postres']
    
    for restaurant in restaurants:
        for i, name in enumerate(category_names):
            category, _ = ProductCategory.objects.get_or_create(
                name=f'{name}_{timestamp}{i}',
                business=restaurant
            )
            categories.append(category)
    return categories

def create_products(restaurants, categories, num_products=15):
    timestamp = get_timestamp()
    products = []
    for i in range(num_products):
        restaurant = random.choice(restaurants)
        restaurant_categories = [c for c in categories if c.business == restaurant]
        
        product = Product.objects.create(
            restaurant=restaurant,
            name=f'Producto {timestamp}{i}',
            description=f'Descripción del producto {timestamp}{i}',
            price=Decimal(random.uniform(50, 500)),
            category=random.choice(restaurant_categories),
            is_active=True,
            um='pieza',
            amount=1
        )
        products.append(product)
    return products

def create_orders(users, products, addresses, num_orders=10):
    timestamp = get_timestamp()
    orders = []
    for i in range(num_orders):
        user = random.choice(users)
        address = Address.objects.filter(user=user).first()
        order = Order.objects.create(
            user=user,
            status='pending',
            pay_type='cash',
            delivery_address=address,
            delivery_total_distance=random.randint(1, 20)
        )
        
        # Crear detalles de orden
        num_products = random.randint(1, 4)
        selected_products = random.sample(list(products), num_products)
        for product in selected_products:
            OrderDetail.objects.create(
                order=order,
                product=product,
                amount=random.randint(1, 3)
            )
        orders.append(order)
    return orders

def main():
    print("Configurando parámetros iniciales...")
    create_configuration()
    
    print("Creando usuarios...")
    users = create_users()
    
    print("Creando direcciones...")
    addresses = create_addresses(users)
    
    print("Creando restaurantes...")
    restaurants = create_restaurants(users)
    
    print("Creando categorías...")
    categories = create_categories(restaurants)
    
    print("Creando productos...")
    products = create_products(restaurants, categories)
    
    print("Creando órdenes...")
    create_orders(users, products, addresses)
    
    print("¡Datos de prueba creados exitosamente!")

if __name__ == '__main__':
    main()