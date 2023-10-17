from django.db import models


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    built_in = models.BooleanField(default=True)
    seq = models.IntegerField(default=0)
    slug = models.SlugField()
    is_active = models.BooleanField(default=True)
    # main_category_id = models.ForeignKey('self', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.title
    
class ImageModel(models.Model):
    data = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    PUBLISHED_CHOICES = (
        (0, 'Not Published'),
        (1, 'Published')
    )
    name = models.CharField(max_length=70)
    profit_rate = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    is_active = models.IntegerField(choices=PUBLISHED_CHOICES, default=0)
    image_id = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    builtIn = models.BooleanField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=150)
    short_desc = models.CharField(max_length=300, blank=True, null=True)
    long_desc = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField()
    seq = models.IntegerField(default=0)
    is_new = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image_id = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    built_in = models.BooleanField(default=0)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ManyToManyField(Category)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.title


class ProductPropertyKey(models.Model):
    name = models.CharField(max_length=80)
    seq = models.IntegerField()
    built_in = models.BooleanField(default=0)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Product Property Key"
        verbose_name_plural = "Product Property Keys"
    
    def __str__(self):
        return self.name
    

class Currency(models.Model):
    code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    update_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.code
    

class Model(models.Model):
    title = models.CharField(max_length=150)
    sku = models.CharField(max_length=100)
    stock_amount = models.IntegerField()
    in_box_quantity = models.IntegerField(default=1)
    seq = models.IntegerField(default=0)
    image_id = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    built_in = models.BooleanField(default=0)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"
    
    def __str__(self):
        return self.title


class ModelPropertyValue(models.Model):
    value = models.CharField(max_length=100)
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE)
    product_property_key_id = models.ForeignKey(ProductPropertyKey, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Model Property Value"
        verbose_name_plural = "Model Property Values"
    
    def __str__(self):
        return self.value