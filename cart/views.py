from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from cart.models import CheckOutOrder, CheckOutItem
from item.models import Item
from .forms import CheckOutForm, QuickForm
from time import *
from django.urls import reverse
import uuid
from django.db.models import F
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required


DATE = strftime("%B %d,%Y")
TIME = strftime('%I:%M:%S')

@login_required
def unseen_orders_count(request):
    count = CheckOutOrder.objects.filter(is_paid=True, is_seen=False).count()

    # Don't return anything if count is 0 or you're on /dashboard
    if count == 0 or request.path == '/dashboard/':
        return HttpResponse('')

    return HttpResponse(f"""
        <span class='absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold'>
          {count}
        </span>
    """)

@login_required
def chapa_notification(request):
    return render(request, 'cart/notification.html')

@login_required
def chapa_payment(request, order_id, total):
    order = get_object_or_404(CheckOutOrder, id=order_id)
    tx_ref = order.order_number
    data = {
        'amount': float(total),
        'currency': 'ETB',
        'email': order.email or 'example@gmail.com',
        'first_name': order.name or 'Customer',
        'phone_number': order.phone or '',
        'tx_ref': tx_ref,
        'callback_url': request.build_absolute_uri(reverse('notification')),
        'return_url': request.build_absolute_uri(reverse('confirm_checkout', args=[order.id])),
        'customization': {
            'title': f'Order_No {order.order_number}',
            'description': 'Thanks for shopping with us.'
        }
    }
    
    headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
    chapa_url = "https://api.chapa.co/v1/transaction/initialize"
    response = requests.post(chapa_url, json=data, headers=headers)
    
    if response.status_code == 200:
        print(response.json())
        payment_url = response.json()['data']['checkout_url']
        return redirect(payment_url)
    else:
        error_url = response.json()['data']
        print(error_url)
        print(f'the url is {response.json()}')
        return redirect('notification')
    
    

def order_number_generate():
    return str(uuid.uuid4())[:6].upper()


@login_required
def confirm_checkout(request, order_id):
    cart = request.session.get('cart', {})
    total = 0
    order = get_object_or_404(CheckOutOrder, id=order_id)
    checkout_items = []
    for item_id, item_data in cart.items():
        item = get_object_or_404(Item, id=int(item_id))
        quantity = item_data['quantity']
        Item.objects.filter(id=item.id).update(quantity=F('quantity') - quantity)
        subtotal = item.price * quantity
        total += subtotal 
        checkout_items.append(CheckOutItem.objects.create(
            order=order,
            item =item,
            quantity = quantity,
            subtotal = subtotal
        ))
    CheckOutOrder.objects.filter(id=order_id).update(is_paid=True)
    request.session['cart'] = {}
    context = {
        "checkout_items":checkout_items,
        "total":total,
        "date":DATE,
        "time":TIME,
        'order':order,
    }
    
    return render(request, 'cart/confirm.html', context)

@login_required
def check_out(request):
    checkout_items = []
    cart = request.session.get('cart', {})
    total = 0
    
    for item_id, item_data in cart.items():
        item = get_object_or_404(Item, id=int(item_id))
        quantity = item_data['quantity']
        subtotal = item.price * float(quantity)
        total += subtotal
        checkout_items.append({
            "item":item,
            "quantity":quantity,
            "subtotal":subtotal
        })
        
    form = CheckOutForm()
    if request.method == "POST":
        if 'quick_checkout' in request.POST:
            order = CheckOutOrder.objects.create(order_number=order_number_generate(), created_by=request.user)
            return redirect(reverse('chapa_view', args=[order.id, total]))
        form = CheckOutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_number= order_number_generate()
            order.created_by=request.user
            order.save()
            return redirect(reverse('chapa_view', args=[order.id, total]))
        else:
            form = CheckOutForm()
            return

    context = {
        'checkout_items':checkout_items,
        'total':total,
        'form':form 
    }
    
    return render(request, 'cart/checkout.html',context)
        

@login_required
def partial_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    for product_id, item_data in cart.items():
        product = Item.objects.get(id=product_id)
        total_price = product.price * float(item_data['quantity'])
        cart_items.append({
            "product":product,
            "quantity":item_data['quantity'],
            'total_price':total_price
        })    
        cart_total += total_price
    return render(request, 'cart/cart_table.html', {"cart_items":cart_items, 'cart_total':cart_total})

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', {})
    item_key = str(item_id)
    if item_key in cart:
        if item.quantity > cart[item_key]['quantity']:
            cart[item_key]['quantity'] += 1
            request.session['cart'] = cart
        else:
            return HttpResponse(status=204, headers={'HX-Trigger':'maxQuantity'})
    return partial_cart(request)

@login_required
def decrease_quantity(request, item_id):
    cart = request.session.get('cart', {})
    item_key = str(item_id)
    if item_key in cart:
        if cart[item_key]['quantity'] > 1:
            cart[item_key]['quantity'] -= 1
            request.session['cart'] = cart
        else:
            cart[item_key]['quantity'] = 1
            request.session['cart'] = cart
    return partial_cart(request)


@login_required
def remove_cart_item(request, item_id):
    cart = request.session.get('cart', {})
    item_key = str(item_id)
    if item_key in cart:
        del cart[item_key]
        request.session['cart'] = cart
    return partial_cart(request)

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    for product_id, item_data in cart.items():
        product = Item.objects.get(id=product_id)
        total_price = product.price * float(item_data['quantity'])
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'total_price': total_price
        })
        cart_total += total_price
    
    return render(request, 'cart/cart_view.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart':cart,
    })

def cart_count(request):
    count = len(request.session.get('cart', {}))
    return HttpResponse(f"{count} item{'s' if count != 1 else ''}")

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item_key = str(item_id)
    cart = request.session.get("cart", {})
    if item_key in cart:
        cart[item_key]['quantity'] += 1
    else:
        cart[item_key] = {
            'quantity':1,
            'name':item.name,
            'price':str(item.price),
            'image':item.images.url if item.images else ''
        }
    request.session['cart'] = cart
    return HttpResponse(status=204, headers={'HX-Trigger':'cartUpdated'})