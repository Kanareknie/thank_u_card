from django.http import HttpResponse


def google_site_verification(request):
    return HttpResponse(
        "google-site-verification: googlef4d17be882e1d42b.html",
        content_type="text/html",
    )
    
def google_site_verification_2(request):
    return HttpResponse(
    "google-site-verification: googlec94b0d1d7d47336b.html",
    content_type="text/html",
    )