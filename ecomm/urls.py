
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/',views.ContactView.as_view(), name='contact'),  # ✅ Corrected
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", views.user_logout, name="logout"),
    path("forgot/", views.forgot_password, name="forgot_password"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("product/",views.product,name='product'),
    path("product_detail/<int:pid>/", views.product_detail, name="product_detail"),
    path("catfilter/<str:cv>/",views.catfilter, name="catfilter"),
    path("sortfilter/<str:sv>/",views.sortfilter, name="sortfilter"),
    path("pricefilter/",views.pricefilter, name="pricefilter"),
    path("srcfilter/",views.srcfilter, name="srcfilter"),
    path("addtocart/<int:pid>/",views.add_to_cart,name="addtocart"),
    path("cart/",views.cart,name="cart"),
    path("updateqty/<str:x>/<int:cid>/", views.updateqty, name="updateqty"),
    path("remove/<int:cid>/",views.remove, name="remove"),
    path("placeorder/",views.placeorder,name="placeorder"),
    path("fetchorder/",views.fetchorder,name="fetchorder"),
    
]
