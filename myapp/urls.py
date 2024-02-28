from django.urls import path
from django.contrib import admin
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('findbus', views.findbus, name="findbus"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('about',views.about,name="about"),
    path('TC',views.TC),
    path('pp',views.pp),
    path('contact',views.contact,name="contact"),

]
