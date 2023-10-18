from rest_framework import serializers
from commerce.models import Category, ImageModel, Brand, Product, ProductPropertyKey, Currency, Model, ModelPropertyValue


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'is_active']
        
        
class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'
        
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        
        
class ProductPropertyKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPropertyKey
        fields = '__all__'
        

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        
        
class ModelPropertyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPropertyValue
        fields = '__all__'
        
        
class ModelSerializer(serializers.ModelSerializer):
    image_id = ImageModelSerializer()
    currency_id = CurrencySerializer()
    
    class Meta:
        model = Model
        fields = '__all__'
        
        
class ProductSerializer(serializers.ModelSerializer):
    # image_id = ImageModelSerializer()
    # brand_id = BrandSerializer()
    # category_id = CategorySerializer()
    # productpropertykey_set = ProductPropertyKeySerializer()
    # model_set = ModelSerializer()
    
    class Meta:
        model = Product
        fields = '__all__'
        
        
class FeaturedProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'categories']      
        
        
class ReportSerializer(serializers.Serializer)  :
    categories = serializers.IntegerField()
    brands = serializers.IntegerField()
    products = serializers.IntegerField()
    offers = serializers.IntegerField()
    
    
class OfferReportSerializer(serializers.Serializer):
    period = serializers.CharField()
    totalProducts = serializers.IntegerField()
    totalAmount = serializers.DecimalField(max_digits=10, decimal_places=2)