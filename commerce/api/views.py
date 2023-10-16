from datetime import timezone
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from commerce.models import Category, ImageModel, Brand, Product, ProductPropertyKey, Currency, Model, ModelPropertyValue
from .serializers import CategorySerializer, ImageModelSerializer, BrandSerializer, ProductSerializer, ProductPropertyKeySerializer, CurrencySerializer, ModelSerializer, ModelPropertyValueSerializer
from rest_framework import status
from rest_framework.response import Response
from users.models import OfferItem

# Category View
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
# Category Detail View
class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
# Image Model View    
class ImageModelListView(ListAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer
    
# Image Model Detail View    
class ImageModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer
    
# Brand View
class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Brand Detail View
class BrandDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
# Product Property Key View
class ProductPropertyKeyListView(ListAPIView):
    queryset = ProductPropertyKey.objects.all()
    serializer_class = ProductPropertyKeySerializer
    
# Currency View
class CurrencyListView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    
# Model Property Value View
class ModelPropertyValueListView(ListAPIView):
    queryset = ModelPropertyValue.objects.all()
    serializer_class = ModelPropertyValueSerializer
    
# Model Create View
class ModelCreateView(CreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    
    def create(self, request, *args, **kwargs):
        request.data['built_in'] = False
        request.data['create_at'] = timezone.now()
        
        sku = request.data.get('sku')
        if sku and Model.objects.filter(sku=sku).exists():
            return Response({'error': 'SKU already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# Model View
class ModelListView(ListAPIView):
    serializer_class = ModelSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get['pk']
        return Model.objects.filter(product_id=product_id, is_active=1)
    
# Model Detail View
class ModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in models cannot be updated."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in models cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        
        if OfferItem.objects.filter(product__model=instance).exists():
            return Response({"error": "Model has related records in offer_items table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response({'id': instance.id, 'title': instance.title})
    
#Product Create View
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
        request.data['built_in'] = False
        request.data['create_at'] = timezone.now()
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# Product View
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
# Product Detail View
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in products cannot be updated."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in products cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        
        if OfferItem.objects.filter(product=instance).exists():
            return Response({"error": "Product has related records in offer_items table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response({'id': instance.id, 'title': instance.title})
    
# Featuered Product View
class FeatueredProductListView(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.filter(is_featured=True)
    
# Product Properties Create View
class ProductPropertiesCreateView(CreateAPIView):
    queryset = ProductPropertyKey.objects.all()
    serializer_class = ProductPropertyKeySerializer
    
    def create(self, request, *args, **kwargs):
        request.data['built_in'] = False
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# Product Properties View
class ProductPropertiesListView(ListAPIView):
    serializer_class = ModelPropertyValueSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['pk']
        return ModelPropertyValue.objects.filter(model_id__product_id=product_id) 
    
# Product Properties Detail View
class ProductPropertiesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ProductPropertyKey.objects.all()
    serializer_class = ProductPropertyKeySerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in products cannot be updated."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in products cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        
        related_records = instance.modelpropertyvalue_set.all()
        if related_records.exists():
            return Response({"error": "Product has related records in model_property_value table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response({'id': instance.id, 'name': instance.name})