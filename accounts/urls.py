from django.urls import path
from accounts.views import login_page, register_page, activate_email, logout_view, cart,remove_cart, add_to_wishlist, remove_from_wishlist, wishlist
from products.views import add_to_cart

urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('logout/', logout_view, name='logout'),  # Logout URL
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   path('add_to_cart/<uid>/', add_to_cart, name = "add_to_cart"),
   path('cart/', cart, name = 'cart'),
   path('remove-cart/<uid>/', remove_cart, name = 'remove_cart'),
   path('wishlist/add/<uid>/', add_to_wishlist, name='add_to_wishlist'),
   path('wishlist/remove/<uid>/', remove_from_wishlist, name='remove_from_wishlist'),
   path('wishlist/', wishlist, name='wishlist'),
   
]
