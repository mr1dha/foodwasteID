from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

#Function akan melakukam redirect ke landingpage saat base url diakses
def landing(request):
    return render(request=request, template_name='main/landing.html')

#Function ini hanya akan melakukan redirect ke halaman beranda user
@login_required(login_url="/login")
def homepage(request):
    return render(request=request, template_name='main/home.html')

#Function ini berfungsi untuk mendaftarkan akun user baru
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="main/register.html", context={"register_form":form})

# Function ini akan menghandle proses login user
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})

#Function ini akan melakukan logout
@login_required(login_url="/login")
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("landing")