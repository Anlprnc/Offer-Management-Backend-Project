from django.urls import path
from .views import UserRegisterView, UserLoginView, ShoppingCartItemListView, ShoppingCartCreateView, AdminOffersView, OfferAdminDetailView, UserOffersView, AuthUserOffersView, AuthUserOfferDetailView, AuthUserOffersCreateView, AdminOfferUpdateView, FavoritesView, UserListAPIView, UserDetailAdminView
from django.contrib.auth import views


urlpatterns = [
    # Cart
    path('cart/auth/', ShoppingCartItemListView.as_view(), name='cart-items'),
    path('cart/auth/create', ShoppingCartCreateView.as_view(), name='cart-create'),
    # Offers
    path('offers/admin/', AdminOffersView.as_view(), name='admin-offers'),
    path('offers/<int:id>/', OfferAdminDetailView.as_view(), name='offer-detail>'),
    path('offers/admin/user/<int:id>/', UserOffersView.as_view(), name='user-offers'),
    path('offers/auth/', AuthUserOffersView.as_view(), name='auth-user-offers'),
    path('offers/<int:id>/auth/', AuthUserOfferDetailView.as_view(), name='auth-user-offer-details'),
    path('offers/auth/create/', AuthUserOffersCreateView.as_view(), name='auth-user-offers-create'),
    path('offers/admin/<int:id>/', AdminOfferUpdateView.as_view(), name='admin-offer-update'),
    # Users
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path(("user/"), UserListAPIView.as_view(), name="user_personal"),
    path(("user/admin/"), UserListAPIView.as_view(), name="user_all"),
    path(("user/<int:id>/admin/"), UserDetailAdminView.as_view(), name="user_id_admin"),
    # Favorites
    path('favorites/auth/', FavoritesView.as_view(), name='favorites'),
    # Forgat Password
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
