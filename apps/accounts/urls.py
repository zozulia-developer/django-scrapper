from django.urls import path
from apps.accounts import views


urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.RegisterUserView.as_view(), name="register"),
    path('update/', views.UpdateUserView.as_view(), name="update"),
    path('delete/', views.DeleteUserView.as_view(), name="delete"),
    path('contact/', views.ContactFromView.as_view(), name="contact"),
]
