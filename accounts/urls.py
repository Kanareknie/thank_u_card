from django.urls import path
from  accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('account/', views.account_view, name='account'),
    path(
        'account/download/<int:card_id>/',
        views.download_card_pdf,
        name='download_card_pdf'
    ),
    
]
