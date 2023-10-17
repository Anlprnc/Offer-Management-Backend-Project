from django.urls import path
from . import views


urlpatterns = [
    # ----- Products -----
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/properties/', views.ProductPropertiesCreateView.as_view(), name='product-properties-create'),
    path('products/<int:pk>/properties/', views.ProductPropertiesListView.as_view(), name='product-properties-list'),
    path('products/featured/', views.FeatueredProductListView.as_view(), name='featured-product-list'),
    path('products/properties/<int:pk>/', views.ProductPropertiesDetailView.as_view(), name='product-properties-detail'),
    path('products/models/', views.ModelCreateView.as_view(), name='product-model-create'),
    path('products/models/<int:pk>/', views.ModelDetailView.as_view(), name='product-model-detail'),
    path('products/<int:pk>/models/', views.ModelListView.as_view(), name='product-model-list'),
    # ----- Category -----
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/products/', views.CategoryProductsView.as_view(), name='category-products'),
    
    path('images/', views.ImageModelListView.as_view(), name='image-model-list'),
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('propertykeys/', views.ProductPropertyKeyListView.as_view(), name='property-key-list'),
    path('currencies/', views.CurrencyListView.as_view(), name='currency-list'),
    path('propertyvalues/', views.ModelPropertyValueListView.as_view(), name='property-value-list'),
    path('models/', views.ModelListView.as_view(), name='model-list'),
]
