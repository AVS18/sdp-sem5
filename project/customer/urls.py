
from django.urls import path
from . import views
urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('home',views.home,name='home'),
    path('catalogue',views.catalogue,name="catalogue"),
    path('filter',views.filter,name="filter"),
    path('startChat/<str:customer_id>/<str:worker_id>',views.startChat,name="startChat"),
    path('displayChat',views.displayChat,name="displayChat"),
    path('talk/<str:rid>',views.talk,name="talk"),
    path('acceptWork/<str:id>',views.acceptWork,name="acceptWork"),
    path('rejectWork/<str:id>',views.rejectWork,name="rejectWork"),
    path('workAllocated',views.workAllocated,name="workAllocated"),
    path('feedback',views.feedback,name="feedback"),
    path('report',views.report,name="report")
]