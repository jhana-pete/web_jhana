from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
import re
from django.contrib import messages
from django.db.models import Q
import json 
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    return render(request, 'index.html')


def is_valid_username(username):
    pattern = r'^[a-z]+\.[a-z]+$'  # Regular expression pattern for the desired username format
    return re.match(pattern, username)

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if not is_valid_username(username):
                     messages.error(request, "Invalid username format. Please use the format u.muuma.")
            else:
                user = form.save()
                messages.info(request, f"Hello {user.get_username()}, your registration was successfull")                
                return redirect('login_view')
        else:
            messages.error(request, "Form is not valid")
        
    q = request.GET.get("username")
    if q:
        user = User.objects.filter(username = q).exists()
        if user == True:
            return HttpResponse(json.dumps({"message":"Username already taken up"}))
        return HttpResponse(json.dumps({"message":"Username is valid"}))
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if not is_valid_username(username):
                     messages.error(request, "Invalid username format. Please use the format u.muuma.")
            else:
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_admin:
                    login(request, user)
                    return redirect('adminpage')
                elif user is not None and user.is_student:
                    login(request, user)
                    return redirect('student')
                elif user is not None and user.is_employee:
                    login(request, user)
                    return redirect('employee')
                else:
                     messages.error(request, "Please provide valid credentials")
            context = {
                 }
        else:
            msg = 'Error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

@login_required
def complaint_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        email = request.POST.get('email')
        category_name = request.POST.get('categories')
        description = request.POST.get('description')

        submitted_by = request.user   #  Current logged-in user and Assign the current user as the submitted_by value
        category, created = Category.objects.get_or_create(name=category_name)

        # Get the email address from the form
        #email = form.cleaned_data['email']

        # Send notification email
        subject = 'New Complaint Submitted'
        message = 'A new complaint has been submitted. Please review it.'
        from_email = '2001200069@muni.ac.ug'
        to_email = ['umarmawejje16@gmail.com', 'umarmuteeganya16@gmail.com']
        send_mail(subject, message, from_email, to_email)



        complaint = Complaint(title=title, email=email, category=category, description=description)
        complaint.save()
                
        messages.info(request, f"Hello  {submitted_by.get_username()}, Complaint Submitted Successfully!! Thank you for submitting your complaint. We will review it shortly.")
        return redirect('student')
    
    return render(request,'complaint_form.html')


def complaint_list(request):
    complaints = Complaint.objects.all()  # Retrieve all complaints from the database
    context = {'complaints': complaints}

    return render(request, 'complaint_list.html', {'complaints': complaints})

def admin(request):
    return render(request,'admin.html')

@login_required
def student(request):
    user_complaints = Complaint.objects.filter(submitted_by=request.user)  # Retrieve complaints submitted by the current user
    context = {'complaints': user_complaints}
    return render(request, 'student.html', context)

def employee(request):
    complaints = Complaint.objects.all()  # Retrieve all complaints from the database
    context = {'complaints': complaints}


    return render(request,'employee.html', context)

