from django.urls import path, include

from .views import *
from django.urls import path

urlpatterns = [
    path('register/', user_register,name='user_register'),
    path('logout/', user_logout,name='user_logout'),
    path('user-edit-profile/', user_edit_profile,name='user_edit_profile'),
    path('user-change-password/', user_change_password,name='user_change_password'),
    path('user-upload-photo/', user_upload_photo,name='user_upload_photo'),
    path('login/', user_login,name='user_login'),
    path('<username>/', user_profile, name='user_profile')

]