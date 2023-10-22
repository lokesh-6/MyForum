from django.urls import path
from .views import signup,signin,update,logout

urlpatterns=[
    path("signup/",signup,name="signup"),
    path("signin/",signin,name="signin"),
    path("logout/",logout,name="logout"),
    path("update/",update,name="update"),
]