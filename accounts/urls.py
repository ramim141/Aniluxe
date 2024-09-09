from django.urls import path
from accounts.views import login_page,register_page , activate_email
from . import views

urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('logout/', views.logout_view, name='logout'),  # Logout URL
   path('activate/<email_token>/' , activate_email , name="activate_email"),
]
