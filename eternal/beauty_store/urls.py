from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="store"),
    path('beauty_store/about', views.about, name="about"),
    path('beauty_store/blog', views.blog, name="blog"),
    path('beauty_store/blogs', views.blogs, name="blogs"),
    path('beauty_store/cart', views.cart, name="cart"),
    path('beauty_store/checkout', views.checkout, name="checkout"),
    path('beauty_store/contact', views.contact, name="contact"),
    path('beauty_store/cosmetic', views.cosmetic, name="cosmetic"),
    path('beauty_store/cosmetics', views.cosmetics, name="cosmetics"),
    path('beauty_store/fragrance', views.fragrance, name="fragrance"),
    path('beauty_store/news', views.news, name="news"),
    path('beauty_store/skincare', views.skincare, name="skincare"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]