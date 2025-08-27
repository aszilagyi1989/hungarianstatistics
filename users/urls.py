from django.urls import path, include
from users.views import home, landing, login_view, signup_view

urlpatterns = [
    path('', landing, name='landing'),  # Landing page (accessible without login)
    path('home2/', home, name='home2'),   # Home page (requires login)
    path('userlogin/', login_view, name='userlogin'),
    path('usersignup/', signup_view, name='usersignup'),
    path('social-auth/', include('social_django.urls', namespace='social')),
   
]