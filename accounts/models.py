from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from products.models import Product, ColorVariant, SizeVariant
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=300 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False,cart__user = self.user).count()


class Cart(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="carts")
    is_paid = models.BooleanField(default=False)
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant.price
                price.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                price.append(size_variant_price)

        return sum(price)
            
    
# class CartItems(BaseModel):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="cart_items")
#     color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
#     size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

#     def get_product_price(self):
#         price = [self.product.price]
        
#         if self.color_variant:
#             color_variant_price = self.color_variant.price
#             price.append(color_variant_price)

#         if self.size_variant:
#             size_variant_price = self.size_variant.price
#             price.append(size_variant_price)

#         return sum(price)
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="cart_items")
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        if self.product is None:
            return 0
        
        price = self.product.price
        
        if self.color_variant:
            price += self.color_variant.price

        if self.size_variant:
            price += self.size_variant.price

        return price


@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)



class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user can only add a product to their wishlist once

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
