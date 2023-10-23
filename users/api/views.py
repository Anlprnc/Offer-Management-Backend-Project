from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import ShoppingCart, ShoppingCartItem, Offer, OfferItem, UserProfile, Role, UserRole, Favorites, Log, Currency
from .serializers import UserProfileLoginSerializer, UserRegisterSerializer, ShoppingCartItemSerializer, OfferSerializer, OfferItemSerializer, UserSerializer, PasswordResetSerializer, UsersCartItemSerializer, FavoritesSerliazer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters
import math
from core.page_filter import pages_filter
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# ---------- Shopping Cart Views ----------    
# Shopping Cart Item List View
class ShoppingCartItemListView(ListAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        cart_items = ShoppingCartItem.objects.filter(cart_id__user_id=user)
        
        serializer = ShoppingCartItemSerializer(cart_items, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Shopping Cart Create View 
class ShoppingCartCreateView(CreateAPIView):
    serializer_class = ShoppingCartItemSerializer
    
    def perform_create(self, serializer):
        model_id = self.request.data.get('model_id')
        amount = self.request.data.get('amount')
        user = self.request.user
        
        try:
            cart_item = ShoppingCartItem.objects.get(cart_id__user_id=user, model_id=model_id)
            if amount == 0:
                cart_item.delete()
            else:
                cart_item.amount = amount
                cart_item.save()
        except ShoppingCartItem.DoesNotExist:
            if amount != 0:
                serializer.save(
                    cart_id=ShoppingCart.objects.get(user_id=user),
                    product_id=user.shoppingcart.product_id,
                    model_id=model_id,
                    amount=amount
                )
                
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# ---------- Offers Views ----------    
# Offer List View
class AdminOffersView(ListAPIView):
    serializer_class = OfferSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        status = self.request.query_params.get('status', '')
        date1 = self.request.query_params.get('date1', '')
        date2 = self.request.query_params.get('date2', '')
        
        offers = Offer.objects.all()
        
        if query:
            offers = offers.filter(
                Q(code__icontains=query) |
                Q(user_id__first_name__icontains=query) |
                Q(user_id__last_name__icontains=query)
            )
            
        if status:
            offers = offers.filter(status=status)
            
        if date1 and date2:
            offers = offers.filter(create_at__range=[date1, date2])
            
        return offers
    
# Offer Admin Detail View
class OfferAdminDetailView(RetrieveAPIView):
    serializer_class = OfferItemSerializer
    
    def retrieve(self, request, *args, **kwargs):
        offer_id = self.kwargs.get('id')
        
        try:
            offer = Offer.objects.get(id=offer_id)
            offer_items = OfferItem.objects.filter(offer_id=offer_id)
            
            serializer_data = {
                'id': offer.id,
                'code': offer.code,
                'status': offer.status,
                'items': OfferItemSerializer(offer_items, many=True).data,
                'user': {
                    'id': offer.user_id.user.id,
                    'username': offer.user_id.user.username
                }
            }
            
            return Response(serializer_data)
        except Offer.DoesNotExist:
            return Response({'error': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)
        
# User Offers View
class UserOffersView(ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        status = self.request.query_params.get('status', '')
        date1 = self.request.query_params.get('date1', '')
        date2 = self.request.query_params.get('date2', '')
        page = self.request.query_params.get('page', 1)
        size = self.request.query_params.get('size', 10)
        sort = self.request.query_params.get('sort', 'create_at')
        sort_type = self.request.query_params.get('type', 'desc')

        offers = Offer.objects.filter(user_id=user_id)

        if status:
            offers = offers.filter(status=status)

        if date1 and date2:
            offers = offers.filter(create_at__range=[date1, date2])

        if sort_type == 'desc':
            offers = offers.order_by(f'-{sort}')
        else:
            offers = offers.order_by(sort)

        start = (page - 1) * size
        end = start + size
        offers = offers[start:end]

        return offers
    
# Auth User Offers View
class AuthUserOffersView(ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('q', '')
        date1 = self.request.query_params.get('date1', '')
        date2 = self.request.query_params.get('date2', '')
        status = self.request.query_params.get('status', '')
        page = self.request.query_params.get('page', 1)
        size = self.request.query_params.get('size', 10)
        sort = self.request.query_params.get('sort', 'create_at')
        sort_type = self.request.query_params.get('type', 'desc')

        offers = Offer.objects.filter(user_id=user)

        if query:
            offers = offers.filter(code__icontains=query)

        if date1 and date2:
            offers = offers.filter(create_at__range=[date1, date2])

        if status:
            offers = offers.filter(status=status)

        if sort_type == 'desc':
            offers = offers.order_by(f'-{sort}')
        else:
            offers = offers.order_by(sort)

        start = (page - 1) * size
        end = start + size
        offers = offers[start:end]

        return offers
    
# Auth User Offers Detail View
class AuthUserOfferDetailView(RetrieveAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        user = self.request.user
        offer_id = self.kwargs.get('id')

        try:
            offer = Offer.objects.get(id=offer_id, user_id=user)
            return [offer]
        except Offer.DoesNotExist:
            return []
        
# Auth User Offers Create View
class AuthUserOffersCreateView(CreateAPIView):
    serializer_class = OfferSerializer
    
    # def get_queryset(self):
    #     user_id = self.request.user.id
    #     currency_id = self.request.data.get('currency_id')
    #     return Offer.objects.filter(user_id=user_id, currency_id=currency_id)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response
    
# Admin Offer Update View 
class AdminOfferUpdateView(UpdateAPIView):
    serializer_class = OfferSerializer
    
    def get_queryset(self):
        offer_id = self.kwargs.get('id')
        user = self.request.user
        
        try:
            offer = Offer.objects.get(id=offer_id)
            if user.userprofile.role_set.filter(role_name__in=['Sales Specialist', 'Admin']).exists():
                return [offer]
        except Offer.DoesNotExist:
            return []
        
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return response
        
# ---------- Users Views ----------
# Login View
class UserLoginView(ListAPIView):
    serializer_class = UserProfileLoginSerializer
    queryset = User.objects.all()
    def post(self, request):
        serializer = UserProfileLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Kullanıcı adı veya şifre yanlış.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Register View
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    def validate(self, attrs):
        if attrs.get("password") != attrs.get('confirmPassword'):
            raise serializers.ValidationError(
                {'password': 'Password fields did not match'})
        if attrs.get("email") is None:
            raise serializers.ValidationError(
                {'email': 'Email field cannot be empty'})
        if attrs.get("username") is None:
            raise serializers.ValidationError(
                {'username': 'Username field cannot be empty'})
        
        return attrs
    
# Forgot Password View
class PasswordResetAPIView(CreateAPIView):
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Parola sıfırlama e-postası gönderme işlemi
            PasswordResetView.as_view()(request)
            return Response({"message": "Parola sıfırlama bağlantısı e-posta adresinize gönderildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# User List View
class UserListAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["firstName", "email"]

    def get_queryset(self):
        queryset = User.objects.all()

        if self.request.path == '/user/':
            return User.objects.filter(id=self.request.user.id)
        else:
            return queryset
        
    def list(self, request, *args, **kwargs):
        if request.path.startswith('/user/auth/pages/') or request.path.startswith('/user/auth/pages'):
            return pages_filter(self, request, User, *args, **kwargs)
        return super().list(request, *args, **kwargs)

# User Detail Admin View
class UserDetailAdminView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# User Cart Item View
class UsersCartItemView(ListAPIView):
    serializer_class = UsersCartItemSerializer
    
    def get_queryset(self):
        userId = self.kwargs['pk']
        cartitems = ShoppingCartItem.objects.filter(cart__owner=userId).order_by('product__name')
        return cartitems
    
# ---------- Favorites Views ----------
# Favorites List View
class FavoritesView(RetrieveAPIView, CreateAPIView, DestroyAPIView):
    serializer_class = FavoritesSerliazer
    
    def get_queryset(self):
        user_id = self.request.user.id
        return Favorites.objects.filter(user_id=user_id)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        model_id = request.data.get('id')
        user_id = request.user.id
        
        try:
            favorite = Favorites.objects.get(product_id=model_id, user_id=user_id)
            favorite.delete()
            return Response({}, status=status.HTTTP_200_OK)
        except Favorites.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)