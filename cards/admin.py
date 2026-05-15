from django.contrib import admin
from .models import Profile, RecipientType, Theme, Colour, Element, Card

# Register model in Django admin using Django's ModelAdmin register decorator:
# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#the-register-decorator

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_on")
    search_fields = ("user__email",)


@admin.register(RecipientType)
class RecipientTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipient_name",
        "recipient_type",
        "theme",
        "colour",
        "element",
        "is_paid",
        "created_on",
    )

    list_filter = (
        "recipient_type",
        "theme",
        "colour",
        "element",
        "is_paid",
        "created_on",
    )

    search_fields = (
        "user__email",
        "recipient_name",
        "message",
    )

    readonly_fields = (
        "created_on",
        "updated_on",
    )