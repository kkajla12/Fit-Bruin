from django.contrib.auth.models import User
from Menu.models import Profile, Item, FoodLog
from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ModelMultipleChoiceField
from itertools import chain
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import datetime

d = datetime.datetime.today()
t = datetime.datetime.now()
month = d.month
day = d.day
year = d.year
hour = t.hour
minute = t.minute
second = t.second

class CustomUserCreationForm(UserCreationForm):
	GENDER_CHOICES = (
			('Male', 'Male'),
			('Female','Female')
	)
	
	ACTIVITY_CHOICES = (
			('Lightly Active','Lightly Active'),
			('Active','Active'),
			('Very Active','Very Active'),
			('Varsity Athlete','Varsity Athlete'),
	)
	
	gender = forms.ChoiceField(GENDER_CHOICES)
	age = forms.IntegerField()
	weight = forms.IntegerField()
	height = forms.IntegerField(label='Height (inches)')
	activity_level = forms.ChoiceField(ACTIVITY_CHOICES)

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'gender', 'age', 'weight', 'height')
	
	def save(self, commit=True):
		if not commit:
			raise NotImplementedError("Can't create User and Profile without database save")		
		user = super(UserCreationForm, self).save(commit=True)
		user.set_password(self.cleaned_data["password1"])
		user.save()
		profile = Profile(user=user, gender=self.cleaned_data["gender"], age=self.cleaned_data["age"], weight=self.cleaned_data["weight"], height=self.cleaned_data["height"], activity_level=self.cleaned_data["activity_level"])
		profile.save()
		return user, profile
		
class ItemMultipleChoiceField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return obj.name

class CustomSelectMultiple(widgets.CheckboxSelectMultiple):
	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = []
		has_id = attrs and 'id' in attrs
		final_attrs = self.build_attrs(attrs, name=name)
		output = []
		# Normalize to strings
		str_values = set([force_text(v) for v in value])
		for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
		    # If an ID attribute was given, add a numeric index as a suffix,
		    # so that the checkboxes don't all have the same ID attribute.
		    if has_id:
		        final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
		        label_for = format_html(' for="{0}"', final_attrs['id'])
		    else:
		        label_for = ''

		    cb = widgets.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
		    option_value = force_text(option_value)
		    rendered_cb = cb.render(name, option_value)
		    option_label = force_text(option_label)
		    output.append(format_html('<tr class="success">'))
		    output.append(format_html('<td><label{0}>{1} {2}</label></td>',
		                              label_for, rendered_cb, option_label))
		    output.append(format_html('</tr>'))
		return mark_safe('\n'.join(output))

class AddBreakfastForm(forms.Form):
	soups = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	prepared_salads = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	sandwich_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	exhibition_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	euro_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	pizza_oven = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	grill = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	hot_food_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	from_the_bakery = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddBreakfastForm, self).__init__(*args, **kwargs)
		self.fields['soups'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Soups", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['prepared_salads'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Prepared Salads", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['sandwich_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Sandwich Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['exhibition_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Exhibition Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['euro_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Euro Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['pizza_oven'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Pizza Oven", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['grill'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Grill", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['hot_food_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="Hot Food Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['from_the_bakery'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Breakfast", category="From the Bakery", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for i, item in self.cleaned_data['soups']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Soups", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['prepared_salads']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Prepared Salads", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['sandwich_bar']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Sandwich Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['exhibition_kitchen']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Exhibition Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['euro_kitchen']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Euro Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['pizza_oven']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Pizza Oven", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['grill']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Grill", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['hot_food_bar']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="Hot Food Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['from_the_bakery']:
			item = Item.objects.filter(name=item, meal="Breakfast", category="From the Bakery", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Breakfast")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddLunchForm(forms.Form):
	soups = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	prepared_salads = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	sandwich_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	exhibition_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	euro_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	pizza_oven = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	grill = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	hot_food_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	from_the_bakery = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddLunchForm, self).__init__(*args, **kwargs)
		self.fields['soups'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Soups", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['prepared_salads'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Prepared Salads", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['sandwich_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Sandwich Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['exhibition_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Exhibition Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['euro_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Euro Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['pizza_oven'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Pizza Oven", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['grill'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Grill", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['hot_food_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="Hot Food Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['from_the_bakery'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Lunch", category="From the Bakery", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['soups']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Soups", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['prepared_salads']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Prepared Salads", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['sandwich_bar']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Sandwich Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['exhibition_kitchen']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Exhibition Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['euro_kitchen']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Euro Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['pizza_oven']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Pizza Oven", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['grill']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Grill", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['hot_food_bar']:
			item = Item.objects.filter(name=item, meal="Lunch", category="Hot Food Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['from_the_bakery']:
			item = Item.objects.filter(name=item, meal="Lunch", category="From the Bakery", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			if len(item) > 0:
				item = item[0]
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Lunch")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddDinnerForm(forms.Form):	
	soups = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	prepared_salads = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	sandwich_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	exhibition_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	euro_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	pizza_oven = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	grill = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	hot_food_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	from_the_bakery = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddDinnerForm, self).__init__(*args, **kwargs)
		self.fields['soups'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Soups", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['prepared_salads'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Prepared Salads", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['sandwich_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Sandwich Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['exhibition_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Exhibition Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['euro_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Euro Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['pizza_oven'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Pizza Oven", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['grill'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Grill", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['hot_food_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="Hot Food Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['from_the_bakery'].queryset = Item.objects.filter(restaurant="Dining Hall", meal="Dinner", category="From the Bakery", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['soups']:
			item = Item.objects.get(name=item, meal="Dinner", category="Soups", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['prepared_salads']:
			item = Item.objects.get(name=item, meal="Dinner", category="Prepared Salads", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['sandwich_bar']:
			item = Item.objects.get(name=item, meal="Dinner", category="Sandwich Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['exhibition_kitchen']:
			item = Item.objects.get(name=item, meal="Dinner", category="Exhibition Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['euro_kitchen']:
			item = Item.objects.get(name=item, meal="Dinner", category="Euro Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['pizza_oven']:
			item = Item.objects.get(name=item, meal="Dinner", category="Pizza Oven", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['grill']:
			item = Item.objects.get(name=item, meal="Dinner", category="Grill", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['hot_food_bar']:
			item = Item.objects.get(name=item, meal="Dinner", category="Hot Food Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['from_the_bakery']:
			item = Item.objects.get(name=item, meal="Dinner", category="From the Bakery", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Dinner")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddSnacksForm(forms.Form):

	
	soups = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	prepared_salads = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	sandwich_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	exhibition_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	euro_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	pizza_oven = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	grill = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	hot_food_bar = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	from_the_bakery = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())

	
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.meal = kwargs.pop('meal', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddSnacksForm, self).__init__(*args, **kwargs)
		self.fields['soups'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Soups", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['prepared_salads'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Prepared Salads", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['sandwich_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Sandwich Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['exhibition_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Exhibition Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['euro_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Euro Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['pizza_oven'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Pizza Oven", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['grill'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Grill", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['hot_food_bar'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Hot Food Bar", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['from_the_bakery'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="From the Bakery", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['soups']:
			item = Item.objects.get(name=item, meal=self.meal, category="Soups", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['prepared_salads']:
			item = Item.objects.get(name=item, meal=self.meal, category="Prepared Salads", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['sandwich_bar']:
			item = Item.objects.get(name=item, meal=self.meal, category="Sandwich Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['exhibition_kitchen']:
			item = Item.objects.get(name=item, meal=self.meal, category="Exhibition Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['euro_kitchen']:
			item = Item.objects.get(name=item, meal=self.meal, category="Euro Kitchen", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['pizza_oven']:
			item = Item.objects.get(name=item, meal=self.meal, category="Pizza Oven", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['grill']:
			item = Item.objects.get(name=item, meal=self.meal, category="Grill", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['hot_food_bar']:
			item = Item.objects.get(name=item, meal=self.meal, category="Hot Food Bar", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['from_the_bakery']:
			item = Item.objects.get(name=item, meal=self.meal, category="From the Bakery", day=self.datetime.day, month=self.datetime.month, year=self.datetime.year)
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal="Snacks")
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddCafe1919Form(forms.Form):	
	breakfast = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	pizzette = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	panini = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	insalate = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	lasagna = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	sides = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	bibite = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	dolce = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.meal = kwargs.pop('meal', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddCafe1919Form, self).__init__(*args, **kwargs)
		self.fields['breakfast'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Breakfast", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['pizzette'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Pizzette", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['panini'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Panini", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['insalate'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Insalate", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['lasagna'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Lasagna", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['sides'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Sides", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['bibite'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Bibite", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['dolce'].queryset = Item.objects.filter(restaurant="Cafe 1919", meal=self.meal, category="Dolce", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['breakfast']:
			item = Item.objects.get(name=item, meal=self.meal, category="Breakfast")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['pizzette']:
			item = Item.objects.get(name=item, meal=self.meal, category="Pizzette")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['panini']:
			item = Item.objects.get(name=item, meal=self.meal, category="Panini")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['insalate']:
			item = Item.objects.get(name=item, meal=self.meal, category="Insalate")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['lasagna']:
			item = Item.objects.get(name=item, meal=self.meal, category="Lasagna")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['sides']:
			item = Item.objects.get(name=item, meal=self.meal, category="Sides")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['bibite']:
			item = Item.objects.get(name=item, meal=self.meal, category="Bibite")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['dolce']:
			item = Item.objects.get(name=item, meal=self.meal, category="Dolce")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddBruinCafeForm(forms.Form):	
	breakfast = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	lunch_and_dinner = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	coffee_tea_and_pastries = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	drinks = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.meal = kwargs.pop('meal', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddBruinCafeForm, self).__init__(*args, **kwargs)
		self.fields['breakfast'].queryset = Item.objects.filter(restaurant="Bruin Cafe", meal=self.meal, category="Breakfast", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['lunch_and_dinner'].queryset = Item.objects.filter(restaurant="Bruin Cafe", meal=self.meal, category="Lunch & Dinner", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['coffee_tea_and_pastries'].queryset = Item.objects.filter(restaurant="Bruin Cafe", meal=self.meal, category="Coffee, Tea, & Pastries", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['drinks'].queryset = Item.objects.filter(restaurant="Bruin Cafe", meal=self.meal, category="Drinks", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['breakfast']:
			item = Item.objects.get(name=item, meal=self.meal, category="Breakfast")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['lunch_and_dinner']:
			item = Item.objects.get(name=item, meal=self.meal, category="Lunch & Dinner")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['coffee_tea_and_pastries']:
			item = Item.objects.get(name=item, meal=self.meal, category="Coffee, Tea, & Pastries")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['drinks']:
			item = Item.objects.get(name=item, meal=self.meal, category="Drinks")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddRendezvousForm(forms.Form):	
	breakfast = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	mexican_entrees = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	asian_entrees = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	daily_specials = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.meal = kwargs.pop('meal', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddRendezvousForm, self).__init__(*args, **kwargs)
		self.fields['breakfast'].queryset = Item.objects.filter(restaurant="Rendezvous", meal=self.meal, category="Breakfast", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['mexican_entrees'].queryset = Item.objects.filter(restaurant="Rendezvous", meal=self.meal, category="Mexican Entrees", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['asian_entrees'].queryset = Item.objects.filter(restaurant="Rendezvous", meal=self.meal, category="Asian Entrees", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['daily_specials'].queryset = Item.objects.filter(restaurant="Rendezvous", meal=self.meal, category="Daily Specials", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['breakfast']:
			item = Item.objects.get(name=item, meal=self.meal, category="Breakfast")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['mexican_entrees']:
			item = Item.objects.get(name=item, meal=self.meal, category="Mexican Entrees")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['asian_entrees']:
			item = Item.objects.get(name=item, meal=self.meal, category="Asian Entrees")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['daily_specials']:
			item = Item.objects.get(name=item, meal=self.meal, category="Daily Specials")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddLateNightForm(forms.Form):	
	entrees = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	sides_and_beverages = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	mypizza_and_wings = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.meal = kwargs.pop('meal', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddLateNightForm, self).__init__(*args, **kwargs)
		self.fields['entrees'].queryset = Item.objects.filter(restaurant="De Neve Late Night", meal=self.meal, category="Entrees", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['sides_and_beverages'].queryset = Item.objects.filter(restaurant="De Neve Late Night", meal=self.meal, category="Sides & Beverages", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['mypizza_and_wings'].queryset = Item.objects.filter(restaurant="De Neve Late Night", meal=self.meal, category="MyPizza & Wings", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['entrees']:
			item = Item.objects.get(name=item, meal=self.meal, category="entrees")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['sides_and_beverages']:
			item = Item.objects.get(name=item, meal=self.meal, category="Sides & Beverages")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['mypizza_and_wings']:
			item = Item.objects.get(name=item, meal=self.meal, category="MyPizza & Wings")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items

class AddFeastForm(forms.Form):	
	bruin_wok = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	spice_kitchen = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	greens_and_more = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	iron_grill = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	stone_oven = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	sweets = ItemMultipleChoiceField(required=False, widget=CustomSelectMultiple, queryset=Item.objects.none())
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.meal = kwargs.pop('meal', None)
		self.datetime = kwargs.pop('datetime', None)
		super(AddFeastForm, self).__init__(*args, **kwargs)
		self.fields['bruin_wok'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Bruin Wok", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['spice_kitchen'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Spice Kitchen", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['greens_and_more'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Greens & More", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['iron_grill'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Iron Grill", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['stone_oven'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Stone Oven", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)
		self.fields['sweets'].queryset = Item.objects.filter(restaurant="Dining Hall", meal=self.meal, category="Sweets", month=self.datetime.month, day=self.datetime.day, year=self.datetime.year)

	def addunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 + num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 + (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 + (num2 * 1000)

	def subtractunits(self, num1, unit1, num2, unit2):
		if unit2 == 'n/a':
			return num1
		elif unit1 == unit2:
			return num1 - num2
		elif unit1 == 'g' and unit2 == 'mg':
			return num1 - (num2 / 1000.0)
		elif unit1 == 'mg' and unit2 == 'g':
			return num1 - (num2 * 1000)

	def additemcalc(self, user, item):
		user.calories_remaining -= item.calories 
		user.total_fat_remaining = self.subtractunits(user.total_fat_remaining, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_remaining = subtractunits(user.saturated_fat_remaining, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_remaining = subtractunits(user.trans_fat_remaining, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_remaining = self.subtractunits(user.cholesterol_remaining, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_remaining = self.subtractunits(user.sodium_remaining, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_remaining = self.subtractunits(user.total_carbs_remaining, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_remaining = self.subtractunits(user.dietary_fiber_remaining, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_remaining = subtractunits(user.sugars_remaining, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_remaining = self.subtractunits(user.protein_remaining, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_remaining -= item.vitamin_A_dv
		user.vitamin_C_remaining -= item.vitamin_C_dv
		user.calcium_remaining -= item.calcium_dv
		user.iron_remaining -= item.iron_dv
		user.calories_eaten += item.calories
		user.total_fat_eaten = self.addunits(user.total_fat_eaten, user.total_fat_units, item.total_fat, item.total_fat_units)
		#user.saturated_fat_eaten = addunits(user.saturated_fat_eaten, user.saturated_fat_units, item.saturated_fat, item.saturated_fat_units)
		#user.trans_fat_eaten = addunits(user.trans_fat_eaten, user.trans_fat_units, item.trans_fat, item.trans_fat_units)
		user.cholesterol_eaten = self.addunits(user.cholesterol_eaten, user.cholesterol_units, item.cholesterol, item.cholesterol_units)
		user.sodium_eaten = self.addunits(user.sodium_eaten, user.sodium_units, item.sodium, item.sodium_units)
		user.total_carbs_eaten = self.addunits(user.total_carbs_eaten, user.total_carbs_units, item.total_carbs, item.total_carbs_units)
		user.dietary_fiber_eaten = self.addunits(user.dietary_fiber_eaten, user.dietary_fiber_units, item.dietary_fiber, item.dietary_fiber_units)
		#user.sugars_eaten = addunits(user.sugars_eaten, user.sugars_units, item.sugars, item.sugars_units)
		user.protein_eaten = self.addunits(user.protein_eaten, user.protein_units, item.protein, item.protein_units)
		user.vitamin_A_eaten += item.vitamin_A_dv
		user.vitamin_C_eaten += item.vitamin_C_dv
		user.calcium_eaten += item.calcium_dv
		user.iron_eaten += item.iron_dv
		return

	def additemtoprofile(self, user, item):
		self.additemcalc(user.profile, item)
		user.profile.save()
		user.save()

	def save(self, commit=True):
		added_items = []
		for item in self.cleaned_data['bruin_wok']:
			item = Item.objects.get(name=item, meal=self.meal, category="Bruin Wok")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['spice_kitchen']:
			item = Item.objects.get(name=item, meal=self.meal, category="Spice Kitchen")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['greens_and_more']:
			item = Item.objects.get(name=item, meal=self.meal, category="Greens & More")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['iron_grill']:
			item = Item.objects.get(name=item, meal=self.meal, category="Iron Grill")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['stone_oven']:
			item = Item.objects.get(name=item, meal=self.meal, category="Stone Oven")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		for item in self.cleaned_data['sweets']:
			item = Item.objects.get(name=item, meal=self.meal, category="Sweets")
			foodlog, created = FoodLog.objects.get_or_create(item=item, profile=self.user.profile, meal=self.meal)
			if not created:
				foodlog.portion += 1
				foodlog.save()
			self.additemtoprofile(self.user, item)
			added_items.append(foodlog)
		return added_items
