import urllib2
import datetime
import re
from bs4 import BeautifulSoup
from UclaCalorieCounter import settings
from django.core.management import setup_environ
setup_environ(settings)
from Menu.models import Item

#still need to implement the helper function which will (using a loop) parse each individual nutrition facts link. Also need to parse the links for breakfast, lunch, and dinner.


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
def parseLink(link, meal, category, month, day, year):
	url = urllib2.urlopen(link).read()
	soup = BeautifulSoup(url)
	
	#check certain conditions in the link to see what type of item it is. Then use beautiful soup to parse the nutrition facts and fill 		the database appropriately.
	newItem = Item()
	newItem.name = soup.title.text
	newItem.restaurant = "Dining Hall"
	if meal == 1:
		newItem.meal = "Breakfast"
	elif meal == 2:
		newItem.meal = "Lunch"
	elif meal == 3:
		newItem.meal = "Dinner"
	newItem.category = category
	newItem.month = month
	newItem.day = day
	newItem.year = year
	#error handling: in case of no info available on website
	if soup.find(class_="rderror"):
		#newItem.save()		
		return

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

	defaults = {'calories' :newItem.calories, 'fat_calories': newItem.fat_calories, 'total_fat': newItem.total_fat, 'total_fat_units': newItem.total_fat_units, 'total_fat_dv': newItem.total_fat_dv, 'saturated_fat': newItem.saturated_fat, 'saturated_fat_units': newItem.saturated_fat_units, 'saturated_fat_dv': newItem.saturated_fat_dv, 'trans_fat': newItem.trans_fat, 'trans_fat_units': newItem.trans_fat_units, 'cholesterol': newItem.cholesterol, 'cholesterol_units': newItem.cholesterol_units, 'cholesterol_dv': newItem.cholesterol_dv, 'sodium': newItem.sodium, 'sodium_units': newItem.sodium_units, 'sodium_dv': newItem.sodium_dv, 'total_carbs': newItem.total_carbs, 'total_carbs_units': newItem.total_carbs_units, 'total_carbs_dv': newItem.total_carbs_dv, 'dietary_fiber': newItem.dietary_fiber, 'dietary_fiber_units': newItem.dietary_fiber_units, 'dietary_fiber_dv': newItem.dietary_fiber_dv, 'sugars': newItem.sugars, 'sugars_units': newItem.sugars_units, 'protein': newItem.protein, 'protein_units': newItem.protein_units, 'vitamin_A_dv': newItem.vitamin_A_dv, 'vitamin_C_dv': newItem.vitamin_C_dv, 'calcium_dv': newItem.calcium_dv, 'iron_dv': newItem.iron_dv}	
	
	item = Item.objects.get_or_create(name=newItem.name, restaurant=newItem.restaurant, meal=newItem.meal, category=newItem.category, month=newItem.month, day=newItem.day, year=newItem.year, defaults=defaults)

	print soup.title.text
	print '\n'

#datetime object to keep track of what the date and time currently are
date = datetime.datetime.today()

#nested for loop which will traverse through the various links and parse each one using the parseLink function
"""for diff in range(0, 8):
	for meal in range(1, 4):
		soup = BeautifulSoup(urllib2.urlopen('http://menu.ha.ucla.edu/foodpro/default.asp?date=' + str(d.month) + '%2F' + str(d.day + diff) + '%2F' + str(d.year) + '&meal=' + str(meal) +'&threshold=2').read())

		regularLinks = soup.find_all("a", class_="itemlink")
		veganLinks = soup.find_all("a", class_="itemlinkt")

		for link in regularLinks:
			url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
			parseLink(url, meal)

		for link in veganLinks:
			url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
			parseLink(url, meal)"""

for diff in range(0, 8):
	d = date + datetime.timedelta(days=diff)
	for meal in range(1, 4):
		print str(d.month) + '/' + str(d.day) + '/' + str(d.year) + ': meal - ' + str(meal)
		soup = BeautifulSoup(urllib2.urlopen('http://menu.ha.ucla.edu/foodpro/default.asp?date=' + str(d.month) + '%2F' + str(d.day) + '%2F' + str(d.year) + '&meal=' + str(meal) +'&threshold=2').read())

		uls = soup.find_all(class_=re.compile("(?=menugridcell)"))

		for ul in uls:
			if ul.find('li') is not None:
				category = ul.find('li').text
			else:
				continue
			links = ul.find_all('li')
			for link in links:
				print link.text
				link = link.find('a')
				if link is not None:
					url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
					parseLink(url, meal, category, d.month, d.day, d.year)

