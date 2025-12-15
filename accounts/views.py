from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    message = ''

    if request.method =="POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email,password=password)

            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                message = 'Invalid email or password'
    return render(request, 'accounts/login.html', {'form': form, 'message': message})
    
@login_required(login_url='login')
def dashboard_view(request):

    user = request.user
    return render(request,'accounts/dashboard.html',{'user':user})



