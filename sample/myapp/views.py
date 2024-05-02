from contextlib import redirect_stderr
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth  import authenticate,login,logout
from sample import settings
from django.core.mail import send_mail



# Create your views here.
def home(request):
    return render(request,"myapp/index.html")

def signup(request):
    if request.method == "POST":
        print("Hello")
        #username= request.POST.get('username')
        username= request.POST['username']
        fname= request.POST['fname']
        lname= request.POST['lname']
        email= request.POST['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']
        
        print(fname + lname)
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request,"Email already exist")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "username must be less than 10 character")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passowrd didnt match")
            
        if not username.isalnum():
            messages.error(request, "username must be alpha numeric")
            return redirect('home')
        
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
         
        print(fname + lname)
        
        myuser.save()
        messages.success(request, "Your Account has been Successfuly created.")
        
        #welcome email
        
        #subject='welcome to login'
        #message= "hello"+ myuser.first_name + "!! \n"+ " Welcome...\n thank you for visiting our website\n we have sent you confirmation email, please confirm your email to activate account"
        #from_email= settings.EMAIL_HOST_USER
        #to_list = [myuser.email]
        #send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect('signin')
    
    return render(request, "myapp/signup.html")   

 
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname=user.first_name
            return render(request, "myapp/index.html",{'fname':fname})
        else:
            messages.error(request, "Bad credentials!")
            return redirect('home')
            
            
    return render(request, "myapp/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')