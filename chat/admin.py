from django.contrib import admin
from chat.models import User,UserGroup,testDate
# Register your models here.

admin.site.register(User);
admin.site.register(UserGroup);
admin.site.register(testDate);