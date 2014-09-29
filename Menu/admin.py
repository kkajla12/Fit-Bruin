from Menu.models import Item
from Menu.models import Profile
from Menu.models import FoodLog
from Menu.models import Post
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
	inlines = (ProfileInline, )

admin.site.register(Item)
admin.site.register(FoodLog)
admin.site.register(Post)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
