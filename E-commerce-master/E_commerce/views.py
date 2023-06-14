from django.shortcuts import render,redirect,HttpResponse
from app.models import Category,Products,Contact_us,Order,Brand,Profile

from django.contrib.auth import authenticate,login,update_session_auth_hash
from app.models import UserCreateForm

# add to cart
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm

def master(request):
    return render(request, 'master.html')


def index(request):
    category = Category.objects.all() #all category fetch from database
    brand = Brand.objects.all()

    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')

    if categoryID:
        product = Products.objects.filter(sub_category =categoryID)

    elif brandID:
        product = Products.objects.filter(brand=brandID)

    else:
        product = Products.objects.all()


    context = {
        'category' : category,  #context dict 'category' access through html
        'product'  : product,
        'brand'    : brand,
    }
    return render(request, 'index.html',context)


def signup(request):
    if request.method == 'POST':    #post method use transfer data from client to server
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],

            )
            login(request,new_user)
            return redirect('index')
    else:                              #Method GET include all data for action like query
        form = UserCreateForm()

    context = {
        'form':form,
    }
    return render(request,'registration/signup.html',context)





# add to cart

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def Contact_Page(request):
    if request.method == 'POST':
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),

        )
        contact.save()
    return render(request,'contact.html')

def CheckOut(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        transactionId = request.POST.get('transactionId')
        cart = request.session.get('cart') #get cart value from cart
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)

        for i in cart:
            a = (int(cart[i]['price'])) #price str so convert into int
            b = cart[i]['quantity']
            total = a * b
                                     #cart data example('userid': 1, 'product_id': 1,)

            order = Order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone = phone,
                transactionId = transactionId,
                total = total,

            )
            order.save()
        request.session['cart']={}
        return redirect("index")
    return HttpResponse("checkout")


@login_required(login_url="/accounts/login/")
def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    order = Order.objects.filter(user=user) #show login user order
    context = {
        'order':order,
    }

    return render(request,'order.html',context)

def Product_Page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()

    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')

    if categoryID:
        product = Products.objects.filter(sub_category=categoryID)

    elif brandID:
        product = Products.objects.filter(brand=brandID)

    else:
        product = Products.objects.all()
    context ={
        'category': category,
        'brand' :brand,
        'product' : product,
    }
    return render(request,'product.html',context)

def Product_Detail(request,id):
    product = Products.objects.filter(id=id).first()
    context ={
        'product':product
    }
    return render(request, 'product_detail.html',context)


def Search(request):

    query = request.GET['query']  #get fron search input name
    product = Products.objects.filter(name__icontains=query) # product name filter
    context = {
        'product': product
    }
    return render(request, 'search.html',context)

def Info(request):
    return render(request,'info.html')

@login_required(login_url="/accounts/login/")
def Your_Profile(request):
    return render(request,'profile.html')

'''def UpdatePassword(request):
    if request.method=='POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            update_session_auth_hash(request,form.user)   #kon user er password hash change
            return redirect('index')
    else:
        form=PasswordChangeForm(user=request.user)

    context = {
        'form': form
        }
    return render(request,'change_pass.html',context)'''












