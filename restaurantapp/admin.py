from django.contrib import admin
from restaurantapp.models import Menu,Customer,Payment,OrderPlaced

# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display=['id','name','price','description','cat','is_active']
    list_filter=['cat','price','is_active']
admin.site.register(Menu,MenuAdmin)

admin.site.register(Payment)

admin.site.register(OrderPlaced)