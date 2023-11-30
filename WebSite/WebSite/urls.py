from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views
from store.views import watched_list, watch_product

from store.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("store.urls")),
    path("products", views.products, name="products"),
    path("success", views.success, name="success"),
    path("profile", views.profile, name="profile"),
    path('register', RegisterView.as_view(), name="register"),
    path("about", views.about, name="about"),
    path("policy", views.policy, name="policy"),
    path("settings", views.settings, name="settings"),
    path("feedback", views.feedback, name="feedback"),
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
