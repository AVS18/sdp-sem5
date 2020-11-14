from django.urls import path
from . import views
urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('home',views.home,name='home'),
    path('addSkill',views.addSkill,name="addSkill"),
    path('catalogue',views.catalogue,name="catalogue"),
    path('filter',views.filter,name="filter"),
    path('displayChat',views.displayChat,name="displayChat"),
    path('talk/<str:rid>',views.talk,name="talk"),
    path('workAllocated',views.workAllocated,name="workAllocated"),
    path('feedback',views.feedback,name="feedback"),
    path('report',views.report,name="report")
]