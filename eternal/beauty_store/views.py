from django.shortcuts import render
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from .utils import cookieCart, cartData
from django.http import JsonResponse
# Create your views here.

def index(request):

    return render(request, 'beauty_store/index.html')

def about(request):
    return render(request, 'beauty_store/about.html')

def blog(request):
    return render(request, 'beauty_store/blog.html')

def blogs(request):
    return render(request, 'beauty_store/blogs.html')

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'beauty_store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'beauty_store/checkout.html', context)


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'beauty_store/contact.html', {'thank': thank})




def cosmetic(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'beauty_store/cosmetic.html', context)

def cosmetics(request):
    return render(request, 'beauty_store/cosmetics.html')

def fragrance(request):
    return render(request, 'beauty_store/fragrance.html')

def news(request):
    return render(request, 'beauty_store/news.html')

def skincare(request):
    return render(request, 'beauty_store/skincare.html')

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create ( customer=customer, complete=False )

    orderItem, created = OrderItem.objects.get_or_create(order= order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer    
        order, created = Order.objects.get_or_create ( customer=customer, complete=False )


        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')
        print('COOKIES:', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customer.objects.get_or_create(
            email=email,
        )
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer = customer,
            complete=False,
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity=item['quantity'],
            )

        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address= data['shipping']['address'],
            city= data['shipping']['city'],
            state= data['shipping']['state'],
            zipcode= data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)


    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create ( customer=customer, complete=False )
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete!', safe=False)

