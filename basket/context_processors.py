from .models import BasketItem


# Context processor to add the count of items in the user's basket to the template context
# This allows us to display the number of items in the basket in the header or 
# other parts of the site without having to manually pass this information from every view.

# https://docs.djangoproject.com/en/3.2/_modules/django/template/context_processors/
# https://djangocentral.com/how-to-create-custom-context-processors-in-django

def basket_item_count(request):
    if request.user.is_authenticated:
        count = BasketItem.objects.filter(
            basket__user=request.user
        ).count()
    else:
        count = 0

    return {
        "basket_item_count": count
    }
    