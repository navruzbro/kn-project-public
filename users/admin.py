from django.contrib import admin
from users.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username','second_id','first_name','last_name','email']
    list_filter = ['is_active',]



admin.site.register(CustomUser, CustomUserAdmin)