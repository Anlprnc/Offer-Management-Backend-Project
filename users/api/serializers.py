from rest_framework import serializers
from users.models import UserProfile, Role, UserRole, ShoppingCart, ShoppingCartItem, Offer, OfferItem, Favorites, Log
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordResetForm


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password= serializers.CharField()
    
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),email=email,password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            attrs['user']=user
            return attrs
        else:
            raise serializers.ValidationError('Both email and password are required')
        
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "phone", "password", "confirmPassword", "birthDate", "email")

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        return attrs
    
    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
        

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        
        password_reset_form = PasswordResetForm(data=self.initial_data)
        if not password_reset_form.is_valid():
            raise serializers.ValidationError("Bu e-posta adresine sahip bir kullanıcı bulunamadı.")
        return value 
        

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=False,
        required=False,
    )
    
    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "phone", "password", "confirmPassword", "birthDate", "email")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        roles_str = data.pop('roles')
        roles_list = "".join(roles_str).replace("[", "").replace("]", "").replace("'", "")
        roles_list = roles_list.split(",")
        data['roles'] = roles_list

        return data
    
    
class UsersCartItemSerializer(serializers.ModelSerializer):
    pass


class ShoppingCartSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    user_id = UserSerializer()
    
    class Meta:
        model = ShoppingCart
        fields = ['id', 'product', 'model', 'amount']
        

class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product_id.title', read_only=True)
    model_title = serializers.CharField(source='model_id.title', read_only=True)
    
    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'product_id', 'model_id', 'amount', 'product_title', 'model_title']
                
        
class OfferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferItem
        fields = '__all__'
        
        
class OfferSerializer(serializers.ModelSerializer):
    items = OfferItemSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'code', 'status', 'sub_total', 'discount', 'user_id', 'currency_id', 'delivery_at', 'create_at', 'update_at', 'items']