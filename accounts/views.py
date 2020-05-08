from django.shortcuts import render, redirect

from accounts.filters import OrderFilter
from accounts.forms import OrderForm, CreateUserForm, CustomerForm, AddTagsForm, AddProductForm, SetNumberForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import login_required
from accounts.models import *
from django.forms import inlineformset_factory, formset_factory
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for User ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'UserName or Password Incorrect')
    context = {}
    return render(request, 'accounts/login.html')


def logOutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    # customer_order = Order.objects.filter(customer=request.customer_order).count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        # 'customer_order': customer_order
    }
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customers_details = Customer.objects.get(id=pk)
    orders = customers_details.order_set.all()
    customer_order = orders.count()
    customer_filter = OrderFilter(request.GET, queryset=orders)
    orders = customer_filter.qs
    context = {
        'customer_details': customers_details,
        'orders': orders,
        'total_orders': customer_order,
        'customer_filter': customer_filter,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    all_product = Product.objects.all()
    all_tags = Tags.objects.all()
    context = {
        'all_product': all_product,
        'all_tags': all_tags
    }
    return render(request, 'accounts/product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):

    number = 1
    set_order_number = SetNumberForm()
    if request.method == 'GET':
        set_order_number = SetNumberForm(request.GET)
        if set_order_number.is_valid():
            number = set_order_number.cleaned_data['order_number']
        else:
            set_order_number = SetNumberForm()

    orderformfet = inlineformset_factory(Customer, Order, fields=('product', 'status', 'note'), extra=number)  # instance of formset
    customer_order = Customer.objects.get(id=pk)
    formset = orderformfet(queryset=Order.objects.none(), instance=customer_order)
    # form = OrderForm(initial={'customer': customer_order})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = orderformfet(request.POST, instance=customer_order)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {
        'formset': formset, 'order_number': set_order_number
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('home')

    context = {'item': item}
    return render(request, 'accounts/delete_order.html', context)


# view for user profile dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'delivered': delivered,
               'pending': pending,
               'total_orders': total_orders
               }
    return render(request, 'accounts/user.html', context)


# view for customer settings
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.error(request, 'There is error in form submission')
    context = {'form': form}
    return render(request, 'accounts/customer_settings.html', context)


def addTags(request):
    num = 1
    set_tag_num = SetNumberForm()
    if request.method == 'GET':
        set_tag_num = SetNumberForm(request.GET)
        if set_tag_num.is_valid():
            num = set_tag_num.cleaned_data['order_number']
        else:
            set_tag_num = SetNumberForm()

    TagFormSet = formset_factory(AddTagsForm, extra=num)
    formset = TagFormSet()
    if request.method == 'POST':
        formset = TagFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
                messages.success(request, 'Tags added Successfully')
                return redirect('product')
    context = {'formset': formset, 'tag_num': set_tag_num}
    return render(request, 'accounts/add_product.html', context)


def addProduct(request):
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added Successfully')
            # return redirect('product')
        else:
            form = AddProductForm()
            messages.error(request, "Error in Form Submission")
    context = {'form': form}
    return render(request, 'accounts/add_product.html', context)


def deleteProduct(request, pk):
    item = Product.objects.get(id=pk)
    item2 = Tags.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        item2.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('product')
    context = {'item': item, 'item2': item2}
    return render(request, 'accounts/delete_product.html', context)


def deleteTags(request, pk):
    item = Tags.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Tag deleted successfully')
        return redirect('product')
    context = {'item': item}
    return render(request, 'accounts/delete_product.html', context)