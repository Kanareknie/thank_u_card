"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cards.views import home, edit_card
from accounts.views import (
    register, 
    CustomLoginView, 
    CustomLogoutView, 
    account_view,
    account_card_preview,
    add_saved_card_to_basket,
    delete_saved_card,
    
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core.views import google_site_verification, google_site_verification_2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basket/', include('basket.urls')), 
    path('payments/', include('payments.urls')),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('account/', account_view, name='account'),
    path('account/preview/<int:card_id>/', account_card_preview, name='account_card_preview'),
    path('account/add-to-basket/<int:card_id>/', add_saved_card_to_basket, name='add_saved_card_to_basket'),
    path('account/delete/<int:card_id>/', delete_saved_card, name='delete_saved_card'),
    path("accounts/", include("allauth.urls")),
    path('cards/edit/<int:card_id>/', edit_card, name='edit_card'),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path(
        "googlef4d17be882e1d42b.html",
        google_site_verification,
        name="google_site_verification",
    ),
    path(
        "googlec94b0d1d7d47336b.html",
        google_site_verification_2,
        name="google_site_verification_2",
    ),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
