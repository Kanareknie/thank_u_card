from django.urls import path
from  accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('account/', views.account_view, name='account'),
]
