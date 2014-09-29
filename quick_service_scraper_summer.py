import urllib2
import datetime
import re
from bs4 import BeautifulSoup
from UclaCalorieCounter import settings
from django.core.management import setup_environ
setup_environ(settings)
from Menu.models import Item

def checkCal(calories):
	if calories == None:
		return 0
	else:
		return calories.next_element

def checkNF(nutritionFacts):
	if nutritionFacts == None:
		return 0
	else:
		return float(nutritionFacts.group())

#start parseLink
def parseLink(link, restaurant):
	url = urllib2.urlopen(link).read()
	soup = BeautifulSoup(url)
	
	#check certain conditions in the link to see what type of item it is. Then use beautiful soup to parse the nutrition facts and fill 		the database appropriately.
	newItem = Item()
	newItem.name = soup.title.text
	newItem.restaurant = restaurant
	newItem.meal = "any"

	#error handling: in case of no info available on website
	if soup.find(class_="nfbox"):
		newItem.calories = checkCal(soup.find(text="Calories"))
		newItem.fat_calories = checkNF(re.search("\d+\.?\d*", soup.find(class_="nffatcal").text))

		newItem.total_fat = checkNF(re.search("\d+\.?\d*", soup.find(text="Total Fat").next_element))  
		newItem.total_fat_units = re.search("[m]?[g]", soup.find(text="Total Fat").next_element).group()
		newItem.total_fat_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Total Fat").next_element.next_element.text))

		newItem.saturated_fat = checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Saturated Fat)"))))  
		newItem.saturated_fat_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Saturated Fat)"))).group()
		newItem.saturated_fat_dv = checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Saturated Fat)")).next_element.text))

		newItem.trans_fat = checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Trans Fat)"))))
		newItem.trans_fat_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Trans Fat)"))).group()

		newItem.cholesterol = checkNF(re.search("\d+\.?\d*", soup.find(text="Cholesterol").next_element))
		newItem.cholesterol_units = re.search("[m]?[g]", soup.find(text="Cholesterol").next_element).group()
		newItem.cholesterol_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Cholesterol").next_element.next_element.text))
	
		newItem.sodium = checkNF(re.search("\d+\.?\d*", soup.find(text="Sodium").next_element))
		newItem.sodium_units = re.search("[m]?[g]", soup.find(text="Sodium").next_element).group()
		newItem.sodium_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Sodium").next_element.next_element.text))
	
		newItem.total_carbs = checkNF(re.search("\d+\.?\d*", soup.find(text="Total Carbohydrate").next_element))
		newItem.total_carbs_units = re.search("[m]?[g]", soup.find(text="Total Carbohydrate").next_element).group()
		newItem.total_carbs_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Total Carbohydrate").next_element.next_element.text))
	
		newItem.dietary_fiber = checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Dietary Fiber)"))))
		newItem.dietary_fiber_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Dietary Fiber)"))).group()
		newItem.dietary_fiber_dv = checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Dietary Fiber)")).next_element.text))
	
		newItem.sugars = checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Sugars)"))))
		newItem.sugars_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Sugars)"))).group()
	
		newItem.protein = checkNF(re.search("\d+\.?\d*", soup.find(text="Protein").next_element))
		newItem.protein_units = re.search("[m]?[g]", soup.find(text="Protein").next_element).group()

		newItem.vitamin_A_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Vitamin A").next_element.next_element.text))
		newItem.vitamin_C_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Vitamin C").next_element.next_element.text))
		newItem.calcium_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Calcium").next_element.next_element.text))
		newItem.iron_dv = checkNF(re.search("\d+\.?\d*", soup.find(text="Iron").next_element.next_element.text))

		#newItem.save()
		newItem, created = Item.objects.get_or_create(name=newItem.name, restaurant=newItem.restaurant, meal=newItem.meal, calories=newItem.calories, fat_calories=newItem.fat_calories, total_fat=newItem.total_fat, total_fat_units=newItem.total_fat_units, total_fat_dv=newItem.total_fat_dv, saturated_fat=newItem.saturated_fat, saturated_fat_units=newItem.saturated_fat_units, saturated_fat_dv=newItem.saturated_fat_dv, trans_fat=newItem.trans_fat, trans_fat_units=newItem.trans_fat_units, cholesterol=newItem.cholesterol, cholesterol_units=newItem.cholesterol_units, cholesterol_dv=newItem.cholesterol_dv, sodium=newItem.sodium, sodium_units=newItem.sodium_units, sodium_dv=newItem.sodium_dv, total_carbs=newItem.total_carbs, total_carbs_units=newItem.total_carbs_units, total_carbs_dv=newItem.total_carbs_dv, dietary_fiber=newItem.dietary_fiber, dietary_fiber_units=newItem.dietary_fiber_units, dietary_fiber_dv=newItem.dietary_fiber_dv, sugars=newItem.sugars, sugars_units=newItem.sugars_units, protein=newItem.protein, protein_units=newItem.protein_units, vitamin_A_dv=newItem.vitamin_A_dv, vitamin_C_dv=newItem.vitamin_C_dv, calcium_dv=newItem.calcium_dv, iron_dv=newItem.iron_dv)
	else:
		newItem.save()		
		return
	print soup.title.text
	print '\n'

soup = BeautifulSoup(urllib2.urlopen('http://menu.ha.ucla.edu/foodpro/bruincafe.asp').read())
links = soup.find_all("a", class_="itemlink")
for link in links:
	url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
	parseLink(url, "Bruin Cafe")

soup = BeautifulSoup(urllib2.urlopen('http://menu.ha.ucla.edu/foodpro/rendezvous.asp').read())
links = soup.find_all("a", class_="itemlink")
for link in links:
	url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
	parseLink(url, "Rendezvous")

soup = BeautifulSoup(urllib2.urlopen('http://menu.ha.ucla.edu/foodpro/cafe1919_summer.asp').read())
links = soup.find_all("a", class_="itemlink")
for link in links:
	url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
	parseLink(url, "Cafe 1919")

soup = BeautifulSoup(urllib2.urlopen('http://menu.ha.ucla.edu/foodpro/denevelatenight.asp').read())
links = soup.find_all("a", class_="itemlink")
for link in links:
	url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
	parseLink(url, "De Neve Late Night")
