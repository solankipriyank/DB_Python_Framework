from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductMst, ProductSubCat
from django import forms

class ProductMstForm(forms.ModelForm):
    class Meta:
        model = ProductMst
        fields = ['product_name']

class ProductSubCatForm(forms.ModelForm):
    class Meta:
        model = ProductSubCat
        fields = ['product', 'product_price', 'product_image', 'product_model', 'product_ram']

def add_product(request):
    if request.method == 'POST':
        form = ProductMstForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductMstForm()
    return render(request, 'products/add_product.html', {'form': form})

def add_product_subcat(request):
    if request.method == 'POST':
        form = ProductSubCatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductSubCatForm()
    return render(request, 'products/add_product_subcat.html', {'form': form})

def product_list(request):
    products = ProductSubCat.objects.select_related('product').all()
    return render(request, 'products/product_list.html', {'products': products})

def search_products(request):
    query = request.GET.get('q')
    products = ProductSubCat.objects.select_related('product').filter(product__product_name__icontains=query)
    return render(request, 'products/product_list.html', {'products': products})

def update_product_subcat(request, sub_cat_id):
    sub_cat = get_object_or_404(ProductSubCat, pk=sub_cat_id)
    if request.method == 'POST':
        form = ProductSubCatForm(request.POST, request.FILES, instance=sub_cat)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductSubCatForm(instance=sub_cat)
    return render(request, 'products/update_product_subcat.html', {'form': form})

def delete_product_subcat(request, sub_cat_id):
    sub_cat = get_object_or_404(ProductSubCat, pk=sub_cat_id)
    if request.method == 'POST':
        sub_cat.delete()
        return redirect('product_list')
    return render(request, 'products/delete_product_subcat.html', {'sub_cat': sub_cat})
