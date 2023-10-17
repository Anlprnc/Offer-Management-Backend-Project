from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(ImageModel)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductPropertyKey)
admin.site.register(Currency)
admin.site.register(Model)
admin.site.register(ModelPropertyValue)