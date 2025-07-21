from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="root"),
    path("home/", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("cart/", views.cart_view, name="cart"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("checkout/cancel/", views.checkout_cancel, name="checkout_cancel"),
]