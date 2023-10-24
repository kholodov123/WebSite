from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views

from store.views import watched_list, watch_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("store.urls")),
    path("products", views.products, name="products"),
    path("cart", views.cart, name="cart"),
    path("add_to_cart", views.add_to_cart, name="add"),
    path("confirm_payment/<str:pk>", views.confirm_payment, name="add"),
    path("watch-product/<int:product_id>/", watch_product, name="watch_product"),
    path("watched_list/", watched_list, name="watched_list"),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)