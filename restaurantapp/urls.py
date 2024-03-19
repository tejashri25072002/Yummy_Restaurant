from django.urls import path
from restaurantapp import views
from restaurant import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('about',views.about),
    path('registration',views.registration),
    path('login',views.ulogin),
    path('logout',views.ulogout),
    path('menu',views.menu),
    path('dishes_available_category',views.dishes_available_category),
    path('search',views.search,name='search'),
    path('menu_item_filter/<mv>',views.menu_item_filter),
    path('catfilter/<cv>',views.catfilter),
    path('dishdetails/<did>',views.dishdetails),
    path('add_to_cart/<pid>',views.add_to_cart),
    #path('pluswishlist/<wpid>',views.pluswishlist),
    path('cart',views.cart,name='cart'),
    #path('remove/<cid>',views.remove,name='remove_object'),
    path('updatequantity/<qv>/<cid>',views.updatequantity),
    path('checkout',views.checkout.as_view(),name='checkout'),
    path('paymentdone',views.payment_done,name='paymentdone'),
    path('orders',views.orders,name='orders'),
    path('profile',views.ProfileView.as_view(),name='profile'),
    path('address',views.address,name='address'),
    path('updateaddress/<int:pk>',views.UpdateAddress.as_view(),name='updateaddress'),
    path('changepassword/<uid>',views.changepassword,name='changepassword'),
    path('password',views.password,name='changepassword'),
    path('changepassworddone',views.changepassworddone,name='changepassworddone'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
