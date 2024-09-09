from pydoc import render_doc
from tkinter import E
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Review

from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

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


@login_required
def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('get_product', slug=product_slug)
    else:
        form = ReviewForm()
    
    return render(request, 'product/add_review.html', {'form': form, 'product': product})