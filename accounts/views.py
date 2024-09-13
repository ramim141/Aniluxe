from cmath import log
from tkinter import E
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
from .models import Profile, Cart, CartItems
from django.contrib.auth import logout
from .models import Wishlist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')

def remove_cart(request, uid):
    try:
        cart_item = CartItems.objects.get(uid = uid)
        cart_item.delete()
    except Exception as e:
        print (e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def activate_email(request , email_token):
#     try:
#         user = Profile.objects.get(email_token= email_token)
#         user.is_email_verified = True
#         user.save()
#         return redirect('/')
#     except Exception as e:
#         return HttpResponse('Invalid Email token')
def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.email_token = None  # Clear the token after verification
        user.save()
        messages.success(request, 'Your email has been verified successfully!')
        return redirect('/')
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid verification link or token.')
        return redirect('/')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return redirect('/')



def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login') 



def cart(request):
    context = {'cart': Cart.objects.filter(is_paid = False, user = request.user)}
    return render(request, 'accounts/cart.html', context)

def cart(request):
    cart_items = CartItems.objects.filter(cart__user=request.user, cart__is_paid=False)
    
 
    total_price = sum(item.get_product_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'accounts/cart.html', context)
# def cart(request):
#     cart_items = CartItems.objects.filter(cart__user=request.user, cart__is_paid=False)

#     total_price = 0
#     for item in cart_items:
#         try:
#             total_price += item.get_product_price()
#         except Exception as e:
#             print(f"Error calculating price for item {item.id}: {e}")

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }
#     return render(request, 'accounts/cart.html', context)



@login_required
def wishlist(request):
    wishlist_items = request.user.wishlist.all()
    return render(request, 'accounts/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, uid):
    product = get_object_or_404(Product, uid=uid)
    user = request.user
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
    
    if created:
        messages.success(request, 'Product added to wishlist!')
    else:
        messages.info(request, 'Product is already in your wishlist.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_from_wishlist(request, uid):
    product = get_object_or_404(Product, uid=uid)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product=product)
    wishlist_item.delete()
    
    messages.success(request, 'Product removed from wishlist!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))