from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
import json

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def home_view(request):
    return render(request, "pages/home.html")


def about_view(request):
    return render(request, "pages/about.html")


def cart_view(request):
    # Dummy products data - in a real app, this would come from a database
    products = [
        {
            'id': 1,
            'name': 'Premium Notebook',
            'description': 'High-quality leather-bound notebook perfect for note-taking',
            'price': 29.99,
            'quantity': 2,
            'image': 'https://picsum.photos/150/150?text=Notebook'
        },
        {
            'id': 2,
            'name': 'Wireless Headphones',
            'description': 'Noise-cancelling wireless headphones with premium sound',
            'price': 159.99,
            'quantity': 1,
            'image': 'https://picsum.photos/150/150'
        }
    ]
    
    # Add subtotal to each product
    for product in products:
        product['subtotal'] = product['price'] * product['quantity']
    
    # Calculate totals
    subtotal = sum(product['price'] * product['quantity'] for product in products)
    tax_rate = 0.08  # 8% tax
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    context = {
        'products': products,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'tax_rate': tax_rate * 100,  # Convert to percentage for display
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    
    return render(request, "pages/cart.html", context)


@csrf_exempt
@require_POST
def create_checkout_session(request):
    try:
        # Parse the request data
        data = json.loads(request.body)
        
        # Get products from the request (or use the same dummy data)
        products = [
            {
                'id': 1,
                'name': 'Premium Notebook',
                'description': 'High-quality leather-bound notebook perfect for note-taking',
                'price': 29.99,
                'quantity': 2,
            },
            {
                'id': 2,
                'name': 'Wireless Headphones',
                'description': 'Noise-cancelling wireless headphones with premium sound',
                'price': 159.99,
                'quantity': 1,
            }
        ]
        
        # Create line items for Stripe
        line_items = []
        for product in products:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['name'],
                        'description': product['description'],
                    },
                    'unit_amount': int(product['price'] * 100),  # Stripe expects cents
                },
                'quantity': product['quantity'],
            })
        
        # Add tax as a separate line item
        subtotal = sum(product['price'] * product['quantity'] for product in products)
        tax = subtotal * 0.08
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Tax (8%)',
                },
                'unit_amount': int(tax * 100),  # Stripe expects cents
            },
            'quantity': 1,
        })
        
        # Create the checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/checkout/success/'),
            cancel_url=request.build_absolute_uri('/checkout/cancel/'),
        )
        
        return JsonResponse({'id': checkout_session.id})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def checkout_success(request):
    return render(request, 'pages/checkout_success.html')


def checkout_cancel(request):
    return render(request, 'pages/checkout_cancel.html')