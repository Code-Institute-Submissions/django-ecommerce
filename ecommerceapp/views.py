from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as dj_logout, authenticate, login as dj_login
from sales.models import Order, Item

# Create your views here.
def index(request):

    products = Product.objects.order_by('-created_date').filter(published=True)

    data = {
        "products":products,
        "user":request.user
    }
    return render(request,'index.html', data)

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_return = {
        'product': product
    }
    return render(request,'product.html',product_return)

def search(request):

    if 'search' in request.GET:
        filterSearch = request.GET['search']

    products = Product.objects.filter(name__icontains=filterSearch, published=True)

    data = {
        "products":products
    }
    return render(request,'search.html', data)


def register(request):
    form = UserCreationForm
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            dj_login(request, user)
            return redirect("index")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request, template_name = "register.html",  context={"form":form})

    return render(request, template_name = "register.html", context={"form":form})


def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        dj_login(request, user)
        return redirect("index")

    return render(request, template_name = "login.html")

def logout(request):
    dj_logout(request)
    return redirect("index")

def order(request, order_product_id):
    product = get_object_or_404(Product, pk=order_product_id)
    product_return = {
        'product': product
    }
    return render(request,'order.html',product_return)

def myorders(request):

    orders = Order.objects.order_by('-created_date').filter(user_id=request.user.id)

    data = {
        "orders":orders      
    }
    return render(request,'myorders.html', data)



