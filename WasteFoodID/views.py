from django.shortcuts import  render, redirect
from .forms import NewUserForm, WasteFoodCreate

from .models import WasteFoodID

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from pprint import pprint
from datetime import datetime
from calendar import monthrange

#Function akan melakukam redirect ke landingpage saat base url diakses
def landing(request):
    return render(request=request, template_name='main/landing.html')

#Function ini hanya akan melakukan redirect ke halaman beranda user
@login_required(login_url="/login")
def homepage(request):
	return render(request, 'main/home.html')

@login_required(login_url="/login")
def calculator(request):
    return render(request=request, template_name='main/calculator.html')

@login_required(login_url="/login")
def history(request):
	if request.method == "POST":
		my = request.POST['waste_date']
		my = my.split("-")
		y = int(my[0])
		m = int(my[1])

		waste = WasteFoodID.objects.filter(month=m, year=y, user_id=request.user.id)
		res = []

		for day in range(1, number_of_days_in_month(y,m)+1):
			res.append(0)

		for w in waste:
			res[int(w.day)-1] += w.weight

		if m < 10:
			m = "0"+str(m)

		return render(request=request, template_name='main/history.html', context={"datas":res, "mon": m, "year" : y})
	else:
		d = datetime.now().day
		m = datetime.now().month
		y = datetime.now().year
		
		waste = WasteFoodID.objects.filter(month=m, year=y, user_id=request.user.id)
		res = []

		for day in range(1, number_of_days_in_month(y,m)+1):
			res.append(0)

		for w in waste:
			res[int(w.day)-1] += w.weight

		return render(request=request, template_name='main/history.html', context={"datas":res})

@login_required(login_url="/login")
def upload_waste(request):

	if request.method == 'POST':
		post_values = request.POST.copy()
		post_values['user_id'] = request.user.id;
		upload = WasteFoodCreate(post_values)
		upload.save()
		return redirect('homepage')

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
		return render (request=request, template_name="main/register.html", context={"register_form":form})
	form = NewUserForm()
	pprint(form.errors)
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
			return render(request=request, template_name="main/login.html", context={"login_form":form})

	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})

#Function ini akan melakukan logout
@login_required(login_url="/login")
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("landing")


def number_of_days_in_month(year=2019, month=2):
    return monthrange(year, month)[1]