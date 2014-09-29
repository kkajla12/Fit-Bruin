# Create your views here.
import datetime
from math import fabs

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.template import RequestContext, loader
from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.forms.util import ErrorList

from Menu.models import Item
from Menu.models import Profile
from Menu.models import FoodLog
from Menu.forms import CustomUserCreationForm, AddBreakfastForm, AddLunchForm, AddDinnerForm, AddSnacksForm, AddCafe1919Form, AddBruinCafeForm, AddRendezvousForm, AddLateNightForm, AddFeastForm, AddFreestyleForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login

d = datetime.datetime.today()
month = d.month
day = d.day
year = d.year
t = datetime.datetime.now()

#helper functions for the retrieval, modification, and calculation functions below
def getdate():
	return datetime.datetime.today()

def getmealtime():
	now = datetime.datetime.now().time()
	breakfaststart = datetime.time(0, 0, 0)
	breakfastend = datetime.time(10, 0, 0)
	lunchstart = datetime.time(10, 0, 1)
	lunchend = datetime.time(15, 0, 0)
	dinnerstart = datetime.time(15, 0, 1)
	dinnerend = datetime.time(23, 59, 59)

	if now >= breakfaststart:
		if now <= breakfastend:
			return "Breakfast"
	if now >= lunchstart:
		if now <= lunchend:
			return "Lunch"
	if now >= dinnerstart:
		if now <= dinnerend:
			return "Dinner"

def addunits(num1, unit1, num2, unit2):
	if unit2 == 'n/a':
		return num1
	elif unit1 == unit2:
		return num1 + num2
	elif unit1 == 'g' and unit2 == 'mg':
		return num1 + (num2 / 1000.0)
	elif unit1 == 'mg' and unit2 == 'g':
		return num1 + (num2 * 1000.0)

def subtractunits(num1, unit1, num2, unit2):
	if unit2 == 'n/a':
		return num1
	elif unit1 == unit2:
		return num1 - num2
	elif unit1 == 'g' and unit2 == 'mg':
		return num1 - (num2 / 1000.0)
	elif unit1 == 'mg' and unit2 == 'g':
		return num1 - (num2 * 1000.0)

def additemcalc(user, item):
	user.calories_remaining -= item.calories 
	user.total_fat_remaining = subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
	#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
	#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
	user.cholesterol_remaining = subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
	user.sodium_remaining = subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
	user.total_carbs_remaining = subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
	user.dietary_fiber_remaining = subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
	#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
	user.protein_remaining = subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
	user.vitamin_A_remaining -= item.vitamin_A_dv
	user.vitamin_C_remaining -= item.vitamin_C_dv
	user.calcium_remaining -= item.calcium_dv
	user.iron_remaining -= item.iron_dv
	user.calories_eaten += item.calories
	user.total_fat_eaten = addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
	#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
	#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
	user.cholesterol_eaten = addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
	user.sodium_eaten = addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
	user.total_carbs_eaten = addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
	user.dietary_fiber_eaten = addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
	#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
	user.protein_eaten = addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
	user.vitamin_A_eaten += item.vitamin_A_dv
	user.vitamin_C_eaten += item.vitamin_C_dv
	user.calcium_eaten += item.calcium_dv
	user.iron_eaten += item.iron_dv
	return

def removeitemcalc(user, item):
	user.calories_remaining += item.calories 
	user.total_fat_remaining = addunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
	#user.saturated_fat_remaining = addunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
	#user.trans_fat_remaining = addunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
	user.cholesterol_remaining = addunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
	user.sodium_remaining = addunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
	user.total_carbs_remaining = addunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
	user.dietary_fiber_remaining = addunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
	#user.sugars_remaining = addunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
	user.protein_remaining = addunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
	user.vitamin_A_remaining += item.vitamin_A_dv
	user.vitamin_C_remaining += item.vitamin_C_dv
	user.calcium_remaining += item.calcium_dv
	user.iron_remaining += item.iron_dv
	user.calories_eaten -= item.calories
	user.total_fat_eaten = subtractunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
	#user.saturated_fat_eaten = subtractunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
	#user.trans_fat_eaten = subtractunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
	user.cholesterol_eaten = subtractunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
	user.sodium_eaten = subtractunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
	user.total_carbs_eaten = subtractunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
	user.dietary_fiber_eaten = subtractunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
	#user.sugars_eaten = subtractunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
	user.protein_eaten = subtractunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
	user.vitamin_A_eaten -= item.vitamin_A_dv
	user.vitamin_C_eaten -= item.vitamin_C_dv
	user.calcium_eaten -= item.calcium_dv
	user.iron_eaten -= item.iron_dv
	return

#retrieval, modification, and calculation functions that perform operations needed by the view functions
def getmenu(rstrnt):
	return Item.objects.filter(restaurant=rstrnt)

def getmealmenu(rstrnt, which_meal):
	return Item.objects.filter(restaurant=rstrnt, meal=which_meal)

def getuseritems(username):
	return User.objects.get(username=username).profile.items

def getuser(username):
	return User.objects.get(username=username).profile

def additemtoprofile(user, item):
	additemcalc(user.profile, item)
	user.profile.save()
	user.save()

def removeitemfromprofile(user, item):
	removeitemcalc(user.profile, item)
	user.save()
	user.profile.save()

def createnutrition(user_profile, age, gender, height, weight, activity, goal):
	activity_mult = 1	
	if activity == "Lightly Active":
		activity_mult = 1.2
	elif activity == "Active":
		activity_mult = 1.375
	elif activity == "Very Active":
		activity_mult = 1.55
	elif activity == "Varsity Athlete":
		activity_mult = 1.9

	cal_cut = 0
	portions = [ .50, .25, .25 ]
	if goal == "Gain Muscle":
		cal_cut = -500
		portions = [ .40, .40, .20 ]
	elif goal == "Lose 1lb/Week":
		cal_cut = 500
		portions = [ .45, .35, .20 ]
		
	if gender == "Male":
		user_profile.calories_limit = (activity_mult * (88.362 + ((13.397 * (weight / 2.20462)) + (4.799 * (height * 2.54)) - (5.677 * age)))) - cal_cut
		user_profile.calories_remaining = user_profile.calories_limit
		user_profile.total_carbs_limit = (portions[0] * user_profile.calories_limit) / 4
		user_profile.total_carbs_remaining = user_profile.total_carbs_limit
		user_profile.protein_limit = (portions[1] * user_profile.calories_limit) / 4
		user_profile.protein_remaining = user_profile.protein_limit
		user_profile.total_fat_limit = (portions[2] * user_profile.calories_limit) / 9
		user_profile.total_fat_remaining = user_profile.total_fat_limit
		user_profile.dietary_fiber_limit = 38
		user_profile.dietary_fiber_remaining = user_profile.dietary_fiber_limit
		user_profile.save()
	elif gender == "Female":
		user_profile.calories_limit = (activity_mult * (447.593 + ((9.247 * (weight / 2.20462)) + (3.098 * (height * 2.54)) - (4.33 * age)))) - cal_cut
		user_profile.calories_remaining = user_profile.calories_limit
		user_profile.total_carbs_limit = (portions[0] * user_profile.calories_limit) / 4
		user_profile.total_carbs_remaining = user_profile.total_carbs_limit
		user_profile.protein_limit = (portions[1] * user_profile.calories_limit) / 4
		user_profile.protein_remaining = user_profile.protein_limit
		user_profile.total_fat_limit = (portions[2] * user_profile.calories_limit) / 9
		user_profile.total_fat_remaining = user_profile.total_fat_limit
		user_profile.dietary_fiber_limit = 38
		user_profile.dietary_fiber_remaining = user_profile.dietary_fiber_limit
		user_profile.save()
	else:
		print age, gender, height, weight, activity_level
		print "gender not entered"

#view functions
def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/profile")
	else:
		return render_to_response("home.html", {
			'user': request.user,
		})

def newuser(request):
	if request.method == 'POST':
        	form = CustomUserCreationForm(request.POST)
        	if form.is_valid():
			new_user, new_user_profile = form.save()
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password1"]
			createnutrition(new_user_profile, new_user_profile.age, new_user_profile.gender, new_user_profile.height, new_user_profile.weight, new_user_profile.activity_level, new_user_profile.weight_goal)
			new_user = authenticate(username=username, password=password)
			if request.user.is_authenticated():		
				login(request, new_user)
			return HttpResponseRedirect("/profile/")

	args = {}
	args.update(csrf(request))
	
	args['form'] = CustomUserCreationForm()

	return render_to_response("newuser.html", args)

def profile(request):
	if request.user.is_authenticated():
		user = request.user
		recentitems = FoodLog.objects.filter(profile=user.profile, date=getdate().date())[:5]
		template = loader.get_template('Menu/profile.html')
		context = RequestContext(request, {
			'user': user,
			'recentitems' : recentitems,
		})
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect("/accounts/login/")

def foodlog(request):
	if request.user.is_authenticated():
		user = request.user
		items = user.profile.items.all()
		breakfast = FoodLog.objects.filter(profile=user.profile, meal="Breakfast", date=getdate().date())
		lunch = FoodLog.objects.filter(profile=user.profile, meal="Lunch", date=getdate().date())
		dinner = FoodLog.objects.filter(profile=user.profile, meal="Dinner", date=getdate().date())
		snacks = FoodLog.objects.filter(profile=user.profile, meal="Snacks", date=getdate().date())
		
		return render_to_response("foodlog.html", {
			'user': user,
			'items': items,
			'breakfast': breakfast,
			'lunch': lunch,
			'dinner': dinner,
			'snacks': snacks,
		})
	else:
		return HttpResponseRedirect("/accounts/login/")

def additem(request):
	if request.user.is_authenticated():
		user = request.user
		template = loader.get_template('Menu/additem.html')
		context = RequestContext(request, {
			'user': user,
		})
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect("/accounts/login/")

def toptens(request):
	date = datetime.datetime.today()
	month = date.month
	day = date.day
	year = date.year
	mostfatbreakfast = Item.objects.filter(meal="Breakfast", month=month, day=day, year=year).order_by('-total_fat')[:10]
	mostcaloriesbreakfast = Item.objects.filter(meal="Breakfast", month=month, day=day, year=year).order_by('-calories')[:10]
	mostproteinbreakfast = Item.objects.filter(meal="Breakfast", month=month, day=day, year=year).order_by('-protein')[:10]
	mostfatlunch = Item.objects.filter(meal="Lunch", month=month, day=day, year=year).order_by('-total_fat')[:10]
	mostcalorieslunch = Item.objects.filter(meal="Lunch", month=month, day=day, year=year).order_by('-calories')[:10]
	mostproteinlunch = Item.objects.filter(meal="Lunch", month=month, day=day, year=year).order_by('-protein')[:10]
	mostfatdinner = Item.objects.filter(meal="Dinner", month=month, day=day, year=year).order_by('-total_fat')[:10]
	mostcaloriesdinner = Item.objects.filter(meal="Dinner", month=month, day=day, year=year).order_by('-calories')[:10]
	mostproteindinner = Item.objects.filter(meal="Dinner", month=month, day=day, year=year).order_by('-protein')[:10]
	mostfatfeast = Item.objects.filter(restaurant="Feast at Rieber", month=month, day=day, year=year).order_by('-total_fat')[:10]
	mostcaloriesfeast = Item.objects.filter(restaurant="Feast at Rieber", month=month, day=day, year=year).order_by('-calories')[:10]
	mostproteinfeast = Item.objects.filter(restaurant="Feast at Rieber", month=month, day=day, year=year).order_by('-protein')[:10]
	mostfatcafe1919 = Item.objects.filter(restaurant="Cafe 1919").order_by('-total_fat')[:10]
	mostcaloriescafe1919 = Item.objects.filter(restaurant="Cafe 1919").order_by('-calories')[:10]
	mostproteincafe1919 = Item.objects.filter(restaurant="Cafe 1919").order_by('-protein')[:10]
	mostfatrendezvous = Item.objects.filter(restaurant="Rendezvous").order_by('-total_fat')[:10]
	mostcaloriesrendezvous = Item.objects.filter(restaurant="Rendezvous").order_by('-calories')[:10]
	mostproteinrendezvous = Item.objects.filter(restaurant="Rendezvous").order_by('-protein')[:10]
	mostfatbruincafe = Item.objects.filter(restaurant="Bruin Cafe").order_by('-total_fat')[:10]
	mostcaloriesbruincafe = Item.objects.filter(restaurant="Bruin Cafe").order_by('-calories')[:10]
	mostproteinbruincafe = Item.objects.filter(restaurant="Bruin Cafe").order_by('-protein')[:10]
	mostfatlatenight = Item.objects.filter(restaurant="De Neve Late Night").order_by('-total_fat')[:10]
	mostcalorieslatenight = Item.objects.filter(restaurant="De Neve Late Night").order_by('-calories')[:10]
	mostproteinlatenight = Item.objects.filter(restaurant="De Neve Late Night").order_by('-protein')[:10]
	template = loader.get_template('Menu/toptens.html')
	context = RequestContext(request, {
		'user': request.user,
		'mostfatbreakfast': mostfatbreakfast,
		'mostcaloriesbreakfast': mostcaloriesbreakfast,
		'mostproteinbreakfast': mostproteinbreakfast,
		'mostfatlunch': mostfatlunch,
		'mostcalorieslunch': mostcalorieslunch,
		'mostproteinlunch': mostproteinlunch,	
		'mostfatdinner': mostfatdinner,
		'mostcaloriesdinner': mostcaloriesdinner,
		'mostproteindinner': mostproteindinner,
		'mostfatbruincafe': mostfatbruincafe,
		'mostcaloriesbruincafe': mostcaloriesbruincafe,
		'mostproteinbruincafe': mostproteinbruincafe,
		'mostfatcafe1919': mostfatcafe1919,
		'mostcaloriescafe1919': mostcaloriescafe1919,
		'mostproteincafe1919': mostproteincafe1919,	
		'mostfatrendezvous': mostfatrendezvous,
		'mostcaloriesrendezvous': mostcaloriesrendezvous,
		'mostproteinrendezvous': mostproteinrendezvous,
		'mostfatlatenight': mostfatlatenight,
		'mostcalorieslatenight': mostcalorieslatenight,
		'mostproteinlatenight': mostproteinlatenight,
		'mostfatfeast': mostfatfeast,
		'mostcaloriesfeast': mostcaloriesfeast,
		'mostproteinfeast': mostproteinfeast,
	})
	return HttpResponse(template.render(context))

def mostpopular(request):
	items = FoodLog.objects.all().order_by('-portion')[:15]
	return render_to_response("mostpopular.html", items)

def about(request):
	return render_to_response("about.html", { 'user': request.user })

def viewitem(request, itemid):
	item = Item.objects.get(id=itemid)
	return render_to_response("viewitem.html", { 'item': item })

def updateportion(request, foodlogid, portion):
	if request.is_ajax():
		try:
			foodlog = FoodLog.objects.get(pk=foodlogid)
		except FoodLog.DoesNotExist:
			raise Http404
		portion = int(portion)
		if portion <= 0:
			return HttpResponse()
		portiondiff = portion - foodlog.portion
		foodlog.portion = portion
		foodlog.save()
		if portiondiff == 0:
			return HttpResponse()
		elif portiondiff > 0:
			for i in range(int(fabs(portiondiff))):
				additemtoprofile(request.user, foodlog.item)
		elif portiondiff < 0:
			for i in range(int(fabs(portiondiff))):
				removeitemfromprofile(request.user, foodlog.item)
		return HttpResponse()
	else:
		return HttpResponseNotFound('<h1><center>404: Page not found</center></h1>')

def deletefoodlog(request, foodlogid):
	if request.is_ajax():
		try:
			foodlog = FoodLog.objects.get(pk=foodlogid)
		except FoodLog.DoesNotExist:
			raise Http404
		user = request.user
		for i in range(foodlog.portion):
			removeitemfromprofile(user, foodlog.item)
		foodlog.delete()
		return HttpResponse()
	else:
		return HttpResponseNotFound('<h1><center>404: Page not found</center></h1>')
	
def addbreakfast(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddBreakfastForm(request.POST, user=request.user, datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddBreakfastForm(datetime=getdate())
		args['date'] = getdate().date()

		return render_to_response("addbreakfast.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addlunch(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddLunchForm(request.POST, user=request.user, datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddLunchForm(datetime=getdate())
		args['date'] = getdate().date()

		return render_to_response("addlunch.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def adddinner(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddDinnerForm(request.POST, user=request.user, datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddDinnerForm(datetime=getdate())
		args['date'] = getdate().date()

		return render_to_response("adddinner.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addsnacks(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddSnacksForm(request.POST, user=request.user, meal=getmealtime(), datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddSnacksForm(meal=getmealtime(), datetime=getdate())
		args['date'] = getdate().date()
		args['meal'] = getmealtime()

		return render_to_response("addsnacks.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addfeastlunch(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddFeastForm(request.POST, user=request.user, meal="Lunch", datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddFeastForm(meal="Lunch", datetime=getdate())
		args['date'] = getdate().date()
		args['meal'] = getmealtime()

		return render_to_response("feastlunch.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addfeastdinner(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddFeastForm(request.POST, user=request.user, meal="Dinner", datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddFeastForm(meal="Dinner", datetime=getdate())
		args['date'] = getdate().date()
		args['meal'] = getmealtime()

		return render_to_response("feastdinner.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addcafe1919(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddCafe1919Form(request.POST, user=request.user, meal=getmealtime(), datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddCafe1919Form(meal=getmealtime(), datetime=getdate())
		args['date'] = getdate().date()
		args['meal'] = getmealtime()

		return render_to_response("addcafe1919.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")
def addbruincafe(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddBruinCafeForm(request.POST, user=request.user, meal=getmealtime(), datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddBruinCafeForm(meal=getmealtime(), datetime=getdate())
		args['date'] = getdate().date()
		args['meal'] = getmealtime()

		return render_to_response("addbruincafe.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addrendezvous(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddRendezvousForm(request.POST, user=request.user, meal=getmealtime(), datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddRendezvousForm(meal=getmealtime(), datetime=getdate())
		args['date'] = getdate().date()
		args['meal'] = getmealtime()

		return render_to_response("addrendezvous.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addlatenight(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = AddLateNightForm(request.POST, user=request.user, meal=getmealtime(), datetime=getdate())
			if form.is_valid():
				print "form is valid"
				print form.cleaned_data
				added_items = form.save()
			return HttpResponseRedirect("/foodlog/")
		args = {}
		args.update(csrf(request))
	
		args['user'] = request.user
		args['form'] = AddLateNightForm(meal=getmealtime(), datetime=getdate())
		args['date'] = getdate().date()
		args['meal'] = getmealtime()

		return render_to_response("addlatenight.html", args)
	else:
		return HttpResponseRedirect("/accounts/login/")

def addfreestyle(request):
        if request.user.is_authenticated():
                if request.method == 'POST':
                        form = AddFreestyleForm(request.POST, user=request.user, meal=getmealtime(), datetime=getdate())
                        if form.is_valid():
                                print "form is valid"
                                print form.cleaned_data
                                added_items = form.save()
                        return HttpResponseRedirect("/foodlog/")
                args = {}
                args.update(csrf(request))

                args['user'] = request.user
                args['form'] = AddFreestyleForm(meal=getmealtime(), datetime=getdate())
                args['date'] = getdate().date()
                args['meal'] = getmealtime()

                return render_to_response("freestyle.html", args)
        else:
                return HttpResponseRedirect("/accounts/login/")

def DiningHalls(request):
	template = loader.get_template('Menu/DiningHalls.html')
	context = RequestContext(request, {
		'breakfast': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', month=month, day=day, year=year),
		'lunch': Item.objects.filter(restaurant='Dining Hall', meal='Lunch', month=month, day=day, year=year),
		'dinner':Item.objects.filter(restaurant='Dining Hall', meal='Dinner', month=month, day=day, year=year),
	})
	return HttpResponse(template.render(context))

def Breakfast(request):
	template = loader.get_template('Menu/Breakfast.html')
	context = RequestContext(request, {
		'Soups': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Soups', month=month, day=day, year=year),
		'Prepared_Salads': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Prepared Salads', month=month, day=day, year=year),
		'Exhibition_Kitchen': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Exhibition Kitchen', month=month, day=day, year=year),
		'Euro_Kitchen': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Euro Kitchen', month=month, day=day, year=year),
		'Pizza_Oven': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Pizza Oven', month=month, day=day, year=year),
		'Grill': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Grill', month=month, day=day, year=year),
		'Hot_Food_Bar': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Hot Food Bar', month=month, day=day, year=year),
		'From_the_Bakery': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='From the Bakery', month=month, day=day, year=year),
		'Soups_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Soups', month=month, day=day, year=year).count(),
		'Prepared_Salads_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Prepared Salads', month=month, day=day, year=year).count(),
		'Exhibition_Kitchen_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Exhibition Kitchen', month=month, day=day, year=year).count(),
		'Euro_Kitchen_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Euro Kitchen', month=month, day=day, year=year).count(),
		'Pizza_Over_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Pizza Oven', month=month, day=day, year=year).count(),
		'Grill_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Grill', month=month, day=day, year=year).count(),
		'Hot_Food_Bar_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='Hot Food Bar', month=month, day=day, year=year).count(),
		'From_the_Bakery_count': Item.objects.filter(restaurant='Dining Hall', meal='Breakfast', category='From the Bakery', month=month, day=day, year=year).count(),
	})
	return HttpResponse(template.render(context))

def Cafe1919(request):
	itemsList = Item.objects.filter(restaurant="Cafe 1919")
	template = loader.get_template('Menu/Cafe1919.html')
	context = RequestContext(request, {
		'itemsList': itemsList,	
	})
	return HttpResponse(template.render(context))
