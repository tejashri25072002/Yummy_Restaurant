from django.db import models
from django.contrib.auth.models import User
#AbstractUser

# Create your models here.

'''
class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
'''
class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images')  # Assuming image storage
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()  # Assuming a numerical rating system
    CAT=((1,'Breakkfast'),(2,'Lunch'),(3,'Dinner'),(4,'Beverages'),(5,'Anytime'))
    cat=models.IntegerField(verbose_name="category",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    MENU_LIST=((1,'Appetizers'),
               (2,'Soups'),
               (3,'Bread and Rice'),
               (4,'Curries'),
               (5,'Tandoori Specialties'),
               (6,'Vegetarian Main Courses'),
               (7,'Non-Vegetarian Main Courses'),
               (8,'Desserts'),
               (9,'Beverages'))
    menu_list = models.IntegerField(verbose_name="Menu List",choices=MENU_LIST,default=1)

class AddCart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Menu,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    zipcode=models.IntegerField()
    STATE_CHOICES=(('Maharashtra','Maharashtra'),
                   ('Gujarat','Gujarat'),
                   ('MadhyaPradesh','MadhyaPradesh'),
                   ('Hariyana','Hariyana'),
                   ('Panjab','Panjab'))
    state=models.CharField(choices=STATE_CHOICES,max_length=100)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,db_column="cust_id")
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES=(('Accepted','Accepted'),
                    ('On the Way','On the Way'),
                    ('Delivered','Delivered'),
                    ('Cancel','Cancel'),
                    ('Pending','Pending'))
    status=models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default=None, null=True)

    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)

