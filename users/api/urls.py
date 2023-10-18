from django.urls import path
from . import views


urlpatterns = [
    # Cart
    path('cart/auth/', views.ShoppingCartItemListView.as_view(), name='cart-items'),
    path('cart/auth/create', views.ShoppingCartCreateView.as_view(), name='cart-create'),
    # Offers
    path('offers/admin/', views.AdminOffersView.as_view(), name='admin-offers'),
    path('offers/<int:pk>/', views.OfferDetailView.as_view(), name='offer-detail>'),
    path('offers/admin/user/<int:id>/', views.UserOffersView.as_view(), name='user-offers'),
    path('offers/auth/', views.AuthUserOffersView.as_view(), name='auth-user-offers'),
    path('offers/<int:id>/auth/', views.AuthUserOfferDetailView.as_view(), name='auth-user-offer-details'),
    path('offers/auth/create/', views.AuthUserOffersCreateView.as_view(), name='auth-user-offers-create'),
    path('offers/admin/<int:id>/', views.AdminOfferUpdateView.as_view(), name='admin-offer-update'),
    # Users
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(("user/"), UserListAPIView.as_view(), name="user_personal"),
    path(("user/admin/"), UserListAPIView.as_view(), name="user_all"),
    path(("user/<int:id>/admin/"), UserDetailAdminView.as_view(), name="user_id_admin"),
    # Forgat Password
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
