from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from restaurantapp.models import Menu,AddCart,Customer,Payment,OrderPlaced,Wishlist
from django.db.models import Q
from django.contrib import messages
from .forms import CustomerProfileForm
from urllib import request
from django.views import View
import random
import razorpay
from django.contrib.auth.hashers import make_password

# Create your views here.

def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(AddCart.objects.filter(uid=request.user.id))
    return render(request,'home.html',locals())

def about(request):
    return render(request,'about.html',locals())
    
def registration(request):
    if request.method=="POST":
        uname=request.POST['uname']
        uemail=request.POST['uemail']
        umob=request.POST['umob']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        #print(uname)
        context={}
        if uname=="" or uemail=="" or umob=="" or upass=="" or ucpass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"registration.html",context)
        elif upass!=ucpass:
            context['errmsg']="Password did not match"
            return render(request,"registration.html",context)
        else:
            try:
                u=User.objects.create(password=upass,username=uemail,first_name=uname,last_name=umob)
                u.set_password(upass)
                u.save()
                context['success']="User Registered Successfully"
                return render(request,"login.html",context)
            except Exception:
                context['errmsg']="Username already exists! Try Login."
                return render(request,"registration.html",context)
    else:
        return render(request,'registration.html')

def ulogin(request):
    if request.method=="POST":
        uemail=request.POST['uemail']
        upass=request.POST['upass']
        context={}
        if uemail=="" or upass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"login.html",context)
            #print(uname)
            #print(upass)
            #return HttpResponse("Data Fetched")
        else:
            u=authenticate(username=uemail,password=upass)
            #print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid Username/Password"
                return render(request,"login.html",context)        
    else:
        return render(request,"login.html")

def ulogout(request):
    logout(request)
    return redirect('/login')

def menu(request):
    if request.user.is_authenticated:
        userid=request.user.id
        context={}
        menu=Menu.objects.filter(is_active=True)
        context['menu']=menu
        return render(request,'menu.html',context)
    else:
        return redirect('/login')

def dishes_available_category(request):
    if request.user.is_authenticated:
        userid=request.user.id
        context={}
        menu=Menu.objects.filter(menu_list=True)
        context['menu']=menu
        return render(request,'dishes_available_category.html',context)
    else:
        return redirect('/login')
    
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    menu=Menu.objects.filter(q1 & q2)
    context={}
    context['menu']=menu
    return render(request,'menu.html',context)

def menu_item_filter(request,mv):
    q1=Q(is_active=True)
    q2=Q(menu_list=mv)
    menu=Menu.objects.filter(q1 & q2)
    context={}
    context['menu']=menu
    return render(request,'menu.html',context)

def dishdetails(request,did):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(AddCart.objects.filter(uid=request.user.id))
    menu=Menu.objects.filter(id=did)
    #wishlist = Wishlist.objects.filter(Q(menu=menu) & (user=user))
    context={}
    context['menu']=menu
    return render(request,'dishdetails.html',locals())
'''
def pluswishlist(request,wpid):
    userid=request.user.id
    u=User.objects.filter(id=userid)
    menu=Menu.objects.filter(id=wpid)
    q1=Q(id=u[0])
    q2=Q(menu_id=menu[0])
    wishlist=Wishlist.objects.filter(q1 & q2)

    wishlist=Wishlist.objects.create(id=u[0],menu_id=menu[0])
    wishlist.save()
    return render(request,'dishdetails.html',locals())
'''
def add_to_cart(request,pid):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(AddCart.objects.filter(uid=request.user.id))
        userid=request.user.id
        u=User.objects.filter(id=userid)
        menu=Menu.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=menu[0])
        cart=AddCart.objects.filter(q1 & q2)
        context={}
        context['totalitem']=totalitem
        n=len(cart)
        
        if n==1:
            context['errmsg']="Product already present in Cart"
            context['menu']=menu
            return render(request,'dishdetails.html',context)
        else:
            cart=AddCart.objects.create(uid=u[0],pid=menu[0])
            cart.save()
            context['success']="Order Added to Cart!"
            context['menu']=menu
            return render(request,'dishdetails.html',context)
    else:
        return redirect('/login') 

def cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(AddCart.objects.filter(uid=request.user.id))
    cart=AddCart.objects.filter(uid=request.user.id)
    print(cart)
    context={}
    context['data']=cart
    context['totalitem']=totalitem
    amount=0
    for x in cart:
        #print(x)
        #print(x.pid.price)
        amount=amount + x.quantity * x.pid.price
        totalamount = amount + 40
        print(amount)
        context['total']=amount
        context['totalamount']=totalamount
    return render(request,"addtocart.html",context) 
'''
def remove(request):
    cart=AddCart.objects.filter(id=cid)
    cart.delete()
    return redirect('/cart')
'''

class checkout(View):
    def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem=len(AddCart.objects.filter(uid=request.user.id))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=AddCart.objects.filter(uid=request.user.id)
        famount = 0
        for p in cart_items:
            famount=famount + p.quantity * p.pid.price
        totalamount = famount + 40
        razoramount=int(totalamount * 100)
        client = razorpay.Client(auth=("rzp_test_YvjZinDbG3pKzW", "3ahukKWs5YofrX6HW2Y8cCi9"))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment_response=client.order.create(data=data)
        print(payment_response)
        #{'id': 'order_NW3F8mPZRjRkQB', 'entity': 'order', 'amount': 8000, 'amount_paid': 0, 'amount_due': 8000, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1706885698}

        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status == 'created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'checkout.html',locals())

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = AddCart.objects.filter(uid=request.user.id)
    for c in cart:
        OrderPlaced(user=user,customer=customer,menu=c.pid,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('orders')

def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(AddCart.objects.filter(uid=request.user.id))
    order_placed = OrderPlaced.objects.filter(user=request.user.id)
    return render(request,'orders.html',locals())


def updatequantity(request,qv,cid):
    c=AddCart.objects.filter(id=cid)
    print(c[0])
    print(c[0].quantity)  
    if qv=='1':
        t=c[0].quantity+1
        c.update(quantity=t)
    else:
        t=max(c[0].quantity-1,1)
        c.update(quantity=t)
    return redirect('/cart')

def show_cart(request):
    user=request.user
    cart=AddCart.objects.filter(user=user)

    return render (request,'addtocart.html',locals())

class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem=len(AddCart.objects.filter(uid=request.user.id))
        return render(request,'profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            mobile=form.cleaned_data['mobile']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            #print(uname)
            profile=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            profile.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
            return render(request,"home.html",locals()) 
        else:
            messages.warning(request,"Invalid Input Data")  
        return render(request,'profile.html',locals())

def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(AddCart.objects.filter(uid=request.user.id))
    return render(request,'address.html',locals())

class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem=len(AddCart.objects.filter(uid=request.user.id))
        return render(request,'updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.mobile=form.cleaned_data['mobile']
            add.city=form.cleaned_data['city']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")  
        return redirect('address')

def password(request):
    context={}
    c=User.objects.filter(username=request.user.username)
    # t=User.objects.get(id=request.user.id)
    # o=t.password
    
    context['data']=c
    return render(request,'change_password.html',context) 

def changepassword(request,uid):
    if request.method == 'POST':
        uname=request.POST['uname']
        passw=request.POST['passw']
        newpass=request.POST['newpass']
        confirmpass=request.POST['confrimpass']
        upass1=make_password(confirmpass)
        context={}
        c=User.objects.filter(username=request.user.username)
        u=authenticate(username=uname,password=passw)

        if passw=="" or newpass=="" or confirmpass=="" :
            context['data']=c
            context['errmsg']="Fields can not be empty"
            return render(request ,'change_password.html',context)

        elif newpass!=confirmpass:
            context['data']=c
            context['errmsg']="Password is not matching "
            return render(request ,'change_password.html',context)
        else:
            u=authenticate(username=uname,password=passw)
            if u is not None:
                m=User.objects.filter(id=uid)
                m.update(password=upass1)
                context['data']=c
                context['success']='Password updated successfully,'
                return render(request ,'passwordchangedone.html',context)   
    else:
        return redirect('/changepassword') 

def changepassworddone(request):
    return render(request,'passwordchangedone.html')


def search(request):
    query = request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
        totalitem=len(AddCart.objects.filter(uid=request.user.id))
    menu=Menu.objects.filter(Q(name__icontains=query))
    return render(request,"search.html",locals())