from django.db import models
from django.contrib.auth.models import User
from commerce.models import Product, Model, Currency


# Create your models here.

class UserProfile(models.Model):
    STATUS_CHOICES = [
        (0, 'pending'),
        (1, 'activated'),
        (2, 'anonymous'),
    ]
    user = models.OneToOneField(User, primary_key=True, 
                                on_delete=models.CASCADE, related_name="user")
    phone_number = models.CharField(max_length=12, verbose_name="Telefon Numarası")
    address = models.TextField(max_length=500, verbose_name="Adres")
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tax_no = models.CharField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    built_in = models.BooleanField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        
    def __str__(self):
        return self.user.username


class Role(models.Model):
    class Roles(models.TextChoices):
        CUSTOMER = 'Customer', 'Customer'
        PRODUCT_MANAGER = 'Product Manager', 'Product Manager'
        SALES_SPECIALIST = 'Sales Specialist', 'Sales Specialist'
        SALES_MANAGER = 'Sales Manager', 'Sales Manager'
        ADMIN = 'Admin', 'Admin'

    role_name = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CUSTOMER,
        unique=True
    )
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.role_name


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)  

    class Meta:
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"
        
    def __str__(self):
        return self.user_id.user.username


class ShoppingCart(models.Model):
    cartId = models.AutoField("Sepet ID",primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        
    def __str__(self):
        return self.cartId


class ShoppingCartItem(models.Model):
    cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="items")
    amount = models.DecimalField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Shopping Cart Item"
        verbose_name_plural = "Shopping Cart Items"
        
    def __str__(self):
        return self.product_id.title


class Offer(models.Model):
    STATUS_CHOICES = [
        (0, 'Created'),
        (1, 'Waiting for approval'),
        (2, 'Approved'),
        (3, 'Rejected'),
        (4, 'Pai')
    ]
    code = models.CharField(max_length=8, unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    delivery_at = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def grand_total(self):
        return self.sub_total * (1 + (self.discount / 100))
    
    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        
    def __str__(self):
        return self.code


class OfferItem(models.Model):
    sku = models.CharField(min_length=10, max_length=100)
    quantity = models.PositiveIntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)  
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2)  
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    @property
    def selling_price(self):
        return self.buying_price + (self.buying_price * self.profit_margin)
    
    class Meta:
        verbose_name = "Offer Item"
        verbose_name_plural = "Offer Items"
        
    def __str__(self):
        return self.sku


class Favorites(models.Model):
    product_id = models.ForeignKey(Product)
    user_id = models.ForeignKey(UserProfile)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        
    def __str__(self):
        return self.product_id.title


class Log(models.Model):
    log = models.CharField()
    user_id = models.ForeignKey(UserProfile)
    offer_id = models.ForeignKey(Offer)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        
    def __str__(self):
        return self.log