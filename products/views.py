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
# def get_product(request , slug):
#     try:
#         product = Product.objects.get(slug =slug)
#         return render(request  , 'product/product.html' , context = {'product' : product})

#     except Exception as e:
#         print(e)

# views.py


def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()  # Fetch reviews related to the product
    average_rating = product.average_rating()  # Get average rating

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
    }
    return render(request, 'product/product.html', context)


# @login_required
# def add_review(request, product_slug):
#     product = get_object_or_404(Product, slug=product_slug)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.product = product
#             review.user = request.user
#             review.save()
#             return redirect('get_product', slug=product_slug)
#     else:
#         form = ReviewForm()

#     return render(request, 'product/add_review.html', {'form': form, 'product': product})
# @login_required
# def add_review(request, product_slug):
#     product = get_object_or_404(Product, slug=product_slug)

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.product = product
#             review.user = request.user
#             review.save()
#             messages.success(request, "Your review has been submitted successfully!")
#             return redirect('get_product', slug=product_slug)
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = ReviewForm()

#     context = {
#         'form': form,
#         'product': product,
#     }

#     return render(request, 'product/product.html', context)
@login_required
def add_review(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.body = request.POST["body"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.product = product
                data.save()
                return redirect("product/product.html", id)
        else:
            form = ReviewForm()
        return render(request, "product/product.html", {'form': form})
    else:
        return redirect("login")


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
