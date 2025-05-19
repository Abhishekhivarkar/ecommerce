# from pyclbr import Class
# from django.shortcuts import render
# from django.views import View 
# from django.views.decorators.csrf import csrf_protect
# from django.utils.decorators import method_decorator
# from django.db import IntegrityError, DatabaseError
# from django.contrib import messages
# from django.shortcuts import redirect
# from . models import contact



# @method_decorator(csrf_protect, name='dispatch')
# class ContactView(View):
#     template_name = 'contact.html'
#     def get(self,request):
#         return render(request, self.template_name)

# def contact(request):
#     return render(request,'contact.html')

# from django.shortcuts import render, redirect
# from django.views import View 
# from django.views.decorators.csrf import csrf_protect
# from django.utils.decorators import method_decorator
# from django.db import IntegrityError, DatabaseError
# from django.contrib import messages
# from .models import contact  # assuming your model is named `contact`, but consider renaming to `Contact`

def home(request):
    return render(request, 'home.html')

# @method_decorator(csrf_protect, name='dispatch')
# class ContactView(View):
#     template_name = 'contact.html'

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         name = request.POST.get('name')
#         contact_number = request.POST.get('contact')  # renamed to avoid shadowing model
#         email = request.POST.get('email')
#         description = request.POST.get('description')

#         if not all([name, contact_number, email, description]):
#             messages.error(request, "All fields are required.")
#             return render(request, self.template_name)

#         try:
#             contact.objects.create(
#                 name=name,
#                 contact=contact_number,
#                 email=email,
#                 description=description
#             )
#             messages.success(request, "Your message has been sent successfully.")
#             return redirect('home')
#         except IntegrityError:
#             messages.error(request, "There was a problem saving your message. Please try again.")
#         except DatabaseError:
#             messages.error(request, "A database error occurred. Please contact support.")

#         return render(request, self.template_name)

# from copy import error
# from django.shortcuts import render, redirect
# from django.views import View 
# from django.views.decorators.csrf import csrf_protect
# from django.utils.decorators import method_decorator
# from django.db import IntegrityError, DatabaseError
# from django.contrib import messages
# from .models import Contact  # assuming your model is named `contact`, but consider renaming to `Contact`

# @method_decorator(csrf_protect, name='dispatch')
# class ContactView(View):
#     template_name = 'contact.html'

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         name = request.POST.get('name').strip()
#         contact = request.POST.get('contact').strip()
#         email = request.POST.get('email').strip()
#         description = request.POST.get('description')
        
#         errors = []
#         if not name:
#             errors.append('name is required')
#         if not contact.isdigit() or len(contact) < 10:
#             errors.append(' Enter a valid contact number( at least 10 digits)')
#         if "@" not in email or "." not in email:
#             errors.append("enter a valid email address")
#         if not description:
#             errors.append("Description cannot be empty")

#         # if not all([name, contact, email, description]):
#         #     messages.error(request, "All fields are required.")
#         #     return render(request, self.template_name)
#         if errors:
#             for errors in errors:
#                 messages.error(request,error)
#             return render(request,self.template_name)
#         Contact.objects.create(name=name,contact=contact,email=email,description=description)
#         try:
#             Contact.objects.create(
#                 name=name,
#                 contact=contact,
#                 email=email,
#                 description=description
#             )
#             messages.success(request, "Your message has been sent successfully.")
#             return redirect('contact')
#         except IntegrityError:
#             messages.error(request, "There was a problem saving your message. Please try again.")
#         except DatabaseError:
#             messages.error(request, "A database error occurred. Please contact support.")
#         except Exception as e:
#             messages.error(request, f"An unexpected error occurred: {str(e)}")
#         return render(request, self.template_name)
    
    

#         return render(request, self.template_name)
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from .models import Contact  # Ensure your model is correctly named `Contact`
from django.contrib.auth import authenticate, login
# from django.conf import settings
import re
from django.contrib.auth.models import User


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

def register(request):
    return render(request,'register.html')
def login(request):
    return render(request,'login.html')


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('uname')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')  # replace 'home' with your homepage URL name
#         else:
#             messages.error(request, 'Invalid username or password')

#     return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')  # Matches the input name
        password = request.POST.get('upass')  # Changed from 'password' to 'upass'

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')  # Updated template path


import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.utils import IntegrityError

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validate form fields manually for additional checks
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect("register")

        if not re.search(r'[A-Za-z]', password1) or not re.search(r'[0-9]', password1):
            messages.error(request, "Password must contain both letters and numbers.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = email  # manually add email to user object
                user.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect("login")
            except IntegrityError:
                messages.error(request, "Database error. Please try again.")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, "register.html", {"form": form})

    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
