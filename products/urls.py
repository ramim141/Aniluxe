from django.urls import path
from . import views 

urlpatterns = [
   
    path('<slug>/' ,views.get_product , name="get_product"),
    path('addreview/<int:id>/',views.add_review,name="add_review"),
    
   
 
    
   
]
