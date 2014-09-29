from django.core.management.base import BaseCommand, CommandError
from UclaCalorieCounter import settings
from django.core.management import setup_environ
setup_environ(settings)
from Menu.models import Item, FoodLog, Profile
from django.contrib.auth.models import User
import datetime

class Command(BaseCommand):

	def handle(self, *args, **options):
		date = datetime.datetime.today().date()

		users = User.objects.exclude(is_superuser=True)
		for user in users:
			self.stdout.write(user.username)
        		if user.username == "admin":
               			continue
	       		if user.username == "AdminAllie":
	                	continue
	        	user.profile.calories_eaten = 0
	        	user.profile.calories_remaining = user.profile.calories_limit

	        	user.profile.total_fat_eaten = 0
	        	user.profile.total_fat_remaining = user.profile.total_fat_limit

	        	user.profile.sodium_eaten = 0
	        	user.profile.sodium_remaining = user.profile.sodium_limit
	
	        	user.profile.dietary_fiber_eaten = 0
	        	user.profile.dietary_fiber_remaining = user.profile.dietary_fiber_limit
	
	        	user.profile.cholesterol_eaten = 0
	        	user.profile.cholesterol_remaining = user.profile.cholesterol_limit
	
	        	user.profile.total_carbs_eaten = 0
	        	user.profile.total_carbs_remaining = user.profile.total_carbs_limit
	
	        	user.profile.protein_eaten = 0
	        	user.profile.protein_remaining = user.profile.protein_limit

	        	user.profile.vitamin_A_eaten = 0
	        	user.profile.vitamin_A_remaining = user.profile.vitamin_A_limit
	
	        	user.profile.vitamin_C_eaten = 0
	        	user.profile.vitamin_C_remaining = user.profile.vitamin_C_limit

	        	user.profile.calcium_eaten = 0
	        	user.profile.calcium_remaining = user.profile.calcium_limit
	
	        	user.profile.iron_eaten = 0
	        	user.profile.iron_remaining = user.profile.iron_limit
	
	        	user.profile.save()
	        	user.save()

		foodlogs = FoodLog.objects.exclude(date=date).delete()
		items = Item.objects.filter(restaurant="Dining Hall", day=date.day, month=date.month, year=date.year).delete()
		self.stdout.write('User Data Reset')
