
import random
import time
from venv import create
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from .models import Cart, Contact, Order, Product
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import re
from django.contrib.auth.models import User
from django.core.mail import send_mail  # Correct import for email

@method_decorator(csrf_protect, name='dispatch')
class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name', '').strip()
        contact = request.POST.get('contact', '').strip()
        email = request.POST.get('email', '').strip()
        description = request.POST.get('description', '').strip()

        errors = []

        # Input validation
        if not name:
            errors.append('Name is required.')
        if not contact.isdigit() or len(contact) < 10:
            errors.append('Enter a valid contact number (at least 10 digits).')
        if '@' not in email or '.' not in email:
            errors.append('Enter a valid email address.')
        if not description:
            errors.append('Description cannot be empty.')

        # If there are errors, display them and return the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, self.template_name)

        # Try saving the contact
        try:
            Contact.objects.create(
                name=name,
                contact=contact,
                email=email,
                description=description
            )
            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')  # Make sure you have a URL named 'contact'
        except IntegrityError:
            messages.error(request, "There was a problem saving your message. Please try again.")
        except DatabaseError:
            messages.error(request, "A database error occurred. Please contact support.")

        return render(request, self.template_name)


def home(request):
    return render(request, 'home.html')


def login(request):  # Renamed to avoid conflict with django.contrib.auth.login
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        try:
            uname = request.POST.get("uname")
            uemail = request.POST.get("uemail")
            upass = request.POST.get("upass")
            ucpass = request.POST.get("ucpass")

            # Validate form data
            if not uname or not uemail or not upass or not ucpass:
                messages.error(request, "All fields are required.")
                return redirect("register")

            if upass != ucpass:
                messages.error(request, "Passwords do not match.")
                return redirect("register")

            if len(upass) < 6:
                messages.error(request, "Password must be at least 6 characters long.")
                return redirect("register")

            if not re.search(r'[A-Za-z]', upass) or not re.search(r'[0-9]', upass):
                messages.error(request, "Password must contain both letters and numbers.")
                return redirect("register")

            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already taken.")
                return redirect("register")

            if User.objects.filter(email=uemail).exists():
                messages.error(request, "Email already registered.")
                return redirect("register")

            user = User.objects.create_user(username=uname, email=uemail, password=upass)
            user.save()
            
            # Email details
            subject = "Welcome to E-commerce"
            message = (
                f"Hello {uname},\n\n"
                "Thank you for registering on our e-commerce platform. We are excited to have you on board!\n\n"
                "Best regards,\n"
                "E-commerce Team"
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [uemail]

            # Send email
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Add success message and redirect
            messages.success(request, "Registration successful! A welcome email has been sent to your email address.")
            return redirect("login")

        except IntegrityError:
            messages.error(request, "Database error. Please try again.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, "register.html")




@csrf_protect
def user_login(request):
    if request.method == "POST":
        uname = request.POST.get('uname').strip()
        upass = request.POST.get('upass').strip()

        user = authenticate(username=uname, password=upass)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect("login")

    return render(request, "login.html")



def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

def forgot_password(request):
    return render(request, "forgot.html")

from django.utils.timezone import now

otp_storage = {}
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_storage[email]= {"otp": otp}
            subject = "password reset otp - shopping kart"
            message = f""" 
Hello {user.username},
you requested a password reset. use the following OTP to reset your password:

your OTP is {otp}

This OTP is valid for 5 minutes.
Thank you for using our service.
"""
           

            # Send email
            send_mail(subject, message, settings.EMAIL_HOST_USER,[email], fail_silently=False)

            messages.success(request, "An OTP has been sent to your email address.")
            return redirect("verify_otp")  # Redirect to OTP verification page
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("forgot_password")
    return render(request, "forgot.html")


def forget_pass(request):
    if request.method == "POST":
        email = request.POST.get('email')


def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        otp = request.POST.get("otp").strip()

        if email in otp_storage:
            otp_date = otp_storage[email]
            otp_correct = otp_date["otp"]

            if str(otp) == str(otp_correct):
                messages.success(request, "OTP verified successfully! You can now reset your password.")
                return redirect("reset_password")
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect("verify_otp")
        else:
            messages.error(request, "otp expired or invalid.")
            return redirect("forgot_password")

    return render(request, "verify_otp.html")

    


otp_storage = {}

@csrf_protect
def reset_password(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")

        if (
            len(new_password) < 6 or
            not any(char.isdigit() for char in new_password) or
            not any(char.isalpha() for char in new_password)
        ):
            messages.error(request, "Password must be at least 6 characters long and contain both letters and numbers.")
            return redirect("reset_password")

        try:
            user = User.objects.get(username=uname)  # Or use `email=uname` if you're using email
            user.set_password(new_password)
            user.save()

            # Optional: remove the OTP after successful reset
            otp_storage.pop(uname, None)

            messages.success(request, "Password reset successfully. You can now log in.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "User with this username does not exist.")
            return redirect("reset_password")

    return render(request, "reset_password.html")


def product(request):
    p=Product.objects.filter(is_active=True)
    # print(p)
    context={'data':p}
    return render(request, 'product.html',context)


def product_detail(request,pid):
    p=Product.objects.filter(id=pid)
    context = {'data' : p}
    return render(request,'product_detail.html',context)

from django.db.models import Q

def catfilter(request,cv):
    q1 = Q(category=cv)
    q2 = Q(is_active=True)

    p = Product.objects.filter(q1 & q2)

    context = {'data':p}
    return render(request, 'product.html', context)

def sortfilter(request,sv):
    # print(sv,type(sv))
    if sv=='1':
        t = '-price'
    else:
        t = 'price'
    p=Product.objects.order_by(t).filter(is_active=True)
    context = {'data': p}
    return render(request, 'product.html', context)

def pricefilter(request):
    mn= request.GET['min']
    mx= request.GET['max']

    q1 = Q(price__gte = mn)
    q2 = Q(price__lte = mx)
    q3 = Q(is_active = True)

    p = Product.objects.filter(q1&q2&q3)
    context = {'data' : p}
    return render(request,'product.html', context)

def srcfilter(request):
    s = request.GET.get('search','').strip()
    pname = Product.objects.filter(name__icontains=s)
    pdet = Product.objects.filter(pdetails__icontains = s)
    alldata = pname.union(pdet)
    context = {}
    if alldata.count()==0:
        context['errmsg']='product not found'
    context['data']=alldata
    return render(request,'product.html',context)

def add_to_cart(request, pid):
    if request.user.is_authenticated:
        user= request.user
        product = Product.objects.get(id=pid)
        cart_item, created = Cart.objects.get_or_create(uid=user, pid=product)
        if not created:
            messages.error(request, "Product already in cart")
        else:
            messages.success(request, "Product added successfully")
        return redirect("cart")
    return redirect("login")

def cart(request):
    user_cart = Cart.objects.filter(uid=request.user.id)
    total_price= sum(item.pid.price * item.qty for item in user_cart)
    return render(request, "cart.html",{"data": user_cart, "total":total_price , "n":len(user_cart)})

def updateqty(request,x,cid):
    c= Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/cart')

def remove(request,cid):
    c= Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        a= i.pid.price * i.qty
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=a)
        o.save()
        i.delete()
    return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={}
    s=0
    for i in o:
        s=s+i.amt
    context['data']=o
    context['total']=s
    context['n']=len(o)
    return render(request,'placeorder.html',context)

            