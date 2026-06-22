from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish,Cart
from .forms import DishForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from decimal import Decimal
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout




def index(request):
    dishes = Dish.objects.all()
    cart = request.session.get('cart', {})
    cart = {int(k): v for k, v in cart.items()}
    return render(request, 'index.html', {'dishes': dishes, 'cart': cart})


def update_cart(request, dish_id, action):
    cart = request.session.get('cart', {})

    dish_id = str(dish_id)
    quantity = int(cart.get(dish_id, 0))

    if action == 'add':
        quantity += 1
    elif action == 'remove':
        quantity -= 1

    if quantity > 0:
        cart[dish_id] = quantity
    else:
        cart.pop(dish_id, None)

    request.session['cart'] = cart
    return JsonResponse({'status': 'ok', 'quantity': quantity})


def about(request):
    return render(request, 'about.html')

def menu(request):
    dishes = Dish.objects.all()
    return render(request, 'menu.html', {'dishes': dishes})

def contact(request):
    return render(request, 'contact.html')

def payment_done(request):
    return render(request, 'payment_done.html')

def faqs(request):
    return render(request, 'faqs.html')

def terms_conditon(request):
    return render(request, 'terms_condition.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        dish = Dish.objects.get(id=dish_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, dish=dish)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return JsonResponse({'quantity': cart_item.quantity})
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        dish = Dish.objects.get(id=dish_id)
        cart_item = Cart.objects.get(user=request.user, dish=dish)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return JsonResponse({'quantity': cart_item.quantity if cart_item.quantity > 0 else 0})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.dish.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})


def proceed_to_payment(request):
    return render(request, 'payment.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def add_to_cart(request, dish_id):
    cart = request.session.get('cart', {})
    cart[str(dish_id)] = cart.get(str(dish_id), 0) + 1
    request.session['cart'] = cart
    return redirect('kitchen:cart')  

def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})
    if str(dish_id) in cart:
        del cart[str(dish_id)]
    request.session['cart'] = cart
    return redirect('kitchen:cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for dish_id, qty in cart.items():
        dish = get_object_or_404(Dish, id=int(dish_id))
        subtotal = dish.price * qty
        items.append({'dish': dish, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'cart.html', {'items': items, 'total': total})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('kitchen:login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff_user)
def add_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kitchen:index')  # or your menu url name
    else:
        form = DishForm()
    return render(request, 'add_dish.html', {'form': form})

@login_required(login_url='/login/')
def checkout(request):
    cart = request.session.get('cart', {})
    total = 0
    for dish_id, qty in cart.items():
        dish = Dish.objects.get(id=int(dish_id))
        total += float(dish.price) * int(qty)

    if request.method == "POST":
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")

        amount_paise = int(total * 100)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        context = {
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "amount": amount_paise,
            "total_rupees": total,
            "address": address,
            "city": city,
            "pincode": pincode,
            "phone": phone
        }
        return render(request, "payment.html", context)  # 👈 ye important line hai

    return render(request, "checkout.html", {"total_rupees": total})


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')

        # verify signature
        import hmac, hashlib
        msg = razorpay_order_id + "|" + razorpay_payment_id
        generated_sig = hmac.new(settings.RAZORPAY_KEY_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()

        if generated_sig == razorpay_signature:
            # Payment is successful and verified
            # Here: create Order model row, clear session cart, render success page
            request.session['cart'] = {}
            return JsonResponse({'status': 'Payment verified'})
        else:
            return HttpResponseBadRequest('Invalid signature')
    return HttpResponseBadRequest('Invalid request')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def about_view(request):
    return render(request, 'about.html')