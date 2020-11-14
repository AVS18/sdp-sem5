
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('contact',views.contact,name='contact'),
    path('register',views.register,name='register'),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('changeProfilePic',views.changeProfilePic,name='changeProfilePic'),
    path('setNewPassword',views.setNewPassword,name="setNewPassword"),
    path('validateOtp',views.validateOtp,name="validateOtp"),
    path('changePassword',views.changePassword,name="changePassword"),
    path('profile',views.profile,name="profile"),
    path('contactSupport',views.contactSupport,name="contactSupport")
]
