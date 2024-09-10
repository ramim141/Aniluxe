from django.urls import path
from . import views 

urlpatterns = [
   
    path('<slug>/' ,views.get_product , name="get_product"),
    path('product/<slug:product_slug>/add-review/', views.add_review, name='add_review'),
    
   
 
    
   
]
