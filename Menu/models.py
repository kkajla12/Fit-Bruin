from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Item(models.Model):
	name = models.CharField(max_length=150)

	restaurant = models.CharField(max_length=35)

	meal = models.CharField(max_length=35)

	category = models.CharField(max_length=35, default="n/a")
	
	month = models.IntegerField(default=0)

	day = models.IntegerField(default=0)

	year = models.IntegerField(default=0)

	calories = models.IntegerField(default=0)

	fat_calories = models.IntegerField(default=0)

	total_fat = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	total_fat_units = models.CharField(max_length=3, default="n/a")
	total_fat_dv = models.IntegerField(default=0)

	saturated_fat = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	saturated_fat_units = models.CharField(max_length=3, default="n/a")
	saturated_fat_dv = models.IntegerField(default=0)

	trans_fat = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	trans_fat_units = models.CharField(max_length=15, default="n/a")

	cholesterol = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	cholesterol_units = models.CharField(max_length=3, default="n/a")
	cholesterol_dv = models.IntegerField(default=0)

	sodium = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	sodium_units = models.CharField(max_length=3, default="n/a")
	sodium_dv = models.IntegerField(default=0)

	total_carbs = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	total_carbs_units = models.CharField(max_length=3, default="n/a")
	total_carbs_dv = models.IntegerField(default=0)

	dietary_fiber = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	dietary_fiber_units = models.CharField(max_length=3, default="n/a")
	dietary_fiber_dv = models.IntegerField(default=0)

	sugars = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	sugars_units = models.CharField(max_length=3, default="n/a")

	protein = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	protein_units = models.CharField(max_length=3, default="n/a")

	vitamin_A_dv = models.DecimalField(default=0, max_digits=8, decimal_places=2)

	vitamin_C_dv = models.DecimalField(default=0, max_digits=8, decimal_places=2)

	calcium_dv = models.DecimalField(default=0, max_digits=8, decimal_places=2)

	iron_dv = models.DecimalField(default=0, max_digits=8, decimal_places=2)

	#times_selected = models.IntegerField(null=False)

	def __unicode__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User)

	GENDER_CHOICES = (
			('Male', 'Male'),
			('Female','Female'),
	)

	ACTIVITY_CHOICES = (
			('Lightly Active','Lightly Active'),
			('Active','Active'),
			('Very Active','Very Active'),
			('Varsity Athlete','Varsity Athlete'),
	)

	GOAL_CHOICES = (
		('Maintain Weight', 'Maintain Weight'),
		('Gain Muscle', 'Gain Muscle'),
		('Lose 1lb/Week', 'Lose 1lb/Week')
	)

	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
	age = models.IntegerField(default=0)
	weight = models.IntegerField(default=0)
	height = models.IntegerField(default=0)
	activity_level = models.CharField(max_length=15, choices=ACTIVITY_CHOICES)
	weight_goal = models.CharField(max_length=15, choices=GOAL_CHOICES)

	calories_limit = models.IntegerField(default=0)
	calories_eaten = models.IntegerField(default=0)
	calories_remaining = models.IntegerField(default=0)

	total_fat_limit = models.DecimalField(default=65, max_digits=8, decimal_places=2)
	total_fat_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	total_fat_remaining = models.DecimalField(default=65, max_digits=8, decimal_places=2)
	total_fat_units = models.CharField(max_length=3, default="g")	
	
	sodium_limit = models.DecimalField(default=2300, max_digits=8, decimal_places=2)
	sodium_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	sodium_remaining = models.DecimalField(default=2300, max_digits=8, decimal_places=2)
	sodium_units = models.CharField(max_length=3, default="mg")

	dietary_fiber_limit = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	dietary_fiber_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	dietary_fiber_remaining = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	dietary_fiber_units = models.CharField(max_length=3, default="g")

	cholesterol_limit = models.DecimalField(default=300, max_digits=8, decimal_places=2)
	cholesterol_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	cholesterol_remaining = models.DecimalField(default=300, max_digits=8, decimal_places=2)
	cholesterol_units = models.CharField(max_length=3, default="mg")
	
	total_carbs_limit = models.DecimalField(default=130, max_digits=8, decimal_places=2)
	total_carbs_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	total_carbs_remaining = models.DecimalField(default=130, max_digits=8, decimal_places=2)
	total_carbs_units = models.CharField(max_length=3, default="g")
	
	protein_limit = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	protein_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	protein_remaining = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	protein_units = models.CharField(max_length=3, default="g")
	
	vitamin_A_limit = models.DecimalField(default=100, max_digits=8, decimal_places=2)
	vitamin_A_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	vitamin_A_remaining = models.DecimalField(default=100, max_digits=8, decimal_places=2)

	vitamin_C_limit = models.DecimalField(default=100, max_digits=8, decimal_places=2)
	vitamin_C_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	vitamin_C_remaining = models.DecimalField(default=100, max_digits=8, decimal_places=2)
	
	calcium_limit = models.DecimalField(default=100, max_digits=8, decimal_places=2)
	calcium_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	calcium_remaining = models.DecimalField(default=100, max_digits=8, decimal_places=2)

	iron_limit = models.DecimalField(default=100, max_digits=8, decimal_places=2)
	iron_eaten = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	iron_remaining = models.DecimalField(default=100, max_digits=8, decimal_places=2)

	items = models.ManyToManyField(Item, through='FoodLog', blank=True)

	def __unicode__(self):
		return self.user.username

class FoodLog(models.Model):
	item = models.ForeignKey(Item)
	profile = models.ForeignKey(Profile)
	portion = models.IntegerField(default=1, blank=True)
	meal = models.CharField(max_length=9)
	date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return unicode(self.profile)

class Post(models.Model):
        title = models.CharField(max_length=255)
        slug = models.SlugField(unique=True, max_length=255)
        description = models.CharField(max_length=255)
        content = models.TextField()
        published = models.BooleanField(default=True)
        created = models.DateTimeField(auto_now_add=True)
     
        class Meta:
            ordering = ['-created']
     
        def __unicode__(self):
            return u'%s' % self.title
     
        def get_absolute_url(self):
            return reverse('blog.views.post', args=[self.slug])
