from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("main_app.urls", namespace="main_app")),
    path("cart/", include("main_app_cart.urls", namespace="main_app_cart")),

    path("account/", include("main_app_account.urls", namespace="main_app_account")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)