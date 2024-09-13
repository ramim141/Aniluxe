from pydoc import render_doc
from tkinter import E
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Review, SizeVariant
from accounts.models import Cart, CartItems

from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.db.models import Avg
from django.contrib import messages
from django.http import HttpResponseRedirect



def get_product(request, slug):
    product = Product.objects.get( slug=slug)
    reviews = product.reviews.all()  
    average_rating = product.average_rating()  
   

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
       
    }
    return render(request, 'product/product.html', context)



@login_required
def add_review(request, slug):  
    product = get_object_or_404(Product, slug=slug)  

    if request.method == 'POST':
        comment_form = ReviewForm(request.POST)
        if comment_form.is_valid():
            new_review = comment_form.save(commit=False)
            new_review.product = product  
            new_review.user = request.user  
            new_review.save()
            return redirect('get_product', slug=product.slug)
    else:
        comment_form = ReviewForm()

    #
    return render(request, 'product/product.html', {'form': comment_form, 'product': product})

 

@login_required
def add_to_cart(request, uid):
    variant = request.GET.get('variant')

    product = Product.objects.get(uid=uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItems.objects.create(cart=cart, product=product)
    if variant:
        variant = request.GET.get('vendor')
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
