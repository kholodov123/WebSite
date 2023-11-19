from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import RegisterForm
from .models import Product, Cart, CartItem, WatchedList
from django.http import JsonResponse
import json
from django.contrib import messages
import uuid
from django.contrib.auth import authenticate, login


def index(request):
    context = {}
    return render(request, "index.html", context)


def profile(request):
    contex = {}
    return render(request, "account.html", contex)


def success(request):
    context = {}
    return render(request, "success.html", context)


def products(request):
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "products.html", context)


def registration(request):
    context = {}
    return render(request, "registration.html", context)


def about(request):
    context = {}
    return render(request, "about.html", context)


def contacts(request):
    context = {}
    return render(request, "contacts.html", context)


def policy(request):
    context = {}
    return render(request, "policy.html", context)


def cart(request):
    cart = None
    cartitems = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, complete=False)
        cartitems = cart.cartitems.all()

    context = {"cart": cart, "items": cartitems}
    return render(request, "cart.html", context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, complete=False)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        num_of_item = cart.num_of_items

    else:

        try:
            cart = Cart.objects.get(session_id=request.session['nonuser'], complete=False)
            cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_item = cart.num_of_items


        except:
            request.session['nonuser'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id=request.session['nonuser'], complete=False)
            cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cartitem.quantity += 1
            cartitem.save()
            num_of_item = cart.num_of_items

        print(cartitem)
    return JsonResponse(num_of_item, safe=False)


def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.complete = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("index")


def watch_product(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if not WatchedList.objects.filter(user=user, product=product).exists():
        WatchedList.objects.create(user=user, product=product)
        return
    redirect('product_detail', product_id=product_id)


def watched_list(request):
    user = request.user
    watched_products = WatchedList.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'watched_list.html', {'watched_products': watched_products})


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
