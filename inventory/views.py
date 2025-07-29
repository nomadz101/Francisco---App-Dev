from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import LoginActivity
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import InventoryItem
from .forms import InventoryForm
from .forms import InventoryItemForm
from django.db.models import Sum
from django.db.models.functions import Lower, Trim

def home(request):
    return render(request, 'inventory/home.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            LoginActivity.objects.create(user=user, ip_address=request.META.get('REMOTE_ADDR'))
            return redirect('dashboard')
        else:
            return render(request, 'inventory/login.html', {'error': 'Invalid credentials'})
    return render(request, 'inventory/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'inventory/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'inventory/register.html')


def dashboard(request):
    inventory_items = InventoryItem.objects.all()
    return render(request, 'inventory/dashboard.html', {'inventory_items': inventory_items})

@login_required
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'inventory/inventory_list.html', {'items': items})

@login_required
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Add Item'})

@login_required
def inventory_update(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=item)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Edit Item'})

@login_required
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_confirm_delete.html', {'item': item})


def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_inventory_item.html', {'form': form})

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Group items by name and description and sum the quantity
    inventory_items = (
        InventoryItem.objects
        .values('name', 'description')
        .annotate(quantity_sum=Sum('quantity'))
        .order_by('name', 'description')
    )

    return render(request, 'inventory/dashboard.html', {
        'inventory_items': inventory_items
    })
