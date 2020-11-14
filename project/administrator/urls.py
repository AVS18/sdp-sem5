
from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home, name="home"),
    path('reports',views.reports,name="reports"),
    path('catalogue',views.catalogue,name="catalogue"),
    path('feedback',views.feedback,name="feedback"),
    path('block',views.block,name="block"),
    path('site',views.site,name="site"),
    path('filter',views.filter,name="filter"),
    path('email',views.email,name="email")
]
