from django.core.management.base import BaseCommand, CommandError
import urllib2
import datetime
import re
from bs4 import BeautifulSoup
from UclaCalorieCounter import settings
from django.core.management import setup_environ
setup_environ(settings)
from Menu.models import Item

class Command(BaseCommand):

	def checkCal(self, calories):
	        if calories == None:
	                return 0
	        else:
	                return calories.next_element

	def checkNF(self, nutritionFacts):
	        if nutritionFacts == None:
	                return 0
	        else:
	                return float(nutritionFacts.group())

	#start parseLink
	def parseLink(self, name, link, meal, category, month, day, year):
	        try:
	                url = urllib2.urlopen(link)
	        except urllib2.HTTPError:
	                return
	        url = url.read()
	        soup = BeautifulSoup(url)
	        unicode(soup)
	       	str(soup)
	        soup.prettify()

	        #check certain conditions in the link to see what type of item it is. Then use beautiful soup to parse the nutrition facts and fill             the database appropriately.
	        newItem = Item()
		newItem.name = name
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

        	newItem.calories = self.checkCal(soup.find(text="Calories"))
        	newItem.fat_calories = self.checkNF(re.search("\d+\.?\d*", soup.find(class_="nffatcal").text))

        	newItem.total_fat = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Total Fat").next_element))
        	newItem.total_fat_units = re.search("[m]?[g]", soup.find(text="Total Fat").next_element).group()
        	newItem.total_fat_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Total Fat").next_element.next_element.text))
	
        	newItem.saturated_fat = self.checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Saturated Fat)"))))
        	newItem.saturated_fat_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Saturated Fat)"))).group()
        	newItem.saturated_fat_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Saturated Fat)")).next_element.text))

        	newItem.trans_fat = self.checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Trans Fat)"))))
        	newItem.trans_fat_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Trans Fat)"))).group()

        	newItem.cholesterol = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Cholesterol").next_element))
        	newItem.cholesterol_units = re.search("[m]?[g]", soup.find(text="Cholesterol").next_element).group()
        	newItem.cholesterol_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Cholesterol").next_element.next_element.text))
	
	        newItem.sodium = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Sodium").next_element))
	        newItem.sodium_units = re.search("[m]?[g]", soup.find(text="Sodium").next_element).group()
	        newItem.sodium_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Sodium").next_element.next_element.text))
	
	        newItem.total_carbs = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Total Carbohydrate").next_element))
		newItem.total_carbs_units = re.search("[m]?[g]", soup.find(text="Total Carbohydrate").next_element).group()
        	newItem.total_carbs_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Total Carbohydrate").next_element.next_element.text))
	
	        newItem.dietary_fiber = self.checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Dietary Fiber)"))))
	        newItem.dietary_fiber_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Dietary Fiber)"))).group()
	        newItem.dietary_fiber_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Dietary Fiber)")).next_element.text))
	
	        newItem.sugars = self.checkNF(re.search("\d+\.?\d*", soup.find(text=re.compile("(?=Sugars)"))))
	        newItem.sugars_units = re.search("[m]?[g]", soup.find(text=re.compile("(?=Sugars)"))).group()
	
	        newItem.protein = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Protein").next_element))
	        newItem.protein_units = re.search("[m]?[g]", soup.find(text="Protein").next_element).group()
	
	        newItem.vitamin_A_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Vitamin A").next_element.next_element.text))
	        newItem.vitamin_C_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Vitamin C").next_element.next_element.text))
	        newItem.calcium_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Calcium").next_element.next_element.text))
	        newItem.iron_dv = self.checkNF(re.search("\d+\.?\d*", soup.find(text="Iron").next_element.next_element.text))
	
	        #newItem.save()
	
	        defaults = {'calories' :newItem.calories, 'fat_calories': newItem.fat_calories, 'total_fat': newItem.total_fat, 'total_fat_units': newItem.total_fat_units, 'total_fat_dv': newItem.total_fat_dv, 'saturated_fat': newItem.saturated_fat, 'saturated_fat_units': newItem.saturated_fat_units, 'saturated_fat_dv': newItem.saturated_fat_dv, 'trans_fat': newItem.trans_fat, 'trans_fat_units': newItem.trans_fat_units, 'cholesterol': newItem.cholesterol, 'cholesterol_units': newItem.cholesterol_units, 'cholesterol_dv': newItem.cholesterol_dv, 'sodium': newItem.sodium, 'sodium_units': newItem.sodium_units, 'sodium_dv': newItem.sodium_dv, 'total_carbs': newItem.total_carbs, 'total_carbs_units': newItem.total_carbs_units, 'total_carbs_dv': newItem.total_carbs_dv, 'dietary_fiber': newItem.dietary_fiber, 'dietary_fiber_units': newItem.dietary_fiber_units, 'dietary_fiber_dv': newItem.dietary_fiber_dv, 'sugars': newItem.sugars, 'sugars_units': newItem.sugars_units, 'protein': newItem.protein, 'protein_units': newItem.protein_units, 'vitamin_A_dv': newItem.vitamin_A_dv, 'vitamin_C_dv': newItem.vitamin_C_dv, 'calcium_dv': newItem.calcium_dv, 'iron_dv': newItem.iron_dv}

	        item = Item.objects.get_or_create(name=newItem.name, restaurant=newItem.restaurant, meal=newItem.meal, category=newItem.category, month=newItem.month, day=newItem.day, year=newItem.year, defaults=defaults)

	        self.stdout.write('\n')

	def handle(self, *args, **options):
		#datetime object to keep track of what the date and time currently are
		date = datetime.datetime.today()

		#nested for loop which will traverse through the various links and parse each one using the parseLink function
		for diff in range(0, 8):
	        	d = date + datetime.timedelta(days=diff)
	        	for meal in range(1, 4):
	        	        self.stdout.write(str(d.month) + '/' + str(d.day) + '/' + str(d.year) + ': meal - ' + str(meal))
	        	        soup = BeautifulSoup(urllib2.urlopen('http://menu.ha.ucla.edu/foodpro/default.asp?date=' + str(d.month) + '%2F' + str(d.day) + '%2F' + str(d.year) + '&meal=' + str(meal) +'&threshold=1').read())
	                	unicode(soup)
	                	str(soup)
	                	soup.prettify()

	                	uls = soup.find_all(class_=re.compile("(?=menugridcell)"))

	                	for ul in uls:
	                	        if ul.find('li') is not None:
	                	                category = str(ul.find('li').text)
	                	        else:
	                	                continue
	                	        links = ul.find_all('li')
	                	        for link in links:
		                       	        link = link.find('a')
		                                if link is not None:
		                                        name = link.text
		                                        name = str(name.encode('ascii', errors='ignore'))
		                                        self.stdout.write(name)
							try:
								href = link['href']
							except KeyError:
								continue
		                                        url = "http://menu.ha.ucla.edu/foodpro/" + link['href']
		                                        self.parseLink(name, url, meal, category, d.month, d.day, d.year)
						else:
							continue
